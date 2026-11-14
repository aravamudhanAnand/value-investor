# Keeping Value Investor up to date

Two kinds of update. Do the first monthly; do the second after earnings season.

## 1. Prices: automatic, every Saturday

The **Refresh prices** workflow runs every Saturday morning. It pulls each
company's latest close and 52-week range from Yahoo Finance and the 10-year
Treasury yield from FRED, rebuilds every report and commits the result. The live
site updates a minute or two later. You do nothing.

- **Run it now:** Actions tab -> Refresh prices -> Run workflow.
- **Check what changed:** open `tools/refresh_log.txt`. A line starting
  `SKIPPED` means that company kept its old price: the feed failed, or the price
  moved more than 40% (usually a stock split, which needs the share count in
  `tools/data/<TICKER>.txt` updated too).
- **If the feed stops working** the job fails without changing anything, and
  GitHub emails you. Prices can still be edited by hand in `tools/prices.csv`.

Not automated, because no free feed carries them: analysts' ratings and price
targets, beta, forward P/E and PEG. These live in `tools/market.csv` and the
data files and are refreshed with the quarterly update below. Forward P/E and
PEG are scaled with the price in between.

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
