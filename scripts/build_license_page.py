#!/usr/bin/env python3
"""Render LICENSE into site/license/index.html so the site shows the exact license text.

Run after any edit to LICENSE. scripts/validate.py fails if the page and LICENSE differ.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "site" / "license" / "index.html"

PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="description" content="The WenceStudio Prompt Packs Library License: free to use in your own and client work, with clear limits on republishing."><title>License | Prompt Packs Library | WenceStudio by SmartDesign</title><base href="../"><link rel="icon" type="image/png" href="assets/images/wencestudio-logo.png"><link rel="stylesheet" href="styles.css?v=20261031-license-page"></head>
<body><a class="skip-link" href="#license">Skip to the license</a><header class="site-header platform-page-header"><div class="brand-lockup"><img class="brand-logo" src="assets/images/wencestudio-logo.png" width="640" height="640" alt="WenceStudio by SmartDesign logo"><p class="eyebrow">WenceStudio by SmartDesign</p></div><nav class="platform-nav" aria-label="Primary navigation"><a href="./">Overview</a><a href="library/">Library</a><a href="collections/">Collections</a><a href="guides/">Guides</a></nav><div class="simple-page-hero"><p class="hero-kicker">Terms of use</p><h1>Library<br><em>license.</em></h1><p class="lede">The full text, exactly as published in the project repository. Questions or permission requests: hello@wencestudio.com.</p></div></header><main id="license"><pre class="license-text">{text}</pre></main><footer class="page-footer"><a href="library/">Search all prompts</a><a href="collections/">Collections</a><p>WenceStudio by SmartDesign</p></footer></body></html>
"""


def render() -> str:
    text = (ROOT / "LICENSE").read_text(encoding="utf-8").rstrip("\n")
    return PAGE.replace("{text}", escape(text, quote=False))


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
