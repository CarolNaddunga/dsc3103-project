import pandas as pd
from src.validate import rules

raw_path = "data/raw/prices.csv"    
data_path = "data/processed/prices_clean.parquet"

def clean_data(path=raw_path):
    df = pd.read_csv(path)

    log = []

    repeated_rows = rules.rule_duplicate_rows(df)
    if len(repeated_rows) > 0:
       df = df.drop_duplicates()
       log.append(f"Removed {len(repeated_rows)} duplicate rows.")
    return df, log
    
    duplicate_ids = rules.rule_duplicate_ids(df)
    if len(duplicate_ids) > 0:
        before = len(df)
        df =df.drop_duplicates(subset='id', keep='first')
        log.append(f"Dropped {before - len(df)} rows with duplicate record_id (kept first occurrence).")

    bad_price = rules.rule_positive_price(df)
    if len(bad_price) > 0:
        df = df.drop(index=bad_price.index)
        log.append(f"Removed {len(bad_price)} rows with price <= 0 "
                    f"(treated as invalid, not imputed — a fabricated price "
                    f"would be misleading).")
        
    bad_dates = rules.rule_valid_date(df)
    if len(bad_dates) > 0:
        df = df.drop(index=bad_dates.index)
        log.append(f"Removed {len(bad_dates)} rows with unparseable dates.")

    missing_market = rules.rule_missing_market(df)
    if len(missing_market) > 0:
        df.loc[missing_market.index, "market"] = df.loc[missing_market.index, "market"].fillna("Unknown")
        log.append(f"Imputed {len(missing_market)} missing 'market' values with 'Unknown'.")

    bad_commodity = rules.rule_known_commodity(df)
    if len(bad_commodity) > 0:
        df["commodity"] = df["commodity"].str.strip().str.title()
        log.append(f"Normalized {len(bad_commodity)} inconsistent commodity "
                    f"labels (stripped whitespace, standardized casing).")

    return df, log

if __name__ == "__main__":
    df_clean, log = clean_data()

    df_clean.to_parquet(data_path, index=False)

    print(f"Cleaned data saved to {data_path}")
    print(f"Final row count: {len(df_clean)}")
    print("\n--- Cleaning log ---")
    for entry in log:
        print(f"- {entry}")