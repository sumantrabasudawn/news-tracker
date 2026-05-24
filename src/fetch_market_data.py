import yfinance as yf
import pandas as pd
from pathlib import Path

MARKETS = {
    "NIFTY 50": "^NSEI",
    "SENSEX": "^BSESN",
    "NASDAQ": "^IXIC",
    "S&P 500": "^GSPC",
    "BRENT": "BZ=F",
    "GOLD": "GC=F",
    "DOLLAR INDEX": "DX-Y.NYB",
    "INDIA VIX": "^INDIAVIX",
    "USD/INR": "INR=X"
}

rows = []

for name, ticker in MARKETS.items():
    try:
        data = yf.Ticker(ticker).history(period="5d")

        if len(data) >= 2:
            latest = data["Close"].iloc[-1]
            previous = data["Close"].iloc[-2]
            change = (latest - previous) / previous

            rows.append({
                "asset": name,
                "price": round(latest, 2),
                "change": round(change, 4)
            })

    except Exception as e:
        print(f"Failed: {name} — {e}")

Path("output").mkdir(exist_ok=True)

pd.DataFrame(rows).to_csv("output/market_data.csv", index=False)

print("Market data updated.")
