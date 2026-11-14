#!/usr/bin/env python3
"""Refresh prices, 52-week ranges and the 10-year Treasury yield. Run by .github/workflows/prices.yml.

Sources   Yahoo Finance chart feed (one request per company, daily bars for the past year)
          FRED series DGS10 (10-year Treasury constant-maturity yield)
Writes    tools/prices.csv     latest close and its date
          tools/market.csv     low52, high52, chg52 (beta, rating, target and as_of are left as they are)
          tools/settings.json  treasury_10y, prices_as_of
          tools/refresh_log.txt what changed and what was skipped

A company is skipped, and its old figures kept, if the feed fails or the new price is more than 40% away
from the price on file (a likely split or bad data point: check it by hand).
"""
import csv, datetime, json, os, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "value-investor-site (+https://github.com/aravamudhanAnand/value-investor)"}
log = []


def fetch(url):
    last = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001
            last = e; time.sleep(2 * (attempt + 1))
    raise last


def quote(ticker):
    """Latest daily close, its date, and the past year's low, high and price change."""
    sym = ticker.replace(".", "-")
    res = json.loads(fetch(f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=1y&interval=1d"))["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    bars = [(t, c, h, l) for t, c, h, l in zip(res["timestamp"], q["close"], q["high"], q["low"]) if c is not None and h is not None and l is not None]
    if len(bars) < 200: raise ValueError(f"only {len(bars)} daily bars")
    if res["meta"].get("currency") != "USD": raise ValueError(f"currency {res['meta'].get('currency')}")
    t, close = bars[-1][0], bars[-1][1]
    date = datetime.datetime.fromtimestamp(t + res["meta"].get("gmtoffset", 0), datetime.timezone.utc).date().isoformat()
    return dict(price=round(close, 2), date=date, low52=round(min(b[3] for b in bars), 2), high52=round(max(b[2] for b in bars), 2),
                chg52=round((close / bars[0][1] - 1) * 100, 2))


def main():
    prices = list(csv.DictReader(open(os.path.join(HERE, "prices.csv"))))
    mpath = os.path.join(HERE, "market.csv")
    market = {r["ticker"]: r for r in csv.DictReader(open(mpath))}
    ok = skipped = 0
    for row in prices:
        t = row["ticker"]
        try:
            n = quote(t)
            old = float(row["price"])
            if abs(n["price"] / old - 1) > 0.40:
                raise ValueError(f"price moved {old} -> {n['price']}; check for a split")
            if n["date"] < row["date"]:
                raise ValueError(f"feed date {n['date']} is older than {row['date']} on file")
            if n["price"] != old: log.append(f"{t}: {old} ({row['date']}) -> {n['price']} ({n['date']})")
            row["price"], row["date"] = f"{n['price']:.2f}", n["date"]
            m = market.setdefault(t, dict(ticker=t, low52="n/a", high52="n/a", beta="n/a", rating="n/a", target="n/a", as_of=n["date"]))
            m["low52"], m["high52"], m["chg52"] = f"{n['low52']:.2f}", f"{n['high52']:.2f}", f"{n['chg52']:.2f}"
            ok += 1
        except Exception as e:  # noqa: BLE001
            skipped += 1; log.append(f"SKIPPED {t}: {type(e).__name__}: {e}")
        time.sleep(0.4)
    if ok < len(prices) * 0.8:
        open(os.path.join(HERE, "refresh_log.txt"), "w").write(f"ABORTED: only {ok} of {len(prices)} quotes fetched; nothing written.\n" + "\n".join(log) + "\n")
        sys.exit(f"Only {ok} of {len(prices)} quotes fetched; nothing written.")
    with open(os.path.join(HERE, "prices.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ticker", "price", "date"]); w.writeheader(); w.writerows(prices)
    with open(mpath, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["ticker", "low52", "high52", "beta", "rating", "target", "as_of", "chg52"], restval="n/a")
        w.writeheader(); w.writerows(sorted(market.values(), key=lambda r: r["ticker"]))
    spath = os.path.join(HERE, "settings.json")
    cfg = json.load(open(spath))
    try:
        start = (datetime.date.today() - datetime.timedelta(days=21)).isoformat()
        rows = [l.split(",") for l in fetch(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10&cosd={start}").decode().strip().splitlines()[1:]]
        d, y = [(r[0], float(r[1])) for r in rows if len(r) == 2 and r[1] not in ("", ".")][-1]
        if not 0.5 <= y <= 15: raise ValueError(f"implausible yield {y}")
        if y != cfg["treasury_10y"]: log.append(f"10-year Treasury: {cfg['treasury_10y']} -> {y} ({d})")
        cfg["treasury_10y"] = y
    except Exception as e:  # noqa: BLE001
        log.append(f"SKIPPED Treasury yield: {type(e).__name__}: {e}")
    cfg["prices_as_of"] = max(r["date"] for r in prices)
    json.dump(cfg, open(spath, "w"))
    head = f"Price refresh {datetime.date.today().isoformat()}: {ok} updated, {skipped} skipped.\n"
    open(os.path.join(HERE, "refresh_log.txt"), "w").write(head + "\n".join(log) + "\n")
    print(head + "\n".join(log))


if __name__ == "__main__":
    main()
