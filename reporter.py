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


def _verdict(s1: dict, s2: dict) -> str:
    lines = []

    if s1["volatility"] is not None and s2["volatility"] is not None:
        stable = s1 if s1["volatility"] < s2["volatility"] else s2
        growth = s1 if s1["one_year_return"] > s2["one_year_return"] else s2
        lines.append(
            f"<strong>{stable['ticker']}</strong> is the more stable pick "
            f"(lower annualized volatility: {_fmt_pct(stable['volatility'])})."
        )
        lines.append(
            f"<strong>{growth['ticker']}</strong> has delivered more growth "
            f"over the past year ({_fmt_pct(growth['one_year_return'])})."
        )

    return " ".join(lines) if lines else "Insufficient data for a comparison verdict."


def generate_report(s1: dict, s2: dict, output_path: str = "report.html") -> None:
    dates_json = json.dumps(s1["history_dates"])
    prices1_json = json.dumps(s1["history_prices"])
    prices2_json = json.dumps(s2["history_prices"])

    def metric_row(label, v1, v2):
        return f"""
        <tr>
            <td class="metric-label">{label}</td>
            <td>{v1}</td>
            <td>{v2}</td>
        </tr>"""

    rows = (
        metric_row("Current Price", _fmt_price(s1["price"]), _fmt_price(s2["price"]))
        + metric_row("Market Cap", _fmt_market_cap(s1["market_cap"]), _fmt_market_cap(s2["market_cap"]))
        + metric_row("P/E Ratio", _fmt_ratio(s1["pe_ratio"]), _fmt_ratio(s2["pe_ratio"]))
        + metric_row("Beta", _fmt_ratio(s1["beta"]), _fmt_ratio(s2["beta"]))
        + metric_row("Dividend Yield", _fmt_pct(s1["dividend_yield"]), _fmt_pct(s2["dividend_yield"]))
        + metric_row("52-Week High", _fmt_price(s1["fifty_two_week_high"]), _fmt_price(s2["fifty_two_week_high"]))
        + metric_row("52-Week Low", _fmt_price(s1["fifty_two_week_low"]), _fmt_price(s2["fifty_two_week_low"]))
        + metric_row("1-Year Return", _fmt_pct(s1["one_year_return"]), _fmt_pct(s2["one_year_return"]))
        + metric_row("Annualized Volatility", _fmt_pct(s1["volatility"]), _fmt_pct(s2["volatility"]))
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{s1['ticker']} vs {s2['ticker']}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #0f1117; color: #e2e8f0; padding: 2rem; }}
        h1 {{ text-align: center; font-size: 1.8rem; margin-bottom: 0.25rem; color: #f8fafc; }}
        .subtitle {{ text-align: center; color: #94a3b8; margin-bottom: 2rem; font-size: 0.9rem; }}
        .card {{ background: #1e2130; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }}
        table {{ width: 100%; border-collapse: collapse; }}
        thead th {{ padding: 0.75rem 1rem; text-align: left; color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #2d3148; }}
        thead th:not(:first-child) {{ text-align: right; font-size: 1rem; text-transform: none; letter-spacing: 0; color: #f8fafc; }}
        tbody td {{ padding: 0.75rem 1rem; border-bottom: 1px solid #2d3148; }}
        tbody tr:last-child td {{ border-bottom: none; }}
        .metric-label {{ color: #94a3b8; font-size: 0.9rem; }}
        tbody td:not(:first-child) {{ text-align: right; font-weight: 500; }}
        .verdict {{ background: #1e2130; border-left: 4px solid #6366f1; border-radius: 0 12px 12px 0; padding: 1.25rem 1.5rem; line-height: 1.7; color: #cbd5e1; }}
        .verdict-title {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; color: #6366f1; margin-bottom: 0.5rem; }}
        .chart-wrapper {{ position: relative; height: 300px; }}
    </style>
</head>
<body>
    <h1>{s1['ticker']} vs {s2['ticker']}</h1>
    <p class="subtitle">{s1['name']} &nbsp;·&nbsp; {s2['name']}</p>

    <div class="card">
        <table>
            <thead>
                <tr>
                    <th>Metric</th>
                    <th>{s1['ticker']}</th>
                    <th>{s2['ticker']}</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>

    <div class="card">
        <div class="chart-wrapper">
            <canvas id="priceChart"></canvas>
        </div>
    </div>

    <div class="verdict">
        <div class="verdict-title">At a Glance</div>
        {_verdict(s1, s2)}
    </div>

    <script>
        const dates = {dates_json};
        const ctx = document.getElementById("priceChart").getContext("2d");
        new Chart(ctx, {{
            type: "line",
            data: {{
                labels: dates,
                datasets: [
                    {{
                        label: "{s1['ticker']}",
                        data: {prices1_json},
                        borderColor: "#6366f1",
                        backgroundColor: "rgba(99,102,241,0.08)",
                        borderWidth: 2,
                        pointRadius: 0,
                        tension: 0.3,
                        fill: true,
                    }},
                    {{
                        label: "{s2['ticker']}",
                        data: {prices2_json},
                        borderColor: "#22d3ee",
                        backgroundColor: "rgba(34,211,238,0.08)",
                        borderWidth: 2,
                        pointRadius: 0,
                        tension: 0.3,
                        fill: true,
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                interaction: {{ mode: "index", intersect: false }},
                plugins: {{
                    legend: {{ labels: {{ color: "#e2e8f0" }} }}
                }},
                scales: {{
                    x: {{
                        ticks: {{ color: "#64748b", maxTicksLimit: 8 }},
                        grid: {{ color: "#2d3148" }}
                    }},
                    y: {{
                        ticks: {{ color: "#64748b", callback: v => "$" + v.toLocaleString() }},
                        grid: {{ color: "#2d3148" }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
