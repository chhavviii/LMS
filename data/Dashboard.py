import streamlit as st
import plotly.express as px
import pandas as pd

def load_dashboard_tab(df):
    st.title("📊 Course Dashboard")

    # Sidebar Filters
    st.sidebar.subheader("Dashboard Filters")
    level_filter = st.sidebar.multiselect("Select Level", df["level"].unique(), default=df["level"].unique())
    subject_filter = st.sidebar.multiselect("Select Subject", df["subject"].unique(), default=df["subject"].unique())

    # Apply filters
    filtered_df = df[df["level"].isin(level_filter) & df["subject"].isin(subject_filter)].copy()

    # Convert 'published_timestamp' to datetime if not already
    if not pd.api.types.is_datetime64_any_dtype(df["published_timestamp"]):
        df["published_timestamp"] = pd.to_datetime(df["published_timestamp"], errors="coerce")
    if not pd.api.types.is_datetime64_any_dtype(filtered_df["published_timestamp"]):
        filtered_df["published_timestamp"] = pd.to_datetime(filtered_df["published_timestamp"], errors="coerce")

    # --- Metrics Row (Horizontal Layout) ---
    col1, col2, col3 = st.columns(3)

    col1.metric("📘 Total Courses", len(filtered_df))
    col2.metric("👨‍🎓 Total Subscribers", int(filtered_df["num_subscribers"].sum()))
    estimated_revenue = (filtered_df['price'] * filtered_df['num_subscribers']).sum()
    col3.metric("💰 Total Revenue (Est.)", f"${int(estimated_revenue):,}")

    st.markdown("---")

    # --- Top 10 Courses by Subscribers ---
    top_courses = filtered_df.sort_values(by="num_subscribers", ascending=False).head(10)
    fig1 = px.bar(
        top_courses,
        x="course_title",
        y="num_subscribers",
        color="subject",
        title="📈 Top 10 Courses by Subscribers",
        labels={"course_title": "Course Title", "num_subscribers": "Subscribers"},
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- Pie Chart: Subject Distribution ---
    subject_counts = filtered_df["subject"].value_counts().reset_index()
    subject_counts.columns = ["subject", "count"]
    fig2 = px.pie(
        subject_counts,
        values="count",
        names="subject",
        title="📚 Course Distribution by Subject",
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- Line Chart: Course Publishing Trend ---
    time_df = filtered_df.dropna(subset=["published_timestamp"]).copy()
    time_df["year_month"] = time_df["published_timestamp"].dt.to_period("M").astype(str)
    time_count = time_df["year_month"].value_counts().sort_index()

    fig3 = px.line(
        x=time_count.index,
        y=time_count.values,
        labels={"x": "Month", "y": "Courses Published"},
        title="🕒 Course Publishing Trend Over Time"
    )
    st.plotly_chart(fig3, use_container_width=True)
