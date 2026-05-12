---
name: draft-insight
description: Turn raw findings, observations, or query results into Key Insights for Section 9 of REPORT.md. Use when user says "draft insight", "write insights", "turn this into a finding", "what does this mean", or pastes numbers/observations and asks for analysis. Each insight = headline + magnitude + interpretation + next-step pointer.
---

# Draft Insight

Goal: convert raw observations into structured Key Insights that fit Section 9 of `reports/REPORT.md`.

## When to use
- User pastes findings, query results, or notes and asks for insights
- User says "draft insight", "write a key finding", "turn this into a Section 9 entry"
- User has numbers but no narrative

## Insight anatomy

Each insight = 4 parts:

1. **Headline** (bold, one sentence) — the finding stated as a claim, not an observation
2. **Magnitude** — the number(s) that support it
3. **Interpretation** — what it means for the business / problem
4. **Next step** (optional) — what to investigate or do

## Format

```markdown
**N. [Claim, not observation]** — [Magnitude in concrete numbers]. [What it means in 1 sentence]. [Where to look next, if relevant.]
```

## Rules

- **Claim, not observation.** "Pricing change drove 60% of churn" beats "Churn was high after pricing change."
- **Numbers anchor the claim.** Always include the magnitude.
- **One insight, one idea.** Don't compound.
- **3–5 insights per report.** More than 5 = noise.
- **Order by impact**, not chronology.
- Skip hedging: drop "may", "might", "could suggest". If the data is uncertain, say so explicitly in Limitations.

## Anti-patterns

- ❌ "We found that churn went up." (observation, no claim)
- ❌ "There seems to be a possible correlation between X and Y." (hedge soup)
- ❌ "Sales were lower in Q3 than Q2." (no magnitude, no interpretation)

## Good example

> **1. Pricing change drove 60% of churn** — Customers on the legacy plan churned at 3× the rate after the June price increase, concentrated in the first 30 days post-change. Pricing, not product quality, is the lever. Next: model elasticity by tier before next price action.

## Workflow

1. Read user's raw findings
2. Identify 3–5 distinct claims (not observations)
3. For each: pull the supporting number, write interpretation, add next-step if obvious
4. Order by business impact
5. Output as numbered list ready to drop into Section 9
