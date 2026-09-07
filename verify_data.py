import hashlib
from src.validate import profile
from src.transform import clean

raw_path = "data/raw/prices.csv"


def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


if __name__ == "__main__":
    hash_before = file_hash(raw_path)

    # run your full pipeline
    df_clean, log = clean.clean_data(raw_path)
    df_clean.to_parquet("data/processed/prices_clean.parquet", index=False)

    hash_after = file_hash(raw_path)

    if hash_before == hash_after:
        print("Raw file unchanged — hashes match.")
    else:
        print("WARNING: Raw file was modified!")
        print(f"Before: {hash_before}")
        print(f"After:  {hash_after}")