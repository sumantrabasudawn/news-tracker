import os
import requests
import pandas as pd
from datetime import datetime

# -----------------------------------
# Ensure output directory exists
# -----------------------------------
os.makedirs("output", exist_ok=True)


# -----------------------------------
# MARKET DATA (Twelve Data API - FIXED)
# -----------------------------------
def fetch_market_data():
    API_KEY = os.getenv("TWELVE_API_KEY")

    if not API_KEY:
        print("❌ API key missing. Set TWELVE_API_KEY")
        return

    # ✅ Free-tier working symbols only
    symbols = {
        "GOLD": "XAU/USD",
        "USDINR": "USD/INR",
        "EURUSD": "EUR/USD",
        "GBPUSD": "GBP/USD",
        "USDJPY": "USD/JPY"
    }

    data = []

    for name, symbol in symbols.items():
        try:
            url = f"https://api.twelvedata.com/quote?symbol={symbol}&apikey={API_KEY}"
            res = requests.get(url, timeout=5).json()

            # 🔥 Handle BOTH formats correctly
            if "price" in res:
                price = float(res["price"])
                change = float(res.get("percent_change", 0))

            elif "close" in res:
                price = float(res["close"])
                change = float(res.get("percent_change", 0))

            else:
                print(f"⚠️ Failed: {name} → {res}")
                continue

            data.append({
                "asset": name,
                "price": price,
                "change_percent": change
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
# NEWS PLACEHOLDER (keeps pipeline stable)
# -----------------------------------
def generate_news_stub():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    df = pd.DataFrame([{
        "title": "AION Intelligence",
        "timestamp": now,
        "summary": "Pipeline running successfully"
    }])

    df.to_csv("output/latest.csv", index=False)

    with open("output/latest.md", "w") as f:
        f.write(f"# AION Intelligence\n\nLast updated: {now}\n\nPipeline running.")

    print("✅ News stub updated")


# -----------------------------------
# MAIN EXECUTION
# -----------------------------------
if __name__ == "__main__":
    print("🔄 Running AION pipeline...")

    generate_news_stub()
    fetch_market_data()

    print("✅ Pipeline complete")