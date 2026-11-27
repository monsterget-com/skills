#!/usr/bin/env python3
"""VOC analyzer — normalize comment/review CSV exports and compute VOC stats.

Stdlib only. Designed for the MonsterGet `voc-miner` skill.

Usage:
  python analyze.py --type comment --input comments1.csv comments2.csv --out comments.json
  python analyze.py --type review  --input reviews1.csv reviews2.csv   --out reviews.json
  python analyze.py --preset voc --comments comments.json --reviews reviews.json --out stats.json

The script does NOT code themes. Theme coding and clustering are done by the
LLM using references/taxonomy.md; this script only normalizes and computes
deterministic counts/percentiles so the LLM does not have to do arithmetic.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import statistics
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Generic helpers
# ---------------------------------------------------------------------------

CJK_RE = re.compile(r"[\u4e00-\u9fff]+")
WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9'\-]{1,}")

STOPWORDS_EN = {
    "the", "and", "for", "you", "your", "this", "that", "with", "have", "has",
    "but", "not", "are", "was", "were", "from", "they", "them", "will", "would",
    "can", "could", "should", "about", "what", "when", "where", "which", "who",
    "how", "why", "all", "any", "our", "out", "get", "got", "just", "too", "very",
    "really", "much", "more", "most", "some", "than", "then", "there", "here",
    "been", "being", "into", "over", "under", "again", "also", "only", "even",
    "still", "such", "because", "before", "after", "while", "does", "did", "doing",
    "use", "used", "using", "make", "made", "like", "want", "need", "one", "two",
}

STOPWORDS_ZH = {
    "这个", "那个", "就是", "真的", "可以", "没有", "什么", "怎么", "为什么",
    "还是", "但是", "因为", "所以", "如果", "已经", "我们", "你们", "他们",
    "一个", "不是", "现在", "感觉", "觉得", "而且", "然后", "这么", "那么",
    "东西", "时候", "问题", "使用", "用了", "一直", "有点", "非常", "特别",
}


def norm_key(value: str) -> str:
    return re.sub(r"[\s_\-]+", "", (value or "").strip().lower())


def pick(row: dict, aliases: list[str]):
    """Return the first non-empty value matching an alias (case/space-insensitive)."""
    if not row:
        return None
    lookup = {norm_key(k): v for k, v in row.items()}
    for alias in aliases:
        v = lookup.get(norm_key(alias))
        if v is not None and str(v).strip() != "":
            return v
    return None


def parse_number(raw) -> float | None:
    if raw is None:
        return None
    if isinstance(raw, (int, float)):
        return float(raw)
    s = str(raw).strip().replace(",", "").replace(" ", "")
    if not s:
        return None
    mult = 1.0
    suffix = s[-1].upper()
    if suffix in ("K", "M", "B"):
        mult = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000}[suffix]
        s = s[:-1]
    elif s.endswith("万"):
        mult = 10_000
        s = s[:-1]
    elif s.endswith("亿"):
        mult = 100_000_000
        s = s[:-1]
    s = s.replace("%", "")
    try:
        return float(s) * mult
    except ValueError:
        return None


def parse_date(raw) -> str | None:
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    # epoch seconds / milliseconds
    if re.fullmatch(r"\d{10,13}", s):
        n = int(s)
        if len(s) == 13:
            n //= 1000
        try:
            return datetime.fromtimestamp(n, tz=timezone.utc).isoformat()
        except (ValueError, OSError):
            pass
    # ISO and common formats
    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%Y/%m/%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
    ):
        try:
            dt = datetime.strptime(s, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat()
        except ValueError:
            continue
    return s  # keep original if unknown


def sentence_case(s: str) -> str:
    s = (s or "").strip()
    return s[:1].upper() + s[1:] if s else s


# ---------------------------------------------------------------------------
# Normalization
# ---------------------------------------------------------------------------

COMMENT_ALIASES = {
    "id": ["评论ID", "id", "comment_id", "cid"],
    "text": ["评论内容", "评论", "正文", "text", "comment", "content", "body"],
    "author": ["用户名", "作者", "用户名称", "authorName", "author", "user", "username"],
    "likes": ["点赞量", "点赞数", "点赞", "likeCount", "likes", "like_count"],
    "replies": ["子评论数", "回复数", "replyCount", "replies", "reply_count"],
    "date": ["评论时间", "发布时间", "publishTime", "createdAt", "createTime", "date", "time"],
    "url": ["视频链接", "推文链接", "评论链接", "sourceTweetUrl", "tweetUrl", "url", "link"],
    "platform": ["platform", "平台"],
    "parent_id": ["父评论ID", "parentCommentId", "parent_id"],
    "depth": ["评论层级", "depth", "level"],
}

REVIEW_ALIASES = {
    "id": ["Review ID", "评论ID", "id", "review_id"],
    "rating": ["评分", "rating", "stars", "star"],
    "title": ["标题", "title", "subject"],
    "text": ["正文", "评论内容", "内容", "text", "review", "content", "body"],
    "author": ["用户", "用户名称", "author", "user", "username"],
    "date": ["时间", "评论时间", "date", "published_at", "createdAt", "time"],
    "version": ["版本", "version", "app_version"],
    "country": ["国家", "country", "storefront"],
    "lang": ["语言", "lang", "language"],
    "developer_reply": ["开发者回复", "developer_reply", "reply", "developerResponse"],
    "helpful": ["点赞数", "helpful", "helpful_count", "likes"],
    "platform": ["Platform", "platform", "平台"],
}


def normalize_platform(value: str) -> str:
    p = (value or "").strip().lower().replace("_", "-").replace(" ", "-")
    if p in ("appstore", "app-store", "ios", "apple"):
        return "app-store"
    if p in ("googleplay", "google-play", "android", "play"):
        return "google-play"
    return p


def infer_platform(row: dict, fallback: str = "") -> str:
    p = pick(row, ["platform", "平台"])
    if p:
        return normalize_platform(str(p))
    headers = " ".join(row.keys()).lower()
    if "tiktok" in headers:
        return "tiktok"
    if "tweet" in headers or "x.com" in headers:
        return "x"
    if "app store" in headers or "apps.apple" in headers:
        return "app-store"
    if "google play" in headers or "play.google" in headers:
        return "google-play"
    return normalize_platform(fallback)


def normalize_rows(rows: list[dict], kind: str, source: str) -> list[dict]:
    aliases = COMMENT_ALIASES if kind == "comment" else REVIEW_ALIASES
    out = []
    for row in rows:
        text = pick(row, aliases["text"])
        if text is None or str(text).strip() == "":
            continue
        item = {
            "id": str(pick(row, aliases["id"]) or ""),
            "platform": infer_platform(row, "tiktok" if kind == "comment" else ""),
            "source_file": source,
            "text": str(text).strip(),
            "author": str(pick(row, aliases["author"]) or "").strip(),
            "url": str(pick(row, aliases["url"]) or "").strip() if "url" in aliases else "",
            "date": parse_date(pick(row, aliases["date"])),
        }
        if kind == "comment":
            item.update({
                "likes": parse_number(pick(row, aliases["likes"])),
                "replies": parse_number(pick(row, aliases["replies"])),
                "parent_id": str(pick(row, aliases["parent_id"]) or ""),
                "depth": parse_number(pick(row, aliases["depth"])),
            })
        else:
            item.update({
                "rating": parse_number(pick(row, aliases["rating"])),
                "title": str(pick(row, aliases["title"]) or "").strip(),
                "version": str(pick(row, aliases["version"]) or "").strip(),
                "country": str(pick(row, aliases["country"]) or "").strip(),
                "lang": str(pick(row, aliases["lang"]) or "").strip(),
                "developer_reply": str(pick(row, aliases["developer_reply"]) or "").strip(),
                "helpful": parse_number(pick(row, aliases["helpful"])),
            })
        out.append(item)
    return out


def dedupe(items: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for item in items:
        key = (
            (item.get("text") or "").strip().lower(),
            (item.get("author") or "").strip().lower(),
            (item.get("url") or "").strip().lower(),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def read_csv(path: Path) -> list[dict]:
    for enc in ("utf-8-sig", "utf-8", "gbk"):
        try:
            with path.open("r", encoding=enc, newline="") as f:
                return list(csv.DictReader(f))
        except UnicodeDecodeError:
            continue
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------

def keywords(items: list[dict], limit: int = 50) -> list[list]:
    counter = Counter()
    for item in items:
        text = item.get("text") or ""
        for w in WORD_RE.findall(text.lower()):
            if w not in STOPWORDS_EN and len(w) > 2:
                counter[w] += 1
        for run in CJK_RE.findall(text):
            if len(run) < 2:
                continue
            for i in range(len(run) - 1):
                bg = run[i:i + 2]
                if bg not in STOPWORDS_ZH:
                    counter[bg] += 1
    return [[w, c] for w, c in counter.most_common(limit)]


def confidence(comments: list[dict], reviews: list[dict], sources: int) -> dict:
    n = len(comments) + len(reviews)
    if n < 30:
        level = "Low"
    elif n < 100:
        level = "Medium"
    elif len(reviews) >= 300 or len(comments) >= 100:
        level = "High"
    else:
        level = "Medium"
    reasons = [f"total={n}", f"comments={len(comments)}", f"reviews={len(reviews)}", f"sources={sources}"]
    if sources < 2:
        level = "Low" if level == "Medium" else level
        reasons.append("single source")
    return {"level": level, "reasons": reasons}


def stats_for(comments: list[dict], reviews: list[dict]) -> dict:
    platforms = Counter()
    dates = []
    for item in comments + reviews:
        platforms[item.get("platform") or "unknown"] += 1
        if item.get("date"):
            dates.append(item["date"])

    ratings = [r["rating"] for r in reviews if isinstance(r.get("rating"), (int, float))]
    rating_dist = Counter(str(int(r)) if float(r).is_integer() else str(r) for r in ratings)
    rating_stats = {
        "count": len(ratings),
        "mean": round(statistics.mean(ratings), 2) if ratings else None,
        "median": statistics.median(ratings) if ratings else None,
        "distribution": dict(sorted(rating_dist.items())),
    }

    by_country = Counter(r.get("country") or "unknown" for r in reviews)
    by_lang = Counter(r.get("lang") or "unknown" for r in reviews)
    by_version = Counter(r.get("version") or "unknown" for r in reviews)

    return {
        "counts": {
            "total": len(comments) + len(reviews),
            "comments": len(comments),
            "reviews": len(reviews),
            "by_platform": dict(platforms),
        },
        "ratings": rating_stats,
        "countries": dict(by_country.most_common(20)),
        "languages": dict(by_lang.most_common(20)),
        "versions": dict(by_version.most_common(20)),
        "dates": {"min": min(dates) if dates else None, "max": max(dates) if dates else None},
        "top_keywords": keywords(comments + reviews),
        "confidence": confidence(comments, reviews, len(platforms)),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser(description="Normalize VOC CSVs and compute stats.")
    ap.add_argument("--type", choices=["comment", "review"], help="input type")
    ap.add_argument("--input", nargs="+", help="CSV files")
    ap.add_argument("--out", required=True, help="output JSON")
    ap.add_argument("--preset", choices=["voc"], help="compute a preset")
    ap.add_argument("--comments", help="normalized comments JSON")
    ap.add_argument("--reviews", help="normalized reviews JSON")
    args = ap.parse_args()

    if args.preset == "voc":
        comments = load_json(args.comments).get("items", []) if args.comments else []
        reviews = load_json(args.reviews).get("items", []) if args.reviews else []
        result = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "stats": stats_for(comments, reviews),
        }
        Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(result["stats"]["counts"], ensure_ascii=False))
        return 0

    if not args.type or not args.input:
        ap.error("--type and --input are required unless --preset voc is used")

    items: list[dict] = []
    for name in args.input:
        path = Path(name)
        if not path.exists():
            print(f"missing input: {name}", file=sys.stderr)
            return 2
        rows = read_csv(path)
        items.extend(normalize_rows(rows, args.type, path.name))

    items = dedupe(items)
    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "kind": args.type,
        "inputs": [Path(p).name for p in args.input],
        "count": len(items),
        "items": items,
    }
    Path(args.out).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"kind": args.type, "count": len(items)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
