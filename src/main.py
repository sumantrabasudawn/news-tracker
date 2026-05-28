import os
import pandas as pd
import yfinance as yf
from datetime import datetime

# -----------------------------------
# Ensure output directory exists
# -----------------------------------
os.makedirs("output", exist_ok=True)


# -----------------------------------
# MARKET DATA (Yahoo Finance)
# -----------------------------------
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
    else:
        print("❌ No market data fetched")


# -----------------------------------
# NEWS PLACEHOLDER
# -----------------------------------
def generate_news_stub():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df = pd.DataFrame([{
        "title": "AION Intelligence",
        "timestamp": now,
        "summary": "Pipeline running successfully"
    }])

    df.to_csv("output/latest.csv", index=False)

    with open("output/latest.md", "w", encoding="utf-8") as f:
        f.write(
            f"# AION Intelligence\n\n"
            f"Last updated: {now}\n\n"
            f"Pipeline running successfully.\n"
        )

    print("✅ News stub updated")


# -----------------------------------
# MAIN EXECUTION
# -----------------------------------
if __name__ == "__main__":
    print("🔄 Running AION pipeline...")

    generate_news_stub()
    fetch_market_data()

    print("✅ Pipeline complete")