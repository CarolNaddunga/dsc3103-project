#%%
def rule_positive_price(df):
    neg_prices = df[df["price"] <= 0].copy()
    neg_prices["Reason"] = "Negative price"
    return neg_prices
# %%
def rule_duplicate_ids(df):
    dup_id = df["id"].duplicated(keep=False)
    dup_id_mask = df[dup_id].copy()
    dup_id_mask["Reason"] = "duplicate ids"
    return dup_id_mask
# %%
def rule_duplicate_rows(df):
    dup_rows = df.duplicated(keep="first")
    dup_rows_noticed = df[dup_rows].copy()
    dup_rows_noticed["Reason"] = "duplicate rows"
    return dup_rows_noticed
# %%
from datetime import datetime
import pandas as pd
def rule_valid_date_format(df):
    parsed = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    invalid_dates = parsed.isnull() | (parsed > datetime.now())
    invalid_date_rows = df[invalid_dates].copy()
    invalid_date_rows["Reason"] = "Invalid date format"
    return invalid_date_rows
  
# %%
def rule_missing_market(df):
    missing_market = df[df["market"].isna()].copy()
    missing_market["Reason"] = "Missing Market"
    return missing_market

#%%
def rule_known_commodity(df):
    known = {"maize", "beans"}
    bad_commodity = df[~df["commodity"].str.lower().isin(known)].copy()
    bad_commodity["Reason"] = "Unknown Commodity"
    return bad_commodity
