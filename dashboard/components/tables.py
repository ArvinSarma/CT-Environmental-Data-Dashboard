import pandas as pd
import streamlit as st


def render_data_table(df):
    """Renders an interactive search table and CSV export option."""
    st.subheader("Raw Data Explorer")

    display_df = df.copy()

    # Ensure median_income is numeric for proper sorting
    display_df["median_income"] = pd.to_numeric(
        display_df["median_income"], errors="coerce"
    )

    st.dataframe(
        display_df[
            [
                "town_name",
                "median_income",
                "environmental_impact_score",
                "data_year",
            ]
        ].rename(
            columns={
                "town_name": "Town Name",
                "median_income": "Median Income",
                "environmental_impact_score": "Hazardous Waste Reports",
                "data_year": "Year",
            }
        ),
        column_config={
            "Median Income": st.column_config.NumberColumn(
                "Median Income",
                format="$%d",  # Formats visually as currency while preserving numeric sorting
            )
        },
        use_container_width=True,
    )

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Full Dataset (.CSV)",
        data=csv_data,
        file_name="ct_towns_income_environmental_analysis.csv",
        mime="text/csv",
    )