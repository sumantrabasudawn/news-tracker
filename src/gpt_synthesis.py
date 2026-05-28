import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def synthesize_aion_brief(events_list):
    if not events_list:
        return None

    system_instruction = """
You are AION Intelligence.

You convert raw news and market signals into institutional-grade strategic intelligence.

Do not merely summarise. Interpret.

Write in a sober, boardroom-grade tone. Avoid hype, filler, and generic AI language.

Output sections:
1. Executive Signal
2. Strategic Interpretation
3. India Relevance
4. Energy and Infrastructure Implications
5. Market and Policy Implications
6. Watch Points for the Next 24 Hours
"""

    user_input = f"""
Analyse these ingested AION signals:

{json.dumps(events_list, indent=2)}
"""

    response = client.responses.create(
        model="gpt-5.5",
        input=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        reasoning={"effort": "medium"}
    )

    return response.output_text