# SKILL.md — AI Prompt Reference for Data Analysts

Copy-paste prompts for tasks **not** covered by auto-triggered Claude skills.

---

## Auto-Triggered Skills (no prompt needed)

These activate from `.claude/skills/` when you describe the task naturally:

| Skill | Triggers on |
|-------|-------------|
| `profile-data` | "profile this", "explore [file]", "what's in [dataset]" |
| `draft-insight` | "draft insight", "write key findings", "turn this into Section 9" |
| `write-sql` | "write SQL for", "convert to SQL", "query this" |

Just describe the task. Claude picks the skill.

---

## Manual Prompt Patterns

For tasks outside the three skills above:

**Cleaning suggestions:**
> Suggest cleaning steps for this dataset: [paste df.info() + df.head()]

**Notebook → reusable function:**
> Refactor this notebook cell into a reusable function with type hints and a one-line docstring: [paste]

**Pandas → SQL:**
> Convert this pandas transform to SQL: [paste]

**Stakeholder summary:**
> Summarize this finding in 2 sentences for a non-technical audience: [paste]

**Report section drafts:**
> Draft Section [N] of `reports/REPORT.md` from these notes: [paste]

**Recommendation from insight:**
> Based on this insight: "[paste]" — write a recommendation for Section 10 with priority [High/Med/Low] and suggested owner [team].

**Limitations section:**
> Write the Limitations section based on these data gaps: [list]

**Visualization picker:**
> Suggest the right chart type for showing [relationship/trend/comparison] of [columns]

**Mermaid ERD:**
> Write a Mermaid ERD for these tables: [paste schema]

**Project review:**
> What's missing from my project to make it portfolio-ready?

---

## Pairs With

- `CLAUDE.md` — conventions Claude follows automatically
- `.claude/skills/` — auto-triggered task skills (see table above)
- `reports/REPORT.md` — section structure prompts above target this file
