"""Value Investor: turn sourced figures + analyst judgments into report files.

Inputs   tools/data/<TICKER>.txt   figures (S = statistics, F = 5 fiscal years, B = balance sheet, C = cash flow statement)
         tools/prices.csv          latest prices (edit monthly; overrides the S line)
         tools/settings.json       as-of date, 10-year Treasury yield, framework version
         tools/companies*.py       analyst judgments
Output   data/index.json, data/companies/<TICKER>.json

Every number on the site is either a sourced figure or calculated here with the
rules in framework/value-investor.md, so results are reproducible.
Run:  python3 tools/build.py
"""
import csv, json, math, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from companies import Q  # noqa: E402
from profiles import PROFILE  # noqa: E402
from summaries import S as SUMMARY  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data")
CFG = json.load(open(os.path.join(HERE, "settings.json")))
AS_OF, TY, VERSION = CFG["as_of"], CFG["treasury_10y"], CFG["framework_version"]

# Thresholds (mirror framework/value-investor.md)
MARGIN_MIN, DEBT_ASSETS_MAX, ROIC_MIN, MOS_TARGET = 5.0, 0.40, 10.0, 30.0
DISCOUNT, TERMINAL = 0.10, 0.03
WEIGHTS = dict(meaning=0.10, moat=0.25, industry=0.10, management=0.15, financial_health=0.20, valuation=0.20)
STAGES = {1: "1 · Startup", 2: "2 · Hyper growth", 3: "3 · Operating leverage", 4: "4 · Capital return", 5: "5 · Decline"}
MONEY = {"shares", "cash", "debt", "equity", "rev", "ni", "ebitda", "ebit", "ocf", "capex", "fcf"}


# ---------- reading the data files ----------
def val(s):
    if s is None: return None
    s = s.strip().replace("$", "").replace(",", "").replace("+", "")
    if s.lower() in ("n/a", "", "-", "na"): return None
    mult = 1.0
    if s.endswith("%"): s = s[:-1]
    elif s[-1] in "TBMK": mult = {"T": 1e6, "B": 1e3, "M": 1.0, "K": 1e-3}[s[-1]]; s = s[:-1]
    try: return float(s) * mult
    except ValueError: return None


def load(t):
    s, raw, hist, bs, cf = {}, {}, [], [], []
    for line in open(os.path.join(HERE, "data", t.replace(".", "-") + ".txt")):
        line = line.strip()
        if line.startswith("S "):
            for kv in line[2:].split("; "):
                k, v = kv.split("=", 1); raw[k] = v
                s[k] = v if k in ("date", "price_note") else val(v)
        elif line.startswith("F "):
            p = line[2:].split(","); hist.append((p[0],) + tuple(val(x) for x in p[1:6]))
        elif line.startswith("B "):
            p = line[2:].split(","); bs.append((p[0],) + tuple(val(x) for x in p[1:4]))
        elif line.startswith("C "):  # label, D&A, stock-based pay, operating cash flow, capex, dividends paid, buybacks
            p = line[2:].split(","); cf.append((p[0],) + tuple(val(x) for x in p[1:7]))
    return s, hist, bs, cf


MARKET = {}  # 52-week range, reported beta, analyst consensus: tools/market.csv (refresh monthly with prices)
_mk = os.path.join(HERE, "market.csv")
if os.path.exists(_mk):
    for row in csv.DictReader(open(_mk)):
        f_ = lambda k: None if row[k] in ("", "n/a") else float(row[k])
        MARKET[row["ticker"]] = dict(low52=f_("low52"), high52=f_("high52"), beta=f_("beta"), rating=None if row["rating"] in ("", "n/a") else row["rating"],
                                     target=f_("target"), as_of=row["as_of"],
                                     chg52=f_("chg52") if "chg52" in row else None)

PRICES = {}
_pp = os.path.join(HERE, "prices.csv")
if os.path.exists(_pp):
    for row in csv.DictReader(open(_pp)):
        if row.get("price"): PRICES[row["ticker"].strip()] = (float(row["price"]), row.get("date", "").strip())


# ---------- helpers ----------
def b(v):
    if v is None: return "n/a"
    a = abs(v)
    s = f"${a/1e6:.2f}T" if a >= 1e6 else f"${a/1e3:.1f}B" if a >= 1e3 else f"${a:.0f}M"
    return ("-" if v < 0 else "") + s


def cagr(first, last, years):
    if first is None or last is None or first <= 0 or last <= 0 or years <= 0: return None
    return ((last / first) ** (1 / years) - 1) * 100


def downs(v): return sum(1 for a, c in zip(v, v[1:]) if c < a)
def chk(name, value, threshold, ok): return dict(name=name, value=value, threshold=threshold, **{"pass": ok})
def x(v, d=1): return "n/a" if v is None else f"{v:.{d}f}"
def pct(v, d=1): return "n/a" if v is None else f"{v:.{d}f}%"


def dcf(fcf, g, shares):
    """Two-stage: g for years 1-5, g/2 for years 6-10, then 3% terminal, discounted at 10%."""
    pv, f = 0.0, fcf
    for yr in range(1, 11):
        f *= 1 + (g if yr <= 5 else g / 2) / 100
        pv += f / (1 + DISCOUNT) ** yr
    pv += f * (1 + TERMINAL) / (DISCOUNT - TERMINAL) / (1 + DISCOUNT) ** 10
    return pv / shares


# ---- Damodaran: free cash flow to the firm, from a growth story to a number ----
TAX, ERP, DEBT_SPREAD = 0.25, 4.5, 1.5            # marginal tax rate, equity risk premium, spread on debt (points)
BETA = {"Stable": 0.85, "Steady change": 1.00, "Rapid change": 1.25}  # proxy: the data source carries no beta
EXCESS = {"Wide": 5.0, "Narrow": 2.0, "None": 0.0}  # return above the cost of capital a moat keeps for good (points)


def fcff_value(rev, margin, g, roc, wacc, roc_term, cash, debt, shares):
    """Sales grow g% for five years, fade to 3% by year ten. Reinvestment each year = growth / return on capital."""
    pv, r = 0.0, rev
    for yr in range(1, 11):
        gy = g if yr <= 5 else g + (TERMINAL * 100 - g) * (yr - 5) / 5
        r *= 1 + gy / 100
        nopat = r * margin * (1 - TAX)
        pv += nopat * (1 - min(max(gy / roc, 0.0), 0.9)) / (1 + wacc) ** yr
    nopat_t = r * (1 + TERMINAL) * margin * (1 - TAX)
    tv = nopat_t * (1 - TERMINAL * 100 / roc_term) / (wacc - TERMINAL)
    return (pv + tv / (1 + wacc) ** 10 + cash - debt) / shares


REITS = {"AMT", "SPG"}


def market_block(t, price, pdate, fair):
    """Where the price sits in its 52-week range, and what the analysts' average target implies, next to this site's fair value."""
    m = MARKET.get(t)
    if not m: return None
    lo, hi = m["low52"], m["high52"]
    out = dict(rating=m["rating"], target=m["target"], beta=m["beta"], as_of=m["as_of"], low52=lo, high52=hi, range_pos=None, below_high=None,
               target_vs_price=None, target_vs_fair=None)
    if lo and hi:
        lo, hi = min(lo, price), max(hi, price)  # the range must contain the price used here
        out.update(low52=lo, high52=hi, range_pos=round((price - lo) / (hi - lo) * 100) if hi > lo else None,
                   below_high=round((1 - price / hi) * 100, 1), above_low=round((price / lo - 1) * 100, 1))
    if m["target"]:
        out["target_vs_price"] = round((m["target"] / price - 1) * 100, 1)
        if fair: out["target_vs_fair"] = round((m["target"] / fair - 1) * 100, 1)
    return out


def profile_block(t, q, fin, s, price, pe, pb, roe, dy, mcap, ev, rev, pfcf, fcf_ttm, ocf):
    """What it is, how it makes money, how the stock is valued: written profile plus the multiples that matter for its type."""
    what, money, valued = PROFILE[t]
    ebitda = s.get("ebitda")
    ev_e = ev / ebitda if ebitda and ebitda > 0 else None
    fcfy = fcf_ttm / mcap * 100 if fcf_ttm is not None and not fin else None
    M = lambda key, label, v, unit, note: dict(key=key, label=label, value=None if v is None else round(v, 2), unit=unit, note=note)
    pe_m = M("pe", "Price / earnings", pe, "x", "Trailing twelve months")
    fpe_m = M("fpe", "Price / forward earnings", s.get("fpe"), "x", "Next twelve months, analyst estimates")
    dy_m = M("dy", "Dividend yield", dy, "%", "Trailing dividends ÷ price")
    if fin:
        kind = "Bank, insurer or asset manager"
        ms = [pe_m, M("pb", "Price / book value", pb, "x", "Judge against return on equity"), M("roe", "Return on equity", roe, "%", "Trailing twelve months"), dy_m]
    elif t in REITS:
        kind = "Real estate investment trust"
        ms = [M("pocf", "Price / operating cash flow", mcap / ocf if ocf and ocf > 0 else None, "x", "Stand-in for price / FFO"),
              M("evebitda", "EV / EBITDA", ev_e, "x", "Enterprise value includes debt"), dy_m, pe_m]
    elif q.get("commodity") or t in CYCLICAL:
        kind = "Cyclical or commodity business"
        ms = [M("evebitda", "EV / EBITDA", ev_e, "x", "Judge at mid-cycle, not peak"), pe_m, M("fcfy", "Free cash flow yield", fcfy, "%", "Free cash flow ÷ market value"), dy_m]
    elif int(q["stage"]) <= 2:
        kind = "Growth company"
        ms = [M("ps", "Price / sales", mcap / rev, "x", "Used when profits are still small"), fpe_m, pe_m, M("evebitda", "EV / EBITDA", ev_e, "x", "Enterprise value includes debt")]
    else:
        kind = "Established operating business"
        ms = [pe_m, fpe_m, M("pfcf", "Price / free cash flow", pfcf, "x", "Before deducting stock-based pay"), M("evebitda", "EV / EBITDA", ev_e, "x", "Enterprise value includes debt"), dy_m]
    return dict(what=what, money=money, valued=valued, kind=kind, metrics=ms)


def val_score(mos):
    if mos is None: return 2
    for cut, sc in [(30, 9), (20, 8), (10, 7), (0, 6), (-15, 5), (-30, 4), (-50, 3), (-70, 2)]:
        if mos >= cut: return sc
    return 1


# Lynch's cyclicals: earnings follow the economic or product cycle, so a low P/E can mark the peak
CYCLICAL = {"CAT", "DE", "GM", "MU", "LRCX", "AMAT", "AMD", "INTC", "TXN", "QCOM", "XOM", "CVX", "COP", "GS", "MS", "BA",
            "FDX", "UPS", "UNP", "CSX", "NXPI", "NSC", "ODFL", "PCAR", "CMI", "URI", "ROK", "MCHP", "GLW", "EMR", "MMM", "HON", "GE", "GEV", "KLAC", "ADI"}
LYNCH = {
    "Fast grower": "Earnings compounding at 20% or more on sales growing at least 10%. Lynch's favourite hunting ground, provided the growth is not paid for twice: check the PEG.",
    "Stalwart": "A large company growing earnings at a steady pace, between the slow and the fast growers. Lynch bought these for a 30–50% gain and for protection in recessions, then rotated.",
    "Slow grower": "Earnings growing more slowly than 6% a year, or sales barely growing. Lynch held these only for the dividend, so the payout and its safety matter most.",
    "Cyclical": "Earnings rise and fall with the cycle. Lynch's warning: a low P/E on peak earnings is a signal to sell, not to buy. Timing matters more than the multiple.",
    "Turnaround": "Loss-making now, or in two or more of the last five years. Lynch asked one question first: does it have the cash to survive until the fix works?",
    "Asset play": "The value sits in what the company owns rather than what it earns. Lynch compared the price with the assets per share.",
}


def lens(tests):
    app = [t for t in tests if t["pass"] is not None]
    return dict(passed=sum(1 for t in app if t["pass"]), total=len(app), tests=tests)


# ---------- one company ----------
def build(t):
    s, hist, bs, cf = load(t)
    q = Q[t]
    fin = bool(q.get("fin"))
    price, pdate = s["price"], s.get("date")
    stale52 = False
    if t in PRICES and abs(PRICES[t][0] - price) > 1e-9:
        ratio = PRICES[t][0] / price
        price, pdate = PRICES[t][0], PRICES[t][1] or pdate
        for k in ("fpe", "peg"):
            if s.get(k) is not None: s[k] *= ratio
        stale52 = True
    elif t in PRICES and PRICES[t][1]:
        pdate = PRICES[t][1]
    shares, eps = s["shares"], s.get("eps")
    mcap = price * shares
    cash, debt, equity = s.get("cash") or 0.0, s.get("debt") or 0.0, s.get("equity")
    rev, ni, fcf_ttm = s["rev"], s["ni"], s.get("fcf")
    ev = mcap + debt - cash
    pe = price / eps if eps and eps > 0 else None
    bvps = equity / shares if equity is not None else None
    pb = mcap / equity if equity and equity > 0 else None
    pfcf = mcap / fcf_ttm if fcf_ttm and fcf_ttm > 0 else None
    pm = ni / rev * 100
    roe = ni / equity * 100 if equity and equity > 0 else None
    roic = s.get("roic")
    gm_now = s.get("gm")
    dy = (s.get("dps") or 0) / price * 100
    c52 = MARKET[t]["chg52"] if t in MARKET and MARKET[t].get("chg52") is not None else (None if stale52 else s.get("c52"))

    revs = [h[1] for h in hist]; nis = [h[3] for h in hist]; fcfs = [h[5] for h in hist]
    gms = [h[2] for h in hist if h[2] is not None]; epss = [h[4] for h in hist]
    yrs = len(hist) - 1
    eqs = [r[3] for r in bs if r[3] is not None]
    last_bs = next((r for r in reversed(bs) if r[1] and r[2] is not None), None)
    d_a = last_bs[2] / last_bs[1] if last_bs else None

    # ----- Cash flow statement: stock pay, depreciation, dividends, buybacks -----
    cfd = {r[0]: r for r in cf}
    last_cf = cf[-1] if cf else None  # TTM column when shown, otherwise the latest fiscal year
    def cfa(i): return None if last_cf is None or last_cf[i] is None else abs(last_cf[i])
    da_now, sbc_now, div_now, bb_now = cfa(1), cfa(2), cfa(5), cfa(6)
    sbc_reported = bool(cf) and any(r[2] is not None for r in cf)
    def sbc_for(lbl):
        r = cfd.get(lbl)
        return (r[2] if r and r[2] is not None else sbc_now) or 0.0
    fcfs_adj = [None if h[5] is None else h[5] - sbc_for(h[0]) for h in hist]  # free cash flow after stock-based pay
    fcf_ttm_adj = None if fcf_ttm is None else fcf_ttm - (sbc_now or 0.0)
    capex = abs(s["capex"]) if s.get("capex") is not None else None
    ocf = s.get("ocf")
    cum = [(cfd[h[0]][3], h[3], h[5]) for h in hist if h[0] in cfd and cfd[h[0]][3] is not None and h[3] is not None]
    cum_ocf, cum_ni = sum(c[0] for c in cum), sum(c[1] for c in cum)
    conv_ocf = cum_ocf / cum_ni * 100 if len(cum) >= 3 and cum_ni > 0 else None
    tot_ni, tot_fcf = sum(n for n in nis if n is not None), sum(f for f in fcfs if f is not None)
    conv_fcf = tot_fcf / tot_ni * 100 if tot_ni > 0 and not fin else None
    cr, ic, sc, ins, fsc = s.get("cr"), s.get("ic"), s.get("sc"), s.get("ins"), s.get("f")
    sh0 = hist[0][3] / hist[0][4] if hist[0][3] and hist[0][4] and hist[0][3] > 0 and hist[0][4] > 0 else None
    sh1 = hist[-1][3] / hist[-1][4] if hist[-1][3] and hist[-1][4] and hist[-1][3] > 0 and hist[-1][4] > 0 else None
    sh_chg = (sh1 / sh0 - 1) * 100 if sh0 and sh1 else None

    # ----- Financial health -----
    NA_FIN = "Not meaningful for a bank or insurer"
    rev_c, ni_c = cagr(revs[0], revs[-1], yrs), cagr(nis[0], nis[-1], yrs)
    fcf_ok = None if fin else bool(fcf_ttm is not None and all(f is not None and f > 0 for f in fcfs) and fcf_ttm > fcfs[0])
    ret, ret_name = (roe, "Return on equity") if fin else (roic, "ROIC")
    if fin: cov_ok, cov_txt = None, NA_FIN
    elif ic is not None: cov_ok, cov_txt = ic >= 5, f"Operating income covers interest {ic:.1f}x"
    elif cash >= debt: cov_ok, cov_txt = True, "More cash than debt"
    else: cov_ok, cov_txt = None, "n/a"
    if fin: cq_ok, cq_txt = None, NA_FIN
    elif conv_ocf is not None: cq_ok, cq_txt = conv_ocf >= 100, f"Operating cash flow was {conv_ocf:.0f}% of net income over {len(cum)} fiscal years"
    elif len(cum) >= 3: cq_ok, cq_txt = cum_ocf > 0, "Cumulative net loss over the period"
    else: cq_ok, cq_txt = None, "n/a"
    checks = [
        chk("Revenue trend", f"{rev_c:+.1f}% a year, {downs(revs)} down year(s)" if rev_c is not None else "n/a", "Rising, at most one down year",
            bool(rev_c and rev_c > 0 and downs(revs) <= 1)),
        chk("Net income trend", f"{ni_c:+.1f}% a year, {downs(nis)} down year(s)" if ni_c is not None else "A loss at the start or end of the period",
            "Rising, at most one down year", bool(ni_c and ni_c > 0 and downs(nis) <= 1)),
        chk("Net profit margin", pct(pm), f"≥ {MARGIN_MIN:.0f}%", pm >= MARGIN_MIN),
        chk("Debt to assets", NA_FIN if fin else x(d_a, 2), f"≤ {DEBT_ASSETS_MAX:.2f}", None if fin or d_a is None else d_a <= DEBT_ASSETS_MAX),
        chk("Shareholders' equity", f"{b(eqs[0])} → {b(eqs[-1])}, {downs(eqs)} dip(s)", "Rising, at most one dip", eqs[-1] > eqs[0] and downs(eqs) <= 1),
        chk(ret_name, pct(ret), f"≥ {ROIC_MIN:.0f}%", None if ret is None else ret >= ROIC_MIN),
        chk("Free cash flow", NA_FIN if fin else f"{b(fcfs[0])} → {b(fcfs[-1])}; TTM {b(fcf_ttm)}", "Positive every year and rising", fcf_ok),
        chk("Interest cover", cov_txt, "Operating income ≥ 5x interest", cov_ok),
        chk("Earnings backed by cash", cq_txt, "Operating cash flow ≥ net income", cq_ok),
    ]
    applicable = [c for c in checks if c["pass"] is not None]
    fin_score = round(10 * sum(c["pass"] for c in applicable) / len(applicable))

    z = s.get("z")
    payback = debt / ni if ni and ni > 0 else None
    red = []
    if q.get("commodity"): red.append("Revenue depends on commodity prices, so free cash flow is not predictable.")
    if not fin and (fcf_ttm is None or fcf_ttm <= 0 or min(f for f in fcfs if f is not None) <= 0): red.append("Not consistently generating free cash flow.")
    if downs(revs) >= 2: red.append("Inconsistent revenue: two or more down years in five.")
    if any(n is not None and n < 0 for n in nis) or ni < 0: red.append("At least one loss-making year in the period.")
    if q["moat"][0] == "None": red.append("No durable moat.")
    if q["ind"][0] == "Rapid change": red.append("Rapidly changing industry.")
    if z is not None and z < 1.8 and not fin: red.append(f"Altman Z-score of {z:.2f} is in the distress zone (below 1.8).")

    # ----- Valuation -----
    norm = None
    iv_lo = iv_hi = None
    methods, dam, stress = [], None, None
    def M(name, lo_, hi_, basis): methods.append(dict(name=name, low=round(lo_, 2), high=round(hi_, 2), basis=basis))
    if q.get("too_hard"):
        method = "No valuation: " + q["too_hard"]
    elif fin:
        if q.get("pb_low"):
            lo_m, hi_m = q["pb_low"], q["pb_high"]
            method = f"Book value per share (${bvps:,.0f}) × {lo_m}–{hi_m}. Reported earnings swing with investment marks, so a judgment range on book value is used."
        else:
            eq_by = {r[0]: r[3] for r in bs}
            roes = [h[3] / eq_by[h[0]] for h in hist[-3:] if eq_by.get(h[0]) and eq_by[h[0]] > 0 and h[3] is not None] + ([roe / 100] if roe else [])
            avg = min(max(statistics.median(roes), 0.0), 0.25)
            lo_m, hi_m = max((avg - TERMINAL) / (0.11 - TERMINAL), 0), max((avg - TERMINAL) / (0.09 - TERMINAL), 0)
            method = (f"Banks are valued on book value, not free cash flow. Justified price-to-book = (ROE − 3% growth) ÷ (required return − 3%), "
                      f"using a normalised ROE of {avg*100:.1f}% (median of the last three fiscal years and TTM, capped at 25%) and a required return of 11% (low) to 9% (high): "
                      f"{lo_m:.2f}–{hi_m:.2f} × book value per share of ${bvps:,.2f}.")
        iv_lo, iv_hi = bvps * lo_m, bvps * hi_m
        M("Book value range" if q.get("pb_low") else "Excess-return model on book value", iv_lo, iv_hi,
          f"Book value per share ${bvps:,.2f} × {lo_m:.2f}–{hi_m:.2f}. This is how Damodaran values banks and insurers: equity is worth book value plus the returns earned above the cost of equity.")
    else:
        pool = [f for f in fcfs_adj[-3:] if f is not None] + ([fcf_ttm_adj] if fcf_ttm_adj is not None else [])
        norm = (q["norm_fcf"] - (sbc_now or 0.0)) if q.get("norm_fcf") else (statistics.median(pool) if pool else None)
        sbc_txt = (f"free cash flow after deducting stock-based pay (about {b(sbc_now)} a year), which is a real cost to owners" if sbc_reported and sbc_now
                   else "free cash flow (stock-based pay is not reported separately by the data source, so none is deducted)")
        g = q.get("g")
        g_lo, g_hi = (max(g - 3, 0), g + 3) if g is not None else (None, None)
        # Heavy growth spending: when capex runs at more than twice depreciation, deducting all of it values the
        # expansion at nothing. Owner cash is then measured with capex held at depreciation (a maintenance proxy).
        heavy = bool(capex and da_now and capex > 2 * da_now and q["sector"] != "Utilities" and len(cf) >= 3)
        own = norm
        if heavy:
            mpool = [r[3] - r[1] - (r[2] or 0.0) for r in cf[-4:] if r[3] is not None and r[1] is not None]
            own = statistics.median(mpool) if mpool else norm
        if g is not None and own is not None and own > 0:
            o_lo, o_hi = dcf(own, g_lo, shares), dcf(own, g_hi, shares)
            if heavy:
                M("Owner cash flow, capex held at depreciation", o_lo, o_hi,
                  f"{b(own)} a year: operating cash flow less depreciation and stock-based pay (median of the last three fiscal years and TTM). "
                  f"Capex is running at {capex/da_now:.1f}x depreciation, so most of it is expansion, not upkeep.")
                if norm is not None and norm > 0:
                    stress = dict(low=round(dcf(norm, g_lo, shares), 2), high=round(dcf(norm, g_hi, shares), 2),
                                  basis=f"If the expansion spending never earns a return: {b(norm)} a year after deducting all capex and stock-based pay.")
                else:
                    stress = dict(low=None, high=None, basis="If the expansion spending never earns a return, no cash is left for owners after capex and stock-based pay.")
            else:
                M("Owner cash flow", o_lo, o_hi, f"{b(own)} a year: free cash flow less stock-based pay (median of the last three fiscal years and TTM"
                  f"{'; adjusted' if q.get('norm_fcf') else ''}).")
        norm = own
        # Damodaran FCFF
        ebit = s.get("ebit")
        if g is not None and ebit and ebit > 0:
            beta = BETA[q["ind"][0]]
            ke, kd = TY + beta * ERP, (TY + DEBT_SPREAD) * (1 - TAX)
            wd = debt / (debt + mcap)
            wacc = (ke * (1 - wd) + kd * wd)
            roc = min(max(roic if roic is not None else 12.0, 8.0), 40.0)
            roc_t = wacc + EXCESS[q["moat"][0]]
            margin = ebit / rev
            fv = lambda gg: fcff_value(rev, margin, gg, roc, wacc / 100, roc_t, cash, debt, shares)
            d_lo, d_hi = fv(g_lo), fv(g_hi)
            if d_hi > 0:
                d_lo = max(d_lo, 0.0)
                M("Damodaran: cash flow to the firm", d_lo, d_hi,
                  f"Sales grow {g_lo}–{g_hi}% for five years, fading to 3%; operating margin held at {margin*100:.0f}%; cost of capital {wacc:.1f}%. Cash added, debt subtracted.")
                a_, z_ = -20.0, 60.0  # what growth does today's price need? (bisection)
                if fv(a_) < price < fv(z_):
                    for _ in range(50):
                        m_ = (a_ + z_) / 2
                        if fv(m_) < price: a_ = m_
                        else: z_ = m_
                    implied = round((a_ + z_) / 2, 1)
                else: implied = None
                rev10 = rev
                for yr in range(1, 11): rev10 *= 1 + (g if yr <= 5 else g + (TERMINAL * 100 - g) * (yr - 5) / 5) / 100
                dam = dict(growth=g, growth_low=g_lo, growth_high=g_hi, margin=round(margin * 100, 1), tax=TAX * 100, roc=round(roc, 1),
                           reinvestment=round(min(max(g / roc, 0), 0.9) * 100), beta=beta, cost_of_equity=round(ke, 1), cost_of_debt=round(kd, 1),
                           debt_weight=round(wd * 100), cost_of_capital=round(wacc, 1), terminal_growth=TERMINAL * 100, terminal_roc=round(roc_t, 1),
                           revenue_now=b(rev), revenue_year10=b(rev10), low=round(d_lo, 2), high=round(d_hi, 2), implied_growth=implied,
                           implied_note=None if implied is not None else ("Today's price is below the value even with sales shrinking 20% a year." if price <= fv(a_) else "No growth rate up to 60% a year justifies today's price."))
        if methods:
            iv_lo = sum(m_["low"] for m_ in methods) / len(methods)
            iv_hi = sum(m_["high"] for m_ in methods) / len(methods)
            method = ("Fair value is the average of " + ("two methods" if len(methods) == 2 else "the one method that applies") + ": "
                      + " ".join(f"({i+1}) {m_['name']}: {m_['basis']}" for i, m_ in enumerate(methods))
                      + " The owner cash flow method grows the cash for five years, then at half that rate, 3% after year ten, discounted at 10%."
                      + (f" {sbc_txt[0].upper() + sbc_txt[1:]}." if not (sbc_reported and sbc_now) else " Stock-based pay is deducted because it is a real cost to owners."))
            if q.get("norm_note"): method += " " + q["norm_note"]
        else:
            method = "No valuation: neither owner cash flow nor operating income is positive, so there is nothing to discount."
    has_iv = iv_lo is not None and iv_hi and iv_hi > 0
    iv_mid = (iv_lo + iv_hi) / 2 if has_iv else None
    mos = (iv_mid - price) / iv_mid * 100 if has_iv else None
    v_score = val_score(mos)

    if fin:
        multiples = [("P/E", pe), ("Forward P/E", s.get("fpe")), ("P/B", pb), ("P/S", mcap / rev)]
        prim, sec = ("Trailing P/E", pe), ("Price-to-book", pb)
    else:
        multiples = [("EV/Sales", ev / rev), ("EV/EBITDA", ev / s["ebitda"] if s.get("ebitda") and s["ebitda"] > 0 else None),
                     ("EV/EBIT", ev / s["ebit"] if s.get("ebit") and s["ebit"] > 0 else None), ("P/E", pe),
                     ("EV/FCF", ev / fcf_ttm if fcf_ttm and fcf_ttm > 0 else None), ("P/FCF", pfcf), ("P/B", pb)]
        st = q["stage"]
        if st <= 2:
            prim = ("Trailing P/S (forward not available)", mcap / rev)
            sec = ("Trailing P/Gross profit", mcap / (rev * gm_now / 100) if gm_now else None)
        elif st == 4: prim, sec = ("Trailing P/E", pe), ("Trailing P/FCF", pfcf)
        else: prim, sec = ("Forward P/E", s.get("fpe")), ("P/FCF", pfcf)

    # ----- Scores and verdict -----
    scores = dict(meaning=q["ms"], moat=q["moat"][2], industry=q["ind"][1], management=q["mg"][0], financial_health=fin_score, valuation=v_score)
    overall = round(sum(scores[k] * w for k, w in WEIGHTS.items()) * 10)

    hard = []
    if q.get("too_hard"): hard.append("its financials are in transition")
    if q["ind"][0] == "Rapid change": hard.append("its industry is changing too fast to predict")
    if q["ms"] <= 6: hard.append("the business is too complex or uncertain to forecast")
    fail = []
    if q["moat"][0] == "None": fail.append("no durable moat")
    if q.get("commodity"): fail.append("commodity-driven cash flows")
    if fin_score < 5: fail.append("weak financial health")
    if not fin and (fcf_ttm is None or fcf_ttm <= 0): fail.append("no free cash flow")
    elif not fin and norm is not None and norm <= 0: fail.append("no free cash flow left after stock-based pay")
    if q["rules"][1][0] is False: fail.append("its best days look to be behind it")
    if hard: verdict = "TOO_HARD"
    elif fail: verdict = "PASS"
    elif mos is not None and mos >= MOS_TARGET: verdict = "BUY_ZONE"
    else: verdict = "WATCHLIST"

    if verdict == "TOO_HARD":
        one = f"Goes in the too-hard pile: {' and '.join(hard)}. No verdict on price."
    elif verdict == "PASS":
        one = f"Fails the quality test ({', '.join(fail)}), so price does not matter."
    elif verdict == "BUY_ZONE":
        one = f"A {q['moat'][0].lower()}-moat business trading {mos:.0f}% below fair value."
    elif mos is None:
        one = "Passes the quality test, but no reliable fair value can be estimated."
    else:
        gap = (f"it trades at {price/iv_mid:.1f}x fair value" if mos < 0 else f"the margin of safety is only {mos:.0f}% against a 30% target")
        one = f"A {q['moat'][0].lower()}-moat business worth owning, but {gap}. Interesting below about ${iv_mid*0.7:,.0f}."

    # ----- The five investors' lenses -----
    ey = eps / price * 100 if eps is not None else None
    e0 = epss[0]
    if eps is None or e0 is None: g_growth, g_txt = None, "n/a"
    elif e0 <= 0: g_growth, g_txt = (None if eps > 0 else False), "From a loss"
    else: g_growth, g_txt = eps / e0 - 1 >= 0.15, f"{(eps/e0-1)*100:+.0f}% (${e0:.2f} → ${eps:.2f})"
    gn = math.sqrt(22.5 * eps * bvps) if eps and eps > 0 and bvps and bvps > 0 else None
    e3 = [e for e in epss[-3:] if e is not None]
    avg3 = sum(e3) / len(e3) if e3 else None
    pe3 = price / avg3 if avg3 and avg3 > 0 else None
    graham = lens([
        chk("Strong current position", NA_FIN if fin else x(cr, 2), "Current ratio ≥ 2.0", None if fin or cr is None else cr >= 2),
        chk("Earnings stability", f"{sum(1 for n in nis if n is not None and n > 0)} of {len(nis)} fiscal years profitable; TTM {'profit' if ni > 0 else 'loss'}",
            "No loss in the last five years", all(n is not None and n > 0 for n in nis) and ni > 0),
        chk("Dividend record", f"${s['dps']:.2f} a share ({dy:.1f}% yield)" if s.get("dps") else "No dividend", "Pays a dividend", bool(s.get("dps"))),
        chk("Earnings growth", g_txt, "EPS up at least 15% in four years", g_growth),
        chk("Moderate P/E", "Average earnings are not positive" if pe3 is None else f"{pe3:.1f}x three-year average earnings (${avg3:.2f}); {x(pe)}x trailing",
            "Price ≤ 15x average earnings of the last three years", False if pe3 is None else pe3 <= 15),
        chk("Graham number", f"P/E × P/B = {pe*pb:.0f}; Graham number ${gn:,.0f} vs price ${price:,.0f}" if gn and pe and pb else "Negative earnings or book value",
            "P/E × P/B ≤ 22.5", False if not (gn and pe and pb) else pe * pb <= 22.5),
        chk("Earnings beat bonds", f"Earnings yield {pct(ey)} vs 10-year Treasury {TY:.2f}%", "Earnings yield ≥ Treasury yield", False if ey is None else ey >= TY),
        chk("No financial distress", NA_FIN if fin else ("n/a" if z is None else f"Altman Z-score {z:.2f}"), "Altman Z ≥ 3.0", None if fin or z is None else z >= 3),
    ])

    oe = ni if fin else (ni + da_now - capex if da_now is not None and capex is not None else fcf_ttm_adj)
    oey = (oe or 0) / mcap * 100
    oe_txt = (f"Earnings yield {oey:.1f}%" if fin else
              f"Owner earnings {b(oe)} (net income + depreciation − capex) = {oey:.1f}% yield" if da_now is not None and capex is not None else f"Free cash flow yield {oey:.1f}%")
    # return on retained earnings: EPS gained per dollar of earnings kept back over the period
    kept = 0.0; rore = None
    if all(e is not None and e > 0 for e in epss):
        for h in hist[1:]:
            shr = h[3] / h[4]; r = cfd.get(h[0])
            kept += h[4] - (abs(r[5]) / shr if r and r[5] is not None else 0.0 if r else (s.get("dps") or 0.0))
        if kept > 0: rore = (epss[-1] - epss[0]) / kept * 100
    de = debt / equity if equity and equity > 0 else None
    if fin: b_roe = chk("High return on equity", pct(roe), "ROE ≥ 15%", None if roe is None else roe >= 15)
    elif roe is None: b_roe = chk("High return on capital", f"ROIC {pct(roic)} (book equity is negative)", "ROIC ≥ 15%", None if roic is None else roic >= 15)
    else: b_roe = chk("High return on equity without heavy debt", f"ROE {pct(roe)}, debt/equity {x(de, 2)}", "ROE ≥ 15% and debt/equity ≤ 1.0", roe >= 15 and de <= 1.0)
    gm_rng = max(gms) - min(gms) if len(gms) >= 4 else None
    if sh_chg is not None: sh_ok, sh_txt = (True if sh_chg <= -1 else False if sh_chg >= 1 else None), f"{sh_chg:+.1f}% over four fiscal years"
    elif sc is not None: sh_ok, sh_txt = (True if sc <= -1 else False if sc >= 1 else None), f"{sc:+.1f}% over the last year"
    else: sh_ok, sh_txt = None, "n/a"
    if fin: ic_ok, ic_txt = None, NA_FIN
    elif ic is not None: ic_ok, ic_txt = ic >= 6.7, f"Operating income covers interest {ic:.1f}x"
    elif cash >= debt: ic_ok, ic_txt = True, "More cash than debt"
    else: ic_ok, ic_txt = None, "n/a"
    buffett = lens([
        chk("Owner-earnings yield beats bonds", f"{oe_txt} vs 10-year Treasury {TY:.2f}%", "Yield ≥ Treasury yield", oey >= TY),
        b_roe,
        chk("Retained earnings put to good use", "Not meaningful: a loss in the period" if rore is None and kept == 0 else ("Nothing retained: more paid out than earned" if rore is None else
            f"EPS rose ${epss[-1]-epss[0]:.2f} on ${kept:.2f} a share retained over {yrs} years: {rore:.0f}% return"),
            "Each dollar kept back earns ≥ 12%", None if rore is None else rore >= 12),
        chk("Pricing power", NA_FIN if fin and not gms else ("n/a" if gm_rng is None or gm_now is None else f"Gross margin {gm_now:.0f}%, {gm_rng:.1f}-point range over five years"),
            "Gross margin ≥ 40% and stable (≤ 6-point range)", None if gm_rng is None or gm_now is None else gm_now >= 40 and gm_rng <= 6),
        chk("Low capital intensity", NA_FIN if fin else ("n/a" if capex is None else (f"Capex is {capex/ni*100:.0f}% of net income" if ni > 0 else "Net loss")),
            "Capex ≤ 50% of net income", None if fin or capex is None else (ni > 0 and capex / ni <= 0.5)),
        chk("Light interest burden", ic_txt, "Interest < 15% of operating income (cover ≥ 6.7x)", ic_ok),
        chk("Debt repayable from earnings", NA_FIN if fin else (f"{payback:.1f} years of net income" if payback is not None else "Net loss"),
            "Total debt ≤ 4 years of net income", None if fin else (payback is not None and payback <= 4)),
        chk("Shrinking share count", sh_txt, "Fewer shares than four years ago", sh_ok),
    ])

    munger = lens([
        chk("Inside the circle of competence", f"Meaning score {q['ms']} / 10", "Simple enough to explain and predict (≥ 8)", True if q["ms"] >= 8 else False if q["ms"] <= 6 else None),
        chk("Not a technology war", q["ind"][0], "Industry is not changing rapidly", q["ind"][0] != "Rapid change"),
        chk("Skin in the game", "n/a" if ins is None else f"Insiders own {ins:.2f}%", "Insiders own ≥ 1%", None if ins is None else ins >= 1),
        chk("No dilution of owners", "n/a" if sc is None else f"Share count {sc:+.2f}% over the last year", "Share count flat or falling", None if sc is None else (True if sc <= 0 else False if sc > 1 else None)),
        chk("Modest stock-based pay", NA_FIN if fin else ("Not reported separately" if not (sbc_reported and sbc_now and ocf) else f"{b(sbc_now)}, {sbc_now/ocf*100:.0f}% of operating cash flow"),
            "Stock pay ≤ 10% of operating cash flow", None if fin or not (sbc_reported and sbc_now and ocf and ocf > 0) else sbc_now / ocf <= 0.10),
        chk("Earnings are real cash", cq_txt, "Operating cash flow ≥ net income over five years", cq_ok),
        chk("Accounting quality check", NA_FIN if fin else ("n/a" if fsc is None else f"Piotroski F-score {fsc:.0f} of 9"), "F-score ≥ 7 (≤ 3 is a warning)",
            None if fin or fsc is None else (True if fsc >= 7 else False if fsc <= 3 else None)),
    ])
    munger["inversion"] = list(q["kill"])
    if payback is not None and payback > 8 and not fin: munger["inversion"].append(f"Debt equals {payback:.0f} years of earnings, which leaves little room for a bad stretch.")
    if ni <= 0: munger["inversion"].append("The business is currently loss-making.")

    if has_iv:
        up = (iv_hi - price) / price * 100
        dn = max(price - iv_lo, 0) / price * 100
        if up <= 0: asym_ok, asym_txt = False, f"No upside even to the high-case value (${iv_hi:,.0f}); {dn:.0f}% downside to the low case"
        elif dn == 0: asym_ok, asym_txt = True, f"{up:.0f}% upside to the high case; price is already below the low-case value"
        else: asym_ok, asym_txt = up / dn >= 3, f"{up:.0f}% upside to the high case vs {dn:.0f}% downside to the low case ({up/dn:.1f} to 1)"
    else:
        up = dn = None; asym_ok, asym_txt = None, "No fair value estimate"
    pabrai = lens([
        chk("A simple, existing business", f"Meaning score {q['ms']} / 10", "Easy to understand (≥ 8)", q["ms"] >= 8),
        chk("Slow rate of change", q["ind"][0], "Stable industry", True if q["ind"][0] == "Stable" else False if q["ind"][0] == "Rapid change" else None),
        chk("Durable moat", f"{q['moat'][0]} moat", "Wide moat", True if q["moat"][0] == "Wide" else False if q["moat"][0] == "None" else None),
        chk("Out of favour", "n/a" if c52 is None else f"Share price {c52:+.0f}% over 52 weeks", "Down 20% or more: bargains come from distress", None if c52 is None else c52 <= -20),
        chk("Bought well below value", "No fair value estimate" if mos is None else f"Margin of safety {mos:.0f}%", "≥ 30%", None if mos is None else mos >= MOS_TARGET),
        chk("Low risk of permanent loss", NA_FIN if fin else ("More cash than debt" if cash >= debt else (f"Debt is {payback:.1f} years of net income" if payback is not None else "Net loss with debt")),
            "Net cash, or debt ≤ 4 years of earnings", None if fin else (cash >= debt or (payback is not None and payback <= 4))),
        chk("Heads I win, tails I don't lose much", asym_txt, "Upside at least 3x the downside", asym_ok),
    ])
    pabrai.update(upside_pct=None if up is None else round(up, 1), downside_pct=None if dn is None else round(dn, 1))

    # ----- Peter Lynch: know what kind of stock it is, then check growth against price -----
    eps_c = cagr(epss[0], epss[-1], yrs)
    lossy = any(n is not None and n < 0 for n in nis) or ni < 0
    if q.get("lynch"): cat = q["lynch"]
    elif q.get("pb_low"): cat = "Asset play"
    elif ni < 0 or (nis[-1] is not None and nis[-1] < 0) or sum(1 for n in nis if n is not None and n < 0) >= 2: cat = "Turnaround"
    elif q.get("commodity") or t in CYCLICAL: cat = "Cyclical"
    elif eps_c is None: cat = "Fast grower" if (rev_c or 0) >= 15 else "Stalwart"  # one loss year distorts the EPS rate, so sales growth decides
    elif eps_c >= 20 and (rev_c or 0) >= 10: cat = "Fast grower"
    elif eps_c < 6 or (rev_c or 0) < 3: cat = "Slow grower"
    else: cat = "Stalwart"
    peg = s.get("peg")
    payout = s["dps"] / eps * 100 if s.get("dps") and eps and eps > 0 else None
    g_l = None if eps_c is None else min(eps_c, 30.0)
    lr = (g_l + dy) / pe if g_l is not None and pe else None
    net_cash = cash >= debt
    if fin: bs_ok, bs_txt = None, NA_FIN
    elif net_cash: bs_ok, bs_txt = True, f"Net cash of {b(cash - debt)}"
    elif de is None: bs_ok, bs_txt = False, "Book equity is negative and debt exceeds cash"
    else: bs_ok, bs_txt = (True if de <= 0.5 else False if de > 1.0 else None), f"Debt is {de:.2f}x equity"
    eps_up = None if epss[0] is None or epss[-1] is None else bool(epss[-1] > epss[0] and downs([e for e in epss if e is not None]) <= 1)
    lynch = lens([
        chk("The two-minute drill", f"Meaning score {q['ms']} / 10", "The story can be told simply (≥ 8)", True if q["ms"] >= 8 else False if q["ms"] <= 6 else None),
        chk("Not a hot stock in a hot industry", q["ind"][0], "Industry is not changing rapidly", q["ind"][0] != "Rapid change"),
        chk("Growth at a reasonable price", "n/a" if peg is None else f"PEG {peg:.2f}", "PEG ≤ 1.0 (above 2.0 fails)", None if peg is None or peg <= 0 else (True if peg <= 1 else False if peg > 2 else None)),
        chk("Growth plus yield against P/E", "n/a" if lr is None else f"({g_l:.0f}% EPS growth{' (capped)' if eps_c > 30 else ''} + {dy:.1f}% yield) ÷ P/E {pe:.1f} = {lr:.2f}",
            "≥ 1.5 is attractive (below 1.0 fails)", None if lr is None else (True if lr >= 1.5 else False if lr < 1 else None)),
        chk("Consistent earnings", "n/a" if eps_c is None else f"EPS {eps_c:+.1f}% a year, {downs([e for e in epss if e is not None])} down year(s)", "EPS higher than four years ago, at most one down year", eps_up),
        chk("Strong balance sheet", bs_txt, "Net cash, or debt ≤ 0.5x equity (above 1.0x fails)", bs_ok),
        chk("Dividend is safe", "No dividend" if payout is None else f"Pays out {payout:.0f}% of earnings", "Payout ≤ 60% of earnings", None if payout is None else payout <= 60),
    ])
    if cat == "Asset play":
        for i in (2, 3, 4):
            lynch["tests"][i].update(value="Not meaningful: reported earnings swing with investment marks", **{"pass": None})
        lynch = lens(lynch["tests"])
    lynch.update(category=cat, category_note=LYNCH[cat])

    # ----- Ratio sheet: every figure a value investor checks, against a yardstick -----
    last_assets = next((r[1] for r in reversed(bs) if r[1]), None)
    roa = ni / last_assets * 100 if last_assets else None
    om = s["ebit"] / rev * 100 if s.get("ebit") is not None and not fin else None
    fm = fcf_ttm / rev * 100 if fcf_ttm is not None and not fin else None
    nd_e = (debt - cash) / s["ebitda"] if s.get("ebitda") and s["ebitda"] > 0 else None
    d_fcf = debt / fcf_ttm if fcf_ttm and fcf_ttm > 0 else None
    fcf_c = cagr(fcfs[0], fcfs[-1], yrs) if not fin else None
    eq_by = {r[0]: r[3] for r in bs}
    bv0 = eq_by.get(hist[0][0]) / sh0 if sh0 and eq_by.get(hist[0][0]) else None
    bv1 = eq_by.get(hist[-1][0]) / sh1 if sh1 and eq_by.get(hist[-1][0]) else None
    bv_c = cagr(bv0, bv1, yrs)
    bby = bb_now / mcap * 100 if bb_now is not None else (0.0 if cf else None)
    fcfy = fcf_ttm_adj / mcap * 100 if fcf_ttm_adj is not None and not fin else None
    hi = lambda v, cut: None if v is None else v >= cut
    lo = lambda v, cut: None if v is None else v <= cut
    R = chk
    if fin:
        e_a = equity / last_assets * 100 if equity and last_assets else None
        ratios = [
            dict(group="Profitability", rows=[
                R("Net profit margin", pct(pm), "≥ 15%", hi(pm, 15)),
                R("Return on equity", pct(roe), "≥ 12%", hi(roe, 12)),
                R("Return on assets", pct(roa, 2), "≥ 1%", hi(roa, 1))]),
            dict(group="Capital strength", rows=[
                R("Equity to assets", pct(e_a), "≥ 8%", hi(e_a, 8)),
                R("Shareholders' equity", f"{b(eqs[0])} → {b(eqs[-1])}", "Rising", eqs[-1] > eqs[0])]),
            dict(group=f"Growth ({yrs}-year annual rate)", rows=[
                R("Revenue", "n/a" if rev_c is None else f"{rev_c:+.1f}%", "≥ 5%", hi(rev_c, 5)),
                R("Earnings per share", "From or to a loss" if eps_c is None else f"{eps_c:+.1f}%", "≥ 7%", hi(eps_c, 7)),
                R("Book value per share", "n/a" if bv_c is None else f"{bv_c:+.1f}%", "≥ 7%", hi(bv_c, 7))]),
            dict(group="Returns to shareholders", rows=[
                R("Dividend yield", pct(dy), f"For reference; 10-year Treasury {TY:.2f}%", None),
                R("Payout ratio", "No dividend" if payout is None else pct(payout, 0), "≤ 60% of earnings", lo(payout, 60)),
                R("Share count", "n/a" if sh_chg is None else f"{sh_chg:+.1f}% over {yrs} years", "Falling", None if sh_chg is None else sh_chg <= -1)]),
            dict(group="Price", rows=[
                R("Earnings yield", pct(ey), f"≥ 10-year Treasury ({TY:.2f}%)", hi(ey, TY)),
                R("Price to book", x(pb, 2), "Compare with the justified P/B in M4", None)]),
        ]
        ratio_gaps = "Not available from the data source: net interest margin, efficiency ratio, CET1 capital ratio, loan-loss reserves and tangible book value. Read them in the 10-K before acting."
    else:
        ratios = [
            dict(group="Profitability", rows=[
                R("Gross margin", pct(gm_now), "≥ 40% signals pricing power", hi(gm_now, 40)),
                R("Operating margin", pct(om), "≥ 15%", hi(om, 15)),
                R("Net profit margin", pct(pm), "≥ 10%", hi(pm, 10)),
                R("Free cash flow margin", pct(fm), "≥ 10%", hi(fm, 10)),
                R("Return on equity", "Negative book equity" if roe is None else pct(roe), "≥ 15%", hi(roe, 15)),
                R("Return on invested capital", pct(roic), "≥ 12%", hi(roic, 12)),
                R("Return on assets", pct(roa), "≥ 6%", hi(roa, 6))]),
            dict(group="Debt and solvency", rows=[
                R("Debt to equity", "Negative book equity" if de is None else f"{de:.2f}x", "≤ 1.0x", lo(de, 1.0)),
                R("Debt to assets", x(d_a, 2), "≤ 0.40", lo(d_a, 0.40)),
                R("Net debt to EBITDA", "Net cash" if net_cash else ("n/a" if nd_e is None else f"{nd_e:.1f}x"), "≤ 2.5x", True if net_cash else lo(nd_e, 2.5)),
                R("Interest cover", "More cash than debt" if ic is None and net_cash else ("n/a" if ic is None else f"{ic:.1f}x"), "≥ 5x", True if ic is None and net_cash else hi(ic, 5)),
                R("Years of free cash flow to repay debt", "No free cash flow" if d_fcf is None else f"{d_fcf:.1f}", "≤ 4 years", False if d_fcf is None and debt > cash else lo(d_fcf, 4)),
                R("Current ratio", x(cr, 2), "≥ 1.0 (Graham asked for 2.0)", hi(cr, 1.0)),
                R("Altman Z-score", x(z, 2), "≥ 3.0 safe; below 1.8 distress", hi(z, 3))]),
            dict(group="Cash quality", rows=[
                R("Operating cash flow to net income", "n/a" if conv_ocf is None else f"{conv_ocf:.0f}% over {len(cum)} years", "≥ 100%: earnings arrive as cash", hi(conv_ocf, 100)),
                R("Free cash flow to net income", "n/a" if conv_fcf is None else f"{conv_fcf:.0f}% over {len(hist)} years", "≥ 80%", hi(conv_fcf, 80)),
                R("Capex share of operating cash flow", "n/a" if not (capex is not None and ocf and ocf > 0) else f"{capex/ocf*100:.0f}%", "≤ 50%: a capital-light business",
                  None if not (capex is not None and ocf and ocf > 0) else capex / ocf <= 0.5),
                R("Capex to depreciation", "n/a" if not (capex is not None and da_now) else f"{capex/da_now:.1f}x", "For reference: above 1.0x means spending beyond replacement", None),
                R("Stock-based pay", "Not reported separately" if not (sbc_reported and sbc_now and ocf and ocf > 0) else f"{b(sbc_now)}, {sbc_now/ocf*100:.0f}% of operating cash flow", "≤ 10% of operating cash flow",
                  None if not (sbc_reported and sbc_now and ocf and ocf > 0) else sbc_now / ocf <= 0.10),
                R("Piotroski F-score", "n/a" if fsc is None else f"{fsc:.0f} of 9", "≥ 7 strong; ≤ 3 weak", None if fsc is None else (True if fsc >= 7 else False if fsc <= 3 else None))]),
            dict(group=f"Growth ({yrs}-year annual rate)", rows=[
                R("Revenue", "n/a" if rev_c is None else f"{rev_c:+.1f}%", "≥ 5%", hi(rev_c, 5)),
                R("Earnings per share", "From or to a loss" if eps_c is None else f"{eps_c:+.1f}%", "≥ 7%", hi(eps_c, 7)),
                R("Free cash flow", "From or to negative" if fcf_c is None else f"{fcf_c:+.1f}%", "≥ 5%", hi(fcf_c, 5)),
                R("Book value per share", "n/a" if bv_c is None else f"{bv_c:+.1f}%", "For reference: buybacks above book value shrink it", None)]),
            dict(group="Returns to shareholders", rows=[
                R("Dividend yield", pct(dy), f"For reference; 10-year Treasury {TY:.2f}%", None),
                R("Payout ratio", "No dividend" if payout is None else pct(payout, 0), "≤ 60% of earnings", lo(payout, 60)),
                R("Dividends covered by free cash flow", "No dividend" if not div_now else ("No free cash flow" if not (fcf_ttm and fcf_ttm > 0) else f"{fcf_ttm/div_now:.1f}x"), "≥ 1.5x",
                  None if not div_now else bool(fcf_ttm and fcf_ttm > 0 and round(fcf_ttm / div_now, 1) >= 1.5)),
                R("Buyback yield", pct(bby), "For reference: gross repurchases ÷ market value", None),
                R("Share count", "n/a" if sh_chg is None else f"{sh_chg:+.1f}% over {yrs} years", "Falling: buybacks exceed stock issued", None if sh_chg is None else (True if sh_chg <= -1 else False if sh_chg >= 1 else None)),
                R("Return on retained earnings", "n/a" if rore is None else f"{rore:.0f}%", "≥ 12%", hi(rore, 12))]),
            dict(group="Yield against bonds", rows=[
                R("Earnings yield", pct(ey), f"≥ 10-year Treasury ({TY:.2f}%)", hi(ey, TY)),
                R("Free cash flow yield after stock pay", pct(fcfy), f"≥ 10-year Treasury ({TY:.2f}%)", hi(fcfy, TY)),
                R("Owner-earnings yield", pct(oey), f"≥ 10-year Treasury ({TY:.2f}%)", oey >= TY)]),
        ]
        ratio_gaps = ("Not available from the data source, so not shown: a ten-year record, inventory and receivables turnover, the quick ratio, goodwill and tangible book value, "
                      "and maintenance capex split from growth capex. Owner earnings therefore deduct all capex, which is conservative.")
    r_app = [r for g_ in ratios for r in g_["rows"] if r["pass"] is not None]
    ratio_summary = dict(passed=sum(1 for r in r_app if r["pass"]), total=len(r_app))

    # ----- Where each dollar of sales goes, and where the cash goes -----
    dollar = None
    if not fin and gm_now is not None and om is not None and rev:
        dollar = dict(cogs=round(100 - gm_now, 1), opex=round(gm_now - om, 1), op_profit=round(om, 1), net=round(pm, 1),
                      fcf=None if fcf_ttm is None else round(fcf_ttm / rev * 100, 1))
    elif fin:
        dollar = dict(cogs=None, opex=None, op_profit=None, net=round(pm, 1), fcf=None)
    cash_use = None
    fy = [r for r in cf if r[0] != "TTM" and r[3] is not None]
    if not fin and len(fy) >= 3:
        tot = lambda i: sum(abs(r[i]) for r in fy if r[i] is not None)
        o_, cx_, dv_, bb_, sb_ = sum(r[3] for r in fy), tot(4), tot(5), tot(6), tot(2)
        if o_ > 0:
            cash_use = dict(years=len(fy), first=fy[0][0], last=fy[-1][0], ocf=b(o_), capex=round(cx_ / o_ * 100), dividends=round(dv_ / o_ * 100),
                            buybacks=round(bb_ / o_ * 100), left=round((o_ - cx_ - dv_ - bb_) / o_ * 100), sbc=round(sb_ / o_ * 100) if sbc_reported else None,
                            capex_reported=any(r[4] is not None for r in fy))

    if q.get("too_hard"):  # figures are not comparable, so nothing that depends on them is shown as a result
        NC = "Not calculated: financials in transition"
        ratios, ratio_summary, ratio_gaps = [], dict(passed=0, total=0), "Not calculated: " + q["too_hard"]
        dollar = cash_use = None
        for L in (graham, buffett, lynch, munger, pabrai):
            for tst in L["tests"]:
                if not tst["value"].startswith(("Meaning score", "Steady", "Stable", "Rapid", "Wide", "Narrow", "None")):
                    tst["value"], tst["pass"] = NC, None
            app = [tst for tst in L["tests"] if tst["pass"] is not None]
            L["passed"], L["total"] = sum(1 for tst in app if tst["pass"]), len(app)
        multiples = [(n, None) for n, _ in multiples]
        prim, sec, pe = (prim[0], None), (sec[0], None), None
        s["fpe"] = s["peg"] = None
        methods, stress, dam = [], None, None
    rules = [
        chk("Clear-cut competitive advantage", f"{q['moat'][0]} moat: {', '.join(q['moat'][1])}.", "", {"Wide": True, "Narrow": None, "None": False}[q["moat"][0]]),
        chk("Small share of a huge market", q["rules"][0][1], "", q["rules"][0][0]),
        chk("Best days still ahead", q["rules"][1][1], "", q["rules"][1][0]),
        chk("A growing industry is not the same as a profitable one", f"{ret_name} of {pct(ret, 0)}." if ret is not None else "Return on capital not available.", "",
            None if ret is None else ret >= ROIC_MIN),
    ]
    history = [dict(period=h[0], revenue=h[1], net_income=h[3], fcf=None if fin else h[5]) for h in hist]
    if abs(rev / hist[-1][1] - 1) >= 0.005:
        history.append(dict(period="TTM", revenue=rev, net_income=ni, fcf=None if fin else fcf_ttm))
    notes = [n for n in (q.get("note"), s.get("price_note")) if n]
    slug = t.lower().replace(".", "-")
    return dict(
        company=q["name"], ticker=t, exchange=q["exch"], sector=q["sector"], is_financial=fin, as_of=AS_OF, price_date=pdate, currency="USD",
        price=price, market_cap=b(mcap), verdict=verdict, overall_score=overall, one_liner=one, scores=scores, treasury_10y=TY,
        profile=profile_block(t, q, fin, s, price, pe, pb, roe, dy, mcap, ev, rev, pfcf, fcf_ttm, s.get("ocf")),
        market=market_block(t, price, pdate, iv_mid if has_iv else None),
        summary=dict(sentence=SUMMARY[t][0], strengths=q["bull"][:3], risks=q["bear"][:3], swing=SUMMARY[t][1]),
        dollar=dollar, cash_use=cash_use,
        meaning=dict(score=q["ms"], what_it_does=q["m"][0], how_it_makes_money=q["m"][1], how_it_keeps_making_money=q["m"][2], how_it_could_stop=q["m"][3]),
        moat=dict(score=q["moat"][2], strength=q["moat"][0], sources=q["moat"][1], summary=q["moat"][3]),
        industry=dict(score=q["ind"][1], pace=q["ind"][0], summary=q["ind"][2]),
        management=dict(score=q["mg"][0], summary=q["mg"][1]),
        financial_health=dict(score=fin_score, checks=checks, red_flags=red, note=" ".join(notes), history=history,
                              ratios=ratios, ratio_summary=ratio_summary, ratio_gaps=ratio_gaps),
        valuation=dict(score=v_score, lifecycle_stage=STAGES[q["stage"]],
                       primary_metric=dict(name=prim[0], value=x(prim[1])), secondary_metric=dict(name=sec[0], value=x(sec[1])),
                       three_numbers=dict(pe=None if pe is None else x(pe), forward_pe=None if s.get("fpe") is None else x(s["fpe"]),
                                          peg=None if s.get("peg") is None else x(s["peg"], 2)),
                       multiples=[dict(name=n, value=x(v)) for n, v in multiples],
                       intrinsic_value_low=None if not has_iv else round(iv_lo, 2), intrinsic_value_high=None if not has_iv else round(iv_hi, 2),
                       margin_of_safety_pct=None if mos is None else round(mos, 1),
                       interesting_below=None if not has_iv else round(iv_mid * 0.7, 2), method=method,
                       fair_value=None if not has_iv else round(iv_mid, 2), methods=methods, stress_case=stress, damodaran=dam),
        lenses=dict(graham=graham, buffett=buffett, lynch=lynch, munger=munger, pabrai=pabrai),
        rules_of_the_road=rules, bull_case=q["bull"], bear_case=q["bear"], framework_version=VERSION,
        sources=[dict(title=f"{q['name']} statistics — StockAnalysis.com", url=f"https://stockanalysis.com/stocks/{slug.replace('-', '.')}/statistics/"),
                 dict(title=f"{q['name']} income statement — StockAnalysis.com", url=f"https://stockanalysis.com/stocks/{slug.replace('-', '.')}/financials/"),
                 dict(title=f"{q['name']} balance sheet — StockAnalysis.com", url=f"https://stockanalysis.com/stocks/{slug.replace('-', '.')}/financials/balance-sheet/")]
                + ([] if fin else [dict(title=f"{q['name']} cash flow statement — StockAnalysis.com", url=f"https://stockanalysis.com/stocks/{slug.replace('-', '.')}/financials/cash-flow-statement/")]),
    )


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "companies"), exist_ok=True)
    index = []
    for t in sorted(Q):
        rep = build(t)
        slug = t.replace(".", "-")
        json.dump(rep, open(os.path.join(OUT, "companies", slug + ".json"), "w"), indent=1, ensure_ascii=False)
        sc, v, L = rep["scores"], rep["valuation"], rep["lenses"]
        qw = {k: w for k, w in WEIGHTS.items() if k != "valuation"}
        mid = (v["intrinsic_value_low"] + v["intrinsic_value_high"]) / 2 if v["intrinsic_value_low"] is not None else None
        index.append(dict(ticker=t, slug=slug, company=rep["company"], sector=rep["sector"], verdict=rep["verdict"], score=rep["overall_score"],
                          price=rep["price"], mos=v["margin_of_safety_pct"], moat=rep["moat"]["strength"],
                          quality=round(sum(sc[k] * w for k, w in qw.items()) / sum(qw.values()), 2),
                          value_per_dollar=None if mid is None else round(mid / rep["price"], 3), interesting_below=v["interesting_below"], scores=sc,
                          lenses={k: [L[k]["passed"], L[k]["total"]] for k in L}))
    # sector medians for each valuation metric, so each company's multiples are read against its peers
    reps = {r["slug"]: json.load(open(os.path.join(OUT, "companies", r["slug"] + ".json"))) for r in index}
    pool = {}
    for r in reps.values():
        for m_ in r["profile"]["metrics"]:
            if m_["value"] is not None and (m_["unit"] == "%" or m_["value"] > 0):
                pool.setdefault((r["sector"], m_["key"]), []).append(m_["value"])
    for slug, r in reps.items():
        k0 = r["profile"]["metrics"][0]["key"]
        same = [o for o in reps.values() if o["sector"] == r["sector"] and o["profile"]["kind"] == r["profile"]["kind"]]
        grp = same if len(same) >= 4 else [o for o in reps.values() if o["sector"] == r["sector"]]
        r["profile"]["peer_group"] = (r["sector"] + " · " + r["profile"]["kind"].lower()) if len(same) >= 4 and len(same) < sum(o["sector"] == r["sector"] for o in reps.values()) else r["sector"]
        r["profile"]["peers"] = sorted([dict(ticker=o["ticker"], company=o["company"], value=next(m_["value"] for m_ in o["profile"]["metrics"] if m_["key"] == k0))
                                        for o in grp if any(m_["key"] == k0 and m_["value"] is not None and m_["value"] > 0 for m_ in o["profile"]["metrics"])],
                                       key=lambda x: -x["value"])
        for m_ in r["profile"]["metrics"]:
            vals = pool.get((r["sector"], m_["key"]), [])
            m_["sector_median"] = round(statistics.median(vals), 2) if len(vals) >= 3 else None
            m_["sector_n"] = len(vals)
        json.dump(r, open(os.path.join(OUT, "companies", slug + ".json"), "w"), indent=1, ensure_ascii=False)
    index.sort(key=lambda r: -r["score"])
    json.dump(dict(as_of=AS_OF, prices_as_of=CFG.get("prices_as_of"), framework_version=VERSION, treasury_10y=TY, companies=index), open(os.path.join(OUT, "index.json"), "w"), indent=1, ensure_ascii=False)
    import collections
    print(len(index), "companies ·", dict(collections.Counter(r["verdict"] for r in index)))
    if "-v" in sys.argv:
        for r in index:
            print(f"{r['ticker']:6} {r['verdict']:9} {r['score']:3}  ${r['price']:>8.2f}  MoS {r['mos']}  {r['lenses']}")
