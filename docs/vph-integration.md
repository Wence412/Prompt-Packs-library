# Visual Prompts Hub integration

VPH is available as a separate collection in the existing prompt browser. The original repository is unchanged. This is a pinned data import, not an iframe or an automatic live mirror.

## What is preserved

- Original prompt text, APAE fields, categories, tags, negative instructions and variants.
- Engine-specific prompt overrides and the entire original YAML record as structured data.
- Source commit, file path, SHA-256 checksum and a permalink to each original file.
- License. The source repository uses the WenceStudio Visual Prompts Hub License, Version 1.0, with the same terms as this library. See [source license](https://github.com/Wence412/Visual-Prompts-Hub-VPH-/blob/efefe6db7db9c2d392531d3763bb62e2b4c660a3/LICENSE). Copies obtained before 23 October 2026 stay under MIT.

The eight concrete prompt files are imported. The four blank/batch/brand/campaign templates are not counted as prompts. No generated image evidence is present, so imported cards remain untested.

## Compatibility boundary

Historical labels such as `chatgpt_image_2`, `style_preset`, and `quality: hd` remain source metadata, not supported-current-API claims. Engine overrides may contain historical versions and flags. Review these settings before using an API or another engine. Negative instructions are preserved, not represented as a guaranteed negative-prompt API parameter.

The browser displays APAE fields, variants and engine overrides in an expandable section. Users can copy the primary prompt or an engine-specific prompt. Variants are documented changes, not automatically assembled requests.

## Refresh intentionally

Use a clean VPH checkout at the chosen commit. Review the diff and license before importing:

```bash
python3 -m pip install PyYAML==6.0.3
python3 scripts/import_vph.py /path/to/vph-checkout
python3 scripts/import_vph.py /path/to/vph-checkout --check
python3 scripts/validate.py
```

Commit the importer output `vph-import.json` after review. CI checks record counts, duplicate IDs, exact normalized prompt duplicates across libraries, and required content. It does not detect semantic near-duplicates or verify engine compatibility. Review near-duplicates manually.

The browser fetches this approved export from the prompt-packs repository. Failure to load VPH does not hide the original collections. Source README links are not copied because the source repository's actual files are flat rather than in its documented folders.

## Ownership

VPH remains the authoring source. Do not manually edit imported records. The integration creates one public browsing destination without maintaining two independent copies of prompt content.
