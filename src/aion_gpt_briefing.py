import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_aion_briefing(stories):
    news_text = "\n".join([
        f"""
Title: {s.get('title', '')}
Source: {s.get('source', '')}
Published: {s.get('published_at', '')}
Summary: {s.get('summary', '')}
Link: {s.get('link', '')}
"""
        for s in stories[:80]
    ])

    prompt = f"""
You are AION Intelligence, an institutional-grade strategic intelligence system.

Your task is to convert today's raw news flow into a boardroom-ready intelligence briefing.

The report must be analytical, not descriptive.

Structure the briefing as follows:

# AION Intelligence Briefing

## 1. Executive Intelligence Summary
Write 5-7 sharp paragraphs explaining the dominant global and India-relevant signals of the day.

## 2. News Flow Quantitative Snapshot
Analyse the news flow quantitatively:
- total stories analysed
- dominant sectors/themes
- most repeated risks
- source concentration
- India relevance
- global macro relevance

## 3. Top 10 Strategic Signals
Rank the 10 most important developments.
For each:
- what happened
- why it matters
- likely second-order implication
- relevance for business, policy, capital markets or energy systems

## 4. Energy, Infrastructure and Markets Analysis
Focus deeply on:
- energy transition
- power markets
- oil/gas
- renewables
- transmission/grid
- infrastructure
- inflation and capital markets linkages

## 5. India Implications
Explain what the news flow means for India’s economy, energy security, industry, capital expenditure cycle, corporates and policy makers.

## 6. Risk Register
Create a table with:
Risk | Probability | Impact | Why it matters | Watch indicator

## 7. Opportunity Register
Create a table with:
Opportunity | Sector | Time horizon | Why it matters | Potential beneficiaries

## 8. Watch Points for the Next 24-72 Hours
Give specific things to monitor.

## 9. AION Judgement
End with a clear institutional judgement in 3-4 paragraphs.

Tone:
- Financial Times meets investment-bank morning note
- crisp, analytical, senior, institutional
- avoid generic commentary
- do not merely summarise headlines
- extract patterns, signals and implications

Raw news flow:
{news_text}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
        max_output_tokens=5000
    )

    return response.output_text