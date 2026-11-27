#!/usr/bin/env python3
"""MonsterGet app-reviews analyst — CSV in, metrics + HTML report out.

Usage:
  python3 scripts/run.py --job job.json
  python3 scripts/run.py --job job.json --out runs/custom
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT / "lib"))

from ingest import load_datasets  # noqa: E402
from metrics import (  # noqa: E402
    daily_negative,
    negative_share,
    rating_distribution,
    segment_meta,
    theme_gap,
    theme_share,
    top_quotes,
)
from quality import validate  # noqa: E402
from report import render  # noqa: E402
from taxonomy import load_taxonomy  # noqa: E402


def _version() -> dict:
    path = SKILL_ROOT / "VERSION.json"
    try:
        return json.loads(path.read_text("utf-8"))
    except Exception:
        return {"version": "0.0.0", "analysis_schema": "1.0"}


def _parse_day(value: str) -> datetime:
    dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _filter_and_sample(rows: list[dict], options: dict) -> tuple[list[dict], dict]:
    date_range = options.get("date_range") or []
    after_filter = rows
    if len(date_range) == 2:
        start = _parse_day(date_range[0])
        end = _parse_day(date_range[1])
        if "T" not in str(date_range[1]) and " " not in str(date_range[1]):
            end = end + timedelta(days=1)
        after_filter = [r for r in rows if r.get("date") and start <= r["date"] < end]

    target = int(options.get("sample_per_segment") or 0)
    seed = int(options.get("sample_seed") or 42)
    by_seg: dict[str, list[dict]] = {}
    for row in after_filter:
        by_seg.setdefault(str(row.get("platform") or "Unknown"), []).append(row)

    final: list[dict] = []
    stats = {}
    for idx, seg in enumerate(by_seg):
        subset = sorted(by_seg[seg], key=lambda r: (r.get("date") or datetime.min.replace(tzinfo=timezone.utc), str(r.get("id") or "")))
        sampled = False
        if target and len(subset) > target:
            subset = random.Random(seed + idx).sample(subset, target)
            sampled = True
        final.extend(subset)
        stats[seg] = {
            "original": sum(1 for r in rows if r.get("platform") == seg),
            "after_filter": len(by_seg[seg]),
            "final": len(subset),
            "sampled": sampled,
        }
    meta = {
        "date_range": date_range or None,
        "target_per_segment": target or None,
        "seed": seed if target else None,
        "segments": stats,
    }
    return final, meta


def _write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze App Store / Google Play review CSVs.")
    parser.add_argument("--job", required=True, help="path to job JSON")
    parser.add_argument("--out", default="", help="override output directory")
    args = parser.parse_args()

    job_path = Path(args.job).expanduser().resolve()
    job = json.loads(job_path.read_text("utf-8"))
    run_id = str(job.get("run_id") or datetime.now().strftime("%Y%m%d-%H%M%S"))
    out = Path(args.out or job.get("out") or f"runs/{run_id}").expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    options = job.get("options") or {}
    lang = "en" if str(options.get("language", "zh")).lower().startswith("en") else "zh"
    rating_max = int(options.get("rating_max", 2))
    min_rows = int(options.get("min_rows", 50))

    taxonomy_name = options.get("taxonomy") or "app_reviews"
    taxonomy_path = SKILL_ROOT / "taxonomies" / f"{taxonomy_name}.json"
    taxonomy = load_taxonomy(taxonomy_path)

    datasets = load_datasets(job.get("datasets") or [])
    all_rows = [row for ds in datasets for row in ds["rows"]]

    rows, sample_meta = _filter_and_sample(all_rows, options)
    quality = validate(rows, min_rows=min_rows)
    if not quality["ok"]:
        print("ERROR: " + "; ".join(quality["errors"]), file=sys.stderr)
        (out / "quality.json").write_text(json.dumps(quality, ensure_ascii=False, indent=2), "utf-8")
        return 2

    metrics = {
        "schema_version": _version().get("analysis_schema", "1.0"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "recipe": str(job.get("recipe") or "dual_store"),
        "options": {"rating_max": rating_max, "language": lang, "top_quotes": int(options.get("top_quotes", 2))},
        "taxonomy": {
            "id": taxonomy.id,
            "version": taxonomy.version,
            "labels": {t["id"]: {"zh": t["label_zh"], "en": t["label_en"]} for t in taxonomy.themes},
        },
        "sample": sample_meta,
        "quality": quality,
        "segment_meta": segment_meta(rows),
        "rating_distribution": rating_distribution(rows),
        "negative_share": negative_share(rows, rating_max),
        "theme_share": theme_share(rows, taxonomy, rating_max),
        "theme_gap": theme_gap(theme_share(rows, taxonomy, rating_max)),
        "daily": daily_negative(rows, rating_max),
        "quotes": top_quotes(rows, taxonomy, rating_max, max_quotes=int(options.get("top_quotes", 2))),
    }

    version = _version()
    manifest = {
        "run_id": run_id,
        "skill": "monsterget-app-reviews-analyst",
        "skill_version": version.get("version", "0.0.0"),
        "analysis_schema": version.get("analysis_schema", "1.0"),
        "generated_at": metrics["generated_at"],
        "recipe": metrics["recipe"],
        "options": options,
        "datasets": [
            {
                "name": ds["name"],
                "path": ds["path"],
                "platform": ds["platform"],
                "rows": ds["meta"]["rows"],
                "date_min": ds["meta"]["date_min"],
                "date_max": ds["meta"]["date_max"],
            }
            for ds in datasets
        ],
        "outputs": {"metrics": "metrics.json", "report": "report.html", "tables": "tables/"},
        "quality": quality,
        "sample": sample_meta,
    }

    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), "utf-8")
    (out / "metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=2), "utf-8")
    (out / "report.html").write_text(render(manifest, metrics, taxonomy, lang), "utf-8")

    table_rows = []
    for seg, data in metrics["rating_distribution"].items():
        for star in ("1", "2", "3", "4", "5"):
            table_rows.append({"segment": seg, "star": star, "count": data["counts"][star], "share": data["shares"][star]})
    _write_csv(out / "tables" / "rating_distribution.csv", table_rows, ["segment", "star", "count", "share"])

    table_rows = []
    for seg, data in metrics["theme_share"].items():
        for theme, count in data["counts"].items():
            table_rows.append({"segment": seg, "theme": theme, "count": count, "share": data["shares"][theme], "negative_total": data["negative_total"]})
    _write_csv(out / "tables" / "theme_share.csv", table_rows, ["segment", "theme", "count", "share", "negative_total"])

    table_rows = []
    for seg, days in metrics["daily"].items():
        for day in days:
            table_rows.append({"segment": seg, **day})
    _write_csv(out / "tables" / "daily.csv", table_rows, ["segment", "date", "negative", "total", "rate", "smooth"])

    table_rows = []
    for seg, quotes in metrics["quotes"].items():
        for q in quotes:
            table_rows.append({"segment": seg, "theme": q["theme"], "text": q["text"]})
    _write_csv(out / "tables" / "quotes.csv", table_rows, ["segment", "theme", "text"])

    print(f"report: {out / 'report.html'}")
    print(f"metrics: {out / 'metrics.json'}")
    for seg, data in metrics["negative_share"].items():
        print(f"{seg}: 1-{rating_max}★ {data['share']}% ({data['negative']}/{data['total']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
