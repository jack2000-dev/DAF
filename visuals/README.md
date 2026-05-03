# Visuals

Exported charts, screenshots, diagrams, ERDs.

## Conventions

- **Naming**: `purpose_dimension.ext` — e.g. `churn_by_region.png`, `erd_main.svg`.
- **Format**: `.png` for charts (use `dpi=150`+), `.svg` for ERDs/diagrams.
- **Save via paths**:

  ```python
  from scripts.paths import visual
  fig.savefig(visual("churn_by_region.png"), dpi=150, bbox_inches="tight")
  ```

- **Reproducibility**: every visual should be regenerable from a notebook or script. Don't drop in screenshots without provenance.
