# Data

All datasets live here, split by lifecycle stage. **Data files are gitignored** — only this README is committed. Document sources in the root `README.md` ("Data Source" section) and share files through a separate channel.

## Subdirectories

| Folder | What goes here | Rules |
|--------|----------------|-------|
| `raw/` | Original source data, exactly as received | **Never modify.** Source of truth. |
| `processed/` | Cleaned, transformed, or aggregated data ready for analysis | Outputs from notebooks/scripts. Reproducible from `raw/`. |
| `external/` | Reference data, lookup tables, third-party datasets | Read-only auxiliaries (e.g. ISO country codes, FX rates). |

## File placement

```
data/
├── raw/         ← drop source files here, never edit
├── processed/   ← write cleaned outputs here
└── external/    ← drop reference/lookup files here
```

## Conventions

- **Formats**: prefer `.parquet` for processed data (typed, compressed). `.csv` only for raw or final exports.
- **Naming**: `entity_state.ext` — e.g. `customers_raw.csv`, `customers_clean.parquet`, `orders_daily_agg.parquet`.
- **Reading**: always use `scripts/paths.py`:

  ```python
  from scripts.paths import raw, processed, external
  df = pd.read_csv(raw("customers.csv"))
  df.to_parquet(processed("customers_clean.parquet"))
  ```

- **Documenting**: run `make snapshot` to auto-generate `docs/data_dictionary.md` describing every file's columns and types.
