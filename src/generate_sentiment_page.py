import sys
from pathlib import Path
from collections import Counter
from sentiment_engine import generate_sentiment_report
from sentiment_gpt import generate_gpt_sentiment_judgement

query = " ".join(sys.argv[1:]).strip()

if not query:
    print("Please enter a query.")
    sys.exit(1)

r = generate_sentiment_report(query)

all_text = " ".join(
    (s.get("title", "") + " " + s.get("summary", ""))
    for s in r.get("stories", [])
).lower()

theme_map = {
    "AI infrastructure": ["data centre", "data center", "gpu", "chip", "compute", "server"],
    "Climate and water stress": ["water", "climate", "energy", "electricity", "heat", "emissions"],
    "Regulation and governance": ["regulation", "law", "government", "policy", "privacy", "safety"],
    "Jobs and labour displacement": ["jobs", "workers", "employment", "layoff", "automation"],
    "Investment and markets": ["investment", "stock", "market", "funding", "valuation", "capital"],
    "Security and surveillance": ["surveillance", "security", "cyber", "military", "threat"],
    "Healthcare and science": ["health", "vaccine", "medicine", "research", "science"],
}

themes = []
for theme, words in theme_map.items():
    count = sum(all_text.count(w) for w in words)
    if count:
        themes.append((theme, count))

themes = sorted(themes, key=lambda x: x[1], reverse=True)[:5]

if not themes:
    themes = [("General AI adoption", 1), ("Enterprise productivity", 1), ("Public trust", 1)]

geo_map = {
    "United States": ["us ", "u.s.", "america", "american", "trump", "washington"],
    "India": ["india", "indian", "delhi", "bengaluru", "mumbai"],
    "China": ["china", "chinese", "beijing"],
    "Europe": ["europe", "eu ", "european", "brussels"],
    "United Kingdom": ["uk ", "britain", "london", "bbc"],
    "Middle East": ["uae", "saudi", "middle east", "dubai"],
}

geos = []
for geo, words in geo_map.items():
    count = sum(all_text.count(w) for w in words)
    if count:
        geos.append((geo, count))

geos = sorted(geos, key=lambda x: x[1], reverse=True)[:4]

if not geos:
    geos = [("Global / diffuse", 1)]

score = r["score"]

if score >= 50:
    heat = "FAVOURABLE"
    posture = "AMPLIFY"
    interpretation = "The topic is carrying favourable public momentum. The signal suggests that positive narratives currently outweigh reputational drag."
elif score >= 15:
    heat = "CONSTRUCTIVE"
    posture = "AMPLIFY WITH CAUTION"
    interpretation = "The topic is directionally positive, but not uncontested. The favourable signal should be used carefully because counter-narratives may still emerge."
elif score <= -50:
    heat = "ADVERSE"
    posture = "ESCALATE"
    interpretation = "The topic is under reputational stress. Negative narratives are materially shaping perception and may require active response."
elif score <= -15:
    heat = "ELEVATED"
    posture = "CORRECT / CONTAIN"
    interpretation = "The topic has visible pressure points. The narrative is not yet in crisis, but adverse interpretations require close monitoring."
else:
    heat = "WATCH"
    posture = "MONITOR"
    interpretation = "The topic is contested or directionally unclear. The public signal is mixed, and the next movement will depend on which themes gain velocity."

themes_html = ""
for t, c in themes:
    themes_html += f"<div class='pill'>{t}</div>"

geo_html = ""
for g, c in geos:
    geo_html += f"<div class='pill'>{g}</div>"

gpt = generate_gpt_sentiment_judgement(
    query=r["query"],
    stories=r.get("stories", []),
    score=r["score"],
    mood=r["mood"],
    themes=[t for t, c in themes],
    geos=[g for g, c in geos]
)

risk_html = "".join([f"<div class='pill'>{x}</div>" for x in gpt.get("risk_triggers", [])])
opp_html = "".join([f"<div class='pill'>{x}</div>" for x in gpt.get("opportunity_triggers", [])])
cluster_html = "".join([f"<div class='pill'>{x}</div>" for x in gpt.get("organic_conversation_clusters", [])])

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AION Sentiment Signal</title>
<style>
body {{
    margin: 0;
    background: #020617;
    color: #f8fafc;
    font-family: "Segoe UI", Arial, sans-serif;
}}
.container {{
    max-width: 1120px;
    margin: auto;
    padding: 72px 28px;
}}
a {{ color: #94a3b8; text-decoration: none; }}
h1 {{
    font-size: 44px;
    letter-spacing: 2px;
    margin-top: 42px;
}}
h2 {{
    color: #f8fafc;
    margin-top: 0;
}}
.orange {{ color: #ff6a00; }}
.query {{
    margin-top: 30px;
    color: #cbd5e1;
    font-size: 18px;
    letter-spacing: 1px;
}}
.signal {{
    margin-top: 50px;
    border: 1px solid #1e293b;
    background: radial-gradient(circle at top left, rgba(255,106,0,0.18), rgba(15,23,42,0.78));
    border-radius: 18px;
    padding: 42px;
}}
.state {{
    font-size: 13px;
    letter-spacing: 3px;
    color: #94a3b8;
    text-transform: uppercase;
}}
.score {{
    font-size: 72px;
    font-weight: 800;
    margin: 18px 0;
}}
.mood {{
    font-size: 28px;
    color: #ff6a00;
    font-weight: 700;
}}
.grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 18px;
    margin-top: 30px;
}}
.card {{
    background: rgba(15,23,42,0.72);
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 24px;
}}
.label {{
    color: #94a3b8;
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
}}
.value {{
    margin-top: 12px;
    font-size: 22px;
    font-weight: 700;
}}
.reading {{
    margin-top: 32px;
    background: rgba(15,23,42,0.72);
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 28px;
    color: #cbd5e1;
    line-height: 1.8;
    font-size: 17px;
}}
.pillbox {{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 18px;
}}
.pill {{
    border: 1px solid #334155;
    background: rgba(255,106,0,0.08);
    color: #f8fafc;
    border-radius: 999px;
    padding: 10px 15px;
    font-size: 14px;
}}
.small {{
    color: #94a3b8;
    font-size: 14px;
    line-height: 1.7;
}}
.footer {{
    margin-top: 35px;
    color: #64748b;
    font-size: 12px;
    letter-spacing: 1px;
}}
</style>
</head>

<body>
<div class="container">
    <a href="../sentiment.html">← Back to Sentiment Console</a>

    <h1>AION <span class="orange">SENTIMENT SIGNAL</span></h1>

    <div class="query">{r['query'].upper()}</div>

    <div class="signal">
        <div class="state">Signal Polarity</div>
        <div class="score">{r['score']}</div>
        <div class="mood">{r['mood']}</div>
    </div>

    <div class="grid">
        <div class="card">
            <div class="label">Narrative Pressure</div>
            <div class="value">{heat}</div>
        </div>
        <div class="card">
            <div class="label">Reputation Heat</div>
            <div class="value">{heat}</div>
        </div>
        <div class="card">
            <div class="label">Signal Quality</div>
            <div class="value">NEWS + X</div>
        </div>
        <div class="card">
            <div class="label">Posture</div>
            <div class="value">{posture}</div>
        </div>
    </div>

    <div class="grid">
        <div class="card">
            <h2>Key Organic Conversations</h2>
            <div class="pillbox">{cluster_html if cluster_html else themes_html}</div>
        </div>

        <div class="card">
            <h2>Geography Signal</h2>
            <div class="pillbox">{geo_html}</div>
        </div>
    </div>

    <div class="reading">
        <strong>What the Score Means</strong><br><br>
        The polarity score ranges from <strong>-100 to +100</strong>. A negative score indicates adverse narrative pressure; a positive score indicates favourable momentum; a score around zero means the topic is contested, diffuse or still forming.
        <br><br>
        <strong>Term Guide</strong><br>
        <strong>Narrative Pressure</strong> measures how forcefully the conversation is moving. <strong>Reputation Heat</strong> indicates whether the topic can affect perception. <strong>Signal Quality</strong> shows the current source base. <strong>Posture</strong> is the recommended communications stance.
    </div>

    <div class="reading">
        <strong>Strategic Reading</strong><br><br>
        {interpretation}
        <br><br>
        <strong>Prescriptive View:</strong> {r['action']}
    </div>

    <div class="footer">
        AION INTELLIGENCE · SIGNAL CONTEXT JUDGEMENT · GENERATED {r['generated_at']}
    </div>
</div>
</body>
</html>
"""

Path("reports").mkdir(exist_ok=True)
Path("reports/sentiment_report.html").write_text(html, encoding="utf-8")

print("✅ Sentiment signal upgraded: reports/sentiment_report.html")
