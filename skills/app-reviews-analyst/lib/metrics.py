"""Deterministic metrics for app review analysis."""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from datetime import timedelta
from statistics import mean

from taxonomy import Taxonomy

PII_PATTERNS = [
    (re.compile(r"https?://\S+", re.I), "[链接已隐去]"),
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[邮箱已隐去]"),
    (re.compile(r"@[A-Za-z0-9_.-]{2,}"), "[账号已隐去]"),
    (re.compile(r"\+?\d[\d\s-]{7,}\d"), "[号码已隐去]"),
]


def scrub(text: str) -> str:
    s = str(text or "")
    for pattern, repl in PII_PATTERNS:
        s = pattern.sub(repl, s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def segments(rows: list[dict]) -> list[str]:
    order = []
    for row in rows:
        p = str(row.get("platform") or "Unknown")
        if p not in order:
            order.append(p)
    return order


def rating_distribution(rows: list[dict]) -> dict:
    out = {}
    for seg in segments(rows):
        subset = [r for r in rows if r.get("platform") == seg and r.get("rating")]
        counts = Counter(int(r["rating"]) for r in subset)
        total = sum(counts.values())
        out[seg] = {
            "total": total,
            "counts": {str(i): counts.get(i, 0) for i in range(1, 6)},
            "shares": {str(i): round(counts.get(i, 0) / total * 100, 1) if total else 0.0 for i in range(1, 6)},
        }
    return out


def negative_share(rows: list[dict], rating_max: int = 2) -> dict:
    out = {}
    for seg in segments(rows):
        subset = [r for r in rows if r.get("platform") == seg and r.get("rating")]
        neg = [r for r in subset if int(r["rating"]) <= rating_max]
        out[seg] = {
            "negative": len(neg),
            "total": len(subset),
            "share": round(len(neg) / len(subset) * 100, 1) if subset else 0.0,
            "rating_max": rating_max,
        }
    return out


def theme_share(rows: list[dict], taxonomy: Taxonomy, rating_max: int = 2) -> dict:
    out = {}
    for seg in segments(rows):
        subset = [r for r in rows if r.get("platform") == seg and r.get("rating") and int(r["rating"]) <= rating_max]
        counts = Counter()
        for row in subset:
            counts.update(taxonomy.classify(row.get("text") or ""))
        total = len(subset)
        out[seg] = {
            "negative_total": total,
            "counts": {t: counts.get(t, 0) for t in taxonomy.order()},
            "shares": {t: round(counts.get(t, 0) / total * 100, 1) if total else 0.0 for t in taxonomy.order()},
        }
    return out


def theme_gap(theme_data: dict) -> list[dict]:
    segs = list(theme_data.keys())
    if len(segs) < 2:
        return []
    a, b = segs[0], segs[1]
    rows = []
    for theme in theme_data[a]["shares"]:
        va = theme_data[a]["shares"].get(theme, 0.0)
        vb = theme_data[b]["shares"].get(theme, 0.0)
        rows.append({"theme": theme, "a": a, "b": b, "a_share": va, "b_share": vb, "gap": round(va - vb, 1)})
    rows.sort(key=lambda r: abs(r["gap"]), reverse=True)
    return rows


def daily_negative(rows: list[dict], rating_max: int = 2, window: int = 3) -> dict:
    out = {}
    for seg in segments(rows):
        subset = [r for r in rows if r.get("platform") == seg and r.get("date") and r.get("rating")]
        by_day = defaultdict(lambda: [0, 0])
        for row in subset:
            day = row["date"].date()
            by_day[day][1] += 1
            if int(row["rating"]) <= rating_max:
                by_day[day][0] += 1
        if not by_day:
            out[seg] = []
            continue
        start, end = min(by_day), max(by_day)
        days = []
        d = start
        while d <= end:
            neg, total = by_day.get(d, [0, 0])
            days.append({"date": d.isoformat(), "negative": neg, "total": total, "rate": round(neg / total * 100, 1) if total else None})
            d += timedelta(days=1)
        # centered moving average, skip days without data
        for i, item in enumerate(days):
            vals = [x["rate"] for x in days[max(0, i - window // 2): i + window // 2 + 1] if x["rate"] is not None]
            item["smooth"] = round(mean(vals), 1) if vals else None
        out[seg] = days
    return out


def top_quotes(rows: list[dict], taxonomy: Taxonomy, rating_max: int = 2, max_quotes: int = 2, max_themes: int = 3) -> dict:
    out = {}
    for seg in segments(rows):
        subset = [r for r in rows if r.get("platform") == seg and r.get("rating") and int(r["rating"]) <= rating_max]
        if not subset:
            out[seg] = []
            continue
        counts = Counter()
        for row in subset:
            counts.update(taxonomy.classify(row.get("text") or ""))
        theme_order = [t for t, _ in counts.most_common(max_themes)]
        used = set()
        picked = []
        for theme in theme_order:
            n = 0
            for row in sorted(subset, key=lambda r: (-int(r.get("likes") or 0), -len(str(r.get("text") or "")))):
                if n >= max_quotes:
                    break
                text = scrub(row.get("text") or "")
                if not text or text in used or theme not in taxonomy.classify(text):
                    continue
                if len(text) < 15:
                    continue
                used.add(text)
                picked.append({"theme": theme, "text": text[:260]})
                n += 1
        out[seg] = picked
    return out


def segment_meta(rows: list[dict]) -> dict:
    out = {}
    for seg in segments(rows):
        subset = [r for r in rows if r.get("platform") == seg]
        dates = sorted(r["date"] for r in subset if r.get("date"))
        countries = Counter(r.get("country") for r in subset if r.get("country"))
        versions = Counter(r.get("version") for r in subset if r.get("version"))
        out[seg] = {
            "rows": len(subset),
            "date_min": dates[0].isoformat() if dates else None,
            "date_max": dates[-1].isoformat() if dates else None,
            "countries": countries.most_common(5),
            "versions": versions.most_common(5),
        }
    return out
