import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_gpt_sentiment_judgement(query, stories, score, mood, themes, geos):
    raw_signals = []

    for s in stories[:40]:
        raw_signals.append({
            "source_type": s.get("source", "Google News"),
            "headline_or_post": s.get("title", ""),
            "text": s.get("summary", ""),
            "published_at": s.get("published_at", ""),
            "rule_sentiment": s.get("sentiment", ""),
            "engagement": s.get("engagement", 0)
        })

    system_instruction = """
You are AION Intelligence, a strategic narrative-intelligence system.

You are given parsed public signals from Google News and X. Your role is not to summarise them. Your role is to infer the live reputation terrain.

You must synthesize:
1. What is the real sentiment underneath the surface data?
2. What are the dominant organic conversations?
3. What are news institutions amplifying?
4. What is X revealing that news does not?
5. What perception is forming?
6. What is likely to intensify next?
7. What should a senior communications or strategy leader do?

Write like an institutional intelligence analyst advising a CEO.

Avoid generic phrases such as:
- "It is important to note"
- "The conversation is multifaceted"
- "Stakeholders should monitor"
- "In conclusion"

Be direct, specific and judgment-led.

Return valid JSON only with these exact keys:
{
  "aion_intelligence_assessment": "A 180-220 word boardroom-grade intelligence assessment.",
  "sentiment_synthesis": "What the sentiment actually means beyond the numeric score.",
  "news_signal": "What Google News / mainstream media is indicating.",
  "x_signal": "What X/social conversation is indicating.",
  "organic_conversation_clusters": ["cluster 1", "cluster 2", "cluster 3", "cluster 4", "cluster 5"],
  "perception_formation": "What perception is forming in the public/institutional mind.",
  "forward_risk": "What could turn this conversation adverse over the next 7-30 days.",
  "forward_opportunity": "What could strengthen favourable perception over the next 7-30 days.",
  "recommended_posture": "A clear prescriptive communications stance.",
  "risk_triggers": ["...", "...", "..."],
  "opportunity_triggers": ["...", "...", "..."],
  "narrative_state": "One phrase only"
}
"""

    user_payload = {
        "query": query,
        "rule_based_score": score,
        "rule_based_mood": mood,
        "detected_keyword_themes": themes,
        "detected_geographies": geos,
        "raw_news_and_x_signals": raw_signals
    }

    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": json.dumps(user_payload, indent=2)}
        ]
    )

    text = response.output_text.strip()

    try:
        return json.loads(text)
    except Exception:
        return {
            "aion_intelligence_assessment": text,
            "sentiment_synthesis": "",
            "news_signal": "",
            "x_signal": "",
            "organic_conversation_clusters": [],
            "perception_formation": "",
            "forward_risk": "",
            "forward_opportunity": "",
            "recommended_posture": "",
            "risk_triggers": [],
            "opportunity_triggers": [],
            "narrative_state": "Interpreted"
        }
