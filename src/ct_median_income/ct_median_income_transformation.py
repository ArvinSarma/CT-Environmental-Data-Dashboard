import os
import sys

# 1. PATH SETUP
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SRC_DIR)

PROJECT_ROOT = os.path.dirname(SRC_DIR)
CSV_PATH = os.path.join(PROJECT_ROOT, "data", "Median_Household_Income.csv")

# 2. IMPORTS
import pandas as pd
from sqlalchemy import text
from database import get_db_engine


def load_median_income():
    if not os.path.exists(CSV_PATH):
        print(f"Error: Could not find CSV file at {CSV_PATH}")
        return

    print("Reading Median_Household_Income.csv...")
    df_raw = pd.read_csv(CSV_PATH)

    print("Transforming columns...")
    df_clean = df_raw.rename(
        columns={
            "Year": "data_year",
            "GeoID": "geoid",
            "Geography Type": "geography_type",
            "Geography Name": "town_name",
            "Race/Ethnicity": "race_ethnicity",
            "Value": "median_income",
            "Margin of Error": "margin_of_error",
        }
    )

    # 3. DATA CLEANING & TYPE CASTING
    df_clean["geoid"] = df_clean["geoid"].astype(str).str.strip()
    df_clean["geography_type"] = df_clean["geography_type"].str.strip()
    df_clean["town_name"] = df_clean["town_name"].str.strip()
    df_clean["race_ethnicity"] = df_clean["race_ethnicity"].str.strip()

    df_clean["data_year"] = pd.to_numeric(df_clean["data_year"], errors="coerce")
    df_clean["median_income"] = pd.to_numeric(df_clean["median_income"], errors="coerce")
    df_clean["margin_of_error"] = pd.to_numeric(df_clean["margin_of_error"], errors="coerce")

    # Filter out extra columns (drops ObjectId and any raw CSV metadata)
    db_columns = [
        "geoid",
        "town_name",
        "median_income",
        "margin_of_error",
        "data_year",
        "race_ethnicity",
        "geography_type",
    ]
    df_clean = df_clean[db_columns]

    # 4. CONNECT & LOAD INTO POSTGRESQL
    print("Connecting to PostgreSQL using database.py engine...")
    engine = get_db_engine()

    with engine.begin() as conn:
        print("Truncating existing records safely...")
        conn.execute(text("TRUNCATE TABLE ct_towns_median_income CASCADE;"))

        print("Writing records into 'ct_towns_median_income' table...")
        df_clean.to_sql(
            "ct_towns_median_income", con=conn, if_exists="append", index=False
        )

    print(
        f"Successfully loaded {len(df_clean)} median income records into PostgreSQL!"
    )


if __name__ == "__main__":
    load_median_income()