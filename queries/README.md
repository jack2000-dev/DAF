# Queries

SQL files organized by stage. Use subdirectories — don't put loose .sql files here.

## Naming Convention

Prefix with a zero-padded number to make order explicit:

```
queries/
├── exploratory/
│   ├── 001_row_counts.sql
│   └── 002_null_audit.sql
├── transformations/
│   ├── 001_clean_orders.sql
│   └── 002_join_customers.sql
└── final/
    ├── 001_churn_by_segment.sql
    └── 002_revenue_summary.sql
```

## Subdirectories

| Folder | Use for |
|--------|---------|
| `exploratory/` | Ad-hoc queries during initial investigation |
| `transformations/` | Cleaning, reshaping, joining, aggregating |
| `final/` | Production-ready or presentation queries |
