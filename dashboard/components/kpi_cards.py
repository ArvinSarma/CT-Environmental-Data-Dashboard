import streamlit as st


def render_kpi_cards(df):
    """Displays top-level summary KPI metrics."""
    if df.empty:
        st.warning("No data available.")
        return

    valid_df = df.dropna(subset=["median_income"])
    avg_income = valid_df["median_income"].mean()

    top_town = valid_df.iloc[0]
    bottom_town = valid_df.iloc[-1]
    total_spills = valid_df["environmental_impact_score"].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(label="Statewide Mean Income", value=f"${avg_income:,.0f}")

    with col2:
        st.metric(
            label="Highest Income Town",
            value=f"${top_town['median_income']:,.0f}",
            delta=top_town["town_name"],
        )

    with col3:
        st.metric(
            label="Lowest Income Town",
            value=f"${bottom_town['median_income']:,.0f}",
            delta=bottom_town["town_name"],
            delta_color="inverse",
        )

    with col4:
        st.metric(
            label="Total Environmental Events",
            value=f"{total_spills:,}",
            delta="Statewide Total",
            delta_color="off",
        )