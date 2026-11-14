# Value Investor

**Business quality and fair value for 102 large US companies.**

Pick one of 102 large US companies (the S&P 100, plus Waste Management and
Sherwin-Williams) and see it assessed the way a value investor would: first on
the 4 M's, then on a full ratio sheet, then against the checklists of Benjamin
Graham, Warren Buffett, Peter Lynch, Charlie Munger and Mohnish Pabrai.

**Live site:** `https://<your-username>.github.io/value-investor/`

![Value Investor](docs/screenshot.png)

## What each assessment shows

- **A verdict** — Buy zone, Watchlist, Too hard or Pass — with the reason in one sentence.
- **A nine-part story per company** — one sentence with strengths, risks and
  swing factors, then what it is, how it makes money, durability, the numbers,
  valuation, fair value, bull and bear cases, and second opinions.
- **The business in brief** — what the company is, how it makes money, and how
  the stock is valued, with the multiples that matter for its type against its
  sector peers.
- **Price in context** — the main multiple charted against peers, the 52-week
  range, and the analysts' average target alongside this site's fair value.
- **Fair value** — one number per share with its range, the price against it, the
  margin of safety and the buy-below price, built from two methods: owner cash
  flow and Aswath Damodaran's cash-flow-to-the-firm model, plus the growth rate
  today's price assumes.
- **The compass** — a radar of six pillar scores against a 7/10 "wonderful
  business" bar and the median of all companies, with a written reading of the shape.
- **The 4 M's** — Meaning, Moat (with industry stability), Management and
  Margin of safety, including a price-versus-value chart and the "buy below" price.
- **The evidence** — five years of revenue, net income and free cash flow, nine
  financial-health checks, a ratio sheet of about 35 ratios against yardsticks
  (profitability, debt, cash quality, growth, shareholder returns, yield against
  bonds), and the Value 3.0 rules of the road.
- **Five investors' checklists** — 37 calculated tests: Graham's
  defensive-investor screen, Buffett's owner economics, Lynch's stock categories
  and growth-at-a-reasonable-price tests, Munger's inversion and incentives, and
  Pabrai's Dhandho checklist.

The full rulebook is in [`framework/value-investor.md`](framework/value-investor.md)
and is displayed on the site's Methodology page.

## How it is built

A static site: no server, no database, no API keys, nothing to pay for.

```
index.html, assets/          the website (plain HTML, CSS and JavaScript; charts are hand-built SVG)
framework/value-investor.md  the rulebook
data/                        generated reports (one JSON file per company)
tools/data/*.txt             sourced financial figures, one file per company
tools/prices.csv             latest prices: the file to edit each month
tools/settings.json          as-of date, 10-year Treasury yield, framework version
tools/companies_*.py         analyst judgments (meaning, moat, industry, management, growth)
tools/build.py               applies the framework and writes data/
```

Judgment and calculation are kept apart. Meaning, moat, industry, management
and the growth assumption are judgment; every other number is calculated by
`tools/build.py` from the figures in `tools/data/`, so results are reproducible.

## Publish on GitHub Pages

1. Create a public repository named `value-investor` and upload these files.
2. **Settings → Pages**: set Source to *Deploy from a branch*, choose `main` and `/ (root)`.
3. **Settings → Actions → General → Workflow permissions**: choose *Read and write*
   so the rebuild workflow can commit.

## Keeping it current

See [`UPDATING.md`](UPDATING.md). In short: edit `tools/prices.csv` once a month
on github.com and the site rebuilds itself; refresh the financials each quarter
with Claude Code.

## Data

Financial figures from StockAnalysis.com (S&P Global Market Intelligence data),
collected on the date shown on each report. Fiscal years follow each company's
own calendar. Where a source page was incomplete, the report says so.

## Disclaimer

Educational analysis, not financial advice. Verdicts are the mechanical output
of one framework applied to public figures; they may be wrong or out of date.
Verify against company filings before making any investment decision.

---

Built by Anand Chari.
