import streamlit as st


def render_kpi_cards(df):
    """Displays top-level summary metrics mapping Income against Hazardous Waste Reports."""
    if df.empty:
        st.warning("No data available.")
        return

    # Ensure valid rows exist for calculation
    valid_df = df.dropna(subset=["median_income", "environmental_impact_score"])

    if valid_df.empty:
        st.warning("No complete records found for income and environmental scores.")
        return

    # 1. Income Extremes
    highest_income_row = valid_df.loc[valid_df["median_income"].idxmax()]
    lowest_income_row = valid_df.loc[valid_df["median_income"].idxmin()]

    # 2. Environmental Extremes
    most_reports_row = valid_df.loc[valid_df["environmental_impact_score"].idxmax()]
    least_reports_row = valid_df.loc[valid_df["environmental_impact_score"].idxmin()]

    # 3. Median Income Town (50th Percentile)
    sorted_income_df = valid_df.sort_values(by="median_income").reset_index(drop=True)
    median_idx = len(sorted_income_df) // 2
    median_income_row = sorted_income_df.iloc[median_idx]

    # 4. Statewide Total Reports
    total_reports = int(valid_df["environmental_impact_score"].sum())

    st.markdown("### Key Municipal Metrics")

    # ROW 1: Income Extremes & Middle Town
    row1_col1, row1_col2, row1_col3 = st.columns(3)

    with row1_col1:
        st.subheader("Highest Income Town")
        st.write(f"**Town:** {highest_income_row['town_name']}")
        st.write(f"**Median Income:** ${highest_income_row['median_income']:,.0f}")
        st.write(f"**Waste Reports:** {int(highest_income_row['environmental_impact_score']):,}")

    with row1_col2:
        st.subheader("Median Income Town")
        st.write(f"**Town:** {median_income_row['town_name']}")
        st.write(f"**Median Income:** ${median_income_row['median_income']:,.0f}")
        st.write(f"**Waste Reports:** {int(median_income_row['environmental_impact_score']):,}")

    with row1_col3:
        st.subheader("Lowest Income Town")
        st.write(f"**Town:** {lowest_income_row['town_name']}")
        st.write(f"**Median Income:** ${lowest_income_row['median_income']:,.0f}")
        st.write(f"**Waste Reports:** {int(lowest_income_row['environmental_impact_score']):,}")

    st.markdown("---")

    # ROW 2: Report Extremes & Statewide Total
    row2_col1, row2_col2, row2_col3 = st.columns(3)

    with row2_col1:
        st.subheader("Most Waste Reports")
        st.write(f"**Town:** {most_reports_row['town_name']}")
        st.write(f"**Waste Reports:** {int(most_reports_row['environmental_impact_score']):,}")
        st.write(f"**Median Income:** ${most_reports_row['median_income']:,.0f}")

    with row2_col2:
        st.subheader("Least Waste Reports")
        st.write(f"**Town:** {least_reports_row['town_name']}")
        st.write(f"**Waste Reports:** {int(least_reports_row['environmental_impact_score']):,}")
        st.write(f"**Median Income:** ${least_reports_row['median_income']:,.0f}")

    with row2_col3:
        st.subheader("Statewide Total Reports")
        st.write("**Region:** All CT Towns Combined")
        st.write(f"**Total Reports:** {total_reports:,}")
        st.write(f"**Town Count:** {len(valid_df)} Municipalities")