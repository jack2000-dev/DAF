"""Generate data dictionary from raw/processed data files.

Scans data/raw/ and data/processed/ for CSV and Parquet files.
Writes a markdown data dictionary to docs/data_dictionary.md.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

try:
    import pandas as pd
except ImportError:
    print("ERROR: pandas required. Run: pip install pandas")
    sys.exit(1)

ROOT = next(
    (p for p in [Path(__file__).resolve().parent.parent, *Path(__file__).resolve().parents]
     if (p / "pyproject.toml").exists()),
    None,
)
if ROOT is None:
    print("ERROR: pyproject.toml not found in any ancestor directory.")
    sys.exit(1)

_SCAN_DIRS = ["data/raw", "data/processed"]
_READERS: dict[str, object] = {".csv": pd.read_csv, ".parquet": pd.read_parquet}
OUTPUT = ROOT / "docs" / "data_dictionary.md"


def _profile(df: pd.DataFrame) -> str:
    lines = [
        f"- **Rows:** {len(df):,}",
        f"- **Columns:** {len(df.columns)}",
        "",
        "| Column | Type | Nulls | Null % | Sample Values |",
        "|--------|------|-------|--------|---------------|",
    ]
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = int(df[col].isna().sum())
        null_pct = f"{nulls / len(df) * 100:.1f}%" if len(df) else "—"
        samples = df[col].dropna().head(3).tolist()
        sample_str = ", ".join(f"`{v}`" for v in samples) if samples else "—"
        lines.append(f"| `{col}` | {dtype} | {nulls} | {null_pct} | {sample_str} |")
    return "\n".join(lines)


def main() -> None:
    sections = [f"# Data Dictionary\n\n*Generated: {date.today()}*\n"]
    found = 0

    for scan_dir in _SCAN_DIRS:
        folder = ROOT / scan_dir
        if not folder.exists():
            continue
        for path in sorted(folder.iterdir()):
            if path.suffix not in _READERS or path.name.startswith("."):
                continue
            try:
                df = _READERS[path.suffix](path)
                rel = path.relative_to(ROOT)
                sections.append(f"## `{rel}`\n\n{_profile(df)}\n")
                found += 1
                print(f"  ✓ {rel} ({len(df):,} rows, {len(df.columns)} cols)")
            except Exception as e:
                print(f"  ✗ {path.name}: {e}")

    if found == 0:
        print("No CSV or Parquet files found in data/raw/ or data/processed/")
        sys.exit(0)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(sections))
    print(f"\nWrote: docs/data_dictionary.md ({found} dataset(s))")


if __name__ == "__main__":
    main()
