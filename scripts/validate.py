#!/usr/bin/env python3
"""Validate prompt data, catalogs, and repository-local Markdown links."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIELDS = {"id", "phase", "category", "title", "prompt", "best_for", "framework", "tags"}
CAPABILITY_REQUIRED_FIELDS = {"id", "pack", "title", "operation", "prompt", "variables", "inputs", "output", "acceptance_criteria", "rights_and_safety", "evidence"}
CATALOGS = [
    ROOT / "combined-prompt-library.md",
    ROOT / "phase-1-visual-prompt-pack.md",
    ROOT / "phase-2-production-prompt-pack.md",
]


def error(errors: list[str], message: str) -> None:
    errors.append(message)


def check_local_links(errors: list[str]) -> None:
    link_pattern = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
    for document in ROOT.rglob("*.md"):
        for destination in link_pattern.findall(document.read_text(encoding="utf-8")):
            target = destination.split()[0].split("#")[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if not (document.parent / target).resolve().exists():
                error(errors, f"Broken local link in {document.relative_to(ROOT)}: {destination}")


def main() -> int:
    errors: list[str] = []
    data = json.loads((ROOT / "prompts.json").read_text(encoding="utf-8"))
    prompts = data.get("prompts", [])
    metadata = data.get("metadata", {})
    ids: set[str] = set()
    phase_counts: dict[str, int] = {"Phase 1": 0, "Phase 2": 0}

    for index, prompt in enumerate(prompts, start=1):
        missing = REQUIRED_FIELDS - prompt.keys()
        if missing:
            error(errors, f"Prompt #{index} is missing: {', '.join(sorted(missing))}")
            continue
        identifier = prompt["id"]
        if not re.fullmatch(r"P[12]-\d{3}(?:-[a-z0-9-]+)?", identifier):
            error(errors, f"Invalid prompt ID: {identifier}")
        if identifier in ids:
            error(errors, f"Duplicate prompt ID: {identifier}")
        ids.add(identifier)
        if prompt["phase"] not in phase_counts:
            error(errors, f"Invalid phase for {identifier}: {prompt['phase']}")
        else:
            phase_counts[prompt["phase"]] += 1
        if not isinstance(prompt["tags"], list) or len(prompt["tags"]) < 3:
            error(errors, f"{identifier} must contain at least three tags")
        for field in REQUIRED_FIELDS - {"tags"}:
            if not isinstance(prompt[field], str) or not prompt[field].strip():
                error(errors, f"{identifier}.{field} must be a non-empty string")

    if metadata.get("total_prompts") != len(prompts):
        error(errors, "metadata.total_prompts does not match the prompt list")
    if metadata.get("phase_1_prompts") != phase_counts["Phase 1"]:
        error(errors, "metadata.phase_1_prompts does not match Phase 1")
    if metadata.get("phase_2_prompts") != phase_counts["Phase 2"]:
        error(errors, "metadata.phase_2_prompts does not match Phase 2")

    categories = json.loads((ROOT / "categories.json").read_text(encoding="utf-8"))
    mapped: set[str] = set()
    for phase, category_map in categories.items():
        for category, category_ids in category_map.items():
            for identifier in category_ids:
                if identifier in mapped:
                    error(errors, f"Category mapping repeats ID: {identifier}")
                mapped.add(identifier)
                matching = next((p for p in prompts if p["id"] == identifier), None)
                if matching is None:
                    error(errors, f"Category mapping references unknown ID: {identifier}")
                elif matching["phase"] != phase or matching["category"] != category:
                    error(errors, f"Category mapping disagrees with {identifier}")
    if mapped != ids:
        error(errors, "Category mapping does not cover exactly the prompt IDs")

    capability_data = json.loads((ROOT / "capability-packs-v2.json").read_text(encoding="utf-8"))
    capability_cards = capability_data.get("packs", [])
    capability_ids: set[str] = set()
    for index, card in enumerate(capability_cards, start=1):
        missing = CAPABILITY_REQUIRED_FIELDS - card.keys()
        if missing:
            error(errors, f"Capability card #{index} is missing: {', '.join(sorted(missing))}")
            continue
        identifier = card["id"]
        if not re.fullmatch(r"[A-Z][A-Z0-9]*-\d{3}", identifier):
            error(errors, f"Invalid capability card ID: {identifier}")
        if identifier in capability_ids or identifier in ids:
            error(errors, f"Duplicate capability card ID: {identifier}")
        capability_ids.add(identifier)
        if card["operation"] not in {"generate", "edit", "extend", "compose", "iterate"}:
            error(errors, f"Invalid operation for {identifier}: {card['operation']}")
        if not isinstance(card["variables"], list):
            error(errors, f"{identifier}.variables must be an array")
        if not isinstance(card["acceptance_criteria"], list) or not card["acceptance_criteria"]:
            error(errors, f"{identifier} must include acceptance criteria")
        if card["output"].get("format") not in {"png", "jpeg", "webp"}:
            error(errors, f"{identifier} has an unsupported output format")
        if not {"requires_consent_for_people", "no_unlicensed_logos"} <= card["rights_and_safety"].keys():
            error(errors, f"{identifier} is missing a rights-and-safety control")
    if capability_data.get("metadata", {}).get("total_cards") != len(capability_cards):
        error(errors, "Capability metadata total does not match the card list")

    video_data = json.loads((ROOT / "site" / "data" / "video-prompts.json").read_text(encoding="utf-8"))
    video_prompts = video_data.get("prompts", [])
    video_ids: set[str] = set()
    required_video_fields = {"id", "domain", "category", "title", "prompt", "best_for", "operation", "output", "acceptance_criteria", "rights_and_safety", "tags"}
    for index, prompt in enumerate(video_prompts, start=1):
        missing = required_video_fields - prompt.keys()
        if missing:
            error(errors, f"Video prompt #{index} is missing: {', '.join(sorted(missing))}")
            continue
        identifier = prompt["id"]
        if not re.fullmatch(r"VID-\d{3}", identifier):
            error(errors, f"Invalid video prompt ID: {identifier}")
        if identifier in video_ids or identifier in ids or identifier in capability_ids:
            error(errors, f"Duplicate video prompt ID: {identifier}")
        video_ids.add(identifier)
        if prompt["domain"] != "Video":
            error(errors, f"{identifier} must use the Video domain")
        if not isinstance(prompt["tags"], list) or len(prompt["tags"]) < 3:
            error(errors, f"{identifier} must contain at least three tags")
        if not isinstance(prompt["acceptance_criteria"], list) or not prompt["acceptance_criteria"]:
            error(errors, f"{identifier} must include acceptance criteria")
        if not isinstance(prompt["output"], dict) or not prompt["output"].get("format"):
            error(errors, f"{identifier} must include an output format")
    if video_data.get("metadata", {}).get("total_prompts") != len(video_prompts):
        error(errors, "Video metadata total does not match the prompt list")
    general_data = json.loads((ROOT / "site" / "data" / "general-prompts.json").read_text(encoding="utf-8"))
    general_prompts = general_data.get("prompts", [])
    general_ids: set[str] = set()
    general_domains = {"Writing": ("WRT", "write"), "Learning": ("LRN", "learn"), "Business": ("BUS", "plan")}
    for index, prompt in enumerate(general_prompts, start=1):
        missing = required_video_fields - prompt.keys()
        if missing:
            error(errors, f"General prompt #{index} is missing: {', '.join(sorted(missing))}")
            continue
        identifier = prompt["id"]
        domain = prompt["domain"]
        if domain not in general_domains:
            error(errors, f"{identifier} has an invalid general domain: {domain}")
            continue
        prefix, operation = general_domains[domain]
        if not re.fullmatch(rf"{prefix}-\d{{3}}", identifier):
            error(errors, f"Invalid {domain.lower()} prompt ID: {identifier}")
        if identifier in general_ids or identifier in ids or identifier in capability_ids or identifier in video_ids:
            error(errors, f"Duplicate general prompt ID: {identifier}")
        general_ids.add(identifier)
        if prompt["operation"] != operation:
            error(errors, f"Invalid operation for {identifier}: {prompt['operation']}")
        if not isinstance(prompt["tags"], list) or len(prompt["tags"]) < 3:
            error(errors, f"{identifier} must contain at least three tags")
        if not isinstance(prompt["acceptance_criteria"], list) or not prompt["acceptance_criteria"]:
            error(errors, f"{identifier} must include acceptance criteria")
        if not isinstance(prompt["output"], dict) or not prompt["output"].get("format"):
            error(errors, f"{identifier} must include an output format")
    if general_data.get("metadata", {}).get("total_prompts") != len(general_prompts):
        error(errors, "General prompt metadata total does not match the prompt list")
    for path in (
        ROOT / "site" / "image" / "index.html", ROOT / "site" / "video" / "index.html",
        ROOT / "site" / "writing" / "index.html", ROOT / "site" / "learning" / "index.html",
        ROOT / "site" / "business" / "index.html"
    ):
        if not path.exists():
            error(errors, f"Missing dedicated collection page: {path.relative_to(ROOT)}")

    combined = CATALOGS[0].read_text(encoding="utf-8")
    for identifier in ids:
        if identifier not in combined:
            error(errors, f"Combined catalog does not contain {identifier}")
    for catalog, phase in zip(CATALOGS[1:], ("P1-", "P2-")):
        text = catalog.read_text(encoding="utf-8")
        for identifier in ids:
            if identifier.startswith(phase) and identifier not in text:
                error(errors, f"{catalog.name} does not contain {identifier}")

    check_local_links(errors)
    if errors:
        print("Validation failed:", file=sys.stderr)
        print("\n".join(f"- {item}" for item in errors), file=sys.stderr)
        return 1
    print(f"Validated {len(prompts)} image prompts, {len(capability_cards)} capability cards, {len(video_prompts)} video prompts, {len(general_prompts)} general prompts, categories, catalogs, and local links.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
