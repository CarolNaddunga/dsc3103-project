from airflow.sdk  import DAG, task 
import pandas as pd
from datetime import datetime, timedelta

from src.ingest.source_a import ingest_source_a
from src.ingest.source_b import ingest_source_b

from src.transform.clean import clean_data
from src.transform.merge import merge_data

from src.analytics.build_analytics import build_star_schema
from src.common.config import SOURCE_A_RAW_PATH, SOURCE_B_RAW_PATH

import duckdb

CLEAN_OUTPUT_PATH = "data/processed/prices_clean_dag.parquet"
JOINED_OUTPUT_PATH = "data/processed/prices_with-rainfall.parquet"

with DAG(

    dag_id  = "market_pipeline_dag",
    schedule = "@daily",
    start_date = datetime(2026, 10, 2),
    catchup = False

):

    @task
    def acquire_a():
        df = ingest_source_a(SOURCE_A_RAW_PATH)

        return {"path": SOURCE_A_RAW_PATH, "rows": len(df)}

    #a = acquire_()

    @task 
    def acquire_b():
        df = ingest_source_b(SOURCE_B_RAW_PATH)

        return {"path": SOURCE_B_RAW_PATH, "rows": len(df)}
    
    @task
    def clean(acquire_a_result:dict):
        clean_df,log = clean_data(acquire_a_result["path"])
        clean_df.to_parquet(CLEAN_OUTPUT_PATH,index=False)
        return {"path": CLEAN_OUTPUT_PATH,"rows": len(clean_df),"rules_triggered":len(log)}
    
    @task
    def merge(clean_result:dict,acquire_b_result:dict):
        clean_df = pd.read_parquet(clean_result["path"])
        rainfall = ingest_source_b(acquire_b_result["path"])
        merge_data = merge_data(clean_df, rainfall)
        merge_data.to_parquet(JOINED_OUTPUT_PATH,index=False)
        return {"path":JOINED_OUTPUT_PATH,"rows": len(merge_data)}
    
    @task
    def merge(clean_result:dict,acquire_b_result:dict):
        #1. load my cleaned market data
        clean_df = pd.read_parquet(clean_result["path"])
        #2. FIX: Ingest source B using its direct config path variable
        # instead of drilling into the task dictionary mapping
        rainfall = ingest_source_b(SOURCE_B_RAW_PATH)
        #3. Combine and save your data
        merged_df = merge_data(clean_df, rainfall)
        merged_df.to_parquet(JOINED_OUTPUT_PATH,index=False)
        return {"path": JOINED_OUTPUT_PATH, "rows":len(merged_df)}
    
    @task
    def store(join_result:dict):
        build_star_schema()
        return{"status":"Star schema built successfully"}
    

    a = acquire_a()
    b = acquire_b()
    cleaned_data = clean(a)

    merged = merge(cleaned_data, b)
    stored = store(merged)
