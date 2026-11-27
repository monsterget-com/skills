"""Keyword taxonomy loading and classification."""
from __future__ import annotations

import json
import re
from pathlib import Path


class Taxonomy:
    def __init__(self, data: dict):
        self.id = str(data.get("id") or "custom")
        self.version = str(data.get("version") or "0")
        self.themes: list[dict] = []
        for item in data.get("themes") or []:
            patterns = [re.compile(p, re.IGNORECASE) for p in item.get("patterns") or []]
            if not patterns:
                continue
            self.themes.append(
                {
                    "id": str(item["id"]),
                    "label_zh": str(item.get("label_zh") or item["id"]),
                    "label_en": str(item.get("label_en") or item["id"]),
                    "patterns": patterns,
                }
            )

    def classify(self, text: str) -> list[str]:
        t = str(text or "")
        return [theme["id"] for theme in self.themes if any(p.search(t) for p in theme["patterns"])]

    def label(self, theme_id: str, lang: str = "zh") -> str:
        for theme in self.themes:
            if theme["id"] == theme_id:
                return theme["label_en"] if lang == "en" else theme["label_zh"]
        return theme_id

    def order(self) -> list[str]:
        return [theme["id"] for theme in self.themes]


def load_taxonomy(path: Path) -> Taxonomy:
    data = json.loads(Path(path).read_text("utf-8"))
    return Taxonomy(data)
