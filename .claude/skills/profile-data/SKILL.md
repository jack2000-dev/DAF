---
name: profile-data
description: Profile a dataset to understand its shape, types, null rate, and data quality. Use when user asks to "profile", "explore", "describe", "summarize", or "look at" a CSV, parquet, or DataFrame, or asks "what's in this file". Outputs shape, dtypes, null counts, sample rows, and quality flags.
---

# Profile Data

Goal: rapidly assess an unknown dataset so the analyst knows what they have before diving in.

## When to use
- User points at a file in `data/raw/` or `data/external/` and asks what's in it
- User pastes a `df.info()` or `df.head()` output and asks for a profile
- User says "explore", "describe", "summarize", "profile", "look at this dataset"

## What to produce

Always include these sections:

1. **Shape** — rows × columns
2. **Dtypes** — list each column with its type
3. **Nulls** — count + % null per column (highlight any > 5%)
4. **Sample** — 3 rows (use `df.sample(3)` if dataset > 1000 rows, else `df.head(3)`)
5. **Quality flags** — call out issues:
   - High null columns (>30%)
   - Constant columns (single unique value)
   - Suspected ID columns (high cardinality, low duplicate rate)
   - Date columns stored as strings
   - Numeric columns stored as objects
   - Possible PII (email/phone/name patterns)
   - Trailing whitespace, mixed case duplicates in categoricals

## Code style

Use `scripts/paths.py`:

```python
from scripts.paths import raw, external
import pandas as pd

df = pd.read_csv(raw("filename.csv"))

print(f"Shape: {df.shape}")
print(f"\nDtypes:\n{df.dtypes}")
print(f"\nNulls:\n{(df.isna().sum() / len(df) * 100).round(1).sort_values(ascending=False)}")
print(f"\nSample:\n{df.sample(min(3, len(df)))}")
```

## Output format

Lead with shape one-liner. Then table of dtypes + nulls. Then sample. End with bulleted quality flags. Skip narrative — analyst wants signal.

## Next steps

After profiling, suggest one of:
- Cleaning steps if quality issues found
- Join keys if multi-table
- Candidate analysis questions if profile reveals interesting structure
