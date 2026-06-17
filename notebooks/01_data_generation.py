
import numpy as np
import pandas as pd
from pathlib import Path

np.random.seed(42)

N = 5000
dates = pd.date_range("2026-01-01", "2026-03-31")

campaigns = [
    "Credit Card Acquisition",
    "Travel Rewards Campaign",
    "Business Card Paid Search",
    "Cashback Search Campaign",
    "SME Acquisition Campaign",
    "Premium Card Campaign"
]
channels = ["Google Search", "Bing Search", "YouTube", "Display", "Meta", "Affiliate"]
keywords = [
    "best credit card", "business credit card", "travel rewards card",
    "cashback credit card", "premium credit card", "low annual fee card",
    "credit card for business", "airport lounge credit card",
    "fuel cashback card", "no annual fee credit card"
]
devices = ["Mobile", "Desktop", "Tablet"]
geographies = ["Gurgaon", "Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune", "Chennai", "Kolkata"]
segments = ["Young Professionals", "Small Business Owners", "Frequent Travelers", "Premium Customers", "Students", "High Income Urban"]

df = pd.DataFrame({
    "date": np.random.choice(dates, N),
    "campaign": np.random.choice(campaigns, N),
    "channel": np.random.choice(channels, N, p=[0.38, 0.12, 0.12, 0.12, 0.16, 0.10]),
    "keyword": np.random.choice(keywords, N),
    "device": np.random.choice(devices, N, p=[0.65, 0.30, 0.05]),
    "geography": np.random.choice(geographies, N),
    "audience_segment": np.random.choice(segments, N)
})

# Generate realistic metrics
base_impressions = np.random.gamma(shape=2.5, scale=900, size=N).astype(int) + 100
df["impressions"] = base_impressions

intent_boost = df["keyword"].str.contains("business|premium|travel|lounge", case=False).astype(float) * 0.012
search_boost = df["channel"].isin(["Google Search", "Bing Search"]).astype(float) * 0.018
mobile_penalty = (df["device"] == "Mobile").astype(float) * -0.003

ctr = np.clip(0.025 + intent_boost + search_boost + mobile_penalty + np.random.normal(0, 0.01, N), 0.004, 0.12)
df["clicks"] = np.maximum(1, (df["impressions"] * ctr).astype(int))

cpc_base = np.where(df["channel"].isin(["Google Search", "Bing Search"]), 22, 12)
premium_cpc = df["keyword"].str.contains("premium|business|travel", case=False).astype(int) * 8
df["cost"] = np.round(df["clicks"] * (cpc_base + premium_cpc + np.random.normal(0, 4, N)).clip(4, 60), 2)

visit_rate = np.clip(0.72 + np.random.normal(0, 0.08, N), 0.45, 0.95)
df["landing_page_visits"] = np.maximum(0, (df["clicks"] * visit_rate).astype(int))

start_rate = np.clip(0.34 + np.random.normal(0, 0.08, N), 0.08, 0.65)
df["application_starts"] = np.maximum(0, (df["landing_page_visits"] * start_rate).astype(int))

seg_boost = df["audience_segment"].map({
    "Small Business Owners": 0.055,
    "Frequent Travelers": 0.045,
    "Premium Customers": 0.050,
    "High Income Urban": 0.035,
    "Young Professionals": 0.025,
    "Students": 0.010
}).values

conv_rate = np.clip(0.08 + seg_boost + intent_boost * 2 + np.random.normal(0, 0.035, N), 0.01, 0.35)
df["conversions"] = np.maximum(0, (df["application_starts"] * conv_rate).astype(int))

value = df["audience_segment"].map({
    "Small Business Owners": 18000,
    "Frequent Travelers": 16000,
    "Premium Customers": 22000,
    "High Income Urban": 14000,
    "Young Professionals": 9000,
    "Students": 5000
}).values
df["revenue"] = np.round(df["conversions"] * (value + np.random.normal(0, 2500, N)).clip(2000, 30000), 2)

quality = df["audience_segment"].map({
    "Small Business Owners": 82,
    "Frequent Travelers": 78,
    "Premium Customers": 88,
    "High Income Urban": 72,
    "Young Professionals": 62,
    "Students": 45
}).values
df["customer_quality_score"] = np.round(np.clip(quality + np.random.normal(0, 10, N), 1, 100), 1)

# KPIs
df["ctr"] = df["clicks"] / df["impressions"]
df["cpc"] = df["cost"] / df["clicks"]
df["conversion_rate"] = np.where(df["clicks"] > 0, df["conversions"] / df["clicks"], 0)
df["cpa"] = np.where(df["conversions"] > 0, df["cost"] / df["conversions"], np.nan)
df["roas"] = np.where(df["cost"] > 0, df["revenue"] / df["cost"], 0)
df["visit_rate"] = np.where(df["clicks"] > 0, df["landing_page_visits"] / df["clicks"], 0)
df["application_start_rate"] = np.where(df["landing_page_visits"] > 0, df["application_starts"] / df["landing_page_visits"], 0)
df["final_conversion_rate"] = np.where(df["application_starts"] > 0, df["conversions"] / df["application_starts"], 0)

Path("data").mkdir(exist_ok=True)
df.to_csv("data/simulated_campaign_data.csv", index=False)
print("Generated data/simulated_campaign_data.csv", df.shape)
