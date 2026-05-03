# Scripts

Reusable Python helpers.

| Script | Command | Purpose |
|--------|---------|---------|
| `paths.py` | `uv run python scripts/paths.py` | Print all resolved project paths (sanity check) |
| `snapshot.py` | `make snapshot` | Generate `docs/data_dictionary.md` from CSV/Parquet in `data/raw/` and `data/processed/` |

`paths.py` is the core helper — every notebook and script imports from it. See its module docstring for usage examples and notebook setup.

## Adding your own scripts

- Place reusable Python helpers here (anything imported by notebooks or other scripts).
- One-off analysis logic stays in notebooks.
- If a script grows beyond ~150 lines, consider splitting into a module.
