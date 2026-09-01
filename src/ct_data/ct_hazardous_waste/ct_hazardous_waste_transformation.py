import os
import sys
import pandas as pd
from sqlalchemy import text
from ct_data.database import get_db_engine
from ct_data.utils.text_utils import standardize_town_name


# 3. INGESTION & LINKING WORKFLOW
def load_hazardous_data(filename):
    if not os.path.exists(filename):
        print(f"Error: Could not find CSV file at {filename}")
        return

    print("Reading CSV file...")
    df_raw = pd.read_csv(filename)

    print("Transforming columns to match PostgreSQL schema...")
    # Rename CSV headers directly to match your SQL table definitions
    df_clean = df_raw.rename(
        columns={
            "town": "town_name",
            "address": "town_address",
            "client": "client",
            "id1": "manifest_number",
            "id2": "generator_id_number",
            "docdate": "date_shipped",
        }
    )

    print("Calling standardization function on CSV town names...")
    # Apply standardize_town_name to clean and standardize town names
    df_clean["town_name"] = df_clean["town_name"].apply(standardize_town_name)

    # Convert 'Out Of State' and empty/null town names to None (SQL NULL) so FK checks pass
    df_clean["town_name"] = df_clean["town_name"].apply(
        lambda x: None if str(x).strip().lower() in ["out of state", "", "none", "nan"] else x
    )

    # Clean text formatting for remaining string fields
    str_cols = ["town_address", "client", "manifest_number", "generator_id_number"]
    for col in str_cols:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].astype(str).str.strip()

    # Format ISO timestamps (e.g., '2004-09-25T00:00:00.000') to standard YYYY-MM-DD DATE objects
    df_clean["date_shipped"] = pd.to_datetime(df_clean["date_shipped"], errors="coerce").dt.date

    # 4. FETCH GEOIDs FROM POSTGRESQL & JOIN
    engine = get_db_engine()
    print("Fetching existing GEOID lookup mapping from 'ct_towns'...")

    with engine.connect() as conn:
        towns_df = pd.read_sql(
            text("SELECT town_name, geoid FROM ct_towns;"), conn
        )

    # Apply standardize_town_name function to the database town names for symmetrical matching
    towns_df["town_name_std"] = towns_df["town_name"].apply(standardize_town_name)

    print("Matching standardized town names to Census GEOIDs...")
    df_merged = pd.merge(
        df_clean,
        towns_df[["town_name_std", "geoid"]],
        left_on="town_name",
        right_on="town_name_std",
        how="left"
    )

    # Clean up temporary matching key
    df_final = df_merged.drop(columns=["town_name_std"])

    # 5. LOAD INTO POSTGRESQL
    
    with engine.begin() as conn:
        print("Truncating existing ct hazards records safely...")
        conn.execute(text("TRUNCATE TABLE ct_hazardous_data CASCADE;"))

        print("Writing processed records into 'ct_hazardous_data'...")
        df_final.to_sql(
            "ct_hazardous_data",
            con=conn,
            if_exists="append",
            index=False,
            chunksize=5000,
        )

    print(f"Successfully standardized, linked, and inserted {len(df_final)} records into PostgreSQL!")
    return len(df_final)

if __name__ == "__main__":
    # 1. PATH SETUP
    SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if SRC_DIR not in sys.path:
        sys.path.append(SRC_DIR)

    PROJECT_ROOT = os.path.dirname(SRC_DIR)
    CSV_PATH = os.path.join(PROJECT_ROOT, "data", "Hazardous_waste.csv")
    load_hazardous_data(CSV_PATH)