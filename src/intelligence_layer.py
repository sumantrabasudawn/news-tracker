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


def _get_market_value(market_df, asset_name):
    if market_df.empty:
        return "not available"

    row = market_df[market_df["asset"] == asset_name]

    if row.empty:
        return "not available"

    return row.iloc[0]["price"]


def generate_intelligence_assessment(news_df, market_df):
    market = _market_signal(market_df)

    brent = _get_market_value(market_df, "BRENT")
    dollar = _get_market_value(market_df, "DOLLAR INDEX")
    vix = _get_market_value(market_df, "INDIA VIX")
    nifty = _get_market_value(market_df, "NIFTY 50")
    gold = _get_market_value(market_df, "GOLD")
    usdinr = _get_market_value(market_df, "USD/INR")

    assessment = f"""
<h2>Geopolitical Signal</h2>

<p>
Iran-US tensions are again becoming the dominant macro-risk variable. The issue is no longer merely diplomatic escalation; it is whether geopolitical stress begins transmitting into crude prices, shipping costs, inflation expectations, currency markets and broader risk appetite. Brent crude is currently around <strong>{brent}</strong>, the dollar index is near <strong>{dollar}</strong>, gold is around <strong>{gold}</strong>, and USD/INR is near <strong>{usdinr}</strong>. If crude and the dollar firm together, India faces a tighter imported-inflation backdrop at precisely the point when markets are still pricing domestic resilience.
</p>

<p>
The principal market risk is the Strait of Hormuz channel. Roughly one-fifth of globally traded oil moves through that corridor. Even without a physical supply disruption, a sustained escalation premium can raise freight costs, lift energy hedging demand, strengthen safe-haven flows and reduce emerging-market risk appetite. For India, this is not just a foreign-policy event. It is a current-account, inflation, fiscal and market-liquidity variable.
</p>

<h2>Cross-Market Read</h2>

<p>
The current cross-asset tone is <strong>{market["risk_tone"]}</strong>. {market["summary"]} The relevant question is whether commodities, currencies and equities begin confirming the same signal. A rise in Brent alongside a stronger dollar and firmer gold would indicate defensive global positioning. If that is accompanied by weakness in Indian equities or a rise in India VIX, the signal would shift from geopolitical noise to market transmission.
</p>

<p>
India VIX near <strong>{vix}</strong> and the NIFTY 50 near <strong>{nifty}</strong> should be read together. A stable headline index with rising volatility or weak market breadth would suggest that institutional investors are becoming more selective beneath the surface. In that environment, index resilience can mask portfolio-level de-risking.
</p>

<h2>India Macro Implication</h2>

<p>
India’s structural macro story remains stronger than most large emerging markets. Domestic demand, infrastructure execution, financial-sector repair, manufacturing ambition and digital formalisation continue to support the medium-term narrative. But the cyclical vulnerability is clear: India remains exposed to imported energy prices. Every sustained rise in crude affects inflation management, the current account, logistics costs, fiscal assumptions and the credibility of rate-cut expectations.
</p>

<p>
This makes energy security and monetary-policy credibility part of the same analytical frame. If crude remains elevated while the rupee weakens, the RBI’s room to support growth becomes more constrained. If crude stabilises and the dollar softens, India’s resilience narrative becomes easier to defend. The macro risk is therefore not one data point; it is the combination of oil, currency, inflation and liquidity.
</p>

<h2>Capital-Market Signal</h2>

<p>
Indian capital markets remain liquid, but the quality of liquidity is becoming more important than the quantity. IPO markets, infrastructure platforms and private-capital flows depend on a benign mix of domestic confidence and global liquidity. If US yields stay elevated, the dollar remains firm and geopolitical risk rises, investors are likely to become more selective on leverage, execution visibility and balance-sheet credibility.
</p>

<p>
The NIFTY level is therefore less important than the breadth beneath it. A broad rally would confirm domestic risk appetite. A narrow rally led by a small set of large stocks would suggest defensive positioning. For IPO-stage companies, the implication is direct: markets will reward proof, not promise. Order books, cash flows, governance, margins and execution discipline will matter more than sectoral storytelling.
</p>

<h2>Corporate and Reputation Consequence</h2>

<p>
Companies exposed to energy, infrastructure, manufacturing, logistics, financial markets and regulated sectors should assume a sharper operating environment. Investors and policymakers will increasingly look for evidence of resilience: supply-chain depth, energy efficiency, working-capital control, regulatory alignment, risk management and balance-sheet discipline. Generic optimism will be less persuasive in a market that is repricing geopolitical and macro risk.
</p>

<p>
For communications teams, the risk is over-claiming. Markets under stress punish broad narratives quickly. The strongest positioning will come from precise, evidence-led communication: what has been delivered, what is funded, what is contracted, what is protected, and what is resilient under volatility.
</p>

<h2>What To Watch Next</h2>

<ul>
<li>Whether Iran-US escalation begins affecting crude, LNG or shipping insurance costs.</li>
<li>Whether Brent, gold and the dollar index move higher together.</li>
<li>Whether India VIX rises while headline indices remain superficially stable.</li>
<li>Whether USD/INR weakens alongside higher crude.</li>
<li>Whether FII/FPI flows turn more defensive in Indian equities or debt.</li>
<li>Whether RBI, SEBI, finance ministry or energy ministry commentary changes market expectations.</li>
</ul>

<h2>Implied Signal Matrix</h2>

<table>
<tr>
<th>Signal</th>
<th>Current Direction</th>
<th>Strategic Implication</th>
</tr>

<tr>
<td>Iran-US escalation</td>
<td>Elevated</td>
<td>Raises the risk premium in crude, shipping, gold and safe-haven assets.</td>
</tr>

<tr>
<td>Brent crude</td>
<td>{brent}</td>
<td>Key variable for India inflation, current account and energy-import sensitivity.</td>
</tr>

<tr>
<td>Dollar index</td>
<td>{dollar}</td>
<td>Important for emerging-market flows, rupee pressure and global liquidity.</td>
</tr>

<tr>
<td>India VIX</td>
<td>{vix}</td>
<td>Early signal of whether geopolitical risk is transmitting into Indian market volatility.</td>
</tr>

<tr>
<td>NIFTY 50</td>
<td>{nifty}</td>
<td>Headline resilience must be tested against breadth, flows and volatility.</td>
</tr>

<tr>
<td>Gold</td>
<td>{gold}</td>
<td>Safe-haven demand indicator during geopolitical escalation.</td>
</tr>

</table>
"""

    return assessment.strip()


def generate_watchlist(news_df, market_df):
    return [
        "Whether Iran-US escalation begins affecting crude, LNG, freight rates or shipping insurance.",
        "Whether Brent crude, gold and the dollar index move higher together, signalling a broader defensive market impulse.",
        "Whether USD/INR weakens alongside higher crude, tightening India’s imported-inflation backdrop.",
        "Whether Indian equities show broad-based strength or narrow index-level resilience.",
        "Whether India VIX rises even if headline indices remain stable.",
        "Any RBI, SEBI, finance ministry, energy ministry or cabinet signal affecting inflation, capital markets, infrastructure or credit.",
        "Any sharp shift in FII/FPI behaviour, rupee movement or IPO-market sentiment.",
        "Energy, infrastructure and power-sector stories indicating stress in execution, regulation, tariffs, grid capacity or demand."
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
        {"event": "Iran-US escalation headlines", "importance": "High", "why": "Can affect crude, shipping, gold, inflation expectations and emerging-market risk appetite."},
        {"event": "Brent crude movement", "importance": "High", "why": "Direct input into India’s inflation, current account and energy-import bill."},
        {"event": "US inflation / PCE data", "importance": "High", "why": "Can reset Fed expectations, dollar strength and global risk appetite."},
        {"event": "US non-farm payrolls / jobs data", "importance": "High", "why": "Affects yields, dollar direction and equity-market liquidity assumptions."},
        {"event": "RBI commentary / MPC signals", "importance": "High", "why": "Critical for Indian rates, banks, NBFCs, capex confidence and rupee sentiment."},
        {"event": "India CPI / IIP prints", "importance": "High", "why": "Shapes the domestic macro narrative around inflation, consumption and industrial momentum."},
        {"event": "China PMI / industrial data", "importance": "Medium", "why": "Relevant for commodities, Asian exports, manufacturing supply chains and risk appetite."},
        {"event": "OPEC / crude supply signals", "importance": "High", "why": "Directly affects India’s inflation, current account, fiscal sensitivity and energy-import bill."},
        {"event": "SEBI / IPO-market reforms", "importance": "Medium", "why": "Important for listing sentiment, issuer behaviour and capital-market credibility."}
    ]