from components.charts import render_scatter_plot, render_town_comparison_chart
from components.kpi_cards import render_kpi_cards
from components.tables import render_data_table
from queries import get_combined_town_data
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="CT Economic vs. Environmental Explorer",
    page_icon="🌱",
    layout="wide",
)

st.title("Connecticut Economic & Environmental Equity Explorer")
st.markdown(
    "Analyzing **Median Household Income** against **Environmental Metrics** across Connecticut Municipalities."
)

# 1. Fetch Data
try:
    df = get_combined_town_data()
except Exception as e:
    st.error(f"Failed to connect to PostgreSQL database: {e}")
    st.stop()

# 2. Sidebar Filters
st.sidebar.header("Dashboard Controls")

all_towns = sorted(df["town_name"].dropna().unique())
default_towns = [
    t for t in ["Greenwich", "Hartford", "Stamford", "Bridgeport"] if t in all_towns
]

selected_towns = st.sidebar.multiselect(
    "Compare Specific Towns", options=all_towns, default=default_towns
)

# 3. Render Page
render_kpi_cards(df)

st.markdown("---")

tab1, tab2 = st.tabs(["Income vs. Environment Scatter Plot", "Town Comparison"])

with tab1:
    render_scatter_plot(df)

with tab2:
    render_town_comparison_chart(df, selected_towns)

st.markdown("---")

render_data_table(df)