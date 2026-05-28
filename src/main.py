import os
import pandas as pd
import yfinance as yf
from datetime import datetime

os.makedirs("output", exist_ok=True)
os.makedirs("reports", exist_ok=True)


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

    if data:
        df = pd.DataFrame(data)
        df.to_csv("output/market_data.csv", index=False)
        print("✅ Market data updated")
        return df

    print("❌ No market data fetched")
    return pd.DataFrame()


def generate_news_stub():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    stories = [
        {
            "section": "Executive Signal",
            "title": "AION Command is now active",
            "summary": "The intelligence surface is now connected to the pipeline and will generate a fresh command page whenever the system is run."
        },
        {
            "section": "Markets",
            "title": "Market layer refreshed",
            "summary": "The AION ticker is now powered through Yahoo Finance and written into the live data layer."
        },
        {
            "section": "Next Build",
            "title": "GPT synthesis layer pending full activation",
            "summary": "The next build stage will connect RSS ingestion and GPT-generated strategic interpretation into this page."
        }
    ]

    df = pd.DataFrame(stories)
    df.to_csv("output/latest.csv", index=False)

    with open("output/latest.md", "w", encoding="utf-8") as f:
        f.write(f"# AION Intelligence\n\nLast updated: {now}\n\n")
        for story in stories:
            f.write(f"## {story['section']}\n")
            f.write(f"### {story['title']}\n")
            f.write(f"{story['summary']}\n\n")

    print("✅ News output updated")
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

    news_cards = ""

    for _, row in news_df.iterrows():
        news_cards += f"""
        <div class="card">
            <div class="section-label">{row['section']}</div>
            <h2>{row['title']}</h2>
            <p>{row['summary']}</p>
        </div>
        """

    html = f"""<!DOCTYPE html>
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
    grid-template-columns: 1.2fr 0.8fr;
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
    margin-bottom: 10px;
}}

h2 {{
    margin: 0 0 12px;
    font-size: 24px;
}}

p {{
    color: #cbd5e1;
    font-size: 16px;
    line-height: 1.75;
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

            <div class="card">
                <div class="section-label">Strategic Watch</div>
                <h2>Next 24 Hours</h2>
                <p>
                    Monitor market direction, energy prices, currency movement, India policy signals,
                    geopolitical stress points, and corporate reputation triggers. The next upgrade will
                    replace this system-generated note with full GPT-led synthesis from live news feeds.
                </p>
            </div>
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
                <h2>Pipeline Active</h2>
                <p>
                    AION Command is now generated by the local pipeline. Each run of
                    <strong>python src/main.py</strong> refreshes market data and rebuilds this page.
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
        f.write(html)

    print("✅ AION Command page generated")


if __name__ == "__main__":
    print("🔄 Running AION pipeline...")

    market_df = fetch_market_data()
    news_df = generate_news_stub()
    generate_command_page(market_df, news_df)

    print("✅ Pipeline complete")