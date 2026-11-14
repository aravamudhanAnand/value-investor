# Keeping Value Investor up to date

Two kinds of update. Do the first monthly; do the second after earnings season.

## 1. Monthly: refresh prices (about 15 minutes, no tools needed)

Price is the number that moves the verdicts, so this is the update that matters most.

1. On github.com, open `tools/prices.csv` and click the pencil icon.
2. Update the `price` and `date` for each ticker (any quote page works; use the latest close).
3. Open `tools/market.csv` and update each row from the company's overview page
   on StockAnalysis.com: 52-week low and high, beta, analyst rating, average
   price target, and the `as_of` date. These drive the 52-week range bar and the
   analysts' target on the fair value chart.
4. Open `tools/settings.json` and update `as_of` to today's date and
   `treasury_10y` to the current 10-year Treasury yield.
5. Commit. The **Rebuild reports** workflow (Actions tab) recalculates every
   valuation, margin of safety, checklist and verdict, and commits the new `data/`
   folder. The live site updates a minute or two later.

What the price update changes: P/E, P/B, P/FCF, EV multiples, earnings and
owner-earnings yields, the Graham number test, margin of safety, upside/downside
and the verdict. Forward P/E and PEG are scaled with the price. The 52-week
price change cannot be recalculated from a new price, so that one Pabrai test
shows "n/a" until the next full refresh.

Faster alternative: open the repository in Claude Code and say
**"Refresh prices and market data for all companies."** It follows `CLAUDE.md`.

## 2. Quarterly: refresh the financials (with Claude Code)

Fundamentals change four times a year. Open the repository in Claude Code and say
**"Refresh the financial data for all companies"** (or name the ones that have
reported). It re-reads four pages per company (statistics, income statement, balance sheet, cash flow statement) and rewrites `tools/data/<TICKER>.txt`.
Review the printed verdict changes, then commit.

After a refresh, skim the judgments in `tools/companies_*.py` for anything the
new numbers contradict (a moat that has weakened, a bull point that is no longer true).

## 3. When needed

- **Add a company:** add `tools/data/<TICKER>.txt`, an entry in the matching
  `tools/companies_*.py`, a profile in `tools/profiles_*.py`, and rows in
  `tools/prices.csv` and `tools/market.csv`. Claude Code can do all of it.
- **Remove a company:** delete those three things and `data/companies/<TICKER>.json`.
- **Index changes:** the S&P 100 is rebalanced quarterly; check the constituent
  list when you do the quarterly refresh.
- **Change the framework:** edit `framework/value-investor.md`, bump `version:`
  there and in `tools/settings.json`, add a changelog line, and change the matching
  constant or rule in `tools/build.py`.

## Running the build yourself

```
python3 tools/build.py        # rebuilds data/
python3 tools/build.py -v     # also prints every company's verdict
python3 -m http.server        # preview at http://localhost:8000
```
