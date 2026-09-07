#%%
import pandas as pd
#%%
from src.validate import rules
raw_path = "data/raw/prices.csv"

import matplotlib.pyplot as plt
#%%
def inferred_schema(df):
    print("\n----Inferred Schema----")
    print(df.dtypes)

def row_count(df):
    print("\nRow Count")
    print("----------------")
    print(len(df))

def negative_values(df):
    negative_values= rules.rule_positive_price(df)

    print("\nNegative Prices")
    print(len(negative_values))
#%%
def run_files(path = raw_path):
    df =pd.read_csv(path)
    inferred_schema(df)
    row_count(df)
    negative_values(df)
#%%
if __name__ == "__main__":
    run_files()

def plot_price_histogram(df, save_path="docs/price_histogram.png"):
    plt.figure(figsize=(8, 5))
    plt.hist(df["price"], bins=30, edgecolor="black")
    plt.title("Distribution of Price")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.axvline(df["price"].mean(), color="red", linestyle="--", label="Mean")
    plt.legend()
    plt.savefig(save_path)
    plt.close()
    print(f"Histogram saved to {save_path}")

if __name__ == "__main__":
    df = pd.read_csv(raw_path)

    plot_price_histogram(df)
# %%
