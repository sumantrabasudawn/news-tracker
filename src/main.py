import os
import re
import html
import pandas as pd
import yfinance as yf
import feedparser
import yaml

from datetime import datetime
from dateutil import parser

from intelligence_layer import (
    generate_intelligence_assessment,
    generate_watchlist,
    generate_macro_dashboard,
    generate_data_watch_grid
)

os.makedirs("output", exist_ok=True)
os.makedirs("reports", exist_ok=True)


# ---------------------------------------------------
# CLEAN TEXT
# ---------------------------------------------------
def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"<.*?>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ---------------------------------------------------
# MARKET DATA
# ---------------------------------------------------
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

    return df


# ---------------------------------------------------
# STORY CLASSIFICATION
# ---------------------------------------------------
def classify_story(text):

    text = text.lower()

    if any(word in text for word in [
        "oil", "gas", "power", "energy", "renewable",
        "solar", "grid", "battery", "coal", "electricity"
    ]):
        return "Energy & Infrastructure"

    if any(word in text for word in [
        "rbi", "inflation", "gdp", "markets",
        "stocks", "ipo", "fii", "capital"
    ]):
        return "Markets & Macro"

    if any(word in text for word in [
        "iran", "israel", "china", "russia",
        "ukraine", "war", "tariff", "trade"
    ]):
        return "Geopolitics"

    if any(word in text for word in [
        "policy", "government", "ministry",
        "sebi", "regulator", "budget"
    ]):
        return "Policy & Regulation"

    return "Strategic Signals"


# ---------------------------------------------------
# RSS FEEDS
# ---------------------------------------------------
def fetch_news_feeds():

    with open("config/feeds.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    stories = []
    seen = set()

    for feed in config.get("feeds", []):

        name = feed.get("name")
        url = feed.get("url")

        try:
            parsed = feedparser.parse(url)

            for entry in parsed.entries[:8]:

                title = clean_text(entry.get("title", ""))
                link = entry.get("link", "").strip()

                if not title or not link or link in seen:
                    continue

                summary = clean_text(entry.get("summary", ""))[:300]

                published_raw = (
                    entry.get("published")
                    or entry.get("updated")
                    or ""
                )

                try:
                    published_at = parser.parse(
                        published_raw
                    ).strftime("%d %b %Y, %H:%M")

                except Exception:
                    published_at = ""

                stories.append({
                    "section": classify_story(title + " " + summary),
                    "source": name,
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "published_at": published_at
                })

                seen.add(link)

        except Exception as e:
            print(f"❌ Feed error: {name} — {e}")

    df = pd.DataFrame(stories)

    if not df.empty:

        df.to_csv("output/latest.csv", index=False)

        with open("output/latest.md", "w", encoding="utf-8") as f:

            f.write("# AION Intelligence\n\n")

            for _, row in df.iterrows():

                f.write(f"## {row['title']}\n")
                f.write(f"{row['summary']}\n\n")

        print(f"✅ News feeds updated: {len(df)} stories")

    return df


# ---------------------------------------------------
# COMMAND PAGE
# ---------------------------------------------------
def generate_command_page(
    market_df,
    news_df,
    intelligence_text,
    watchlist,
    macro_dashboard,
    watch_grid
):

    now = datetime.now().strftime("%d %B %Y, %I:%M %p IST")

    # ---------------- TICKER ----------------

    ticker_html = ""

    for _, row in market_df.iterrows():

        change = float(row["change"]) * 100

        arrow = "▲" if change >= 0 else "▼"

        direction = "up" if change >= 0 else "down"

        ticker_html += f"""
        <span class="{direction}">
            {row['asset']} {row['price']:,} {arrow} {abs(change):.2f}%
        </span>
        """

    # ---------------- MARKET TABLE ----------------

    market_rows = ""

    for _, row in market_df.iterrows():

        change = float(row["change"]) * 100

        arrow = "▲" if change >= 0 else "▼"

        direction = "up" if change >= 0 else "down"

        market_rows += f"""
        <tr>
            <td>{row['asset']}</td>
            <td>{row['price']}</td>
            <td class="{direction}">
                {arrow} {abs(change):.2f}%
            </td>
        </tr>
        """

    # ---------------- WATCHLIST ----------------

    watchlist_html = ""

    for item in watchlist:

        watchlist_html += f"<li>{item}</li>"

    # ---------------- MACRO DASHBOARD ----------------

    macro_rows = ""

    for item in macro_dashboard:

        macro_rows += f"""
        <tr>
            <td>{item['indicator']}</td>
            <td>{item['latest']}</td>
            <td>{item['signal']}</td>
        </tr>
        """

    # ---------------- WATCH GRID ----------------

    watch_grid_rows = ""

    for item in watch_grid:

        watch_grid_rows += f"""
        <tr>
            <td>{item['event']}</td>
            <td>{item['importance']}</td>
            <td>{item['why']}</td>
        </tr>
        """

    # ---------------- NEWS FLOW ----------------

    news_cards = ""

    grouped = news_df.groupby("section")

    for section, section_df in grouped:

        news_cards += f"""
        <div class="card">
        <div class="section-label">{section}</div>
        """

        for _, row in section_df.head(5).iterrows():

            news_cards += f"""
            <div class="story">
                <h3>
                    <a href="{row['link']}" target="_blank">
                        {row['title']}
                    </a>
                </h3>

                <div class="meta">
                    {row['source']} | {row['published_at']}
                </div>

                <p>{row['summary']}</p>
            </div>
            """

        news_cards += "</div>"

    # ---------------- HTML ----------------

    html_page = f"""
<!DOCTYPE html>
<html>

<head>

<meta charset="UTF-8">

<title>AION Command</title>

<style>

body {{
    margin: 0;
    background: #020617;
    color: #f8fafc;
    font-family: Arial, Helvetica, sans-serif;
}}

.ticker {{
    background: #0f172a;
    padding: 12px;
    overflow: hidden;
    white-space: nowrap;
}}

.ticker span {{
    margin-right: 50px;
    font-size: 13px;
    font-weight: 600;
}}

.up {{
    color: #22c55e;
}}

.down {{
    color: #ef4444;
}}

.wrap {{
    max-width: 1280px;
    margin: auto;
    padding: 50px 30px;
}}

.topline {{
    color: #ff6a00;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 700;
}}

h1 {{
    font-size: 46px;
}}

.grid {{
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 24px;
}}

.card {{
    background: rgba(15,23,42,0.75);
    border: 1px solid #1e293b;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
}}

.section-label {{
    color: #ff6a00;
    text-transform: uppercase;
    font-size: 12px;
    font-weight: 700;
    margin-bottom: 14px;
}}

.story {{
    margin-bottom: 24px;
    padding-bottom: 24px;
    border-bottom: 1px solid #1e293b;
}}

.story:last-child {{
    border-bottom: none;
}}

.story h3 {{
    margin: 0 0 8px;
}}

.story a {{
    color: white;
    text-decoration: none;
}}

.story a:hover {{
    color: #ff6a00;
}}

.meta {{
    color: #94a3b8;
    font-size: 13px;
    margin-bottom: 8px;
}}

p {{
    color: #cbd5e1;
    line-height: 1.75;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

td, th {{
    border-bottom: 1px solid #1e293b;
    padding: 10px 6px;
    text-align: left;
}}

ul {{
    padding-left: 18px;
}}

li {{
    margin-bottom: 10px;
    color: #cbd5e1;
}}

</style>

</head>

<body>

<div class="ticker">
{ticker_html}
</div>

<div class="wrap">

<div class="topline">
AION Command
</div>

<h1>
Executive Intelligence Brief
</h1>

<p>
Generated: {now}
</p>

<div class="grid">

<div>

<div class="card">

<div class="section-label">
AION Intelligence Assessment
</div>

<p>
{intelligence_text}
</p>

</div>

{news_cards}

</div>

<div>

<div class="card">

<div class="section-label">
What To Watch Over Next Few Hours
</div>

<ul>
{watchlist_html}
</ul>

</div>

<div class="card">

<div class="section-label">
Market Dashboard
</div>

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

<div class="section-label">
Macro Dashboard
</div>

<table>

<tr>
<th>Indicator</th>
<th>Latest</th>
<th>Signal</th>
</tr>

{macro_rows}

</table>

</div>

<div class="card">

<div class="section-label">
Data To Watch
</div>

<table>

<tr>
<th>Event</th>
<th>Importance</th>
<th>Why It Matters</th>
</tr>

{watch_grid_rows}

</table>

</div>

</div>

</div>

</div>

</body>

</html>
"""

    with open("reports/latest.html", "w", encoding="utf-8") as f:
        f.write(html_page)

    print("✅ AION Command page generated")


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
if __name__ == "__main__":

    print("🔄 Running AION pipeline...")

    market_df = fetch_market_data()

    news_df = fetch_news_feeds()

    intelligence_text = generate_intelligence_assessment(
        news_df,
        market_df
    )

    watchlist = generate_watchlist(
        news_df,
        market_df
    )

    macro_dashboard = generate_macro_dashboard()

    watch_grid = generate_data_watch_grid()

    generate_command_page(
        market_df,
        news_df,
        intelligence_text,
        watchlist,
        macro_dashboard,
        watch_grid
    )

    print("✅ Pipeline complete")