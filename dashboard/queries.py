import os
import sys
import pandas as pd
from sqlalchemy import text

# Add src/ to sys.path to access database.py
SRC_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"
)
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from database import get_db_engine


def get_combined_town_data():
    """Fetches real median income data from PostgreSQL and joins hazardous waste reports 
    aggregated per town and year extracted directly from the date_shipped DATE column.
    """
    engine = get_db_engine()

    query = """
        WITH filtered_income AS (
            SELECT 
                town_name,
                data_year,
                CAST(median_income AS NUMERIC) AS median_income,
                LOWER(TRIM(race_ethnicity)) AS race_clean,
                ROW_NUMBER() OVER (
                    PARTITION BY town_name, data_year 
                    ORDER BY 
                        CASE 
                            WHEN data_year >= 2023 AND LOWER(TRIM(race_ethnicity)) IN ('all races', 'total', 'total population') THEN 1
                            WHEN LOWER(TRIM(race_ethnicity)) IN ('white alone', 'white') THEN 2
                            ELSE 3
                        END
                ) as rank_priority
            FROM ct_towns_median_income
            WHERE median_income IS NOT NULL
        ),
        income_agg AS (
            SELECT 
                town_name,
                data_year,
                median_income
            FROM filtered_income
            WHERE rank_priority = 1
        ),
        hazardous_agg AS (
            SELECT 
                town_name,
                EXTRACT(YEAR FROM date_shipped)::INT AS data_year,
                COUNT(*) AS num_reports
            FROM ct_hazardous_data
            WHERE town_name IS NOT NULL 
              AND date_shipped IS NOT NULL
            GROUP BY town_name, EXTRACT(YEAR FROM date_shipped)::INT
        )
        SELECT 
            i.town_name,
            i.data_year,
            i.median_income,
            COALESCE(h.num_reports, 0) AS environmental_impact_score
        FROM income_agg i
        LEFT JOIN hazardous_agg h 
            ON i.town_name = h.town_name 
           AND i.data_year = h.data_year;
    """

    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)

    return df