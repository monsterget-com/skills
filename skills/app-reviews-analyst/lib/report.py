"""Render a self-contained HTML report with inline SVG charts."""
from __future__ import annotations

import html
import json
from datetime import datetime

from taxonomy import Taxonomy

COLORS = {"1": "#7A0E0C", "2": "#C8241C", "3": "#AAA094", "4": "#6E96D2", "5": "#2E6BFF"}
SEG_COLORS = ["#FF3B30", "#2E6BFF", "#12A150", "#8E44AD"]

CSS = """
:root { --ink:#151515; --muted:#7c766c; --line:#e4ddd0; --paper:#f7f3ea; --white:#fff; --red:#ff3b30; --blue:#2e6bff; }
* { box-sizing: border-box; }
body { margin:0; background:var(--paper); color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif; line-height:1.65; }
.wrap { max-width:980px; margin:0 auto; padding:56px 32px 80px; }
.eyebrow { font-size:13px; letter-spacing:.08em; text-transform:uppercase; color:var(--muted); }
h1 { font-size:38px; line-height:1.2; margin:14px 0 8px; letter-spacing:-.01em; }
.sub { color:var(--muted); font-size:15px; }
.card { background:var(--white); border:1px solid var(--line); border-radius:16px; padding:28px; margin:22px 0; }
h2 { font-size:24px; margin:0 0 14px; }
h3 { font-size:17px; margin:22px 0 8px; }
p { margin:8px 0; }
ul { margin:8px 0 8px 20px; padding:0; }
li { margin:5px 0; }
.grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
.kpi { background:var(--paper); border-radius:12px; padding:18px; }
.kpi .n { font-size:42px; font-weight:700; line-height:1.1; }
.kpi .l { color:var(--muted); font-size:13px; margin-top:4px; }
table { width:100%; border-collapse:collapse; font-size:14px; }
th,td { text-align:left; padding:10px 8px; border-bottom:1px solid var(--line); vertical-align:top; }
th { color:var(--muted); font-weight:600; font-size:12px; text-transform:uppercase; letter-spacing:.04em; }
.num { text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }
.bar { height:8px; background:#eee7da; border-radius:99px; overflow:hidden; min-width:110px; }
.bar > i { display:block; height:100%; border-radius:99px; }
.quote { border-left:3px solid var(--red); padding:10px 0 10px 14px; margin:12px 0; color:#333; }
.quote small { display:block; color:var(--muted); margin-top:4px; }
.tag { display:inline-block; font-size:12px; padding:3px 9px; border-radius:99px; background:var(--paper); color:var(--muted); margin-right:6px; }
.note { font-size:13px; color:var(--muted); }
.footer { margin-top:34px; padding-top:16px; border-top:1px solid var(--line); color:var(--muted); font-size:12px; }
.warn { background:#fff8e6; border:1px solid #f0d9a6; border-radius:10px; padding:10px 14px; font-size:13px; margin:10px 0; }
.err { background:#ffecec; border:1px solid #f3b4b4; border-radius:10px; padding:10px 14px; font-size:13px; }
@media print { body { background:#fff; } .wrap { max-width:none; padding:0; } .card { break-inside:avoid; border-color:#ddd; } }
@media (max-width:720px) { .grid { grid-template-columns:1fr; } h1 { font-size:30px; } .wrap { padding:28px 16px 50px; } }
"""

L = {
    "zh": {
        "report": "App 评论分析报告",
        "summary": "结论摘要",
        "sample": "样本与方法",
        "rating": "评分分布",
        "themes": "差评主题对比",
        "daily": "每日差评率",
        "quotes": "原话摘录",
        "actions": "基于数据的建议",
        "limits": "局限与口径",
        "appendix": "产出文件",
        "segment": "分组",
        "rows": "条数",
        "date": "时间范围",
        "countries": "国家 / 语言",
        "versions": "版本",
        "negative": "1–2★ 差评",
        "share": "占比",
        "theme": "主题",
        "gap": "差值",
        "count": "命中",
        "method": "方法",
        "generated": "生成时间",
        "run": "运行",
        "no_data": "数据不足，无法生成该图表。",
        "sampled": "抽样",
        "original": "原始",
        "after_filter": "时间过滤后",
        "final": "最终样本",
        "not_sampled": "全量使用",
        "sampling": "抽样",
        "target": "目标 / 组",
    },
    "en": {
        "report": "App Review Analysis",
        "summary": "Executive summary",
        "sample": "Sample & method",
        "rating": "Rating distribution",
        "themes": "Negative themes",
        "daily": "Daily negative rate",
        "quotes": "Quotes",
        "actions": "Data-based actions",
        "limits": "Limitations",
        "appendix": "Outputs",
        "segment": "Segment",
        "rows": "Rows",
        "date": "Date range",
        "countries": "Country / language",
        "versions": "Versions",
        "negative": "1–2★ negative",
        "share": "Share",
        "theme": "Theme",
        "gap": "Gap",
        "count": "Hits",
        "method": "Method",
        "generated": "Generated",
        "run": "Run",
        "no_data": "Not enough data for this chart.",
        "sampled": "sampled",
        "original": "original",
        "after_filter": "after date filter",
        "final": "final",
        "not_sampled": "all rows",
        "sampling": "Sampling",
        "target": "Target / segment",
    },
}


def esc(value) -> str:
    return html.escape(str(value if value is not None else ""))


def pct(value, digits=1) -> str:
    try:
        return f"{float(value):.{digits}f}%"
    except (TypeError, ValueError):
        return "—"


def svg_stacked(dist: dict, lang: str) -> str:
    segs = list(dist.keys())
    if not segs:
        return f'<p class="note">{esc(L[lang]["no_data"])}</p>'
    width, left, bar_w, bar_h, gap = 880, 96, 740, 54, 44
    height = 30 + len(segs) * (bar_h + gap)
    parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="rating distribution">']
    for idx, seg in enumerate(segs):
        y = 16 + idx * (bar_h + gap)
        total = dist[seg]["total"] or 1
        parts.append(f'<text x="0" y="{y + 34}" font-size="16" font-weight="600" fill="#151515">{esc(seg)}</text>')
        x = left
        for star in ("1", "2", "3", "4", "5"):
            c = dist[seg]["counts"].get(star, 0)
            w = bar_w * c / total
            if w <= 0:
                continue
            parts.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{bar_h}" fill="{COLORS[star]}"/>')
            if w > 36:
                parts.append(f'<text x="{x + w / 2:.1f}" y="{y + 33}" font-size="14" font-weight="600" fill="#fff" text-anchor="middle">{c}</text>')
            x += w
        p = dist[seg]["shares"]
        parts.append(f'<text x="{left + bar_w + 10}" y="{y + 33}" font-size="13" fill="#7c766c">1–2★ {pct(p.get("1", 0) + p.get("2", 0))}</text>')
    # legend
    y = height - 4
    for i, star in enumerate(("1", "2", "3", "4", "5")):
        x = left + i * 92
        parts.append(f'<rect x="{x}" y="{y - 12}" width="12" height="12" rx="3" fill="{COLORS[star]}"/>')
        parts.append(f'<text x="{x + 18}" y="{y}" font-size="13" fill="#7c766c">{star}★</text>')
    parts.append("</svg>")
    return "".join(parts)


def svg_daily(daily: dict, lang: str) -> str:
    segs = [s for s, rows in daily.items() if rows]
    if not segs:
        return f'<p class="note">{esc(L[lang]["no_data"])}</p>'
    dates = sorted({r["date"] for s in segs for r in daily[s]})
    if len(dates) < 2:
        return f'<p class="note">{esc(L[lang]["no_data"])}</p>'
    width, height, left, right, top, bottom = 880, 330, 54, 20, 20, 46
    plot_w, plot_h = width - left - right, height - top - bottom
    max_rate = max([r["smooth"] or 0 for s in segs for r in daily[s]] + [10])
    ymax = min(100, max(20, int((max_rate // 20 + 1) * 20)))
    parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="daily negative rate">']
    for tick in range(0, ymax + 1, 20):
        y = top + plot_h - plot_h * tick / ymax
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" stroke="#e4ddd0" stroke-width="1"/>')
        parts.append(f'<text x="{left - 10}" y="{y + 4:.1f}" font-size="12" fill="#7c766c" text-anchor="end">{tick}%</text>')
    for i in range(4):
        idx = round(i * (len(dates) - 1) / 3)
        x = left + plot_w * idx / (len(dates) - 1)
        parts.append(f'<text x="{x:.1f}" y="{height - 14}" font-size="12" fill="#7c766c" text-anchor="middle">{esc(dates[idx][5:])}</text>')
    for si, seg in enumerate(segs):
        color = SEG_COLORS[si % len(SEG_COLORS)]
        by_date = {r["date"]: r for r in daily[seg]}
        points = []
        for i, d in enumerate(dates):
            item = by_date.get(d)
            if not item or item.get("smooth") is None:
                continue
            x = left + plot_w * i / (len(dates) - 1)
            y = top + plot_h - plot_h * item["smooth"] / ymax
            points.append((x, y))
        if len(points) >= 2:
            parts.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in points)}" fill="none" stroke="{color}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')
        for x, y in points[::3]:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{color}"/>')
        parts.append(f'<rect x="{left + si * 130}" y="{height - 34}" width="12" height="12" rx="3" fill="{color}"/>')
        parts.append(f'<text x="{left + si * 130 + 18}" y="{height - 23}" font-size="13" fill="#7c766c">{esc(seg)}</text>')
    parts.append("</svg>")
    return "".join(parts)


def theme_rows(metrics: dict, taxonomy: Taxonomy, lang: str) -> list[dict]:
    theme_data = metrics["theme_share"]
    segs = list(theme_data.keys())
    rows = []
    for theme in taxonomy.order():
        shares = {s: theme_data[s]["shares"].get(theme, 0.0) for s in segs}
        counts = {s: theme_data[s]["counts"].get(theme, 0) for s in segs}
        rows.append({"theme": theme, "shares": shares, "counts": counts, "max": max(shares.values()) if shares else 0})
    rows.sort(key=lambda r: r["max"], reverse=True)
    return rows


def html_theme_table(metrics: dict, taxonomy: Taxonomy, lang: str) -> str:
    segs = list(metrics["theme_share"].keys())
    rows = theme_rows(metrics, taxonomy, lang)
    head = "".join(f'<th class="num">{esc(s)}</th>' for s in segs)
    body = []
    for row in rows:
        if row["max"] <= 0:
            continue
        cells = []
        for s in segs:
            share = row["shares"][s]
            cells.append(
                f'<td class="num">{pct(share)}<div class="bar"><i style="width:{min(100, share * 1.6):.1f}%;background:{SEG_COLORS[segs.index(s) % len(SEG_COLORS)]}"></i></div></td>'
            )
        body.append(f'<tr><td><strong>{esc(taxonomy.label(row["theme"], lang))}</strong></td>{"".join(cells)}</tr>')
    return f'<table><thead><tr><th>{esc(L[lang]["theme"])}</th>{head}</tr></thead><tbody>{"".join(body)}</tbody></table>'


def html_quotes(metrics: dict, taxonomy: Taxonomy, lang: str) -> str:
    blocks = []
    for seg, quotes in metrics["quotes"].items():
        if not quotes:
            continue
        items = []
        for q in quotes:
            items.append(
                f'<div class="quote">“{esc(q["text"])}”<small>{esc(seg)} · {esc(taxonomy.label(q["theme"], lang))}</small></div>'
            )
        blocks.append(f'<h3>{esc(seg)}</h3>{"".join(items)}')
    return "".join(blocks) or f'<p class="note">{esc(L[lang]["no_data"])}</p>'


def html_sample(metrics: dict, lang: str) -> str:
    segs = list(metrics["segment_meta"].keys())
    head = f'<tr><th>{esc(L[lang]["segment"])}</th><th class="num">{esc(L[lang]["rows"])}</th><th>{esc(L[lang]["date"])}</th><th>{esc(L[lang]["countries"])}</th><th>{esc(L[lang]["versions"])}</th></tr>'
    rows = []
    for s in segs:
        m = metrics["segment_meta"][s]
        countries = ", ".join(f"{esc(k)}" for k, _ in m["countries"][:3]) or "—"
        versions = ", ".join(f"{esc(k)}" for k, _ in m["versions"][:3]) or "—"
        date = " — ".join(x[:10] for x in (m["date_min"], m["date_max"]) if x) or "—"
        rows.append(f'<tr><td><strong>{esc(s)}</strong></td><td class="num">{m["rows"]:,}</td><td>{date}</td><td>{countries}</td><td>{versions}</td></tr>')
    return f'<table><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table>'


def summary_items(metrics: dict, taxonomy: Taxonomy, lang: str) -> list[str]:
    neg = metrics["negative_share"]
    segs = list(neg.keys())
    items = []
    if not segs:
        return items
    if len(segs) >= 2:
        a, b = segs[0], segs[1]
        va, vb = neg[a]["share"], neg[b]["share"]
        diff = abs(va - vb)
        if lang == "zh":
            items.append(f"{a} 的 1–2★ 差评占比 {pct(va)}，{b} {pct(vb)}，相差 {diff:.1f} 个百分点。")
        else:
            items.append(f"{a} negative share is {pct(va)} vs {b} {pct(vb)} ({diff:.1f} pp).")
        # common theme
        best, best_avg = None, -1
        for theme in taxonomy.order():
            avg = sum(metrics["theme_share"][s]["shares"].get(theme, 0) for s in segs) / len(segs)
            if avg > best_avg:
                best, best_avg = theme, avg
        if best:
            parts = [f'{s} {pct(metrics["theme_share"][s]["shares"].get(best, 0))}' for s in segs]
            if lang == "zh":
                items.append(f"两端共同第一主题：{taxonomy.label(best, lang)}（{'，'.join(parts)}）。")
            else:
                items.append(f"Top shared theme: {taxonomy.label(best, lang)} ({', '.join(parts)}).")
        gaps = metrics["theme_gap"]
        if gaps:
            top = gaps[0]
            if top["gap"] > 0:
                hi, hi_share, lo_share = top["a"], top["a_share"], top["b_share"]
            else:
                hi, hi_share, lo_share = top["b"], top["b_share"], top["a_share"]
            if lang == "zh":
                items.append(f"{hi} 更突出：{taxonomy.label(top['theme'], lang)}（{pct(hi_share)} vs {pct(lo_share)}）。")
            else:
                items.append(f"{hi} skews higher on {taxonomy.label(top['theme'], lang)} ({pct(hi_share)} vs {pct(lo_share)}).")
    else:
        s = segs[0]
        items.append(f"{s} 的 1–2★ 差评占比 {pct(neg[s]['share'])}。" if lang == "zh" else f"{s} negative share is {pct(neg[s]['share'])}.")
        best = max(taxonomy.order(), key=lambda t: metrics["theme_share"][s]["shares"].get(t, 0))
        items.append(
            f"最常见主题：{taxonomy.label(best, lang)}（{pct(metrics['theme_share'][s]['shares'].get(best, 0))}）。"
            if lang == "zh"
            else f"Top theme: {taxonomy.label(best, lang)} ({pct(metrics['theme_share'][s]['shares'].get(best, 0))})."
        )
    return items


def action_items(metrics: dict, taxonomy: Taxonomy, lang: str) -> list[str]:
    segs = list(metrics["negative_share"].keys())
    if not segs:
        return []
    common = max(
        taxonomy.order(),
        key=lambda t: sum(metrics["theme_share"][s]["shares"].get(t, 0) for s in segs) / len(segs),
    )
    actions = []
    if lang == "zh":
        actions.append(f"先修共同痛点：{taxonomy.label(common, lang)}，两端差评都在提。")
        if len(segs) >= 2:
            gaps = [g for g in metrics["theme_gap"] if g["gap"] != 0][:2]
            for g in gaps:
                hi = g["a"] if g["gap"] > 0 else g["b"]
                actions.append(f"{hi} 单独看：{taxonomy.label(g['theme'], lang)}（{pct(g['a_share'])} vs {pct(g['b_share'])}）。")
        actions.append("下个版本用同一口径复采，验证这些问题是否真的下降。")
    else:
        actions.append(f"Fix the shared pain first: {taxonomy.label(common, lang)}.")
        if len(segs) >= 2:
            for g in [x for x in metrics["theme_gap"] if x["gap"] != 0][:2]:
                hi = g["a"] if g["gap"] > 0 else g["b"]
                actions.append(f"{hi} specific: {taxonomy.label(g['theme'], lang)} ({pct(g['a_share'])} vs {pct(g['b_share'])}).")
        actions.append("Re-collect with the same method next release to verify improvement.")
    return actions


def html_sampling(metrics: dict, lang: str) -> str:
    sample = metrics.get("sample") or {}
    segs = sample.get("segments") or {}
    if not segs:
        return ""
    head = (
        f'<tr><th>{esc(L[lang]["segment"])}</th><th class="num">{esc(L[lang]["original"])}</th>'
        f'<th class="num">{esc(L[lang]["after_filter"])}</th><th class="num">{esc(L[lang]["final"])}</th>'
        f'<th>{esc(L[lang]["sampling"])}</th></tr>'
    )
    rows = []
    for seg, s in segs.items():
        mode = L[lang]["sampled"] if s.get("sampled") else L[lang]["not_sampled"]
        rows.append(
            f'<tr><td><strong>{esc(seg)}</strong></td><td class="num">{s.get("original", 0):,}</td>'
            f'<td class="num">{s.get("after_filter", 0):,}</td><td class="num">{s.get("final", 0):,}</td><td>{esc(mode)}</td></tr>'
        )
    note = ""
    if sample.get("date_range"):
        note = f'<p class="note">date_range: {esc(sample["date_range"][0])} → {esc(sample["date_range"][1])}'
        if sample.get("target_per_segment"):
            note += f' · target {sample["target_per_segment"]}/segment · seed {sample.get("seed")}'
        note += "</p>"
    return f'<table><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table>{note}'


def render(manifest: dict, metrics: dict, taxonomy: Taxonomy, lang: str = "zh") -> str:
    t = L.get(lang, L["zh"])
    segs = list(metrics["negative_share"].keys())
    kpis = []
    for s in segs:
        n = metrics["negative_share"][s]
        kpis.append(f'<div class="kpi"><div class="n">{pct(n["share"])}</div><div class="l">{esc(s)} · 1–2★ ({n["negative"]:,}/{n["total"]:,})</div></div>')
    summary = summary_items(metrics, taxonomy, lang)
    actions = action_items(metrics, taxonomy, lang)
    warnings = metrics["quality"].get("warnings") or []
    warn_html = "".join(f'<div class="warn">{esc(w)}</div>' for w in warnings)
    sample_meta = metrics.get("sample") or {}

    return f"""<!doctype html>
<html lang="{ 'zh-CN' if lang == 'zh' else 'en' }">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(t['report'])} · {esc(manifest['run_id'])}</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <div class="eyebrow">MonsterGet · {esc(t['report'])}</div>
  <h1>{esc(manifest['run_id'])}</h1>
  <div class="sub">{esc(t['generated'])} {esc(manifest['generated_at'][:19].replace('T', ' '))} · {esc(t['run'])} {esc(manifest['run_id'])}</div>

  <div class="card">
    <h2>{esc(t['summary'])}</h2>
    <div class="grid">{''.join(kpis)}</div>
    <ul>{''.join(f'<li>{esc(x)}</li>' for x in summary)}</ul>
  </div>

  <div class="card">
    <h2>{esc(t['sample'])}</h2>
    {html_sample(metrics, lang)}
    <p class="note">{esc(t['method'])}: {esc(metrics['recipe'])} · taxonomy {esc(metrics['taxonomy']['id'])} v{esc(metrics['taxonomy']['version'])} · rating ≤ {esc(metrics['options'].get('rating_max', 2))}</p>
    {''.join(f'<div class="warn">{esc(w)}</div>' for w in warnings)}
    {html_sampling(metrics, lang)}
  </div>

  <div class="card">
    <h2>{esc(t['rating'])}</h2>
    {svg_stacked(metrics['rating_distribution'], lang)}
  </div>

  <div class="card">
    <h2>{esc(t['themes'])}</h2>
    <p class="note">分母 = 各分组的 1–2★ 评论数；一条评论可命中多个主题，所以占比会超过 100%。</p>
    {html_theme_table(metrics, taxonomy, lang)}
  </div>

  <div class="card">
    <h2>{esc(t['daily'])}</h2>
    {svg_daily(metrics['daily'], lang)}
  </div>

  <div class="card">
    <h2>{esc(t['quotes'])}</h2>
    {html_quotes(metrics, taxonomy, lang)}
  </div>

  <div class="card">
    <h2>{esc(t['actions'])}</h2>
    <ul>{''.join(f'<li>{esc(x)}</li>' for x in actions)}</ul>
    <p class="note">这些是基于数据的建议，不是因果结论；发布前请结合版本、地区和业务背景复核。</p>
  </div>

  <div class="card">
    <h2>{esc(t['limits'])}</h2>
    <ul>
      <li>评论来自公开页面；样本不等于全部用户，不能外推到所有用户。</li>
      <li>主题为关键词归类，适合看方向，不适合做严谨学术编码；一条评论可命中多个主题。</li>
      <li>两端评论量不同，时间窗只能近似对齐；跨端比例差异不宜直接当作因果。</li>
      <li>报告不展示用户名、头像、邮箱、电话；原话已做 PII 脱敏。</li>
    </ul>
  </div>

  <div class="card">
    <h2>{esc(t['appendix'])}</h2>
    <ul>
      <li><code>metrics.json</code> — 所有指标、口径和样本信息</li>
      <li><code>manifest.json</code> — 运行清单，供下游内容 skill 读取</li>
      <li><code>tables/*.csv</code> — 评分、主题、每日趋势明细</li>
    </ul>
  </div>

  <div class="footer">MonsterGet · {esc(t['report'])} · {esc(manifest['skill'])} v{esc(manifest['skill_version'])} · schema {esc(manifest['analysis_schema'])}</div>
</div>
</body>
</html>"""
