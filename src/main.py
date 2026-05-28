import os
import re
import html
import pandas as pd
import yfinance as yf
import feedparser
import yaml
from datetime import datetime
from dateutil import parser

os.makedirs("output", exist_ok=True)
os.makedirs("reports", exist_ok=True)


def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"<.*?>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_market_data():
    symbols = {
        "NIFTY 50": "^NSEI",
        "SENSEX": "^BSESN",
        "NASDAQ": "^IXIC",
        "S&P 500": "^GSPC",
        "BRENT": "BZ=F",
        "GOLD": "GC=F",
        "USD/INR": "INR=X",
        "INDIA VIX": "^INDIAVIX",
        "DOLLAR INDEX": "DX-Y.NYB"
    }

    data = []

    for name, ticker in symbols.items():
        try:
            asset = yf.Ticker(ticker)
            hist = asset.history(period="5d")

            if len(hist) < 2:
                print(f"⚠️ Not enough data for {name}")
                continue

            latest = hist["Close"].iloc[-1]
            previous = hist["Close"].iloc[-2]
            change = (latest - previous) / previous

            data.append({
                "asset": name,
                "price": round(float(latest), 2),
                "change": round(float(change), 4)
            })

        except Exception as e:
            print(f"❌ Error fetching {name}: {e}")

    df = pd.DataFrame(data)

    if not df.empty:
        df.to_csv("output/market_data.csv", index=False)
        print("✅ Market data updated")
    else:
        print("❌ No market data fetched")

    return df


def classify_story(text):
    text = text.lower()

    if any(word in text for word in [
        "oil", "gas", "power", "energy", "renewable", "solar",
        "grid", "electricity", "battery", "transmission", "coal"
    ]):
        return "Energy & Infrastructure"

    if any(word in text for word in [
        "rbi", "inflation", "gdp", "rupee", "bond", "markets",
        "stocks", "fii", "capital", "ipo", "sensex", "nifty"
    ]):
        return "Markets & Macro"

    if any(word in text for word in [
        "china", "us", "america", "iran", "israel", "russia",
        "ukraine", "war", "tariff", "geopolitical", "trade"
    ]):
        return "Geopolitics"

    if any(word in text for word in [
        "policy", "government", "ministry", "sebi", "regulator",
        "cabinet", "supreme court", "rbi", "budget"
    ]):
        return "Policy & Regulation"

    if any(word in text for word in [
        "company", "ceo", "earnings", "profit", "revenue",
        "merger", "acquisition", "investment", "funding"
    ]):
        return "Corporate Signals"

    return "Strategic Signals"


def fetch_news_feeds():
    with open("config/feeds.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    stories = []
    seen_links = set()

    for feed in config.get("feeds", []):
        name = feed.get("name")
        url = feed.get("url")

        try:
            parsed = feedparser.parse(url)

            for entry in parsed.entries[:8]:
                title = clean_text(entry.get("title", ""))
                link = entry.get("link", "").strip()
                summary = clean_text(entry.get("summary", ""))[:300]
                published_raw = entry.get("published") or entry.get("updated") or ""

                if not title or not link or link in seen_links:
                    continue

                try:
                    published_at = parser.parse(published_raw).strftime("%d %b %Y, %H:%M") if published_raw else ""
                except Exception:
                    published_at = ""

                section = classify_story(title + " " + summary)

                stories.append({
                    "section": section,
                    "source": name,
                    "title": title,
                    "summary": summary if summary else "Summary unavailable from source feed.",
                    "link": link,
                    "published_at": published_at
                })

                seen_links.add(link)

        except Exception as e:
            print(f"❌ Feed error: {name} — {e}")

    df = pd.DataFrame(stories)

    if not df.empty:
        df.to_csv("output/latest.csv", index=False)

        with open("output/latest.md", "w", encoding="utf-8") as f:
            f.write(f"# AION Intelligence\n\n")
            f.write(f"Last updated: {datetime.now().strftime('%d %B %Y, %I:%M %p IST')}\n\n")

            for section in df["section"].drop_duplicates():
                f.write(f"## {section}\n\n")
                section_df = df[df["section"] == section].head(8)

                for _, row in section_df.iterrows():
                    f.write(f"### {row['title']}\n")
                    f.write(f"Source: {row['source']} | {row['published_at']}\n\n")
                    f.write(f"{row['summary']}\n\n")
                    f.write(f"{row['link']}\n\n")

        print(f"✅ News feeds updated: {len(stories)} stories")
    else:
        print("❌ No news stories fetched")

    return df


def generate_command_page(market_df, news_df):
    now = datetime.now().strftime("%d %B %Y, %I:%M %p IST")

    ticker_spans = ""
    market_rows = ""

    if not market_df.empty:
        for _, row in market_df.iterrows():
            change = float(row["change"]) * 100
            direction = "up" if change >= 0 else "down"
            arrow = "▲" if change >= 0 else "▼"

            ticker_spans += f"""
            <span class="{direction}">
                {row['asset']} {row['price']:,} {arrow} {abs(change):.2f}%
            </span>
            """

            market_rows += f"""
            <tr>
                <td>{row['asset']}</td>
                <td>{row['price']:,}</td>
                <td class="{direction}">{arrow} {abs(change):.2f}%</td>
            </tr>
            """
    else:
        ticker_spans = "<span>Market Data Temporarily Unavailable</span>"
        market_rows = "<tr><td colspan='3'>Market data unavailable</td></tr>"

    sections = [
        "Markets & Macro",
        "Energy & Infrastructure",
        "Geopolitics",
        "Policy & Regulation",
        "Corporate Signals",
        "Strategic Signals"
    ]

    news_cards = ""

    if not news_df.empty:
        for section in sections:
            section_df = news_df[news_df["section"] == section].head(5)

            if section_df.empty:
                continue

            news_cards += f"""
            <div class="card">
                <div class="section-label">{section}</div>
            """

            for _, row in section_df.iterrows():
                news_cards += f"""
                <div class="story">
                    <h3><a href="{row['link']}" target="_blank">{row['title']}</a></h3>
                    <div class="meta">{row['source']} {row['published_at']}</div>
                    <p>{row['summary']}</p>
                </div>
                """

            news_cards += "</div>"
    else:
        news_cards = """
        <div class="card">
            <div class="section-label">System Note</div>
            <h2>No live news available</h2>
            <p>The feed layer did not return stories in this run.</p>
        </div>
        """

    html_page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AION Command</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/png" href="../AION%20Logo.png">

<style>
body {{
    margin: 0;
    background: #020617;
    color: #f8fafc;
    font-family: Arial, Helvetica, sans-serif;
}}

.ticker {{
    height: 42px;
    background: #0f172a;
    border-bottom: 1px solid #1e293b;
    overflow: hidden;
    display: flex;
    align-items: center;
    white-space: nowrap;
}}

.ticker-track {{
    display: inline-block;
    padding-left: 100%;
    animation: tickerScroll 38s linear infinite;
}}

.ticker span {{
    display: inline-block;
    margin-right: 60px;
    font-size: 13px;
    font-weight: 600;
}}

.up {{ color: #22c55e; }}
.down {{ color: #ef4444; }}

@keyframes tickerScroll {{
    0% {{ transform: translateX(0%); }}
    100% {{ transform: translateX(-100%); }}
}}

.wrap {{
    max-width: 1180px;
    margin: auto;
    padding: 64px 28px;
}}

.topline {{
    color: #ff6a00;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 13px;
    font-weight: 700;
}}

h1 {{
    font-size: 48px;
    margin: 14px 0 8px;
}}

.date {{
    color: #94a3b8;
    font-size: 15px;
}}

.grid {{
    display: grid;
    grid-template-columns: 1.25fr 0.75fr;
    gap: 26px;
    margin-top: 42px;
}}

.card {{
    background: rgba(15, 23, 42, 0.72);
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 24px;
}}

.section-label {{
    color: #ff6a00;
    font-size: 12px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 700;
    margin-bottom: 18px;
}}

.story {{
    padding-bottom: 18px;
    margin-bottom: 18px;
    border-bottom: 1px solid #1e293b;
}}

.story:last-child {{
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
}}

h2 {{
    margin: 0 0 12px;
    font-size: 24px;
}}

h3 {{
    margin: 0 0 8px;
    font-size: 18px;
    line-height: 1.45;
}}

a {{
    color: #f8fafc;
    text-decoration: none;
}}

a:hover {{
    color: #ff6a00;
}}

.meta {{
    color: #94a3b8;
    font-size: 13px;
    margin-bottom: 8px;
}}

p {{
    color: #cbd5e1;
    font-size: 15.5px;
    line-height: 1.7;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
}}

td, th {{
    border-bottom: 1px solid #1e293b;
    padding: 12px 6px;
    text-align: left;
    font-size: 14px;
}}

th {{
    color: #94a3b8;
    font-weight: 600;
}}

.back {{
    display: inline-block;
    margin-top: 30px;
    color: #ff6a00;
    text-decoration: none;
}}

@media(max-width: 850px) {{
    .grid {{
        grid-template-columns: 1fr;
    }}

    h1 {{
        font-size: 36px;
    }}
}}
</style>
</head>

<body>

<div class="ticker">
    <div class="ticker-track">
        {ticker_spans}
    </div>
</div>

<div class="wrap">
    <div class="topline">AION Command</div>
    <h1>Executive Intelligence Brief</h1>
    <div class="date">Generated: {now}</div>

    <div class="grid">
        <div>
            {news_cards}
        </div>

        <div>
            <div class="card">
                <div class="section-label">Market Dashboard</div>
                <h2>Live Ticker Snapshot</h2>
                <table>
                    <tr>
                        <th>Asset</th>
                        <th>Price</th>
                        <th>Move</th>
                    </tr>
                    {market_rows}
                </table>
            </div>

            <div class="card">
                <div class="section-label">System Status</div>
                <h2>Content Automation Active</h2>
                <p>
                    AION Command is now pulling live RSS feeds, classifying stories into strategic sections,
                    refreshing market data, and generating this page from the pipeline.
                </p>
            </div>

            <div class="card">
                <div class="section-label">Next Upgrade</div>
                <h2>GPT Synthesis Layer</h2>
                <p>
                    The next phase will convert this live news layer into a boardroom-grade intelligence brief
                    with implications, watch-outs, and strategic interpretation.
                </p>
            </div>
        </div>
    </div>

    <a class="back" href="../index.html">← Back to AION Intelligence</a>
</div>

</body>
</html>
"""

    with open("reports/latest.html", "w", encoding="utf-8") as f:
        f.write(html_page)

    print("✅ AION Command page generated")


if __name__ == "__main__":
    print("🔄 Running AION pipeline...")

    market_df = fetch_market_data()
    news_df = fetch_news_feeds()
    generate_command_page(market_df, news_df)

    print("✅ Pipeline complete")