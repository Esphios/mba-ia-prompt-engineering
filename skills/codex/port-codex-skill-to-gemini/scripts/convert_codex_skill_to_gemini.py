#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import List, Tuple


@dataclass
class ConversionReport:
    source: str
    target: str
    skill_name: str
    copied_files: List[str]
    excluded_files: List[str]
    imported_metadata: List[str]
    warnings: List[str]


def parse_frontmatter(text: str) -> Tuple[dict, str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError("SKILL.md is missing YAML frontmatter")

    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        raise ValueError("Unterminated YAML frontmatter in SKILL.md")

    meta_lines = lines[1:end_idx]
    body = "\n".join(lines[end_idx + 1 :]).lstrip("\n")

    meta: dict[str, str] = {}
    for line in meta_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        meta[key.strip()] = value.strip().strip('"').strip("'")

    return meta, body


def build_frontmatter(meta: dict, body: str) -> str:
    lines = ["---"]
    for required_key in ("name", "description"):
        value = str(meta.get(required_key, "")).strip()
        if not value:
            raise ValueError(f"Missing required frontmatter field: {required_key}")
        lines.append(f"{required_key}: {value}")
    for key, value in meta.items():
        if key in {"name", "description"}:
            continue
        lines.append(f"{key}: {value}")
    lines.append("---")
    lines.append("")
    lines.append(body.rstrip() + "\n")
    return "\n".join(lines)


def parse_simple_yaml_sections(text: str) -> dict[str, dict[str, str]]:
    sections: dict[str, dict[str, str]] = {}
    current_section: str | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        if not line.startswith(" ") and line.endswith(":"):
            current_section = line[:-1].strip()
            sections[current_section] = {}
            continue

        if current_section and line.startswith("  "):
            stripped = line.strip()
            if ":" not in stripped:
                continue
            key, value = stripped.split(":", 1)
            sections[current_section][key.strip()] = value.strip().strip('"').strip("'")

    return sections


def load_codex_interface_metadata(source: Path) -> Tuple[dict[str, str], List[str]]:
    openai_yaml = source / "agents" / "openai.yaml"
    warnings: List[str] = []
    if not openai_yaml.exists():
        return {}, warnings

    sections = parse_simple_yaml_sections(openai_yaml.read_text(encoding="utf-8"))
    interface = sections.get("interface", {})
    policy = sections.get("policy", {})

    if policy.get("allow_implicit_invocation"):
        warnings.append(
            "Source agents/openai.yaml included policy.allow_implicit_invocation. "
            "That metadata was not carried over as Gemini-native behavior."
        )

    return interface, warnings


def inject_imported_metadata_section(body: str, interface: dict[str, str]) -> Tuple[str, List[str]]:
    imported_items: List[str] = []
    if not interface:
        return body, imported_items

    section_lines = [
        "## Imported Metadata",
        "",
        "Preserve the following source metadata as reference only. Gemini does not consume it as native config.",
        "",
    ]

    field_labels = {
        "display_name": "Display name",
        "short_description": "Short description",
        "default_prompt": "Suggested prompt",
    }

    for key in ("display_name", "short_description", "default_prompt"):
        value = interface.get(key, "").strip()
        if not value:
            continue
        section_lines.append(f"- `{field_labels[key]}`: `{value}`")
        imported_items.append(key)

    if not imported_items:
        return body, imported_items

    section = "\n".join(section_lines)
    if "## Imported Metadata" in body:
        return body, imported_items

    lines = body.splitlines()
    insert_at = len(lines)
    heading_count = 0

    for idx, line in enumerate(lines):
        if line.startswith("# "):
            heading_count = 1
            continue
        if heading_count == 1 and line.startswith("## "):
            insert_at = idx
            break

    new_lines = lines[:insert_at]
    if new_lines and new_lines[-1].strip():
        new_lines.append("")
    new_lines.extend(section.splitlines())
    new_lines.append("")
    new_lines.extend(lines[insert_at:])
    return "\n".join(new_lines).rstrip() + "\n", imported_items


def is_codex_only_file(path: Path, skill_root: Path) -> bool:
    rel = path.relative_to(skill_root).as_posix()
    return rel == "agents/openai.yaml"


def copy_tree_filtered(source: Path, target: Path) -> Tuple[List[str], List[str]]:
    copied: List[str] = []
    excluded: List[str] = []

    for item in source.rglob("*"):
        rel = item.relative_to(source)
        target_item = target / rel

        if item.is_dir():
            continue

        if is_codex_only_file(item, source):
            excluded.append(rel.as_posix())
            continue

        target_item.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target_item)
        copied.append(rel.as_posix())

    return copied, excluded


def convert_skill(source: Path, target: Path) -> ConversionReport:
    if not source.exists() or not source.is_dir():
        raise FileNotFoundError(f"Source directory not found: {source}")

    skill_md = source / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"Missing required file: {skill_md}")

    raw = skill_md.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)
    if "name" not in meta or "description" not in meta:
        raise ValueError("SKILL.md frontmatter must include name and description")

    interface_metadata, metadata_warnings = load_codex_interface_metadata(source)
    body, imported_metadata = inject_imported_metadata_section(body, interface_metadata)

    target.mkdir(parents=True, exist_ok=True)
    copied_files, excluded_files = copy_tree_filtered(source, target)

    converted_skill_md = build_frontmatter(meta, body)
    (target / "SKILL.md").write_text(converted_skill_md, encoding="utf-8")

    warnings: List[str] = list(metadata_warnings)
    openai_yaml = source / "agents" / "openai.yaml"
    if openai_yaml.exists():
        warnings.append(
            "Excluded Codex-specific file agents/openai.yaml after importing recoverable interface metadata into SKILL.md."
        )

    return ConversionReport(
        source=str(source.resolve()),
        target=str(target.resolve()),
        skill_name=meta["name"],
        copied_files=sorted(set(copied_files + ["SKILL.md"])),
        excluded_files=sorted(set(excluded_files)),
        imported_metadata=imported_metadata,
        warnings=warnings,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert a Codex skill folder into a Gemini-compatible skill folder."
    )
    parser.add_argument("--source", required=True, help="Path to the source Codex skill directory")
    parser.add_argument("--target", required=True, help="Path to the target Gemini skill directory")
    parser.add_argument(
        "--report-json",
        default="",
        help="Optional path to write a JSON conversion report",
    )
    args = parser.parse_args()

    source = Path(os.path.expanduser(args.source)).resolve()
    target = Path(os.path.expanduser(args.target)).resolve()

    report = convert_skill(source, target)

    print(f"Converted skill: {report.skill_name}")
    print(f"Source: {report.source}")
    print(f"Target: {report.target}")
    print("")
    print("Copied files:")
    for item in report.copied_files:
        print(f"  - {item}")

    if report.excluded_files:
        print("")
        print("Excluded files:")
        for item in report.excluded_files:
            print(f"  - {item}")

    if report.imported_metadata:
        print("")
        print("Imported metadata:")
        for item in report.imported_metadata:
            print(f"  - {item}")

    if report.warnings:
        print("")
        print("Warnings:")
        for item in report.warnings:
            print(f"  - {item}")

    if args.report_json:
        report_path = Path(os.path.expanduser(args.report_json)).resolve()
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
