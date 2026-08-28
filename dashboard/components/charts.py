import plotly.express as px
import streamlit as st


def render_scatter_plot(df):
    """Renders the main Scatter Plot (Income vs Environmental Impact)."""
    fig = px.scatter(
        df,
        x="median_income",
        y="environmental_impact_score",
        text="town_name",
        hover_name="town_name",
        hover_data={
            "median_income": ":$,.0f",
            "environmental_impact_score": ":,",
            "town_name": False,
        },
        title="Town Median Income vs. Environmental Impact Score",
        labels={
            "median_income": "Median Household Income ($)",
            "environmental_impact_score": "Environmental Impact Score / Incidents",
        },
        color="environmental_impact_score",
        color_continuous_scale="Reds",
        trendline="ols",  # Draws an automated trend line to visually highlight correlation
    )

    fig.update_traces(
        marker=dict(size=12, opacity=0.8, line=dict(width=1, color="DarkSlateGrey")),
        textposition="top center",
    )
    fig.update_layout(height=550)

    st.plotly_chart(fig, use_container_width=True)


def render_town_comparison_chart(df, selected_towns):
    """Renders side-by-side bar chart comparison for user-selected towns."""
    if not selected_towns:
        st.info("Select towns from the sidebar to compare them side-by-side.")
        return

    filtered_df = df[df["town_name"].isin(selected_towns)]

    # Reshape data for side-by-side dual bar chart
    fig = px.bar(
        filtered_df,
        x="town_name",
        y=["median_income", "environmental_impact_score"],
        barmode="group",
        title="Side-by-Side Town Comparison",
        labels={
            "town_name": "Town",
            "value": "Metric Value",
            "variable": "Metric Category",
        },
    )

    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)