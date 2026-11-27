"""Read and normalize App Store / Google Play review CSVs."""
from __future__ import annotations

import csv
import re
from datetime import datetime, timezone
from pathlib import Path

PLATFORM_ALIASES = {
    "ios": "iOS",
    "app store": "iOS",
    "appstore": "iOS",
    "apple": "iOS",
    "android": "Android",
    "google play": "Android",
    "googleplay": "Android",
    "play": "Android",
}


def parse_datetime(value) -> datetime | None:
    s = str(value or "").strip()
    if not s:
        return None
    if re.fullmatch(r"\d{10}", s):
        return datetime.fromtimestamp(int(s), tz=timezone.utc)
    if re.fullmatch(r"\d{13}", s):
        return datetime.fromtimestamp(int(s) / 1000, tz=timezone.utc)
    s2 = s.replace("Z", "+00:00").replace("/", "-")
    try:
        dt = datetime.fromisoformat(s2)
    except ValueError:
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
            try:
                dt = datetime.strptime(s2, fmt)
                break
            except ValueError:
                dt = None
        if dt is None:
            return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def normalize_platform(value, hint: str = "") -> str:
    raw = str(value or hint or "").strip()
    return PLATFORM_ALIASES.get(raw.lower(), raw or hint or "Unknown")


def _text(row: dict) -> str:
    parts = []
    for key in ("标题", "正文", "text", "content"):
        v = str(row.get(key) or "").strip()
        if v and v not in parts:
            parts.append(v)
    return " ".join(parts).strip()


def _rating(row: dict) -> int:
    raw = row.get("评分", row.get("rating", 0))
    try:
        value = int(float(str(raw).strip()))
    except (TypeError, ValueError):
        return 0
    return value if 1 <= value <= 5 else 0


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def load_dataset(spec: dict) -> dict:
    path = Path(spec["path"]).expanduser().resolve()
    if not path.exists():
        raise FileNotFoundError(f"dataset not found: {path}")
    hint = str(spec.get("platform") or "")
    rows: list[dict] = []
    for idx, raw in enumerate(read_csv(path)):
        text = _text(raw)
        rating = _rating(raw)
        dt = parse_datetime(raw.get("时间") or raw.get("date") or raw.get("created_at"))
        platform = normalize_platform(raw.get("平台"), hint)
        rid = str(raw.get("评论ID") or raw.get("id") or f"{path.stem}-{idx}")
        likes = raw.get("点赞数", raw.get("likes", 0))
        try:
            likes = int(float(str(likes or 0)))
        except (TypeError, ValueError):
            likes = 0
        rows.append(
            {
                "id": rid,
                "platform": platform,
                "rating": rating,
                "text": text,
                "date": dt,
                "country": str(raw.get("国家") or raw.get("语言") or "").strip(),
                "version": str(raw.get("版本") or "").strip(),
                "likes": likes,
                "source": str(spec.get("name") or path.stem),
            }
        )
    dates = [r["date"] for r in rows if r["date"]]
    return {
        "name": str(spec.get("name") or path.stem),
        "platform": hint or (rows[0]["platform"] if rows else "Unknown"),
        "path": str(path),
        "rows": rows,
        "meta": {
            "rows": len(rows),
            "with_date": len(dates),
            "date_min": min(dates).isoformat() if dates else None,
            "date_max": max(dates).isoformat() if dates else None,
        },
    }


def load_datasets(specs: list[dict]) -> list[dict]:
    if not specs:
        raise ValueError("at least one dataset is required")
    return [load_dataset(spec) for spec in specs]
