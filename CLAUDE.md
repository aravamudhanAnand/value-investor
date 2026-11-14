# Working on Value Investor

Static site. Reports in `data/` are generated, never hand-edited: change the inputs in `tools/`, then run `python3 tools/build.py -v`.

## Refresh prices

Prices, 52-week ranges and the Treasury yield are refreshed automatically each Saturday by `.github/workflows/prices.yml` (`tools/refresh_prices.py`). The manual steps below are the fallback.

For each ticker in `tools/prices.csv`, read `https://stockanalysis.com/stocks/<ticker>/` (BRK.B is `brk.b`) and record the latest closing price and its date. Update `as_of` and `treasury_10y` in `tools/settings.json`. Rebuild and report which verdicts changed.

## Refresh financial data (or add a company)

For each ticker read four StockAnalysis.com pages (three for banks and insurers, which have no `C` lines) and rewrite `tools/data/<TICKER>.txt` in the existing format:

- `S` line from `/stocks/<t>/statistics/`: `price; date; shares; fpe; peg; cash; debt; equity; eps; cr; ic; roic; gm; rev; ni; ebitda; ebit; ocf; capex; fcf; dps; sc; ins; z; f; c52` — values as shown, with B/M/T and % suffixes, `n/a` when absent.
- five `F` lines from `/stocks/<t>/financials/`, oldest first, no TTM: `FYxx,revenue,gross margin %,net income,EPS diluted,free cash flow` (millions).
- `B` lines from `/stocks/<t>/financials/balance-sheet/`: five fiscal years then the latest quarter as `Q`: `label,total assets,total debt,shareholders equity` (millions).

- `C` lines from `/stocks/<t>/financials/cash-flow-statement/`: five fiscal years oldest first, then the TTM column as `TTM` if shown: `label,depreciation & amortization,stock-based compensation,operating cash flow,capital expenditures,common dividends paid,repurchase of common stock` (millions, minus signs kept, `n/a` when the line is absent). If the default page comes back empty, use `?p=trailing` and take each fiscal year-end quarter.

One-sentence summaries and three swing factors per company live in `tools/summaries.py`; reread them at each quarterly refresh. Business profiles live in `tools/profiles_a.py` to `profiles_d.py` as (what it is, how it makes money, how the stock is valued). At each quarterly refresh, reread them against the company's latest annual report and update anything that changed (acquisitions, spin-offs, a new chief executive, a shift in revenue mix). Keep them free of figures that go stale; the build supplies the numbers.

Market data (monthly, with prices): for each ticker read `https://stockanalysis.com/stocks/<t>/` and write one row in `tools/market.csv`: `ticker,low52,high52,beta,rating,target,as_of` (as_of = the date shown next to the price). Only replace a price in `tools/prices.csv` if the page's date is newer than the one on file. Reject any page whose price is more than 20% from the price on file without a newer date: it is a stale cached snapshot. If so, take the rating and target from `/forecast/` and leave the range as `n/a`.

Also update the price row in `tools/prices.csv`. If a statistics page looks stale (its EPS or revenue disagrees with the income statement, or the price is missing), say so and add a `note` for that company in `tools/companies_notes.py`.

For a new company, add a judgment entry to the matching `tools/companies_*.py`, applying `framework/value-investor.md`. Use `fin=True` for banks and insurers and `commodity=True` for commodity producers.

## Rules

- Every figure must trace to a source page; never estimate or carry numbers from memory.
- Judgment text must not state a number the data files do not support.
- Keep `framework/value-investor.md`, `tools/settings.json` (version) and the constants in `tools/build.py` in step.
- The site has no build step and no dependencies beyond Google Fonts and the `marked` CDN script.
