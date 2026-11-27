"""Data quality checks before analysis."""
from __future__ import annotations

from collections import Counter


def validate(rows: list[dict], min_rows: int = 50) -> dict:
    total = len(rows)
    missing_rating = sum(1 for r in rows if not r.get("rating"))
    missing_text = sum(1 for r in rows if not str(r.get("text") or "").strip())
    missing_date = sum(1 for r in rows if not r.get("date"))
    ids = Counter(str(r.get("id") or "") for r in rows)
    duplicates = sum(v - 1 for v in ids.values() if v > 1)
    platforms = Counter(str(r.get("platform") or "Unknown") for r in rows)
    dates = sorted(r["date"] for r in rows if r.get("date"))

    warnings: list[str] = []
    errors: list[str] = []

    if total == 0:
        errors.append("没有读到任何评论行")
    elif total < min_rows:
        errors.append(f"有效样本 {total} 条，低于最小样本 {min_rows} 条；请扩大采集或降低 min_rows")
    if missing_rating:
        warnings.append(f"{missing_rating} 条评论缺评分，已从评分指标中排除")
    if missing_text:
        warnings.append(f"{missing_text} 条评论缺正文，主题与原话会跳过")
    if missing_date:
        warnings.append(f"{missing_date} 条评论缺时间，不参与时间趋势")
    if duplicates:
        warnings.append(f"发现 {duplicates} 条重复评论 ID，指标按全部行计算；建议先去重")

    return {
        "total_rows": total,
        "valid_rows": total - missing_rating,
        "missing_rating": missing_rating,
        "missing_text": missing_text,
        "missing_date": missing_date,
        "duplicates": duplicates,
        "platforms": dict(platforms),
        "date_min": dates[0].isoformat() if dates else None,
        "date_max": dates[-1].isoformat() if dates else None,
        "min_rows": min_rows,
        "warnings": warnings,
        "errors": errors,
        "ok": not errors,
    }
