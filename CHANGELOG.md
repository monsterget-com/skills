# Changelog

## Unreleased

### Changed

- `tiktok-collector` — value-first onboarding pilot: show a 4-goal business menu before setup, ask one input, then show only the setup the chosen task needs; deliver a labelled Quick sample first and offer Standard. Adds `ONBOARDING.md` and `scripts/set-onboarding.sh` to remember the goal across sessions.

## v2.0.0-preview — 2026-11-25

### Added

- `monsterget-context` — shared business context (brand, product, ICP, voice, guardrails).
- `monsterget-business` — router from a business question to the right skill.
- `voc-miner` — VOC report from TikTok/X comments + App Store/Google Play reviews.
  - `scripts/analyze.py` — stdlib-only normalizer + deterministic stats.
  - `references/taxonomy.md` / `references/output-template.md`.
  - `evals/` with 3 cases + fixture smoke test.
- `freelance-lead-radar` — ranked Upwork leads + proposal drafts + pricing guidance.
  - `references/scoring.md` / `references/output-template.md`.
  - `evals/` with 3 cases.
- `CATALOG.md` — collectors + context + router + business skill catalog.
- `scripts/resolve-runtime.sh` — find a collector's `run-scrape.sh` across install layouts.
- `scripts/validate-skills.py` — frontmatter / duplicate-name / collector-presence checks.

### Changed

- `README.md` / `README.zh-CN.md` — added the v2 business skills preview.
- `AGENTS.md` — added the three-layer flow and business-skill install rules.

### Compatibility

- Collectors unchanged: 5 skills, 22 Agent API scrapers.
- `scrapers_api` v4; extension 1.8.0+ (1.12.0+ for app-store reviews).
- Existing `~/.monsterget/skills/<collector>/` installs keep working.

### Known gaps

- `voc-miner` theme coding is LLM-driven; the analyzer only normalizes and computes
  deterministic stats. No automatic theme clustering yet.
- `freelance-lead-radar` scoring is a rubric, not a trained model.
- Business skills are on the `v2` branch until the first 3 design-partner cases pass.
- LinkedIn company employees and profile batch remain devOnly.
