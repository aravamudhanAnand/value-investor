"""All analyst judgments in one place. Edit the companies_*.py files, not this one."""
from companies_core import Q as CORE
from companies_a import Q
import companies_b, companies_c, companies_d, companies_e, companies_f, companies_g  # noqa: F401  (they add to Q)

EXTRA = {  # sector and Munger-style "how does this die?" for the original 20
 "AAPL": ("Technology", ["A product misstep breaks the premium brand.", "Regulators dismantle App Store fees and the Google search payment."]),
 "MSFT": ("Technology", ["AI capital spending never earns its cost.", "Enterprises move to open-source or rival AI platforms."]),
 "GOOGL": ("Communication services", ["AI assistants replace the search box and its ads.", "Antitrust remedies break up the ad business."]),
 "AMZN": ("Consumer discretionary", ["The AI data-centre build-out fails to earn its cost.", "Regulators separate AWS from retail."]),
 "NVDA": ("Technology", ["Hyperscalers' own chips displace GPUs.", "AI capital spending is cut sharply."]),
 "BRK.B": ("Financials", ["A mega-catastrophe hits the insurance operations.", "Capital allocation deteriorates after the founder era."]),
 "V": ("Financials", ["Governments cap card fees.", "Real-time bank payments or stablecoins route around card networks."]),
 "MA": ("Financials", ["Governments cap card fees.", "Real-time bank payments or stablecoins route around card networks."]),
 "KO": ("Consumer staples", ["A lasting consumer shift away from sugary drinks.", "Sugar taxes spread worldwide."]),
 "PEP": ("Consumer staples", ["Appetite-suppressing drugs cut snack consumption.", "Private labels take shelf space."]),
 "PG": ("Consumer staples", ["Private labels and online brands erode premium pricing.", "Retailers squeeze margins."]),
 "JNJ": ("Health care", ["Key drugs lose patents without replacements.", "Talc litigation costs escalate."]),
 "COST": ("Consumer staples", ["It loses its low-price reputation.", "The frugal culture changes under new management."]),
 "WMT": ("Consumer staples", ["A price war with Amazon and discounters.", "It falls behind in e-commerce."]),
 "MCD": ("Consumer discretionary", ["Lasting loss of value perception with low-income customers.", "Franchisee economics break down."]),
 "HD": ("Consumer discretionary", ["A long housing slump.", "Debt-funded acquisitions fail to deliver."]),
 "WM": ("Industrials", ["Regulation that sharply raises landfill costs.", "A large acquisition overpays."]),
 "SHW": ("Materials", ["A long construction slump.", "Raw-material costs spike and cannot be passed on."]),
 "XOM": ("Energy", ["Oil prices stay low for years.", "The energy transition accelerates."]),
 "NKE": ("Consumer discretionary", ["The brand loses cultural relevance.", "The turnaround fails to restore margins."]),
}
for t, q in CORE.items():
    q = dict(q); q["sector"], q["kill"] = EXTRA[t]
    q["bull"], q["bear"] = q["bull"][:3], q["bear"][:3]
    Q[t] = q
Q["BRK.B"]["fin"] = True
from companies_notes import NOTES
for t, n in NOTES.items():
    Q[t]["note"] = n
Q["UBER"]["g"] = 12
Q["HON"]["note"] = "The history below is for the company before its separations, so it is not comparable with the business that trades today."
