import os
import pandas as pd
from sqlalchemy import text
from database import get_db_engine  # Importing our central, secure DB connection!

# 1. SETUP PATHS
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "CT_Towns.csv")

def load_towns():
    # Verify CSV file exists
    if not os.path.exists(CSV_PATH):
        print(f"Error: Could not find CSV file at {CSV_PATH}")
        return

    print("Reading CT_Towns.csv...")
    df_raw = pd.read_csv(CSV_PATH)

    print("Transforming columns...")
    # Rename raw CSV columns to standard lowercase SQL column names
    df_clean = df_raw.rename(columns={
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
        "Shape__Area": "shape_area",      # Fixed double-underscore from raw CSV
        "Shape__Length": "shape_length"    # Fixed double-underscore from raw CSV
    })

    # Ensure GeoID is formatted cleanly as a string
    df_clean["geoid"] = df_clean["geoid"].astype(str).str.strip()
    df_clean["town_name"] = df_clean["town_name"].str.strip()

    # Convert numeric FIPS columns to strings
    fips_cols = ["sfips", "prfips", "tfips", "tfips20", "cfips20", "puma20_code"]
    for col in fips_cols:
        df_clean[col] = df_clean[col].astype(str)

    # 2. CONNECT & LOAD INTO POSTGRESQL
    print("Connecting to PostgreSQL using database.py engine...")
    engine = get_db_engine()

    with engine.begin() as conn:
        print("Writing records into 'towns' table...")
        df_clean.to_sql("towns", con=conn, if_exists="replace", index=False)

        # Enforce Primary Key constraint on geoid
        conn.execute(text("ALTER TABLE towns ADD PRIMARY KEY (geoid);"))

    print(f"Successfully loaded {len(df_clean)} Connecticut towns into PostgreSQL!")

if __name__ == "__main__":
    load_towns()