# Changelog

## 1.3.1 - Unreleased

- Collections and library pages: added the same scroll devices as the landing and guides pages. Collections: hero stagger and cards that rise as they enter view. Library: hero stagger and the page progress hairline only, so filtering and the prompt list stay instant. Cards reveal slightly earlier on every page. Reduced-motion override, and content stays visible without JavaScript.
- Landing and guides pages: added scroll devices from scroll-craft in plain CSS and JS (`site/scroll.js`). The hero planes move at different rates and the hero copy recedes as you scroll, collection cards, steps and tool rows rise in with a short stagger, guide cards rise as they enter view, and a hairline progress bar tracks the page. "How the platform works" is now a rail: the heading holds while the three steps pass. Removed the redundant eyebrows above the Collections and Resources headings. Transform and opacity only, with a reduced-motion override. Content stays visible without JavaScript or if the script fails to load.
- Landing page: removed the stacked padding and duplicate rule under the intro principles strip, and the stacked padding, rule and margins above the footer, so each boundary has one rule and one gap.
- Site: removed the double rule and stacked gap above the footer on the collections and guides pages (144px down to 64px), and aligned the footer with the content above it. Footer links now ease their colour on hover, with a reduced-motion override.
- Landing page: resized the hero headline so it sits on two lines without an orphaned word, moved the "Review" art label out from under the status card, rebuilt the intro section grid so the left column and the prompt card preview fill the row, and added a staggered hero entrance and intro reveal with a reduced-motion override and a no-JavaScript fallback.
- Site: redesigned the License page with a breadcrumb, an In short card, an On this page index and numbered sections, still rendered from LICENSE. The collections footer now groups the License link with the other links.
- Site: added a License page at /license/ that shows the full LICENSE text on the site. The footer and homepage license links now open it. `scripts/build_license_page.py` renders the page from LICENSE, and `scripts/validate.py` fails if the page is out of date.
- License: added a short plain-English summary at the top, a sentence in section 8 that AI output can be wrong or incomplete, and section 9 (Changes to this license). The license version line is unchanged.
- Re-pinned the eight Visual Prompts Hub cards to source commit efefe6d, where the source repository now uses the WenceStudio Visual Prompts Hub License, Version 1.0. The card license field reads "WenceStudio Library License 1.0".
- The new pin also brings in the 22 October 2026 prompt revisions from the source repository: five cards have updated prompt text (editorial character, facade, hero shot, texture, watch).
- Operation dropdown labels now read Edit (image), Editing (video), Plan (business) and Planning (video).

## 1.3.0 - Unreleased

- Added 20 L&D workflow prompt cards (LRN-009 to LRN-028) to the Learning collection, grouped in five pillars.
- Learning now holds 28 cards. Library total is 388 cards across five collections.

## 1.2.0 - Unreleased

- Added 14 capability prompt cards across seven modern generation and editing workflows.
- Added a searchable, accessible static prompt browser for GitHub Pages.
- Extended repository validation to cover capability cards.

## 1.1.0 - Unreleased

- Established `prompts.json` as the canonical structured source.
- Added export and validation scripts with GitHub Actions checks.
- Added a versioned prompt-card schema and a current capability guide.
- Repaired repository-local documentation links.

## 1.0.0

- Combined Phase 1 and Phase 2 prompt packs.
- Added Markdown documentation.
- Added JSON and CSV import files.
- Added templates, examples, and production checklist.
