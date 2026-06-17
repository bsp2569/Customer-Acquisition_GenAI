
-- Customer Acquisition, Marketing ROI & GenAI Insights Platform
-- Campaign KPI SQL examples

-- 1. Campaign level KPIs
SELECT
    campaign,
    SUM(impressions) AS impressions,
    SUM(clicks) AS clicks,
    SUM(cost) AS spend,
    SUM(conversions) AS conversions,
    SUM(revenue) AS revenue,
    SUM(clicks) * 1.0 / NULLIF(SUM(impressions), 0) AS ctr,
    SUM(cost) * 1.0 / NULLIF(SUM(clicks), 0) AS cpc,
    SUM(cost) * 1.0 / NULLIF(SUM(conversions), 0) AS cpa,
    SUM(revenue) * 1.0 / NULLIF(SUM(cost), 0) AS roas,
    SUM(conversions) * 1.0 / NULLIF(SUM(clicks), 0) AS conversion_rate
FROM simulated_campaign_data
GROUP BY campaign
ORDER BY roas DESC;

-- 2. High spend, low ROAS campaigns
WITH campaign_kpis AS (
    SELECT
        campaign,
        SUM(cost) AS spend,
        SUM(revenue) * 1.0 / NULLIF(SUM(cost), 0) AS roas,
        SUM(cost) * 1.0 / NULLIF(SUM(conversions), 0) AS cpa
    FROM simulated_campaign_data
    GROUP BY campaign
)
SELECT *
FROM campaign_kpis
WHERE spend > (SELECT AVG(spend) FROM campaign_kpis)
  AND roas < (SELECT AVG(roas) FROM campaign_kpis)
ORDER BY spend DESC;

-- 3. Audience segment quality
SELECT
    audience_segment,
    SUM(cost) AS spend,
    SUM(conversions) AS conversions,
    SUM(revenue) * 1.0 / NULLIF(SUM(cost), 0) AS roas,
    SUM(cost) * 1.0 / NULLIF(SUM(conversions), 0) AS cpa,
    AVG(customer_quality_score) AS avg_customer_quality_score
FROM simulated_campaign_data
GROUP BY audience_segment
ORDER BY roas DESC;

-- 4. Funnel analysis
SELECT
    campaign,
    SUM(impressions) AS impressions,
    SUM(clicks) AS clicks,
    SUM(landing_page_visits) AS visits,
    SUM(application_starts) AS application_starts,
    SUM(conversions) AS conversions,
    SUM(clicks) * 1.0 / NULLIF(SUM(impressions), 0) AS impression_to_click_rate,
    SUM(landing_page_visits) * 1.0 / NULLIF(SUM(clicks), 0) AS click_to_visit_rate,
    SUM(application_starts) * 1.0 / NULLIF(SUM(landing_page_visits), 0) AS visit_to_application_rate,
    SUM(conversions) * 1.0 / NULLIF(SUM(application_starts), 0) AS application_to_conversion_rate
FROM simulated_campaign_data
GROUP BY campaign;
