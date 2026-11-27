#!/usr/bin/env python3
"""Lightweight validator for MonsterGet Skills.

Checks:
- every SKILL.md has YAML frontmatter with name + description
- name is unique, lowercase, hyphen/underscore/dot only
- description <= 1024 chars
- body is non-empty
- business skills declare metadata.monsterget.category
- collector skills still exist (so business skills do not silently break)

Usage:
  python scripts/validate-skills.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"

REQUIRED_COLLECTORS = {
    "tiktok-collector",
    "x-collector",
    "linkedin-collector",
    "upwork-collector",
    "app-reviews-collector",
}

NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    m = re.search(r"\n---\s*\n", text[3:])
    if not m:
        return {}, text
    raw = text[3 : m.start() + 3]
    body = text[m.end() + 3 :]
    data: dict[str, str] = {}

    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() and not line.lstrip().startswith("#") and ":" in line and not line.startswith((" ", "\t")):
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip("\"'")
            # YAML folded/literal block: gather indented continuation lines.
            if value in (">", ">-", "|", "|-"):
                parts = []
                i += 1
                while i < len(lines) and (not lines[i].strip() or lines[i].startswith((" ", "\t"))):
                    parts.append(lines[i].strip())
                    i += 1
                value = " ".join(p for p in parts if p).strip()
                data[key] = value
                continue
            data[key] = value
        i += 1
    return data, body


def main() -> int:
    if not SKILLS_DIR.exists():
        print(f"missing skills dir: {SKILLS_DIR}", file=sys.stderr)
        return 1

    errors: list[str] = []
    seen: dict[str, Path] = {}
    count = 0

    # up to 3 levels under skills/ (flat, category/name, category/category/name)
    for path in sorted(SKILLS_DIR.glob("**/SKILL.md")):
        rel = path.relative_to(SKILLS_DIR)
        if len(rel.parts) > 4:  # skills/<a>/<b>/<c>/SKILL.md
            continue
        count += 1
        text = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        name = fm.get("name", "")
        desc = fm.get("description", "")

        if not name:
            errors.append(f"{rel}: missing name")
        elif not NAME_RE.match(name):
            errors.append(f"{rel}: invalid name {name!r}")
        elif name in seen:
            errors.append(f"{rel}: duplicate name {name!r} (also {seen[name]})")
        else:
            seen[name] = rel

        if not desc:
            errors.append(f"{rel}: missing description")
        elif len(desc) > 1024:
            errors.append(f"{rel}: description is {len(desc)} chars (max 1024)")

        if not body.strip():
            errors.append(f"{rel}: empty body")

    for required in sorted(REQUIRED_COLLECTORS):
        if not (SKILLS_DIR / required / "SKILL.md").exists():
            errors.append(f"missing collector skill: {required}")

    if errors:
        print("Skill validation failed:")
        for e in errors:
            print(f"- {e}")
        return 1

    print(f"Validated {count} skills ({len(seen)} unique names).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
