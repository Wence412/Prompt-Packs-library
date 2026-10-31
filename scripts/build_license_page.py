#!/usr/bin/env python3
"""Render LICENSE into site/license/index.html so the site shows the exact license text.

The page is built from LICENSE, so there is one source of truth. Run this after any edit
to LICENSE. scripts/validate.py fails if the page and LICENSE differ. The build also
checks that every word of LICENSE appears in the page, so the layout cannot drop text.
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "license" / "index.html"

SECTION = re.compile(r"^(\d+)\. (.+)$")
ITEM = re.compile(r"^  ([a-z])\. (.*)$")
TOKEN = re.compile(r"[A-Za-z0-9'@./:()-]+")

ICON = (
    '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.6" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 3h7l5 5v13H7z"/>'
    '<path d="M14 3v5h5M10 13h6M10 17h6"/></svg>'
)

HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="The WenceStudio Prompt Packs Library License: free to use in your own and client work, with clear limits on republishing."><title>License | Prompt Packs Library | WenceStudio by SmartDesign</title><base href="../"><link rel="icon" type="image/png" href="assets/images/wencestudio-logo.png"><link rel="stylesheet" href="styles.css?v=20261031-license-layout"></head>
<body><script>try{document.body.dataset.theme=localStorage.getItem("prompt-packs-theme")||"dark"}catch(e){}</script><a class="skip-link" href="#license">Skip to the license</a><header class="site-header platform-page-header license-header"><div class="brand-lockup"><img class="brand-logo" src="assets/images/wencestudio-logo.png" width="640" height="640" alt="WenceStudio by SmartDesign logo"><p class="eyebrow">WenceStudio by SmartDesign</p></div><nav class="platform-nav" aria-label="Primary navigation"><a href="./">Overview</a><a href="library/">Library</a><a href="collections/">Collections</a><a href="guides/">Guides</a></nav></header>
"""
FOOT = """<footer class="page-footer"><div class="footer-contact"><a href="library/">Search all prompts</a><a href="collections/">Collections</a><a href="guides/">Guides</a><a href="mailto:hello@wencestudio.com">Work with us</a></div><p>WenceStudio by SmartDesign</p></footer></body></html>
"""


def sentence_case(title: str) -> str:
    return title.lower().capitalize()


def parse(text: str) -> dict:
    lines = text.rstrip("\n").split("\n")
    title, copyright_line = lines[0], lines[2]
    rest = lines[4:]
    blocks: list[list[str]] = [[]]
    for line in rest:
        if SECTION.match(line):
            blocks.append([line])
        else:
            blocks[-1].append(line)
    preface = blocks[0]
    # preface: "IN SHORT" block, then the scope paragraph
    paragraphs, current = [], []
    for line in preface:
        if line.strip() == "":
            if current:
                paragraphs.append(current)
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append(current)
    short_block, scope_block = paragraphs[0], paragraphs[1]
    assert short_block[0] == "IN SHORT", "LICENSE must start with an IN SHORT summary"
    sections = []
    for block in blocks[1:]:
        match = SECTION.match(block[0])
        number, heading = match.group(1), match.group(2)
        body = block[1:]
        items, paras, cur, item_open = [], [], [], False
        parts: list[tuple[str, list[str]]] = []
        for line in body:
            item = ITEM.match(line)
            if line.strip() == "":
                if cur:
                    parts.append(("li" if item_open else "p", cur))
                    cur = []
                item_open = False
            elif item:
                if cur and not item_open:
                    parts.append(("p", cur))
                    cur = []
                if cur and item_open:
                    parts.append(("li", cur))
                cur = [item.group(2)]
                item_open = True
            else:
                cur.append(line.strip())
        if cur:
            parts.append(("li" if item_open else "p", cur))
        sections.append({"n": number, "title": heading, "parts": parts})
    version = re.search(r"Version\s+([\d.]+)", title)
    return {
        "title": title,
        "copyright": copyright_line,
        "version": version.group(1) if version else "",
        "short": " ".join(s.strip() for s in short_block[1:]),
        "scope": " ".join(s.strip() for s in scope_block),
        "sections": sections,
    }


def render_section(sec: dict) -> str:
    out = [f'<section class="license-section" id="section-{sec["n"]}"><span class="license-num" aria-hidden="true">{int(sec["n"]):02d}</span><div><h2 data-lic>{escape(sentence_case(sec["title"]), quote=False)}</h2>']
    index, in_list = 0, False
    for kind, chunk in sec["parts"]:
        text = escape(" ".join(chunk), quote=False)
        if kind == "li":
            if not in_list:
                out.append('<ol class="license-list" type="a">')
                in_list = True
            out.append(f"<li data-lic>{text}</li>")
        else:
            if in_list:
                out.append("</ol>")
                in_list = False
            out.append(f'<p data-lic>{text}</p>')
    if in_list:
        out.append("</ol>")
    out.append("</div></section>")
    return "".join(out)


def render() -> str:
    data = parse((ROOT / "LICENSE").read_text(encoding="utf-8"))
    toc = "".join(
        f'<li><a href="license/#section-{s["n"]}"><span>{int(s["n"]):02d}</span>{escape(sentence_case(s["title"]), quote=False)}</a></li>'
        for s in data["sections"]
    )
    main = (
        '<main id="license" class="license-page">'
        '<nav class="license-crumbs" aria-label="Breadcrumb"><a href="./">Home</a><span aria-hidden="true">/</span><span>Legal</span><span aria-hidden="true">/</span><span aria-current="page">License</span></nav>'
        f'<div class="license-title"><span class="license-icon">{ICON}</span><h1>Library license</h1></div>'
        f'<p class="license-meta"><span data-lic>{escape(data["title"], quote=False)}</span> · <span data-lic>{escape(data["copyright"], quote=False)}</span></p>'
        f'<aside class="license-card license-short"><p class="eyebrow" data-lic>In short</p><p data-lic>{escape(data["short"], quote=False)}</p></aside>'
        f'<p class="license-scope" data-lic>{escape(data["scope"], quote=False)}</p>'
        f'<nav class="license-card license-toc" aria-label="On this page"><p class="eyebrow">On this page</p><ol>{toc}</ol></nav>'
        + "".join(render_section(s) for s in data["sections"])
        + "</main>\n"
    )
    page = HEAD + main + FOOT
    check_words(page)
    return page


class _Collect(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.depth = 0
        self.stack: list[bool] = []
        self.text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("br", "meta", "link", "img", "base"):
            return
        mark = any(name == "data-lic" for name, _ in attrs)
        self.stack.append(mark)
        if mark:
            self.depth += 1

    def handle_endtag(self, tag):
        if not self.stack:
            return
        if self.stack.pop():
            self.depth -= 1

    def handle_data(self, data):
        if self.depth:
            self.text.append(data)


def tokens(text: str) -> Counter:
    return Counter(t.lower() for t in TOKEN.findall(text))


def check_words(page: str) -> None:
    source = (ROOT / "LICENSE").read_text(encoding="utf-8")
    source = re.sub(r"^\d+\. ", "", source, flags=re.M)
    source = re.sub(r"^ {2}[a-z]\. ", "", source, flags=re.M)
    collector = _Collect()
    collector.feed(page)
    shown = tokens(" ".join(collector.text))
    wanted = tokens(source)
    if shown != wanted:
        missing = wanted - shown
        extra = shown - wanted
        raise SystemExit(f"License page text differs from LICENSE. Missing: {dict(missing)} Extra: {dict(extra)}")


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
