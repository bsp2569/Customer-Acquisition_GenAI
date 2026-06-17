
import pandas as pd
import numpy as np
from pathlib import Path

df = pd.read_csv("data/simulated_campaign_data.csv", parse_dates=["date"])

def weighted_kpis(group):
    spend = group["cost"].sum()
    clicks = group["clicks"].sum()
    imps = group["impressions"].sum()
    conv = group["conversions"].sum()
    rev = group["revenue"].sum()
    return pd.Series({
        "impressions": imps,
        "clicks": clicks,
        "spend": spend,
        "conversions": conv,
        "revenue": rev,
        "ctr": clicks / imps if imps else 0,
        "cpc": spend / clicks if clicks else 0,
        "cpa": spend / conv if conv else np.nan,
        "roas": rev / spend if spend else 0,
        "conversion_rate": conv / clicks if clicks else 0,
        "avg_quality_score": group["customer_quality_score"].mean()
    })

Path("reports").mkdir(exist_ok=True)

campaign = df.groupby("campaign").apply(weighted_kpis).reset_index().sort_values("roas", ascending=False)
channel = df.groupby("channel").apply(weighted_kpis).reset_index().sort_values("roas", ascending=False)
keyword = df.groupby("keyword").apply(weighted_kpis).reset_index().sort_values("spend", ascending=False)
segment = df.groupby("audience_segment").apply(weighted_kpis).reset_index().sort_values("roas", ascending=False)

campaign.to_csv("reports/campaign_performance.csv", index=False)
channel.to_csv("reports/channel_performance.csv", index=False)
keyword.to_csv("reports/keyword_performance.csv", index=False)
segment.to_csv("reports/segment_performance.csv", index=False)

# Simple recommendation report
high_spend_low_roas = campaign[(campaign["spend"] > campaign["spend"].median()) & (campaign["roas"] < campaign["roas"].median())]
best_segments = segment.head(3)
best_channels = channel.head(3)
weak_keywords = keyword[(keyword["spend"] > keyword["spend"].median()) & (keyword["roas"] < keyword["roas"].median())].head(5)

report = []
report.append("# Campaign Insights Report\n")
report.append("## Executive Summary\n")
report.append(f"- Total spend: ₹{df['cost'].sum():,.0f}")
report.append(f"- Total revenue: ₹{df['revenue'].sum():,.0f}")
report.append(f"- Overall ROAS: {df['revenue'].sum()/df['cost'].sum():.2f}")
report.append(f"- Overall CPA: ₹{df['cost'].sum()/max(df['conversions'].sum(),1):,.0f}")
report.append(f"- Overall conversion rate: {df['conversions'].sum()/df['clicks'].sum():.2%}\n")

report.append("## Best Audience Segments by ROAS\n")
for _, r in best_segments.iterrows():
    report.append(f"- {r['audience_segment']}: ROAS {r['roas']:.2f}, CPA ₹{r['cpa']:.0f}, Avg quality {r['avg_quality_score']:.1f}")

report.append("\n## Best Channels by ROAS\n")
for _, r in best_channels.iterrows():
    report.append(f"- {r['channel']}: ROAS {r['roas']:.2f}, CPA ₹{r['cpa']:.0f}")

report.append("\n## High Spend / Low ROAS Campaigns to Optimize\n")
if high_spend_low_roas.empty:
    report.append("- No major high-spend low-ROAS campaigns found.")
else:
    for _, r in high_spend_low_roas.iterrows():
        report.append(f"- {r['campaign']}: Spend ₹{r['spend']:.0f}, ROAS {r['roas']:.2f}, CPA ₹{r['cpa']:.0f}")

report.append("\n## Keywords to Review\n")
for _, r in weak_keywords.iterrows():
    report.append(f"- {r['keyword']}: Spend ₹{r['spend']:.0f}, ROAS {r['roas']:.2f}, CPA ₹{r['cpa']:.0f}")

report.append("\n## Recommendations\n")
report.append("- Shift budget from high-spend/low-ROAS campaigns to high-ROAS audience segments.")
report.append("- Review landing page journey for keywords with good CTR but weak conversion.")
report.append("- Increase bids selectively for high-intent keywords with strong conversion probability.")
report.append("- Reduce spend on channels with high CPA and low customer quality score.")
report.append("- Use GenAI assistant to generate weekly campaign optimization summaries.")

Path("reports/campaign_insights_report.txt").write_text("\n".join(report))
print("Created reports and campaign_insights_report.txt")
