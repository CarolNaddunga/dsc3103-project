
from src.ingest.source_a import ingest_source_a
from src.ingest.source_b import ingest_source_b
from src.common.logging_setup import get_logger
from src.transform.clean import clean_data
from src.transform.merge import merge_data

PATH = "data/processed/merged_prices_with_rain.parquet"
logger = get_logger()

def run_pipe():
    logger.info("---Pipeline run started---")

    logger.info("Stage 1: Ingesting source a")

    source_a = ingest_source_a()
    logger.info(f"Stage 11: Ingested source a rows out:{len(source_a)}") 

    logger.info("Stage 2: Ingesting source b")

    source_b = ingest_source_b()
    logger.info(f"Stage 22: Ingested source b rows out:{len(source_b)}")

    logger.info("Stage 3: Cleaning  source_a...")
    clean_prices, decisions = clean_data()
    logger.info(f"Stage 33: Cleaned source a rows out:{len(source_a)}")
    logger.info(f"stage 33: Cleaned prices:{len(clean_prices)}")
    logger.info(f"Stage 33: Cleaning decisions: {len(decisions)}")

    logger.info("Stage 4: ---Merging price and rainfall---")
    merged = merge_data(clean_prices ,source_b)
    logger.info(f"Stage 44: Merged complete: rows in: {len(clean_prices)}:rows out:{len(merged)}")

    logger.info("Stage 5: ---Saving merged file---")
    merged.to_parquet(PATH, index=False)
    logger.info(f"Stage 55: Saving complete: Saved {len(merged)} rows ")

    logger.info("---Pipeline run completed---")

    return 

if __name__ == "__main__":
    run_pipe()