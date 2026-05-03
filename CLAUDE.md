# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

DAF (Data Analysis Framework) — opinionated template for data analysis projects. Every project using DAF follows the same structure, paths, and conventions so analyses stay reproducible and AI-friendly.

## Folder Map

| Folder | Purpose |
|--------|---------|
| `data/raw/` | Original source data. **Never modify.** |
| `data/processed/` | Cleaned/transformed data. |
| `data/external/` | Reference data, lookups, third-party. |
| `notebooks/` | Jupyter notebooks. |
| `scripts/` | Reusable Python helpers. |
| `queries/exploratory/` | Ad-hoc SQL. |
| `queries/transformations/` | Cleaning/reshaping SQL. |
| `queries/final/` | Production-ready SQL. |
| `reports/` | Final deliverables + `REPORT.md`. |
| `visuals/` | Exported charts, screenshots, ERDs. |
| `docs/` | Data dictionary, schema notes. |

## Key Files

- `scripts/paths.py` — path resolver. Always import this, never hardcode paths.
- `reports/REPORT.md` — full structured report (14 sections).
- `README.md` — project one-pager. Stakeholder-facing summary.
- `SKILL.md` — DA prompt reference card.
- `MANUAL.md` — template usage guide.
- `.claude/skills/` — Claude Code skills for DA tasks (`profile-data`, `draft-insight`, `write-sql`).

## Project Root Marker

Project root is identified by `pyproject.toml`. Both `scripts/paths.py` and `scripts/snapshot.py` walk ancestors looking for it.

## Path Convention

**Always use `scripts/paths.py`. Never hardcode paths.**

```python
from scripts.paths import PATHS, raw, processed, report, visual, query

df = pd.read_csv(raw("customers.csv"))
df.to_parquet(processed("customers_clean.parquet"))
fig.savefig(visual("churn_by_region.png"), dpi=150)
sql = query("final/100_churn_summary.sql").read_text()
```

## Naming Conventions

- Queries: `001_explore_users.sql`, `002_transform_events.sql` (numbered, snake_case)
- Notebooks: `00_eda_template.ipynb`, `01_churn_analysis.ipynb` (numbered)
- Visuals: `churn_by_region.png`, `erd_main.png` (descriptive, snake_case)
- Processed data: `customers_clean.parquet`, `orders_daily_agg.parquet`

## Environment

- Python version pinned in `.python-version`
- Deps managed by `uv` (see `pyproject.toml`, `uv.lock`)
- Run scripts: `uv run python scripts/<name>.py` or use `make`

## Make Targets

```
make install    # uv sync
make snapshot   # Generate docs/data_dictionary.md
make help       # List all targets
```

## Report Template

`reports/REPORT.md` — fill sections in order:

1. Project Overview (context → problem → approach → outcome)
2. Objectives (specific, testable)
3. Scope & Tools
4. Repository Structure
5. Data Workflow (mermaid flowchart)
6. Data Model & Schema
7. ERD (SQL projects)
8. Analysis & Metrics (define metrics before reporting them)
9. Key Insights (finding + what it means)
10. Recommendations (actionable, with owner)
11. Assumptions & Limitations
12. Future Enhancements
13. Deliverables
14. Author

The root `README.md` is a separate one-pager — stakeholder-facing, lighter than `REPORT.md`.

## Common AI Tasks

- "Profile `data/raw/[file.csv]` — show shape, dtypes, nulls, sample rows" → triggers `profile-data` skill
- "Draft Section 9 (Key Insights) from these findings: [paste]" → triggers `draft-insight` skill
- "Write SQL window function to calculate [metric] by [dimension]" → triggers `write-sql` skill
- "Refactor this notebook cell to use paths.py"

## Working Style

- Keep changes minimal. Don't refactor outside scope of request.
- Don't add comments explaining what code does — names should explain it.
- When fixing a bug, fix the bug. Don't reformat surrounding code.
- Prefer editing existing files over creating new ones.
- Data files (`*.csv`, `*.parquet`, etc.) are gitignored. Don't commit them.
