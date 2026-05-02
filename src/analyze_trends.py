import pandas as pd
import matplotlib.pyplot as plt

# Improve chart appearance
plt.rcParams.update({"figure.figsize": (8, 5)})

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("output/latest.csv")

# Ensure required columns exist
df["title"] = df.get("title", "").fillna("")
df["summary"] = df.get("summary", "").fillna("")

# Combine text for analysis
df["text"] = df["title"] + " " + df["summary"]

# -----------------------------
# 1. Top Sources
# -----------------------------
if "source" in df.columns:
    top_sources = df["source"].value_counts().head(10)

    plt.figure()
    top_sources.plot(kind="bar")
    plt.title("Top News Sources")
    plt.ylabel("Number of Stories")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("output/top_sources.png")
else:
    print("No source column found")

# -----------------------------
# 2. Keyword Trends
# -----------------------------
keywords = {
    "Energy": ["oil", "gas", "power", "energy", "solar", "renewable"],
    "Geopolitics": ["war", "iran", "china", "conflict", "military"],
    "Economy": ["inflation", "gdp", "growth", "recession"],
    "Technology": ["ai", "data", "semiconductor", "tech"]
}

trend_counts = {}

for key, words in keywords.items():
    count = df["text"].str.lower().apply(
        lambda x: any(word in x for word in words)
    ).sum()
    trend_counts[key] = count

trend_df = pd.Series(trend_counts)

plt.figure()
trend_df.plot(kind="bar")
plt.title("Trend Distribution")
plt.ylabel("Mentions")
plt.xticks(rotation=30)
plt.tight_layout()
plt.savefig("output/trend_distribution.png")

# -----------------------------
# 3. Stories Over Time (by hour)
# -----------------------------
if "published_at" in df.columns:

    # Clean + standardize datetime
    df["published_at"] = pd.to_datetime(
        df["published_at"], errors="coerce", utc=True
    )

    # Drop invalid rows
    df_time = df.dropna(subset=["published_at"]).copy()

    if df_time.empty:
        print("No valid timestamps found for time analysis")
    else:
        # Convert to IST
        df_time["published_at"] = df_time["published_at"].dt.tz_convert("Asia/Kolkata")

        # Extract hour
        df_time["hour"] = df_time["published_at"].dt.hour

        # Aggregate
        hour_counts = df_time["hour"].value_counts().sort_index()

        # Plot
        plt.figure()
        hour_counts.plot(kind="line")
        plt.title("News Flow by Hour")
        plt.xlabel("Hour of Day (IST)")
        plt.ylabel("Number of Stories")
        plt.tight_layout()
        plt.savefig("output/news_flow.png")

else:
    print("No published_at column found")

# -----------------------------
# Done
# -----------------------------
print("Trend analysis charts generated in output/")