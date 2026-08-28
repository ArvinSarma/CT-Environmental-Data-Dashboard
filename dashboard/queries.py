import os
import sys
import numpy as np
import pandas as pd

# Add src/ to sys.path to access database.py
SRC_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"
)
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from database import get_db_engine

def get_combined_town_data():
    """Fetches real median income data from PostgreSQL, aggregates it by town/year, 
    and adds a temporary mock environmental score.
    """
    engine = get_db_engine()

    # We can query directly from ct_towns_median_income since town_name is now there.
    # We filter out NULL medians directly at the SQL level.
    query = """
        SELECT 
            town_name,
            median_income,
            data_year
        FROM ct_towns_median_income
        WHERE median_income IS NOT NULL;
    """

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    # Aggregate: Calculate the total median income per town per year across all races
    df_aggregated = (
        df.groupby(["town_name", "data_year"], as_index=False)["median_income"]
        .median()
    )

    # ------------------------------------------------------------------
    # TEMPORARY MOCK ENVIRONMENTAL DATA
    # Replace this block with a real SQL JOIN once your friend's PostgreSQL table is live!
    # ------------------------------------------------------------------
    np.random.seed(42)  # Keep values consistent across reloads
    df_aggregated["environmental_impact_score"] = np.random.randint(10, 150, size=len(df_aggregated))

    return df_aggregated