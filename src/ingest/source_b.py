import requests 
import pandas as pd
import time
import os

from src.common.config import (SOURCE_B_RAW_PATH,RAINFALL_START_DATE, RAINFALL_END_DATE, RAINFALL_URL, MARKET_COORDS)

def get_mkt_rainfall(mkt_name, latitude, longitude,start_date=RAINFALL_START_DATE,end_date=RAINFALL_END_DATE):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "timezone": "auto",
        "daily": "precipitation_sum"
    }

    response = requests.get(RAINFALL_URL, params=params,timeout=10)
    if response.status_code != 200:
        raise RuntimeError(f"Failed to fetch data for {mkt_name}. Status: {response.status_code}")
    
    daily = response.json()["daily"]
    return pd.DataFrame({
        "date": daily["time"],
        "market": mkt_name,
        "rainfall": daily["precipitation_sum"]
    })

def get_mkt_rain():
    frames = []
    for mkt_name, (latitude, longitude) in MARKET_COORDS.items():
        frames.append(get_mkt_rainfall(mkt_name, latitude, longitude))
        time.sleep(5)
    
    rainfall_df = pd.concat(frames, ignore_index=True)
    #rainfall_df.to_csv(SOURCE_B_RAW_PATH, index=False)
    return rainfall_df
    
def ingest_source_b(path = SOURCE_B_RAW_PATH):
    if os.path.exists(path):
        return pd.read_csv(path)
    df_b = get_mkt_rain()
    df_b.to_csv(path, index=False)
    return df_b
