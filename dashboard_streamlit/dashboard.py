# -*- coding: utf-8 -*-
"""
    GoSki Knowledge Graph Dashboard (Local JSON Version)
    Loads local JSON outputs instead of SPARQL server
"""

import streamlit as st
import pandas as pd
import json
import calendar
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import base64
import streamlit_authenticator as stauth
import yaml
import os
from yaml.loader import SafeLoader

st.set_page_config(page_title="Demo GoSki KG Dashboard", layout="wide")

# ----------------------------
# Favicon
# ----------------------------

def get_base64_favicon(filename="favicon.png"):
    # Try to resolve full path relative to this script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, filename)

    # If not found, try from project root (Streamlit Cloud starts here)
    if not os.path.exists(path):
        alt_path = os.path.join("dashboard_streamlit", filename)
        if os.path.exists(alt_path):
            path = alt_path
        else:
            return None  # Optional: skip if still not found

    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

favicon = get_base64_favicon()

if favicon:
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 12px;">
            <img src="data:image/png;base64,{favicon}" width="32" height="28"/>
            <h1 style="margin: 0;">Demo GoSki Dashboard</h1>
        </div>
    """, unsafe_allow_html=True)
else:
    st.title("❄️ Demo GoSki Dashboard")
# st.markdown("❄️ Demo GoSki Dashboard")

# ----------------------------
# Shared Local JSON Loading
# ----------------------------
@st.cache_data
def load_json_to_df(file_path, limit=None):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        bindings = data.get("results", {}).get("bindings", [])
        df = pd.DataFrame([{k: v["value"] for k, v in row.items()} for row in bindings])
        if limit:
            df = df.head(limit)
        return df
    except Exception as e:
        st.error(f"Failed to load {file_path}: {e}")
        return pd.DataFrame()

# Mapping queries to files
QUERY_TO_FILE = {
    "daily_appointment_count": "dashboard_streamlit/outputs/daily_appointment_count.json",
    "total_paid_by_user": "dashboard_streamlit/outputs/total_paid_by_user.json",
    "appointment_time_distribution": "dashboard_streamlit/outputs/appointment_time_distribution.json",
    "available_months": "dashboard_streamlit/outputs/available_months.json",
    "courses_per_type_with_startTime": "dashboard_streamlit/outputs/courses_per_type_with_startTime.json",
    "revenue_per_class_type_with_startTime": "dashboard_streamlit/outputs/revenue_per_class_type_with_startTime.json",
    "revenue_per_day": "dashboard_streamlit/outputs/revenue_per_day.json",
}

def run_named_query_local(query_name, limit=None):
    file_path = QUERY_TO_FILE.get(query_name)
    if not file_path:
        st.error(f"No file mapped for query '{query_name}'")
        return pd.DataFrame()
    return load_json_to_df(file_path, limit)

# ----------------------------
# Dashboard Display
# ----------------------------

def display_data():
    st.title("📊 GoSki Dashboard")

    tab1, tab2, tab3, tab4 = st.tabs(["📆 Daily Appointments", "💰 Top Clients", "🕒 Popular Time Slots", "💵 Revenue Over Time"])

    # ----------------------------
    # 📆 Daily Appointments Chart
    # ----------------------------
    with tab1:
        st.header("Daily Appointments")

        df = run_named_query_local("daily_appointment_count")

        if df.empty:
            st.warning("No appointment data found.")
        else:
            df["count"] = pd.to_numeric(df["count"], errors="coerce")

            # Parse human-readable format
            df["date"] = pd.to_datetime(df["day"], format="%B %d, %Y", errors="coerce")

            # Sort by date to ensure proper ordering
            df = df.sort_values("date")

            # Format label like 'Sat Dec 14'
            df["date_label"] = df["date"].dt.strftime("%a %b %d")

            fig = px.bar(
                df,
                x="date_label",
                y="count",
                title="Appointments per Day",
                labels={"count": "Number of Appointments", "date_label": "Date"},
                template="plotly_white"
            )

            # Set correct order for x-axis categories
            fig.update_layout(
                xaxis=dict(categoryorder="array", categoryarray=df["date_label"]),
                xaxis_title="Date (Weekday)",
                yaxis_title="Appointments",
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)


    # ----------------------------
    # 💰 Top Clients by Revenue
    # ----------------------------
    with tab2:
        st.header("Top Clients by Revenue")

        df = run_named_query_local("total_paid_by_user")

        if df.empty:
            st.warning("No payment data available.")
        else:
            df["totalPaid"] = pd.to_numeric(df["totalPaid"], errors="coerce")
            df = df.sort_values("totalPaid", ascending=False).reset_index(drop=True)

            # ----------------------------
            # 🎛️ Stats Mode Selector
            # ----------------------------
            st.markdown("#### 📊 Revenue Statistics per Client")

            stats_mode = st.radio(
                "Choose how to calculate average and std:",
                ["All Clients", "Exclude Extreme Values"],
                horizontal=True
            )

            if stats_mode == "All Clients":
                df_for_stats = df
            else:
                trim_percent = st.selectbox("Trim top and bottom percent:", [1, 2, 5, 10], index=2)
                lower = df["totalPaid"].quantile(trim_percent / 100)
                upper = df["totalPaid"].quantile(1 - trim_percent / 100)
                df_for_stats = df[(df["totalPaid"] >= lower) & (df["totalPaid"] <= upper)]

            mean_paid = df_for_stats["totalPaid"].mean()
            std_paid = df_for_stats["totalPaid"].std()

            st.markdown(f"#### • **Average Paid per Client:** `{mean_paid:,.0f} NOK`")
            st.markdown(f"#### • **Standard Deviation:** `{std_paid:,.0f} NOK`")

            # ----------------------------
            # 📈 Top Clients Chart
            # ----------------------------
            top_n = st.slider("Show Top Clients", 3, min(150, len(df)), 10)
            df_top = df.head(top_n)

            fig = px.bar(
                df_top,
                x="email",
                y="totalPaid",
                title="Top Paying Clients",
                labels={"totalPaid": "NOK"},
                template="plotly_dark"
            )
            fig.update_layout(xaxis_tickangle=-45, height=500)
            st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # 📊 Appointments by Weekday & Hour
    # ----------------------------
    with tab3:
        st.header("🗓️ Distribution of Private/Nordic Lessons by Weekday and Hour")

        df = run_named_query_local("appointment_time_distribution", limit=2000)

        if df.empty:
            st.warning("No appointment data available.")
        else:
            df["startTime"] = pd.to_datetime(df["startTime"], errors="coerce")
            df["hour"] = df["startTime"].dt.hour
            df["weekday"] = df["startTime"].dt.day_name()

            # Order weekdays
            weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            df["weekday"] = pd.Categorical(df["weekday"], categories=weekday_order, ordered=True)

            # Group and pivot
            grouped = df.groupby(["weekday", "hour"]).size().reset_index(name="count")

            # Pivot for heatmap-like view (optional)
            pivot = grouped.pivot(index="weekday", columns="hour", values="count").fillna(0)

            fig = px.density_heatmap(
                grouped,
                x="weekday",
                y="hour",
                z="count",
                color_continuous_scale="Rainbow",
                title="Appointments Heatmap: Weekday vs Hour",
                labels={"weekday": "Weekday", "hour": "Hour of Day", "count": "Appointments"},
                text_auto=True  # 👈 show counts directly inside cells
            )

            fig.update_traces(
                selector=dict(type='heatmap'),
                showscale=True,
                xgap=3,  # small horizontal gaps
                ygap=3,  # small vertical gaps
                hoverongaps=False,
                textfont=dict(color="black", size=12),  # nicer text style
            )

            fig.update_layout(
                height=600,
                yaxis=dict(),
                margin=dict(t=50, l=0, r=0, b=0),
            )

            st.plotly_chart(fig, use_container_width=True)

    # ----------------------------
    # 💵 Revenue Over Time
    # ----------------------------
    with tab4:
        st.header("Revenue Over Time")

        col1, col2 = st.columns([1, 2])

        # === col1: Course Type Statistics ===
        with col1:
            # ----------------------------------
            # 📅 Month Filter (Toggleable from separate query)
            # ----------------------------------
            with st.expander("📂 Filter by Month", expanded=False):
                df_months = run_named_query_local("available_months", limit=1000)
                df_months["startTime"] = pd.to_datetime(df_months["startTime"], errors="coerce")

                sorted_months_dt = (
                    df_months["startTime"]
                    .dropna()
                    .dt.to_period("M")
                    .drop_duplicates()
                    .sort_values()
                )

                all_months = sorted_months_dt.dt.strftime("%B %Y").tolist()
                selected_month = st.selectbox("Choose month:", ["All"] + all_months)

            # ----------------------------------
            # 🏷️ Courses by Type
            # ----------------------------------
            st.markdown("### 🏷️ Courses by Type")

            df_courses = run_named_query_local("courses_per_type_with_startTime", limit=1000)

            if selected_month != "All":
                st.markdown(f"Filtered by month: **{selected_month}**")
                month_dt = pd.to_datetime(selected_month)
                df_courses["startTime"] = pd.to_datetime(df_courses["startTime"], errors="coerce")
                df_courses = df_courses[
                    df_courses["startTime"].dt.to_period("M") == month_dt.to_period("M")
                ]
            else:
                df_courses["startTime"] = pd.to_datetime(df_courses["startTime"], errors="coerce")

            df_courses["totalCourses"] = pd.to_numeric(df_courses["totalCourses"], errors="coerce").fillna(0)

            df_grouped = (
                df_courses.groupby("normalizedLabel", as_index=False)
                .agg(totalCourses=("totalCourses", "sum"))
                .sort_values("totalCourses", ascending=True)
            )

            fig = px.bar(
                df_grouped,
                x="totalCourses",
                y="normalizedLabel",
                orientation="h",
                title="Courses Held (Grouped)",
                labels={"totalCourses": "Courses", "normalizedLabel": "Course Type"},
                template="plotly_white",
                height=350
            )

            fig.update_layout(
                margin=dict(t=40, l=20, r=20, b=40),
                yaxis=dict(tickfont=dict(size=12)),
                xaxis_title="Number of Courses",
                yaxis_title=""
            )
            st.plotly_chart(fig, use_container_width=True)

            # ----------------------------------
            # 💰 Revenue by Course Type
            # ----------------------------------
            st.markdown("### 💰 Revenue by Course Type")

            df_revenue_raw = run_named_query_local("revenue_per_class_type_with_startTime", limit=2000)
            df_revenue_raw["startTime"] = pd.to_datetime(df_revenue_raw["startTime"], errors="coerce")
            df_revenue_raw["amount"] = pd.to_numeric(df_revenue_raw["amount"], errors="coerce").fillna(0)

            if selected_month != "All":
                month_dt = pd.to_datetime(selected_month)
                df_revenue_raw = df_revenue_raw[
                    df_revenue_raw["startTime"].dt.to_period("M") == month_dt.to_period("M")
                ]

            if df_revenue_raw.empty:
                st.info("No revenue data found by course type.")
            else:
                df_revenue = (
                    df_revenue_raw.groupby("normalizedLabel", as_index=False)["amount"]
                    .sum()
                    .rename(columns={"amount": "totalEarned"})
                    .sort_values("totalEarned", ascending=False)
                )

                total_sum = df_revenue["totalEarned"].sum()
                st.markdown(f"#### 🧾 Total Revenue: `{total_sum:,.0f} NOK`")

                for _, row in df_revenue.iterrows():
                    label = row["normalizedLabel"]
                    total = row["totalEarned"]
                    st.markdown(f"#### &nbsp;&nbsp;&nbsp;&nbsp;• **{label}**: `{total:,.0f} NOK`", unsafe_allow_html=True)

        # === col2: Revenue Visualization ===
        with col2:
            df = run_named_query_local("revenue_per_day")

            if df.empty:
                st.warning("No revenue data found.")
            else:
                df["totalPaid"] = df["totalPaid"].fillna("0")
                df["totalPaid"] = pd.to_numeric(df["totalPaid"], errors="coerce").fillna(0)
                df["date"] = pd.to_datetime(df["day"], format="%B %d, %Y", errors="coerce")
                df = df.sort_values("date")

                view_mode = st.radio("📊 Choose View", ["Area Chart", "Calendar Heatmap"], horizontal=True)

                if view_mode == "Area Chart":
                    df["weekday"] = df["date"].dt.strftime("%a")
                    df["date_str"] = df["date"].dt.strftime("%b %d")
                    df["x_label"] = df["weekday"] + "\n" + df["date_str"]

                    fig = px.area(
                        df,
                        x="x_label",
                        y="totalPaid",
                        title="Daily Revenue (NOK)",
                        labels={"totalPaid": "NOK"},
                        template="plotly_white"
                    )

                    fig.update_layout(
                        xaxis_title="Date & Weekday",
                        yaxis_title="Total Paid",
                        height=500
                    )
                    st.plotly_chart(fig, use_container_width=True)

                else:
                    st.subheader("🗓️ Calendar Heatmap View")
                    df["year"] = df["date"].dt.year
                    df["month"] = df["date"].dt.month
                    df["day"] = df["date"].dt.day
                    active_months = df[df["totalPaid"] > 0][["year", "month"]].drop_duplicates().sort_values(["year", "month"])
                    months = active_months.to_records(index=False)
                    vmin = df["totalPaid"].min()
                    vmax = df["totalPaid"].max()
                    cols = 3
                    rows = (len(months) + cols - 1) // cols

                    fig = make_subplots(
                        rows=rows, cols=cols,
                        subplot_titles=[f"{calendar.month_name[m]} {y}" for y, m in months],
                        horizontal_spacing=0.05, vertical_spacing=0.12
                    )

                    for i, (year, month) in enumerate(months):
                        cal_df = df[(df["year"] == year) & (df["month"] == month)]
                        month_calendar = calendar.monthcalendar(year, month)
                        heatmap_data = np.zeros((len(month_calendar), 7))

                        for week_i, week in enumerate(month_calendar):
                            for day_i, day in enumerate(week):
                                if day == 0:
                                    continue
                                match = cal_df[cal_df["day"] == day]
                                if not match.empty:
                                    heatmap_data[week_i][day_i] = match["totalPaid"].values[0]

                        row_idx = i // cols + 1
                        col_idx = i % cols + 1

                        fig.add_trace(
                            go.Heatmap(
                                z=heatmap_data,
                                x=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
                                y=[f"Week {w+1}" for w in range(len(month_calendar))],
                                colorscale="Reds",
                                zmin=vmin,
                                zmax=vmax,
                                showscale=(i == len(months) - 1),
                                colorbar=dict(title="NOK", len=0.5, x=1.03)
                            ),
                            row=row_idx, col=col_idx
                        )

                    fig.update_layout(
                        height=rows * 300,
                        title_text="📆 Revenue Calendar (Shared Scale)",
                        margin=dict(t=60, l=20, r=20, b=20),
                        template="plotly_white"
                    )
                    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Authentication
# ----------------------------

with open("dashboard_streamlit/config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

authenticator.login('main')

if st.session_state.get('authentication_status') is True:
    authenticator.logout('Logout', 'sidebar')
    st.write(f"Welcome *{st.session_state.get('name')}*")
    display_data()
elif st.session_state.get('authentication_status') is False:
    st.error("Username/password is incorrect")
elif st.session_state.get('authentication_status') is None:
    st.warning("Please enter your username and password")