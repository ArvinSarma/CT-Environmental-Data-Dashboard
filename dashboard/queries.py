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
    """Fetches real median income data from PostgreSQL and adds a temporary mock

    environmental score until the backend pipeline lands.
    """
    engine = get_db_engine()

    # Query real income and town data
    query = """
        SELECT 
            t.town_name,
            i.geoid,
            i.median_income,
            i.margin_of_error,
            i.data_year,
            i.race_ethnicity,
            i.geography_type
        FROM ct_towns_median_income i
        JOIN ct_towns t ON i.geoid = t.geoid
        ORDER BY i.median_income DESC NULLS LAST;
    """

    with engine.connect() as conn:
        df = pd.read_sql(query, conn)

    # ------------------------------------------------------------------
    # TEMPORARY MOCK ENVIRONMENTAL DATA
    # Replace this block with a real SQL JOIN once your friend's table is live!
    # ------------------------------------------------------------------
    np.random.seed(42)  # Keep values consistent across reloads
    df["environmental_impact_score"] = np.random.randint(10, 150, size=len(df))

    return df