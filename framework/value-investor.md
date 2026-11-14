version: 2.5.0
updated: 2026-11-12

# Value Investor — the framework

Buy wonderful businesses at a sensible price. Business quality comes first and
price second: a cheap price never rescues a weak business, and a business that
cannot be understood goes in the too-hard pile.

Every assessment has three layers:

1. **The 4 M's** — Meaning, Moat, Management, Margin of safety. This decides the verdict.
2. **The evidence** — financial health, the ratio sheet and the rules of the road.
3. **Five investors' checklists** — the same company run through the published
   tests of Graham, Buffett, Lynch, Munger and Pabrai, as a second opinion.

Meaning, moat, industry, management and the growth assumption are analyst
judgment. Everything else is calculated from reported figures with the exact
rules below, so anyone can reproduce it.

## M1 — Meaning (understand the business)

Four questions, answered in plain language:

1. What does the company do?
2. How does it make money?
3. How will it keep making money?
4. How could it stop making money?

The spouse test: if what makes the company special cannot be explained in a
sentence or two, it probably is not special. Scored 0–10.

## M2 — Moat (durable competitive advantage)

A moat lets a company grow consistently, expand margins, fend off competitors
and raise prices. Sources:

- **Brand** — customers trust it and pay more for it.
- **Designated company** — the only, or one of the only, providers of an
  essential service in its area.
- **Intellectual property** — patents, trade secrets, proprietary software.
- **Scale, network effects and switching costs** — advantages that grow with size.

A moat only counts if it stops rivals from being a real threat. Rated **Wide**,
**Narrow** or **None**, and scored 0–10.

### Industry stability

Wonderful businesses are not in a technology war. Signs of one: products go out
of date within a few years; failing to innovate once loses customers; brand does
not drive the purchase. Steady innovation is fine. The danger is a business that
fails unless it out-innovates rivals every cycle, such as a chipmaker. Rated
**Stable**, **Steady change** or **Rapid change**, and scored 0–10.

## M3 — Management

Integrity, intelligence and energy, judged from the record: capital allocation,
returns on capital, candour, and growth in per-share value. Scored 0–10.

## M4 — Margin of safety

### Match the metric to the lifecycle stage

| Stage | Primary metric | Secondary metric |
| --- | --- | --- |
| 1 Startup | Price-to-sales | Price-to-gross-profit |
| 2 Hyper growth | Price-to-sales | Price-to-gross-profit |
| 3 Operating leverage | Forward P/E | Price-to-FCF |
| 4 Capital return | Trailing P/E | Trailing price-to-FCF |
| 5 Decline | Forward P/E | Price-to-FCF |

Reported alongside: trailing P/E, forward P/E, PEG, and the enterprise-value
multiples (EV/Sales, EV/EBITDA, EV/EBIT, EV/FCF). Enterprise value = market cap
+ total debt − cash. A PEG below 1 suggests growth is not fully priced in.

### Fair value

Fair value per share is the **average of two methods**. Each produces a low and
a high case; the mid-point of the averaged range is the fair value used for the
margin of safety. Where only one method applies, it is used alone.

**Method 1: owner cash flow** — a two-stage discounted cash flow:

- **Owner cash flow** = free cash flow minus stock-based pay. Paying staff in
  shares is a real cost to owners, and free cash flow adds it back, so it is
  deducted here. Where the data source does not report stock pay separately,
  nothing is deducted and the report says so.
- **Normalised** = median of the last three fiscal years and the trailing
  twelve months (TTM), so one unusual year does not drive the answer.
- Base-case growth *g* for years 1–5, *g*/2 for years 6–10, then 3% forever,
  discounted at 10%.
- Low case uses *g* − 3 points; high case *g* + 3 points.
- Levered FCF is valued against equity, so debt is reflected through interest.
- **Heavy expansion spending.** When capex runs at more than twice depreciation
  (utilities excepted), deducting all of it values the expansion at nothing.
  Owner cash flow is then operating cash flow minus depreciation minus
  stock-based pay, with depreciation standing in for upkeep. The all-capex
  figure is still shown as a **stress case** but is not in the average.
  Depreciation lags a spending surge, so this basis can flatter; that is why it
  is averaged with a second method.

**Method 2: Aswath Damodaran, cash flow to the firm** — a story turned into numbers:

| Input | Rule |
| --- | --- |
| Sales growth | The same base-case *g* (∓3 points) for years 1–5, fading in a straight line to 3% by year 10 |
| Operating margin | Held at the current EBIT margin (stock-based pay is already an expense in it) |
| Tax | 25% marginal rate |
| Reinvestment | Growth ÷ return on capital each year (ROIC, bounded 8–40%), Damodaran's link between growth and what it costs |
| Cost of equity | 10-year Treasury + beta × 4.5% equity risk premium. Beta is a proxy set by industry pace: Stable 0.85, Steady change 1.00, Rapid change 1.25 |
| Cost of debt | (10-year Treasury + 1.5 points) after tax |
| Cost of capital | Equity and debt costs weighted by market value |
| Terminal value | 3% growth (below the risk-free rate, as Damodaran requires); return on capital falls to the cost of capital plus 5 points for a wide moat, 2 for a narrow one, 0 for none |
| Equity value | Value of operations + cash − debt, per share |

The report also runs the model backwards: **the sales growth today's price
assumes**, at the current margin. Damodaran's point is that every price carries
a story; the reader should decide whether that story is plausible.

**Banks and insurers** — free cash flow is not meaningful, so they are valued on
book value with an excess-return model, which is also Damodaran's approach for
financial firms: justified price-to-book = (ROE − 3%) ÷ (required return − 3%), using
a normalised ROE (median of the last three fiscal years and TTM, capped at 25%)
and a required return of 11% (low case) to 9% (high case).

**Margin of safety** = (fair value − price) ÷ fair value.
**Target: at least 30%.** "Interesting below" is the price that delivers it.

Valuation score: 9 at ≥ 30% margin of safety, 8 at ≥ 20%, 7 at ≥ 10%, 6 at ≥ 0%,
5 at ≥ −15%, 4 at ≥ −30%, 3 at ≥ −50%, 2 at ≥ −70%, otherwise 1.

## The evidence

### Free cash flow & financial health

Nine checks over the last five fiscal years plus TTM:

| Check | Pass condition |
| --- | --- |
| Revenue trend | Positive growth, at most one down year |
| Net income trend | Positive growth, at most one down year |
| Net profit margin | At least 5% |
| Debt to assets | At most 0.40 (not applied to banks and insurers) |
| Shareholders' equity | Higher than five years ago, at most one dip |
| ROIC | At least 10% (return on equity for banks and insurers) |
| Free cash flow | Positive every year and higher than five years ago (not applied to banks and insurers) |
| Interest cover | Operating income at least 5x interest, or more cash than debt (not applied to banks and insurers) |
| Earnings backed by cash | Operating cash flow over five years at least equal to net income (not applied to banks and insurers) |

Score = checks passed ÷ checks that apply × 10.

Red flags: commodity-dependent revenue; not consistently generating free cash
flow; two or more down years in revenue; a loss-making year; no moat; a rapidly
changing industry; an Altman Z-score in the distress zone.

Some businesses trip a mechanical check for a good reason, such as negative
equity after decades of buybacks. Reports flag these in a note rather than
bending the rule.

### Ratio sheet

Every ratio a value investor checks, each against a yardstick. The yardsticks
describe a strong business; they inform the reader and do not change the score.

| Group | Ratio and yardstick |
| --- | --- |
| Profitability | Gross margin ≥ 40%; operating margin ≥ 15%; net margin ≥ 10%; free cash flow margin ≥ 10%; ROE ≥ 15%; ROIC ≥ 12%; return on assets ≥ 6% |
| Debt and solvency | Debt/equity ≤ 1.0x; debt/assets ≤ 0.40; net debt/EBITDA ≤ 2.5x; interest cover ≥ 5x; debt ≤ 4 years of free cash flow; current ratio ≥ 1.0; Altman Z ≥ 3.0 |
| Cash quality | Operating cash flow ≥ 100% of net income; free cash flow ≥ 80% of net income; capex ≤ 50% of operating cash flow; capex ÷ depreciation (reference); stock-based pay ≤ 10% of operating cash flow; Piotroski F-score ≥ 7 |
| Growth (annual rate) | Revenue ≥ 5%; EPS ≥ 7%; free cash flow ≥ 5%; book value per share (reference) |
| Returns to shareholders | Dividend yield (reference); payout ≤ 60% of earnings; dividends covered ≥ 1.5x by free cash flow; buyback yield (reference); falling share count; return on retained earnings ≥ 12% |
| Yield against bonds | Earnings yield, free cash flow yield after stock pay, and owner-earnings yield, each ≥ the 10-year Treasury yield |

Banks and insurers get a shorter sheet: net margin ≥ 15%, ROE ≥ 12%, return on
assets ≥ 1%, equity/assets ≥ 8%, growth in revenue, EPS and book value per
share, payout, share count, earnings yield and price-to-book.

**Not covered, because the data source does not provide it:** a ten-year record,
inventory and receivables turnover, the quick ratio, goodwill and tangible book
value, maintenance versus growth capex, and for banks the net interest margin,
efficiency ratio, CET1 ratio and loan-loss reserves. Read the annual report for
these before acting.

### Value 3.0 rules of the road

Do: look for a clear-cut competitive advantage; prefer a small share of a huge
market; avoid businesses whose best days are behind them, however cheap they
look. Don't: confuse a growing industry with a profitable one.

## The business in brief

Each report opens with three written answers, kept in `tools/profiles_*.py`:
what the company is, how it makes money, and how the market values the stock.
Under the third, the build adds the multiples that fit the company's type and
the median of its sector peers on this site:

| Type | Measures shown |
| --- | --- |
| Bank, insurer or asset manager | P/E, price to book, return on equity, dividend yield |
| Real estate investment trust | Price to operating cash flow (stand-in for price to FFO), EV/EBITDA, dividend yield, P/E |
| Cyclical or commodity business | EV/EBITDA, P/E, free cash flow yield, dividend yield |
| Growth company (stages 1–2) | Price to sales, forward P/E, P/E, EV/EBITDA |
| Established operating business | P/E, forward P/E, price to free cash flow, EV/EBITDA, dividend yield |

A sector median is shown only when at least three companies in the sector have
the figure.

Two charts sit above the table. **Peer bars** rank the company's main multiple
against its peer group: the same sector and type where at least four companies
share both (banks with banks, chipmakers with chipmakers), otherwise the whole
sector. **The 52-week range** shows where today's price sits between the year's
low and high.

**Analysts' average price target** is shown on the fair value chart and in a
"Wall Street's view" note, for comparison only. Sell-side targets usually
assume today's multiples hold; this site's fair value rests only on the cash the
business is expected to produce, so the two can differ widely. The reported
five-year beta is shown for reference but is not used in the cost of capital:
single-stock regression betas are noisy, and Damodaran recommends industry
betas.

## Five investors' checklists

A test can pass, fail or not apply.

### Benjamin Graham — the defensive investor

| Test | Pass condition |
| --- | --- |
| Strong current position | Current ratio ≥ 2.0 |
| Earnings stability | No loss in the last five years (Graham asked for ten) |
| Dividend record | Pays a dividend |
| Earnings growth | EPS up at least 15% in four years (Graham asked for a third in ten) |
| Moderate P/E | Price ≤ 15x average earnings of the last three years |
| Graham number | P/E × P/B ≤ 22.5, i.e. price ≤ √(22.5 × EPS × book value per share) |
| Earnings beat bonds | Earnings yield ≥ 10-year Treasury yield |
| No financial distress | Altman Z-score ≥ 3.0 |

### Warren Buffett — owner economics

| Test | Pass condition |
| --- | --- |
| Owner-earnings yield beats bonds | (Net income + depreciation − capex) ÷ market cap ≥ 10-year Treasury yield (earnings yield for banks) |
| High return on equity without heavy debt | ROE ≥ 15% and debt/equity ≤ 1.0 (ROIC ≥ 15% if equity is negative) |
| Retained earnings put to good use | EPS gained ÷ earnings per share retained over the period ≥ 12% |
| Pricing power | Gross margin ≥ 40% and within a 6-point range over five years |
| Low capital intensity | Capex ≤ 50% of net income |
| Light interest burden | Interest under 15% of operating income (coverage ≥ 6.7x) |
| Debt repayable from earnings | Total debt ≤ 4 years of net income |
| Shrinking share count | Fewer shares than four years ago |

Owner earnings follow Buffett's 1986 definition: net income plus depreciation
and amortisation, minus capital spending. Maintenance capex is not disclosed
separately, so all capex is deducted, which is conservative. Buffett's
one-dollar test compares retained earnings with the market value they created;
without a price history, the return on retained earnings stands in for it.

### Peter Lynch — know what you own

Lynch first sorted every stock into a category, because the category decides
what to expect and when to sell:

| Category | Rule used here |
| --- | --- |
| Fast grower | EPS growing ≥ 20% a year on sales growing ≥ 10% |
| Stalwart | Between the slow and the fast growers |
| Slow grower | EPS growing under 6% a year, or sales growing under 3% |
| Cyclical | Commodity producers and a named list of cycle-driven businesses |
| Turnaround | Loss-making now, or in two or more of the last five years |
| Asset play | Valued on what it owns (Berkshire Hathaway) |

| Test | Pass condition |
| --- | --- |
| The two-minute drill | Meaning score ≥ 8 (≤ 6 fails) |
| Not a hot stock in a hot industry | Industry is not "Rapid change" |
| Growth at a reasonable price | PEG ≤ 1.0 (above 2.0 fails) |
| Growth plus yield against P/E | (EPS growth %, capped at 30, + dividend yield %) ÷ P/E ≥ 1.5 (below 1.0 fails) |
| Consistent earnings | EPS higher than four years ago, at most one down year |
| Strong balance sheet | Net cash, or debt ≤ 0.5x equity (above 1.0x fails) |
| Dividend is safe | Payout ≤ 60% of earnings |

### Charlie Munger — inversion and incentives

| Test | Pass condition |
| --- | --- |
| Inside the circle of competence | Meaning score ≥ 8 (≤ 6 fails) |
| Not a technology war | Industry is not "Rapid change" |
| Skin in the game | Insiders own ≥ 1% |
| No dilution of owners | Share count flat or falling over the last year |
| Modest stock-based pay | Stock pay ≤ 10% of operating cash flow |
| Earnings are real cash | Operating cash flow ≥ net income over five years |
| Accounting quality check | Piotroski F-score ≥ 7 (≤ 3 fails) |

Plus the inversion: a short list of how the business could die.

### Mohnish Pabrai — Dhandho

| Test | Pass condition |
| --- | --- |
| A simple, existing business | Meaning score ≥ 8 |
| Slow rate of change | Industry rated Stable |
| Durable moat | Wide moat |
| Out of favour | Share price down 20% or more over 52 weeks |
| Bought well below value | Margin of safety ≥ 30% |
| Low risk of permanent loss | Net cash, or debt ≤ 4 years of earnings |
| Heads I win, tails I don't lose much | Upside to the high-case value is at least 3x the downside to the low-case value |

## Overall score and verdict

**Overall score (0–100)** = weighted pillar scores × 10. Weights: Moat 25%,
Financial health 20%, Margin of safety 20%, Management 15%, Meaning 10%,
Industry 10%. The checklists and the ratio sheet do not change the score; they are a second opinion.

**Verdict**, tested in this order:

1. **Too hard** — the industry is changing rapidly, or the meaning score is 6 or
   below, or the financials are in transition. No verdict on price.
2. **Pass** — fails the quality test: no moat, commodity-driven cash flows,
   financial-health score below 5, no free cash flow (including none left after
   stock-based pay), or best days behind it.
   Price does not matter.
3. **Buy zone** — passes the quality test and the margin of safety is at least 30%.
4. **Watchlist** — passes the quality test, but the price is too high.

## Changelog

- 2.5.0 (2026-11-14) — Each report is now a nine-part story: one sentence with
  strengths, risks and swing factors; what it is; how it makes money (with the
  split of each dollar of sales); whether it can keep making money; the numbers
  (with where the cash goes); how it is valued; fair value; bull and bear cases
  led by calculated figures; and second opinions. The ratio sheet and checklist
  tests fold away until opened.
- 2.4.0 (2026-11-14) — "How the stock is valued" now charts the company's main
  multiple against its peer group and shows where the price sits in its 52-week
  range. The fair value chart adds the analysts' average price target for
  comparison (not used in the fair value). Each chart states its conclusion as a
  headline. New monthly input: `tools/market.csv`.
- 2.3.0 (2026-11-14) — Every report opens with "The business in brief": what
  the company is, how it makes money, and how the stock is valued, with the
  multiples that matter for its type (bank, REIT, cyclical, growth or
  established business) set against the median of its sector peers on the site.
- 2.2.0 (2026-11-12) — Fair value is now its own section and is the average of
  two methods: owner cash flow and Damodaran's cash flow to the firm, with the
  growth rate implied by the price. Companies in a heavy expansion phase are
  valued with capex held at depreciation; the all-capex figure is shown as a
  stress case.
- 2.1.0 (2026-11-12) — Added Peter Lynch's checklist and stock categories, a
  full ratio sheet, and cash-flow-statement data (depreciation, stock-based pay,
  dividends, buybacks). Intrinsic value now deducts stock-based pay. Financial
  health grew from seven checks to nine (interest cover; earnings backed by
  cash). Buffett's test uses true owner earnings and adds return on retained
  earnings; Graham's P/E uses three-year average earnings; Munger's checklist
  adds stock pay and cash-backed earnings.
- 2.0.0 (2026-11-12) — Renamed Value Investor. Expanded to the S&P 100 plus Waste
  Management and Sherwin-Williams. Added the four masters' lenses, the Too hard
  verdict, the best-days-behind-it rule, and book-value valuation for banks.
- 1.1.0 (2026-11-12) — Static website edition with written calculation rules.
- 1.0.0 (2026-11-12) — First web version, consolidated from the Value Investor
  project notes.
