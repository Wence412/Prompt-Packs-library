# Changelog

## 1.3.1 - Unreleased

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
