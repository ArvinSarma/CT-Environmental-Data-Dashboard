import os
import sys

# 1. PATH SETUP
# Add src/ folder to Python module search path (for database import)
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SRC_DIR)

# Path to project root data-project/ (for data/ folder)
PROJECT_ROOT = os.path.dirname(SRC_DIR)
CSV_PATH = os.path.join(PROJECT_ROOT, "data", "CT_Towns.csv")

# 2. IMPORTS
import pandas as pd
from sqlalchemy import text
from database import get_db_engine


def load_towns():
    # Verify CSV file exists
    if not os.path.exists(CSV_PATH):
        print(f"Error: Could not find CSV file at {CSV_PATH}")
        return

    print("Reading CT_Towns.csv...")
    df_raw = pd.read_csv(CSV_PATH)

    print("Transforming columns...")
    # Rename raw CSV columns to standard lowercase SQL column names
    df_clean = df_raw.rename(
        columns={
            "GeoID": "geoid",
            "FID": "fid",
            "FID_1": "fid_1",
            "sFIPS": "sfips",
            "prFIPS": "prfips",
            "tFIPS": "tfips",
            "TownName": "town_name",
            "CountyName": "county_name",
            "tFIPS20": "tfips20",
            "cFIPS20": "cfips20",
            "PRName": "pr_name",
            "PUMA20code": "puma20_code",
            "PUMA20name": "puma20_name",
            "Shape__Area": "shape_area",  # Fixed double-underscore from raw CSV
            "Shape__Length": "shape_length",  # Fixed double-underscore from raw CSV
        }
    )

    # Ensure GeoID and text columns are clean strings
    df_clean["geoid"] = df_clean["geoid"].astype(str).str.strip()
    df_clean["town_name"] = df_clean["town_name"].str.strip()

    # Convert numeric FIPS columns to strings
    fips_cols = [
        "sfips",
        "prfips",
        "tfips",
        "tfips20",
        "cfips20",
        "puma20_code",
    ]
    for col in fips_cols:
        df_clean[col] = df_clean[col].astype(str)

    # 3. CONNECT & LOAD INTO POSTGRESQL
    print("Connecting to PostgreSQL using database.py engine...")
    engine = get_db_engine()

    with engine.begin() as conn:
        print("Truncating existing records safely...")
        # Clear existing rows while preserving table structure & FK references
        conn.execute(text("TRUNCATE TABLE ct_towns CASCADE;"))

        print("Writing records into 'ct_towns' table...")
        # Append rows into existing table
        df_clean.to_sql(
            "ct_towns", con=conn, if_exists="append", index=False
        )

    print(
        f"Successfully loaded {len(df_clean)} Connecticut towns into PostgreSQL!"
    )


if __name__ == "__main__":
    load_towns()