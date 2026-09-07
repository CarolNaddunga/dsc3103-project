# Validation Report — prices.csv

**Date generated:** <date>
**Raw file:** `data/raw/prices.csv`
**Cleaned output:** `data/processed/prices_clean.parquet`

## Summary

| Rule | Rows Checked | Rows Failed | Action Taken |
|---|---|---|---|
| rule_duplicate_rows | 1000 | 12 | Rejected (dropped) |
| rule_duplicate_ids | 1000 | 8 | Rejected (kept first) |
| rule_positive_price | 1000 | 15 | Rejected (dropped) |
| rule_valid_date | 1000 | 6 | Rejected (dropped) |
| rule_missing_market | 1000 | 20 | Imputed ("Unknown") |
| rule_known_commodity | 1000 | 34 | Normalized (casing/whitespace) |

## Details

### 1. Duplicate rows (`rule_duplicate_rows`)
- **Checked:** exact full-row duplicates.
- **Failed:** 12 rows.
- **Action:** dropped via `drop_duplicates()`.
- **Why:** exact duplicates add no information and would bias any aggregation.

### 2. Duplicate record_id (`rule_duplicate_ids`)
- **Checked:** repeated `record_id` values with differing data.
- **Failed:** 8 rows.
- **Action:** kept first occurrence, dropped rest.
- **Why:** record_id should be unique; ambiguous to know which duplicate is "correct," so first-seen was kept as a simple, documented convention.

*(...repeat for all 6 rules...)*

## Raw File Integrity
- SHA256 before pipeline: `<hash>`
- SHA256 after pipeline: `<hash>`
- Result: unchanged