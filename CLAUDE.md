# CLAUDE.md

Guidance for Claude Code (and other AI assistants) working in this repository.

## What this repo is

A content/data library, not an application — there is no build, no server, no
package.json, and no test suite. It's **170 production-ready AI image prompts**
for GPT Image workflows, published by WenceStudio by SmartDesign, distributed as
Markdown, JSON, and CSV. Changes here are edits to structured data and docs,
not code changes.

## Repository layout (actual, flat — not the aspirational tree in README.md)

The prompt library itself is intentionally flat. Supporting automation,
schemas, and capability guidance live in `scripts/`, `schema/`, and `docs/`.
Keep README.md aligned with that structure.

| File | Role |
|---|---|
| `prompts.json` | Source of truth. `{ metadata, prompts: [...] }`, 170 entries. |
| `chatgpt-image-prompt-library.import.json` | **Byte-for-byte duplicate** of `prompts.json` (verified via `diff`). Any edit to one must be mirrored to the other, or the two should be consolidated. |
| `prompts.csv` | Same 170 records as CSV: `id,phase,category,title,prompt,best_for,framework,tags`. Must stay in sync with `prompts.json`. |
| `categories.json` | Maps `Phase 1` / `Phase 2` → category name → array of prompt `id`s. Must stay in sync with `prompts.json`. |
| `combined-prompt-library.md` | Human-readable rendering of all 170 prompts. |
| `phase-1-visual-prompt-pack.md` | Phase 1 prompts only (75), Markdown. |
| `phase-2-production-prompt-pack.md` | Phase 2 prompts only (95), Markdown. |
| `seed-framework.md` | Defines the S.E.E.D. prompt structure (Subject, Elements, Environment, Details). |
| `production-checklist.md` | QA checklist referenced before "shipping" a prompt. |
| `before-after-workflow.md`, `ad-testing-matrix.md` | Example workflows referenced from README. |
| `universal-*.md` (product-mockup, packaging, ad-creative, ai-influencer) | Reusable template prompts. |
| `VALIDATION.md` | How to run the automated repository checks. |
| `scripts/build_exports.py` | Rebuilds the CSV and import JSON from `prompts.json`. |
| `scripts/validate.py` | Validates data, catalogs, categories, and local Markdown links. |
| `schema/prompt-card-v2.schema.json` | Contract for new generation and editing prompt cards. |
| `docs/model-capabilities.md` | Model-agnostic capability guidance for prompt authors. |
| `CHANGELOG.md` | Version history (currently just `1.0.0`). |
| `CONTRIBUTING.md`, `README.md`, `LICENSE` | Contribution guide, project pitch/usage docs, WenceStudio Library License (proprietary, free to use, not to redistribute). |

## Data model

Each prompt record (identical shape in `prompts.json`, the import JSON, and
`prompts.csv`):

```json
{
  "id": "P1-001",
  "phase": "Phase 1",
  "category": "Product Mockups",
  "title": "Premium Studio Product Mockup",
  "prompt": "Create a premium studio mockup of [product] for [brand] on a clean matte surface ...",
  "best_for": "Visual ideation, product concepts, mockups, brand content, campaign assets",
  "framework": "Subject + context + style + environment + materials + camera/framing + lighting + brand constraints + output format",
  "tags": ["product-mockups", "premium-studio-product-mockup", "chatgpt-image-2", "visual-prompt"]
}
```

- **ID scheme**: `P1-001`..`P1-075` (Phase 1, 9 categories), `P2-001`..`P2-095`
  (Phase 2, 10 categories). Variations use suffixes like `P1-001-v2` or
  `P1-001-luxury`.
- **Placeholders** inside `prompt` text use `[bracket]` notation (e.g.
  `[product]`, `[brand]`, `[audience]`, `[color palette]`, `[environment]`) —
  never fill these in when editing a template prompt; they're meant to stay
  generic.
- Prompts follow the **S.E.E.D. framework** (Subject, Elements, Environment,
  Details) — see `seed-framework.md`. New/edited prompts should be 150–300
  words and structured accordingly.

## Making changes (per CONTRIBUTING.md)

When adding or editing a prompt, update the canonical data and category map,
then regenerate the derivative files:

1. `prompts.json` — add/edit the record under `prompts`, bump
   `metadata.total_prompts` / `phase_N_prompts` if counts change.
2. `categories.json` — add the new `id` under the correct phase/category, or
   create a new category array.
3. `combined-prompt-library.md` (and `phase-1-visual-prompt-pack.md` or
   `phase-2-production-prompt-pack.md`) — add the human-readable Markdown
   entry in the matching category section.
4. Run `python3 scripts/build_exports.py` and `python3 scripts/validate.py`.

Quality bar before considering a prompt done (from `CONTRIBUTING.md`):
- No real-person likenesses, copyrighted characters, or real logos.
- No requests that would produce random/garbled text in the image.
- Uses bracketed placeholders, not hardcoded specifics.
- At least 3 tags, `chatgpt-image-2` and a commercial-use-style tag included.
- Category name matches one already listed in `categories.json` /
  `CONTRIBUTING.md`, or is a deliberate new category added consistently
  everywhere above.

## Conventions

- Tags: lowercase, hyphen-separated.
- No code, no dependencies, no CI — verification is manual (JSON validity,
  cross-file record counts matching, spot-checking prompts in ChatGPT-Image).
- If you need to validate JSON structure or cross-check counts across files,
  a one-off `python3 -c "..."` or `jq` invocation is the idiomatic way in this
  repo (see examples in this file's history) — there's no test runner to wire
  it into.
- License is the WenceStudio Library License (see `LICENSE`); contributions grant the
  owner a right to publish them per `CONTRIBUTING.md`. Records in `vph-import.json`
  keep the license recorded in their source repository.
