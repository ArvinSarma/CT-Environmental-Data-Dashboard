import pandas as pd
import streamlit as st


def render_data_table(df):
    """Renders an interactive search table and CSV export option."""
    st.subheader("Raw Data Explorer")

    display_df = df.copy()
    display_df["median_income"] = display_df["median_income"].apply(
        lambda x: f"${x:,.0f}" if pd.notnull(x) else "N/A"
    )
    display_df["margin_of_error"] = display_df["margin_of_error"].apply(
        lambda x: f"±${x:,.0f}" if pd.notnull(x) else "N/A"
    )

    st.dataframe(
        display_df[
            [
                "town_name",
                "geoid",
                "median_income",
                "margin_of_error",
                "environmental_impact_score",
                "data_year",
            ]
        ].rename(
            columns={
                "town_name": "Town Name",
                "geoid": "GeoID",
                "median_income": "Median Income",
                "margin_of_error": "Margin of Error",
                "environmental_impact_score": "Environmental Score",
                "data_year": "Year",
            }
        ),
        use_container_width=True,
    )

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Full Dataset (.CSV)",
        data=csv_data,
        file_name="ct_towns_income_environmental_analysis.csv",
        mime="text/csv",
    )