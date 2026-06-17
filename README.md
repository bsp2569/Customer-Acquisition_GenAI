
# Customer Acquisition, Marketing ROI & GenAI Insights Platform

## Problem Statement
Marketing and acquisition teams need to improve campaign efficiency by identifying high-performing campaigns, reducing wasted spend, improving customer quality, and generating faster insights from campaign data.

## Business Metrics
- CTR
- CPC
- CPA
- ROAS
- Conversion Rate
- Customer Acquisition Cost
- Funnel Drop-off
- Customer Quality Score

## Tools Used
Python, SQL, Pandas, Scikit-learn, Random Forest, K-Means, Streamlit/Power BI, LangChain, FAISS, Gemini/OpenAI APIs

## Project Workflow
1. Generate simulated paid search and digital acquisition data
2. Calculate KPIs and business metrics
3. Analyze campaign, keyword, channel, device, and audience performance
4. Perform funnel analysis
5. Segment campaigns/audiences using K-Means
6. Predict conversion probability using Random Forest
7. Build Streamlit dashboard
8. Add GenAI/RAG assistant for campaign insights

## How to Run

```bash
pip install -r requirements.txt
python notebooks/01_data_generation.py
python notebooks/02_campaign_eda_kpis.py
python notebooks/03_ml_segmentation_prediction.py
streamlit run app/streamlit_app.py
```

## Resume Bullets

- Built a SQL, Python, dashboarding, and GenAI-based analytics platform to evaluate campaign performance, acquisition efficiency, and customer quality.
- Engineered KPIs including CTR, CPC, CPA, ROAS, conversion rate, funnel drop-off, and customer acquisition cost across campaign, keyword, channel, device, and audience segments.
- Applied K-Means clustering and Random Forest models to segment campaigns and predict conversion probability.
- Designed measurement workflows to compare campaign performance and guide budget reallocation.
- Added a GenAI assistant design using LangChain, FAISS, and Gemini/OpenAI APIs to generate source-backed campaign insights and recommendations.
