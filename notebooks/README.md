# Notebooks

Jupyter notebooks (`.ipynb`) for exploration, analysis, and modeling.

## Conventions

- **Numbered order**: `00_eda_template.ipynb`, `01_churn_analysis.ipynb`, … so flow is explicit.
- **Snake_case purpose**: `02_segment_revenue.ipynb`, not `Analysis2.ipynb`.
- **Paths**: always import from `scripts/paths.py`. Never hardcode.
- **Outputs**: write processed data to `data/processed/`, charts to `visuals/`.

## Starter

`00_eda_template.ipynb` — open first. Pre-wired with `paths.py` imports and a profiling skeleton.

```bash
uv run jupyter lab notebooks/00_eda_template.ipynb
```
