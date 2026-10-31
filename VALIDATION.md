# Validation

Run the repository checks before opening a pull request:

```bash
python3 scripts/build_exports.py --check
python3 scripts/validate.py
```

`prompts.json` is the canonical structured source. The CSV and import JSON are
generated exports and must not be edited by hand. The validator checks prompt
counts, IDs, categories, exports, documentation coverage, and local Markdown
links.

If you edit `LICENSE`, run `python3 scripts/build_license_page.py` to refresh `site/license/index.html`. The validator fails when the two differ.
