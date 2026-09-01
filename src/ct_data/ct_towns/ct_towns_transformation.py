import os
import sys
import pandas as pd
from sqlalchemy import text
from ct_data.database import get_db_engine
from ct_data.utils.text_utils import standardize_town_name


def load_towns(filename):
    # Verify CSV file exists
    if not os.path.exists(filename):
        print(f"Error: Could not find CSV file at {filename}")
        return

    print("Reading CT_Towns.csv...")
    df_raw = pd.read_csv(filename)

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
            "Shape__Area": "shape_area",
            "Shape__Length": "shape_length",
        }
    )

    # Standardize town names using the centralized utility function
    df_clean["town_name"] = df_clean["town_name"].apply(standardize_town_name)

    # Ensure other text columns are cleaned strings
    df_clean["geoid"] = df_clean["geoid"].astype(str).str.strip()
    if "county_name" in df_clean.columns:
        df_clean["county_name"] = df_clean["county_name"].astype(str).str.strip()

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
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()

    # Deduplicate by primary key (town_name) to prevent duplicate key errors
    df_clean = df_clean.drop_duplicates(subset=["town_name"])

    # 3. CONNECT & LOAD INTO POSTGRESQL
    print("Connecting to PostgreSQL using database.py engine...")
    engine = get_db_engine()

    with engine.begin() as conn:
        print("Truncating existing records safely...")
        # Clear existing rows while preserving table structure & FK references
        conn.execute(text("TRUNCATE TABLE ct_towns CASCADE;"))

        print("Writing records into 'ct_towns' table...")
        df_clean.to_sql(
            "ct_towns", con=conn, if_exists="append", index=False
        )

    print(
        f"Successfully loaded {len(df_clean)} Connecticut towns into PostgreSQL!"
    )
    return len(df_clean)

if __name__ == "__main__":
    # 1. PATH SETUP
    SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if SRC_DIR not in sys.path:
        sys.path.append(SRC_DIR)

    PROJECT_ROOT = os.path.dirname(SRC_DIR)
    CSV_PATH = os.path.join(PROJECT_ROOT, "data", "CT_Towns.csv")
    load_towns(CSV_PATH)