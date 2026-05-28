def _top_sections(news_df):
    if news_df.empty or "section" not in news_df.columns:
        return []

    return list(news_df["section"].value_counts().head(5).index)


def _market_signal(market_df):
    if market_df.empty:
        return {
            "summary": "Market data was not available in this run.",
            "risk_tone": "Unclear",
            "signals": []
        }

    signals = []
    risk_score = 0

    for _, row in market_df.iterrows():
        asset = row["asset"]
        change = float(row["change"]) * 100

        if abs(change) >= 0.4:
            direction = "higher" if change > 0 else "lower"
            signals.append(f"{asset} traded {direction} by {abs(change):.2f}%")

        if asset in ["BRENT", "GOLD", "DOLLAR INDEX", "INDIA VIX"] and change > 0:
            risk_score += 1

        if asset in ["NIFTY 50", "SENSEX", "NASDAQ", "S&P 500"] and change < 0:
            risk_score += 1

    if risk_score >= 3:
        risk_tone = "Risk-off bias"
    elif risk_score == 2:
        risk_tone = "Cautious / mixed"
    else:
        risk_tone = "Contained risk tone"

    summary = (
        "; ".join(signals[:5]) + "."
        if signals
        else "Cross-asset moves are contained, suggesting no single market variable is yet dominating the day’s risk tone."
    )

    return {
        "summary": summary,
        "risk_tone": risk_tone,
        "signals": signals
    }


def generate_intelligence_assessment(news_df, market_df):
    sections = _top_sections(news_df)
    section_text = ", ".join(sections) if sections else "markets, policy, energy and geopolitical risk"
    market = _market_signal(market_df)

    assessment = f"""
<strong>Core thesis.</strong> AION’s latest read is that the current information environment is clustering around {section_text}. The intelligence value here is not the existence of individual headlines, but the possibility that separate developments are beginning to interact. In institutional terms, the operating question is whether news flow, market direction, policy signals and geopolitical risk are reinforcing each other or cancelling each other out. This distinction matters because leadership teams rarely lose time because they missed a headline; they lose time because they failed to recognise when disconnected headlines were becoming a system-level signal.

<strong>Market signal.</strong> The cross-asset tone is best described as <strong>{market["risk_tone"]}</strong>. {market["summary"]} For India, the critical transmission chain remains crude, the dollar, global equities, gold, volatility and FII behaviour. A firmer dollar with higher crude would tighten the imported-inflation backdrop and complicate liquidity conditions for emerging markets. Softer crude, stable global equities and contained volatility would support the India resilience narrative. The key is not one index tick, but the combined direction of external pressure and domestic risk appetite.

<strong>Macro implication.</strong> India’s structural story remains underpinned by infrastructure execution, domestic demand, formalisation, energy transition and capital-market depth. But the cyclical layer is more fragile. A strong domestic growth narrative can coexist with pressure from global yields, commodity costs, foreign flows and currency movement. That is why the macro dashboard must be read as a system: monetary-policy rates, inflation prints, industrial production, jobs data, crude and the dollar are not separate boxes. They collectively define the cost of capital, the credibility of earnings expectations and the room available for policy support.

<strong>Geopolitical transmission.</strong> The geopolitical layer should be read through economic channels rather than dramatic headlines. West Asia matters through crude, LNG, shipping costs and inflation expectations. China matters through commodities, Asian manufacturing, trade routes and supply-chain confidence. US policy matters through the dollar, yields, tariffs, technology controls and global capital allocation. Russia-Ukraine risk continues to matter through energy, food, defence and fiscal pressures. The intelligence question is not whether a geopolitical story is loud; it is whether it changes costs, capital, supply chains or political room for manoeuvre.

<strong>India policy and capital-market lens.</strong> The interaction of policy visibility and capital-market sentiment is becoming central. If domestic policy signals remain stable while global volatility is contained, Indian risk assets can sustain a premium. But if regulatory uncertainty, IPO fatigue, FII outflows or inflation concerns rise together, the market narrative can turn quickly from resilience to vulnerability. SEBI, RBI, finance ministry, energy ministry and infrastructure-related signals therefore need to be tracked not as bureaucratic updates, but as inputs into investor confidence and corporate planning.

<strong>Corporate and reputation implication.</strong> Companies exposed to energy, infrastructure, capital markets, technology, manufacturing and regulated sectors should assume that scrutiny will rise where public policy, market expectations and execution credibility intersect. The most valuable corporate positioning over the next cycle will not be generic optimism. It will be evidence-led resilience: order books, execution capacity, balance-sheet discipline, regulatory alignment, energy efficiency, supply-chain depth and credible governance. For communications teams, the risk is not silence alone; it is speaking in broad claims when the market is looking for proof.

<strong>Leadership judgment.</strong> The next few hours should be read for confirmation, not noise. If market variables and news themes move in the same direction, the signal strengthens. If headlines are intense but markets remain calm, the signal is weaker. If policy signals contradict market assumptions, the risk of repricing rises. AION’s priority should therefore be to separate movement from meaning, and volume from consequence.
"""

    return assessment.strip()


def generate_watchlist(news_df, market_df):
    return [
        "Whether crude, the dollar index and gold move together, signalling a broader risk-off impulse.",
        "Whether Indian equities show broad-based strength or narrow index-level resilience.",
        "Any RBI, SEBI, finance ministry or cabinet signal affecting capital markets, inflation, credit or infrastructure.",
        "West Asia, China, Russia-Ukraine and US trade-policy headlines that transmit into crude, shipping, commodities or yields.",
        "Any sharp change in India VIX, FII/FPI behaviour, rupee movement or IPO-market tone.",
        "Energy, infrastructure and power-sector stories that indicate stress in execution, regulation, tariffs, grid capacity or demand.",
        "Any data release that changes the expected path of interest rates, inflation or global liquidity."
    ]


def generate_macro_dashboard():
    return [
        {"indicator": "RBI Repo Rate", "latest": "6.50%", "signal": "Domestic monetary-policy anchor"},
        {"indicator": "US Fed Funds Rate", "latest": "5.25%–5.50%", "signal": "Global liquidity and dollar anchor"},
        {"indicator": "India CPI", "latest": "To connect", "signal": "Inflation and rate-cut visibility"},
        {"indicator": "US CPI", "latest": "To connect", "signal": "Fed path, yields and risk appetite"},
        {"indicator": "India IIP", "latest": "To connect", "signal": "Industrial momentum"},
        {"indicator": "US Jobs Data", "latest": "To connect", "signal": "Dollar, yields and equity sensitivity"},
        {"indicator": "India 10Y Yield", "latest": "To connect", "signal": "Cost of capital and bond-market confidence"},
        {"indicator": "FII/FPI Flows", "latest": "To connect", "signal": "Foreign risk appetite toward India"}
    ]


def generate_data_watch_grid():
    return [
        {"event": "US inflation / PCE data", "importance": "High", "why": "Can reset Fed expectations, dollar strength and global risk appetite."},
        {"event": "US non-farm payrolls / jobs data", "importance": "High", "why": "Affects yields, dollar direction and equity-market liquidity assumptions."},
        {"event": "RBI commentary / MPC signals", "importance": "High", "why": "Critical for Indian rates, banks, NBFCs, capex confidence and rupee sentiment."},
        {"event": "India CPI / IIP prints", "importance": "High", "why": "Shapes the domestic macro narrative around inflation, consumption and industrial momentum."},
        {"event": "China PMI / industrial data", "importance": "Medium", "why": "Relevant for commodities, Asian exports, manufacturing supply chains and risk appetite."},
        {"event": "OPEC / crude supply signals", "importance": "High", "why": "Directly affects India’s inflation, current account, fiscal sensitivity and energy-import bill."},
        {"event": "SEBI / IPO-market reforms", "importance": "Medium", "why": "Important for listing sentiment, issuer behaviour and capital-market credibility."}
    ]