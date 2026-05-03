---
name: write-sql
description: Write SQL for analysis goals — aggregations, window functions, joins, cohort retention, time-series. Use when user asks to "write SQL", "query this", "convert to SQL", "write a CTE", or describes an analytical goal that needs a query. Places output in correct queries/ subfolder by query stage.
---

# Write SQL

Goal: produce clean, readable SQL for DA tasks and place it in the correct `queries/` subfolder.

## When to use
- User asks for SQL: "write a query for…", "SQL to calculate…", "convert this pandas to SQL"
- User describes analytical goal involving DB tables
- User asks for window functions, CTEs, joins, cohort/retention queries

## Subfolder routing

| User intent | Folder |
|-------------|--------|
| Quick lookup, ad-hoc inspection, "what does this table look like" | `queries/exploratory/` |
| Cleaning, reshaping, deduplicating, type casting | `queries/transformations/` |
| Final metric, report-feeding query, dashboard source | `queries/final/` |

Always ask the user where this query lives if ambiguous.

## File naming

`NNN_action_object.sql` where NNN is zero-padded sequence:
- `001_explore_users.sql`
- `010_transform_events_clean.sql`
- `100_final_churn_by_segment.sql`

## SQL style

- **CTEs over nested subqueries.** One CTE per logical step. Name them by what they produce, not by step number.
- **Lowercase keywords or uppercase — pick one and stay consistent.** Default uppercase.
- **One column per line** in SELECT lists when there are 3+.
- **Trailing commas optional**; leading commas only if codebase already uses them.
- **Comments**: one line above each CTE explaining what it produces. No inline comments unless the logic is non-obvious.
- **Aliases**: short and meaningful (`u` for users, `o` for orders). Avoid single-letter aliases for less common tables.

## Template

```sql
-- {{purpose: one line}}
-- Output: {{what columns / grain}}

WITH base AS (
    -- {{what this produces}}
    SELECT
        column_a,
        column_b,
        ...
    FROM schema.table
    WHERE ...
),

aggregated AS (
    -- {{what this produces}}
    SELECT
        dimension,
        COUNT(*) AS row_count,
        SUM(metric) AS total_metric
    FROM base
    GROUP BY dimension
)

SELECT *
FROM aggregated
ORDER BY total_metric DESC;
```

## Common patterns

**Cohort retention:**
```sql
WITH cohorts AS (
    SELECT user_id, DATE_TRUNC('month', MIN(event_date)) AS cohort_month
    FROM events
    GROUP BY user_id
),
activity AS (
    SELECT
        c.cohort_month,
        DATE_TRUNC('month', e.event_date) AS active_month,
        COUNT(DISTINCT e.user_id) AS active_users
    FROM events e
    JOIN cohorts c USING (user_id)
    GROUP BY 1, 2
)
SELECT * FROM activity ORDER BY cohort_month, active_month;
```

**Window for ranking:**
```sql
SELECT
    user_id,
    order_date,
    order_total,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY order_date) AS order_seq
FROM orders;
```

**Period-over-period:**
```sql
SELECT
    metric_date,
    metric_value,
    LAG(metric_value) OVER (ORDER BY metric_date) AS prev_value,
    metric_value - LAG(metric_value) OVER (ORDER BY metric_date) AS delta
FROM daily_metrics;
```

## Reading queries from Python

```python
from scripts.paths import query

sql = query("final/100_churn_by_segment.sql").read_text()
df = pd.read_sql(sql, conn)
```

## Output

When writing the query:
1. State the goal in one sentence
2. State which subfolder + filename
3. Show the SQL
4. Note any assumptions (table grain, time zone, dialect)
