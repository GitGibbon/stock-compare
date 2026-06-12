import json


def _fmt_price(val) -> str:
    return f"${val:,.2f}" if val is not None else "N/A"


def _fmt_market_cap(val) -> str:
    if val is None:
        return "N/A"
    if val >= 1_000_000_000_000:
        return f"${val / 1_000_000_000_000:.2f}T"
    if val >= 1_000_000_000:
        return f"${val / 1_000_000_000:.2f}B"
    return f"${val / 1_000_000:.2f}M"


def _fmt_pct(val) -> str:
    return f"{val * 100:.2f}%" if val is not None else "N/A"


def _fmt_ratio(val) -> str:
    return f"{val:.2f}" if val is not None else "N/A"


def _verdict_comparison(s1: dict, s2: dict) -> str:
    if s1["volatility"] is None or s2["volatility"] is None:
        return "Insufficient data for a comparison verdict."
    stable = s1 if s1["volatility"] < s2["volatility"] else s2
    growth = s1 if s1["one_year_return"] > s2["one_year_return"] else s2
    return (
        f"<strong>{stable['ticker']}</strong> is the more stable pick "
        f"(lower annualized volatility: {_fmt_pct(stable['volatility'])}). "
        f"<strong>{growth['ticker']}</strong> has delivered more growth "
        f"over the past year ({_fmt_pct(growth['one_year_return'])})."
    )


def _verdict_solo(s: dict) -> str:
    vol = _fmt_pct(s["volatility"])
    ret = _fmt_pct(s["one_year_return"])
    beta = _fmt_ratio(s["beta"])
    stability = "relatively stable" if s["beta"] is not None and s["beta"] < 1 else "higher volatility"
    return (
        f"<strong>{s['ticker']}</strong> has a beta of {beta}, making it {stability} relative to the broader market. "
        f"Annualized volatility sits at {vol}, with a 1-year return of {ret}."
    )


_METRICS = [
    ("Current Price",        lambda s: _fmt_price(s["price"])),
    ("Market Cap",           lambda s: _fmt_market_cap(s["market_cap"])),
    ("P/E Ratio",            lambda s: _fmt_ratio(s["pe_ratio"])),
    ("Beta",                 lambda s: _fmt_ratio(s["beta"])),
    ("Dividend Yield",       lambda s: _fmt_pct(s["dividend_yield"])),
    ("52-Week High",         lambda s: _fmt_price(s["fifty_two_week_high"])),
    ("52-Week Low",          lambda s: _fmt_price(s["fifty_two_week_low"])),
    ("1-Year Return",        lambda s: _fmt_pct(s["one_year_return"])),
    ("Annualized Volatility",lambda s: _fmt_pct(s["volatility"])),
]


def _base_styles() -> str:
    return """
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0f1117; color: #e2e8f0; padding: 2rem; }
        h1 { text-align: center; font-size: 1.8rem; margin-bottom: 0.25rem; color: #f8fafc; }
        .subtitle { text-align: center; color: #94a3b8; margin-bottom: 2rem; font-size: 0.9rem; }
        .card { background: #1e2130; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }
        table { width: 100%; border-collapse: collapse; }
        thead th { padding: 0.75rem 1rem; text-align: left; color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #2d3148; }
        thead th:not(:first-child) { text-align: right; font-size: 1rem; text-transform: none; letter-spacing: 0; color: #f8fafc; }
        tbody td { padding: 0.75rem 1rem; border-bottom: 1px solid #2d3148; }
        tbody tr:last-child td { border-bottom: none; }
        .metric-label { color: #94a3b8; font-size: 0.9rem; }
        tbody td:not(:first-child) { text-align: right; font-weight: 500; }
        .verdict { background: #1e2130; border-left: 4px solid #6366f1; border-radius: 0 12px 12px 0; padding: 1.25rem 1.5rem; line-height: 1.7; color: #cbd5e1; }
        .verdict-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #6366f1; margin-bottom: 0.5rem; }
        .chart-wrapper { position: relative; height: 300px; }
    """


def _chart_script(datasets: list, dates_json: str) -> str:
    datasets_json = json.dumps(datasets)
    return f"""
    <script>
        const dates = {dates_json};
        const ctx = document.getElementById("priceChart").getContext("2d");
        new Chart(ctx, {{
            type: "line",
            data: {{
                labels: dates,
                datasets: {datasets_json}
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{ mode: "index", intersect: false }},
                plugins: {{ legend: {{ labels: {{ color: "#e2e8f0" }} }} }},
                scales: {{
                    x: {{ ticks: {{ color: "#64748b", maxTicksLimit: 8 }}, grid: {{ color: "#2d3148" }} }},
                    y: {{ ticks: {{ color: "#64748b", callback: v => "$" + v.toLocaleString() }}, grid: {{ color: "#2d3148" }} }}
                }}
            }}
        }});
    </script>
    """


def _generate_solo(s: dict) -> str:
    rows = "".join(
        f'<tr><td class="metric-label">{label}</td><td>{fn(s)}</td></tr>'
        for label, fn in _METRICS
    )
    dates_json = json.dumps(s["history_dates"])
    datasets = [{
        "label": s["ticker"],
        "data": s["history_prices"],
        "borderColor": "#6366f1",
        "backgroundColor": "rgba(99,102,241,0.08)",
        "borderWidth": 2,
        "pointRadius": 0,
        "tension": 0.3,
        "fill": True,
    }]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{s['ticker']} Report</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        {_base_styles()}
        table {{ max-width: 720px; margin: 0 auto; }}
        .card {{ max-width: 760px; margin: 0 auto 1.5rem auto; }}
        .verdict {{ max-width: 760px; margin: 0 auto; }}
    </style>
</head>
<body>
    <h1>{s['ticker']}</h1>
    <p class="subtitle">{s['name']}</p>

    <div class="card">
        <table>
            <thead><tr><th>Metric</th><th>{s['ticker']}</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>

    <div class="card">
        <div class="chart-wrapper"><canvas id="priceChart"></canvas></div>
    </div>

    <div class="verdict">
        <div class="verdict-title">At a Glance</div>
        {_verdict_solo(s)}
    </div>

    {_chart_script(datasets, dates_json)}
</body>
</html>"""


def _generate_comparison(s1: dict, s2: dict) -> str:
    rows = "".join(
        f'<tr><td class="metric-label">{label}</td><td>{fn(s1)}</td><td>{fn(s2)}</td></tr>'
        for label, fn in _METRICS
    )
    dates_json = json.dumps(s1["history_dates"])
    datasets = [
        {
            "label": s1["ticker"],
            "data": s1["history_prices"],
            "borderColor": "#6366f1",
            "backgroundColor": "rgba(99,102,241,0.08)",
            "borderWidth": 2,
            "pointRadius": 0,
            "tension": 0.3,
            "fill": True,
        },
        {
            "label": s2["ticker"],
            "data": s2["history_prices"],
            "borderColor": "#22d3ee",
            "backgroundColor": "rgba(34,211,238,0.08)",
            "borderWidth": 2,
            "pointRadius": 0,
            "tension": 0.3,
            "fill": True,
        },
    ]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{s1['ticker']} vs {s2['ticker']}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>{_base_styles()}</style>
</head>
<body>
    <h1>{s1['ticker']} vs {s2['ticker']}</h1>
    <p class="subtitle">{s1['name']} &nbsp;·&nbsp; {s2['name']}</p>

    <div class="card">
        <table>
            <thead><tr><th>Metric</th><th>{s1['ticker']}</th><th>{s2['ticker']}</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>

    <div class="card">
        <div class="chart-wrapper"><canvas id="priceChart"></canvas></div>
    </div>

    <div class="verdict">
        <div class="verdict-title">At a Glance</div>
        {_verdict_comparison(s1, s2)}
    </div>

    {_chart_script(datasets, dates_json)}
</body>
</html>"""


def generate_report(*stocks, output_path: str = "report.html") -> None:
    if len(stocks) == 1:
        html = _generate_solo(stocks[0])
    elif len(stocks) == 2:
        html = _generate_comparison(stocks[0], stocks[1])
    else:
        raise ValueError("generate_report accepts 1 or 2 stocks.")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
