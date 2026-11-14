"""One-off check of which free data sources answer from GitHub's servers. Writes tools/probe/result.txt."""
import json, urllib.request, time

UA = {"User-Agent": "value-investor-site (github.com/aravamudhanAnand/value-investor)"}
out = []


def get(name, url, show=400, headers=UA):
    t = time.time()
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=40) as r:
            body = r.read()
        out.append(f"== {name}: HTTP {r.status}, {len(body)} bytes, {time.time()-t:.1f}s\n{body[:show].decode('utf-8', 'replace')}\n")
        return body
    except Exception as e:  # noqa: BLE001
        out.append(f"== {name}: FAILED {type(e).__name__}: {e}\n")
        return None


b = get("SEC companyfacts AAPL", "https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json", 200)
if b:
    f = json.loads(b)["facts"]
    g = f.get("us-gaap", {})
    out.append("us-gaap tags: %d; dei tags: %s\n" % (len(g), list(f.get("dei", {}))[:6]))
    for tag in ["Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax", "NetIncomeLoss", "EarningsPerShareDiluted", "GrossProfit", "OperatingIncomeLoss",
                "NetCashProvidedByUsedInOperatingActivities", "PaymentsToAcquirePropertyPlantAndEquipment", "ShareBasedCompensation", "PaymentsOfDividends",
                "PaymentsForRepurchaseOfCommonStock", "DepreciationDepletionAndAmortization", "Assets", "StockholdersEquity", "LongTermDebt", "InterestExpense"]:
        if tag in g:
            u = g[tag]["units"]; k = list(u)[0]; rows = [r for r in u[k] if r.get("form") == "10-K" and r.get("fp") == "FY"]
            out.append(f"  {tag} [{k}] {len(u[k])} rows; last 10-K: {json.dumps(rows[-1]) if rows else None}\n")
        else:
            out.append(f"  {tag}: absent\n")
get("SEC company tickers", "https://www.sec.gov/files/company_tickers.json", 200)
get("SEC frames (one call, all companies)", "https://data.sec.gov/api/xbrl/frames/us-gaap/Assets/USD/CY2025Q4I.json", 300)
get("Stooq latest quote", "https://stooq.com/q/l/?s=aapl.us&f=sd2t2ohlcv&h&e=csv")
get("Stooq daily history", "https://stooq.com/q/d/l/?s=aapl.us&i=d", 200)
get("Yahoo chart", "https://query1.finance.yahoo.com/v8/finance/chart/AAPL?range=1y&interval=1d", 300, {"User-Agent": "Mozilla/5.0"})
get("Yahoo quoteSummary", "https://query1.finance.yahoo.com/v10/finance/quoteSummary/AAPL?modules=financialData,defaultKeyStatistics", 300, {"User-Agent": "Mozilla/5.0"})
get("S&P 500 constituents", "https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv", 200)
get("US Treasury 10y (FRED csv)", "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10&cosd=2026-10-01", 200)
open("tools/probe/result.txt", "w").write("".join(out))
print("".join(out))
