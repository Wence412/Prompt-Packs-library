#!/usr/bin/env python3
"""Build a traceable VPH browser export from an explicitly pinned source checkout."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/Wence412/Visual-Prompts-Hub-VPH-"


def build(source):
    revision = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    cards = []
    for path in sorted(source.glob("*.yaml")):
        if path.name.endswith("_template.yaml"):
            continue
        raw = path.read_bytes()
        data = yaml.safe_load(raw)
        if not isinstance(data, dict) or not all(k in data for k in ("title", "apae", "chatgpt_image_2")):
            raise ValueError(f"Unsupported prompt file: {path.name}")
        if set(data["apae"]) != {"appearance", "place", "action", "emotion"}:
            raise ValueError(f"Invalid APAE fields: {path.name}")
        prompt = data["chatgpt_image_2"]["prompt"].strip()
        if not prompt:
            raise ValueError(f"Empty prompt: {path.name}")
        cards.append({
            "id": "VPH-" + path.stem.upper().replace("_", "-"),
            "title": data["title"].replace(" — ", ". ").replace("—", ". "), "collection": "Visual Prompts Hub",
            "category": data.get("category", "Uncategorized"), "operation": "generate",
            "prompt": prompt, "apae": data["apae"],
            "tags": data.get("tags", []), "variants": data.get("variants", []),
            "engine_overrides": data.get("engine_overrides", {}),
            "negatives": data.get("negatives", []), "original_record": data,
            "output": {"aspect_ratio": data["chatgpt_image_2"].get("ar", "Flexible"), "format": "Prompt template"},
            "source": {"url": f"{REPO}/blob/{revision}/{path.name}", "revision": revision,
                       "file": path.name, "sha256": hashlib.sha256(raw).hexdigest()},
            "compatibility_note": "Historical engine labels and settings are preserved for reference, not verified current API parameters. Review before use.",
            "evidence": {"tested": False, "sample_assets": []}
        })
    if not cards:
        raise ValueError("No VPH prompt records found")
    return {"metadata": {"source_repository": REPO, "source_revision": revision,
                         "total_cards": len(cards), "license": "WenceStudio Library License 1.0"}, "prompts": cards}


def validate(data):
    cards = data["prompts"]
    if len(cards) != data["metadata"]["total_cards"]:
        raise ValueError("VPH count mismatch")
    ids = [c["id"] for c in cards]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate VPH IDs")
    texts = [" ".join(c["prompt"].lower().split()) for c in cards]
    if len(texts) != len(set(texts)):
        raise ValueError("Duplicate VPH prompt text")
    other = json.loads((ROOT / "prompts.json").read_text())["prompts"]
    other += json.loads((ROOT / "capability-packs-v2.json").read_text())["packs"]
    if set(ids) & {c["id"] for c in other}:
        raise ValueError("VPH ID conflicts with existing library")
    existing = {" ".join(c["prompt"].lower().split()) for c in other}
    if set(texts) & existing:
        raise ValueError("VPH prompt duplicates existing library")
    for card in cards:
        if "—" in card["title"]:
            raise ValueError("Displayed VPH titles must not contain em dashes")
        if not card["prompt"] or not card["source"]["url"] or not card["apae"]:
            raise ValueError("Incomplete VPH card")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", nargs="?", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "vph-import.json"
    if args.check:
        data = json.loads(target.read_text())
        if args.source and build(args.source) != data:
            raise ValueError("Export differs from pinned source checkout")
    else:
        if not args.source:
            parser.error("A source checkout is required for import")
        data = build(args.source)
    validate(data)
    if not args.check:
        target.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"Validated {len(data['prompts'])} VPH cards at {data['metadata']['source_revision']}")
