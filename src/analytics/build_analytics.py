#%%
import os
import time
import pandas as pd
import duckdb as db


# %%
RAW_JOINED_PATH = "data/processed/prices_with_rainfall.parquet"

#%%
DB_PATH = "data/processed/analytics.duckdb"

# %%
def baseline_query():
    t0 = time.perf_counter()
    result = db.sql(f"""
                    
        SELECT market, AVG(price) AS mean_price
        FROM '{RAW_JOINED_PATH}'
        WHERE commodity = 'Maize'
        GROUP BY market
        ORDER BY mean_price DESC
          
    """).df()
    elapsed = time.perf_counter() - t0
    print("--- Step 1 : Baseline query (flat parquet) ---")
    print(result)
    print(f"Time : {elapsed:.4f}s | File size : {os.path.getsize(RAW_JOINED_PATH)} bytes")
    return elapsed, result  

def build_star_schema():
    df = pd.read_parquet(RAW_JOINED_PATH)
    con = db.connect(DB_PATH)

    dim_market = df[["market"]].drop_duplicates().reset_index(drop=True)
    dim_market["market_id"] = dim_market.index
    con.execute("CREATE OR REPLACE TABLE dim_market AS SELECT * FROM dim_market")

    dim_commodity = df[["commodity"]].drop_duplicates().reset_index(drop=True)
    dim_commodity["commodity_id"] = dim_commodity.index
    con.execute("CREATE OR REPLACE TABLE dim_commodity AS SELECT * FROM dim_commodity")

    fact_price_observation = df.merge(dim_market, on="market").merge(dim_commodity, on="commodity")
    fact_price_observation = fact_price_observation[["id", "date", "market_id", "commodity_id", "price", "rainfall_mm"]]
    con.execute("CREATE OR REPLACE TABLE fact_price_observation AS SELECT * FROM fact_price_observation")

    print("--Step 3: Star schema built--")
    print("Fact table:",con.sql("SELECT COUNT(*) FROM fact_price_observation").fetchone()[0])
    con.close()


def run_analytical_queries():
    con = db.connect(DB_PATH)

    print("---Query 1: Average price by market---")
    print(con.sql(f"""
        SELECT dm.market, AVG(f.price) AS mean_price
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        GROUP BY dm.market
        ORDER BY mean_price DESC
    """).df())

    print("---Query 2 : Observation count by commodity---")
    print(con.sql(f"""
        SELECT dc.commodity, COUNT(*) AS n_observations
        FROM fact_price_observation f
        JOIN dim_commodity dc ON f.commodity_id = dc.commodity_id
        GROUP BY dc.commodity
        ORDER BY n_observations DESC
    """).df())

    print(f"---Query 3: Average price and rainfall by commodity---")
    print(con.sql(f"""
        SELECT dc.commodity, AVG(f.price) AS mean_price, AVG(f.rainfall_mm) AS mean_rainfall
        FROM fact_price_observation f
        JOIN dim_commodity dc ON f.commodity_id = dc.commodity_id
        GROUP BY dc.commodity
        ORDER BY mean_price DESC
    """).df())

    print(f"\n=== Query 4: Maximum price by market ===")
    print(con.sql(f"""
        SELECT dm.market, MAX(f.price) AS max_price
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        GROUP BY dm.market
        ORDER BY max_price DESC
    """).df())

    print(f"\n=== Query 5: Observation count by market and commodity ===")
    print(con.sql(f"""
        SELECT dm.market, dc.commodity, COUNT(*) AS observations
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        JOIN dim_commodity dc ON f.commodity_id = dc.commodity_id
        GROUP BY dm.market, dc.commodity
        ORDER BY observations DESC
    """).df())

    con.close()

def compare_performance():
    t0 = time.perf_counter()
    db.sql(f"""
        SELECT market, AVG(price) FROM '{RAW_JOINED_PATH}' GROUP BY market
    """).df()
    flat_time = time.perf_counter() - t0

    t1 = time.perf_counter()
    con = db.connect(DB_PATH)
    con.sql("""
        SELECT dm.market, AVG(f.price)
        FROM fact_price_observation f
        JOIN dim_market dm on f.market_id = dm.market_id
        GROUP BY dm.market
    """).df()
    con.close()

    star_time = time.perf_counter() - t1


    print("---Step 5: Performance comparison ---")
    print(f"Flat Parquet query time: {flat_time:.4f}s")
    print(f"Star schema query time: {star_time:.4f}s")

if __name__ == "__main__":
     
     elapsed, result = baseline_query()
     build_star_schema()
     run_analytical_queries()
     compare_performance()
