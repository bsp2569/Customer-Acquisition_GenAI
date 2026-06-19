import pandas as pd
import numpy as np
import streamlit as st
import os
from genai_insights import answer_campaign_question
from pathlib import Path

st.set_page_config(page_title="Customer Acquisition & Marketing ROI", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("data/simulated_campaign_data.csv", parse_dates=["date"])

df = load_data()

st.title("Customer Acquisition, Marketing ROI & GenAI Insights Platform")
st.caption("Simulated paid search and digital acquisition analytics project")

total_spend = df["cost"].sum()
total_revenue = df["revenue"].sum()
total_conversions = df["conversions"].sum()
total_clicks = df["clicks"].sum()
total_impressions = df["impressions"].sum()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Spend", f"₹{total_spend:,.0f}")
c2.metric("Revenue", f"₹{total_revenue:,.0f}")
c3.metric("ROAS", f"{total_revenue/total_spend:.2f}")
c4.metric("CPA", f"₹{total_spend/max(total_conversions,1):,.0f}")
c5.metric("CTR", f"{total_clicks/total_impressions:.2%}")

st.sidebar.header("Filters")
campaign = st.sidebar.multiselect("Campaign", sorted(df["campaign"].unique()))
channel = st.sidebar.multiselect("Channel", sorted(df["channel"].unique()))
segment = st.sidebar.multiselect("Audience Segment", sorted(df["audience_segment"].unique()))

f = df.copy()
if campaign:
    f = f[f["campaign"].isin(campaign)]
if channel:
    f = f[f["channel"].isin(channel)]
if segment:
    f = f[f["audience_segment"].isin(segment)]

st.header("Campaign Performance")
campaign_perf = f.groupby("campaign").agg(
    impressions=("impressions", "sum"),
    clicks=("clicks", "sum"),
    spend=("cost", "sum"),
    conversions=("conversions", "sum"),
    revenue=("revenue", "sum"),
    quality=("customer_quality_score", "mean")
).reset_index()
campaign_perf["CTR"] = campaign_perf["clicks"] / campaign_perf["impressions"]
campaign_perf["CPA"] = campaign_perf["spend"] / campaign_perf["conversions"].replace(0, np.nan)
campaign_perf["ROAS"] = campaign_perf["revenue"] / campaign_perf["spend"].replace(0, np.nan)
campaign_perf = campaign_perf.fillna(0)

st.dataframe(campaign_perf.sort_values("ROAS", ascending=False), use_container_width=True)
st.bar_chart(campaign_perf.set_index("campaign")[["spend", "revenue"]])

st.header("Funnel Analysis")
funnel = pd.DataFrame({
    "stage": ["Impressions", "Clicks", "Landing Page Visits", "Application Starts", "Conversions"],
    "count": [
        f["impressions"].sum(),
        f["clicks"].sum(),
        f["landing_page_visits"].sum(),
        f["application_starts"].sum(),
        f["conversions"].sum()
    ]
})
st.dataframe(funnel, use_container_width=True)
st.bar_chart(funnel.set_index("stage"))

st.header("Audience Segment Performance")
seg = f.groupby("audience_segment").agg(
    spend=("cost","sum"),
    conversions=("conversions","sum"),
    revenue=("revenue","sum"),
    quality=("customer_quality_score","mean")
).reset_index()
seg["CPA"] = seg["spend"] / seg["conversions"].replace(0, np.nan)
seg["ROAS"] = seg["revenue"] / seg["spend"].replace(0, np.nan)
st.dataframe(seg.sort_values("ROAS", ascending=False).fillna(0), use_container_width=True)

st.header("GenAI Campaign Insights Assistant")

st.info(
    "Ask questions about campaign performance, ROAS, CPA, funnel performance, "
    "audience quality, and budget optimization. The assistant uses the generated "
    "campaign insights report as its knowledge base."
)

# For Streamlit Cloud deployment
try:
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

question = st.text_input(
    "Ask a business question",
    placeholder="Example: Which campaign should be optimized?"
)

if question:
    with st.spinner("Generating campaign insight..."):
        answer = answer_campaign_question(question)

    st.write("### AI-generated insight")
    st.write(answer)

    with st.expander("View knowledge base used"):
        report_path = Path("reports/campaign_insights_report.txt")
        if report_path.exists():
            st.text(report_path.read_text()[:2500])
        else:
            st.warning("Campaign insights report not found.")