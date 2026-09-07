#%%
import pandas as pd
from src.validate.rules import rule_positive_price, rule_duplicate_ids,rule_duplicate_rows,rule_valid_date_format,rule_missing_market,rule_known_commodity

#%%
df = pd.read_csv("data/raw/prices.csv")

#%%
negative_prices = rule_positive_price(df)
#%%
duplicate_ids = rule_duplicate_ids(df)

#%%
duplicate_rows = rule_duplicate_rows(df)

#%%
invalid_dates = rule_valid_date_format(df)

#%%
missing_markets = rule_missing_market(df)

#%%
not_known_commodities = rule_known_commodity(df)

# %%
print(negative_prices)
# %%
print(duplicate_ids)
# %%
print(duplicate_rows)

# %%
print(invalid_dates)

# %%
print(missing_markets)
# %%
print(not_known_commodities)
# %%
