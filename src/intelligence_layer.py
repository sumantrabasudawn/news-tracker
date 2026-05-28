def generate_intelligence_assessment(news_df, market_df):
    sections = news_df["section"].value_counts().to_dict() if not news_df.empty else {}

    top_sections = ", ".join(list(sections.keys())[:3]) if sections else "market and policy signals"

    assessment = f"""
AION’s latest read suggests that the current news flow is concentrated around {top_sections}. The immediate signal is not merely the number of stories, but the clustering of developments across markets, policy, geopolitics, energy and corporate activity.

Markets remain sensitive to cross-asset signals from equities, crude, gold, the dollar index and currency movement. Any simultaneous movement in crude, the dollar and risk assets should be treated as an early warning indicator for volatility in capital flows and business sentiment.

For India, the most important watchpoint is the interaction between global risk appetite, domestic macro resilience, policy visibility and sector-specific investment momentum. Energy, infrastructure, financial markets and regulation remain the most decision-relevant areas.

The leadership implication is clear: decision-makers should not read today’s news as isolated headlines. They should watch whether these signals begin to reinforce each other across markets, policy and reputation.

AION will continue to monitor whether the day’s developments create risk, opportunity or narrative shifts for enterprises, investors, policymakers and strategic communications teams.
"""

    return assessment.strip()


def generate_watchlist(news_df, market_df):
    watchlist = [
        "Crude oil and dollar movement through the day",
        "Indian equity-market breadth and FII/FPI flow signals",
        "Any RBI, SEBI, government or ministry-level policy commentary",
        "Geopolitical headlines from West Asia, China, Russia-Ukraine and US trade policy",
        "Energy, infrastructure and capital-market stories with corporate exposure",
        "Any sharp movement in gold, India VIX or bond-market sentiment"
    ]

    return watchlist


def generate_macro_dashboard():
    return [
        {"indicator": "RBI Repo Rate", "latest": "6.50%", "signal": "Policy rate to watch"},
        {"indicator": "US Fed Funds Rate", "latest": "5.25%–5.50%", "signal": "Global liquidity anchor"},
        {"indicator": "India CPI", "latest": "Update manually / connect source", "signal": "Inflation trajectory"},
        {"indicator": "US CPI", "latest": "Update manually / connect source", "signal": "Fed policy sensitivity"},
        {"indicator": "India IIP", "latest": "Update manually / connect source", "signal": "Industrial momentum"},
        {"indicator": "US Jobs Data", "latest": "Update manually / connect source", "signal": "Dollar and yield trigger"}
    ]


def generate_data_watch_grid():
    return [
        {"event": "US inflation / PCE data", "importance": "High", "why": "Can move Fed expectations, dollar and risk assets"},
        {"event": "US jobs data", "importance": "High", "why": "Important for yields, dollar and global equities"},
        {"event": "RBI commentary / MPC signals", "importance": "High", "why": "Relevant for India rates, banks and capital flows"},
        {"event": "China PMI / growth data", "importance": "Medium", "why": "Can affect commodities and Asia risk sentiment"},
        {"event": "OPEC / crude supply signals", "importance": "High", "why": "Directly relevant for India inflation and current account"},
        {"event": "SEBI / IPO-market developments", "importance": "Medium", "why": "Important for capital-market sentiment"}
    ]