import os
from pathlib import Path
from google import genai


def answer_campaign_question(question: str) -> str:
    """
    Answers business questions using the campaign insights report as context.
    This is a Gemini-powered grounded Q&A layer.
    """

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return (
            "GOOGLE_API_KEY is not set. Please add your Gemini API key as an "
            "environment variable locally or in Streamlit secrets after deployment."
        )

    report_path = Path("reports/campaign_insights_report.txt")

    if not report_path.exists():
        return (
            "Campaign insights report not found. Please run "
            "`python notebooks/02_campaign_eda_kpis.py` first."
        )

    report_text = report_path.read_text()

    prompt = f"""
You are a marketing analytics and customer acquisition assistant.

Use only the campaign insights report below to answer the user's question.
Do not make up numbers that are not present in the report.
Give concise, business-friendly answers with clear recommendations.

Campaign Insights Report:
{report_text}

User Question:
{question}

Answer:
"""

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text