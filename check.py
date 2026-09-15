#%%
import pandas as pd
import src.validate.rules as rules
from src.validate.rules import rule_positive_price, rule_duplicate_ids,rule_duplicate_rows,rule_valid_date_format,rule_missing_market,rule_known_commodity, rule_negative_rain
from src.ingest.source_a import ingest_source_a
from src.transform.merge import merge_data

#%%
from src.transform.clean import clean_data

#%%
from src.ingest.source_b import ingest_source_b

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
source_a = ingest_source_a()
print(source_a.shape)

# %%
source_b = ingest_source_b()
print(source_b.shape)
print(source_b.head(10))
# %%
clean_prices, _ = clean_data()
print(clean_prices.shape)

negative_rain = rules.rule_negative_rain(source_b)
print(len(negative_rain))

bad_dates = rules.rule_valid_date_format(source_b)
print(len(bad_dates))

merged_data = merge_data(clean_prices,source_b)
print(len(merged_data))
print(merged_data.head(10))