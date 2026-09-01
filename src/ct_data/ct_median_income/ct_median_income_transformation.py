import os
import sys
import pandas as pd
from sqlalchemy import text
from ct_data.database import get_db_engine
from ct_data.utils.text_utils import standardize_town_name


def load_median_income(filename):
    # Verify CSV file exists
    if not os.path.exists(filename):
        print(f"Error: Could not find CSV file at {filename}")
        return

    print("Reading Median_Household_Income.csv...")
    df_raw = pd.read_csv(filename)

    print("Transforming columns...")
    # Rename raw CSV columns to standard SQL column names
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

    # Standardize string fields using central utility
    df_clean["town_name"] = df_clean["town_name"].apply(standardize_town_name)
    df_clean["geography_type"] = df_clean["geography_type"].astype(str).str.strip()
    df_clean["race_ethnicity"] = df_clean["race_ethnicity"].astype(str).str.strip()
    df_clean["geoid"] = df_clean["geoid"].astype(str).str.strip()

    # Numeric conversions
    df_clean["data_year"] = pd.to_numeric(df_clean["data_year"], errors="coerce")
    df_clean["median_income"] = pd.to_numeric(df_clean["median_income"], errors="coerce")
    df_clean["margin_of_error"] = pd.to_numeric(df_clean["margin_of_error"], errors="coerce")

    # Filter to town-level geographies
    df_clean = df_clean[df_clean["geography_type"] == "Town"]

    # Connect to DB to validate foreign key against ct_towns
    print("Connecting to PostgreSQL using database.py engine...")
    engine = get_db_engine()

    with engine.connect() as conn:
        valid_towns = pd.read_sql("SELECT town_name FROM ct_towns", conn)["town_name"].tolist()
    
    valid_towns_set = set(standardize_town_name(t) for t in valid_towns)
    df_clean = df_clean[df_clean["town_name"].isin(valid_towns_set)]

    # Select required columns and deduplicate composite key
    db_columns = [
        "town_name",
        "geoid",
        "median_income",
        "margin_of_error",
        "data_year",
        "race_ethnicity",
        "geography_type",
    ]
    df_clean = df_clean[db_columns]
    df_clean = df_clean.drop_duplicates(subset=["town_name", "data_year", "race_ethnicity"])

    # 3. LOAD INTO POSTGRESQL
    with engine.begin() as conn:
        print("Truncating existing median income records safely...")
        conn.execute(text("TRUNCATE TABLE ct_towns_median_income CASCADE;"))

        print("Writing records into 'ct_towns_median_income' table...")
        df_clean.to_sql(
            "ct_towns_median_income", con=conn, if_exists="append", index=False
        )

    print(
        f"Successfully loaded {len(df_clean)} median income records into PostgreSQL!"
    )


if __name__ == "__main__":
    # 1. PATH SETUP
    SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if SRC_DIR not in sys.path:
        sys.path.append(SRC_DIR)

    PROJECT_ROOT = os.path.dirname(SRC_DIR)
    CSV_PATH = os.path.join(PROJECT_ROOT, "data", "Median_Household_Income.csv")
    load_median_income(CSV_PATH)