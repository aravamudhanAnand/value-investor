"""Business profiles, part B: consumer and health care. See profiles_a.py for the format."""

P = {}

P["TSLA"] = (
    "Tesla makes electric cars (Model 3, Model Y, Cybertruck), battery storage for homes and power grids, and solar products. It is also developing self-driving software, a robotaxi service and humanoid robots.",
    "About 70% of 2025 revenue came from selling cars. Energy storage (Megapack, Powerwall) is about 14% and growing quickly. Services, charging and regulatory credits sold to other carmakers make up the rest. Car profit margins have fallen as Tesla cut prices to defend volume.",
    "Tesla is not valued on today's car business: its P/E is far above any carmaker's. The price rests on expectations for robotaxis, self-driving software and robots, so it moves with sentiment about those projects rather than with car deliveries.",
)
P["LOW"] = (
    "Lowe's is the second-largest US home-improvement retailer, with about 1,700 stores selling building materials, appliances, tools and garden supplies to homeowners and professional contractors.",
    "It earns a retail margin on products sold in stores and online. Do-it-yourself homeowners are most of sales; Lowe's is growing its share of professional contractors. Sales follow home sales, home prices and renovation spending.",
    "Lowe's is valued on P/E and free cash flow. The stock moves with the housing market and interest rates: falling mortgage rates raise expectations of a renovation recovery.",
)
P["SBUX"] = (
    "Starbucks is the world's largest coffee-shop chain, with more than 40,000 stores. The US and China are its two largest markets. It is in a turnaround under chief executive Brian Niccol.",
    "Most revenue comes from drinks and food sold in company-operated stores. It also earns royalties from licensed stores, such as those in airports and grocery stores, and sells packaged coffee through Nestlé. The rewards app drives repeat visits.",
    "Starbucks is valued on forward earnings, because current earnings are depressed by the turnaround. The multiple depends on evidence that store traffic and margins are recovering.",
)
P["BKNG"] = (
    "Booking Holdings is the largest online travel company, owning Booking.com, Priceline, Agoda, Kayak and OpenTable. It is strongest in hotel bookings in Europe.",
    "It mostly earns commissions from hotels and other properties when a traveller books through its sites, and increasingly processes the payments itself. It spends heavily on Google advertising to attract travellers and works to bring more of them directly to its app.",
    "Booking is valued on P/E and free cash flow as a high-return, capital-light compounder. Risks to the multiple are a travel slowdown and the possibility that AI assistants or Google take over trip planning.",
)
P["GM"] = (
    "General Motors is the largest US carmaker, selling Chevrolet, GMC, Cadillac and Buick vehicles. It is profitable mainly on pickup trucks and large SUVs in North America.",
    "It sells vehicles to dealers, then earns more from financing them through GM Financial. North American trucks and SUVs earn most of the profit. Electric vehicles still lose money, and the Cruise robotaxi unit has been shut down.",
    "Carmakers trade at low P/Es because earnings are cyclical and capital-hungry. GM is valued on earnings, free cash flow and buybacks, and the stock moves with tariffs, interest rates and car demand.",
)
P["PM"] = (
    "Philip Morris International sells Marlboro and other cigarettes outside the US, and is shifting toward smoke-free products: IQOS heated tobacco and ZYN nicotine pouches.",
    "It earns very high margins on cigarettes and smoke-free products sold through distributors and retailers in more than 180 markets. Smoke-free products are now about 40% of revenue and are growing. Cigarette volumes slowly decline, offset by price increases.",
    "Philip Morris is valued on P/E and dividend yield. Its multiple has risen above other tobacco companies because investors expect ZYN and IQOS to keep the business growing.",
)
P["MO"] = (
    "Altria sells Marlboro cigarettes in the US, plus cigars, oral tobacco and on! nicotine pouches. It owns a stake in brewer Anheuser-Busch InBev.",
    "It earns very high margins on cigarettes sold to wholesalers and retailers. Volumes fall several percent a year, and Altria offsets this with price increases. Most of the cash is returned through dividends.",
    "Altria is valued as an income stock: on dividend yield and a low P/E, because investors expect cigarette volumes to keep falling. The question is how long price increases can offset volume declines.",
)
P["MDLZ"] = (
    "Mondelez is one of the world's largest snack companies, owning Oreo, Cadbury, Milka, Toblerone, Ritz and Trident.",
    "It sells biscuits, chocolate and gum to grocers and convenience stores in more than 150 countries; most sales are outside the US, a large share in emerging markets. Profit depends on pricing power against volatile cocoa and sugar costs.",
    "Mondelez is valued on P/E like other consumer-staples companies. The multiple has fallen on record cocoa costs and weaker volumes.",
)
P["CL"] = (
    "Colgate-Palmolive sells toothpaste and toothbrushes, soap, household cleaners and Hill's pet food in more than 200 countries. Colgate is the most widely used toothpaste brand in the world.",
    "It sells everyday products to retailers, with about two-thirds of sales outside North America. Hill's prescription pet food is the fastest-growing and one of the most profitable parts. Profit comes from steady volumes and pricing power.",
    "Colgate is valued on P/E and dividend yield as a defensive staple. Its premium multiple depends on keeping mid-single-digit organic growth.",
)
P["LLY"] = (
    "Eli Lilly is the largest pharmaceutical company by market value, driven by Mounjaro and Zepbound (tirzepatide) for diabetes and obesity, plus medicines for cancer, immunology and Alzheimer's disease.",
    "It sells prescription drugs to wholesalers, pharmacies and governments, with patent protection that allows high prices for years. Tirzepatide now provides most of its growth, and Lilly sells Zepbound directly to patients. It is building factories to meet demand and developing a pill version (orforglipron).",
    "Lilly trades at a P/E far above other drug companies because investors expect obesity medicines to keep growing for a decade. The multiple moves with obesity-drug prescriptions, pricing and competition.",
)
P["ABBV"] = (
    "AbbVie is a large drug company best known for immunology drugs Skyrizi and Rinvoq, which replaced its former blockbuster Humira. It also sells cancer and neuroscience drugs and Botox through its Allergan aesthetics business.",
    "It sells patented prescription drugs to pharmacies and hospitals. Skyrizi and Rinvoq are its main growth engines; Humira sales collapsed after US biosimilars arrived in 2023. Allergan adds Botox and fillers.",
    "AbbVie is valued on forward earnings and dividend yield. Trailing earnings are distorted by acquisition-related charges, so investors use adjusted earnings. The multiple depends on Skyrizi and Rinvoq growth.",
)
P["MRK"] = (
    "Merck & Co. is a large drug company whose biggest product is Keytruda, the world's best-selling cancer drug. It also sells the Gardasil vaccine and animal-health products.",
    "Keytruda alone is close to half of drug sales, sold to hospitals and cancer centres. Its key US patent expires in 2028, so Merck is buying and developing replacements, including a version of Keytruda injected under the skin.",
    "Merck trades at a low P/E because investors expect Keytruda's patent expiry to cut earnings. The multiple depends on whether new drugs can fill the gap.",
)
P["UNH"] = (
    "UnitedHealth Group is the largest US health insurer (UnitedHealthcare) and owns Optum: doctor practices, a pharmacy-benefit manager (Optum Rx) and health data services.",
    "UnitedHealthcare collects premiums from employers, individuals and the government (Medicare Advantage and Medicaid) and pays medical claims; profit is the gap between the two. Optum earns fees for managing pharmacy benefits and providing care. Medical costs rose faster than expected in 2025, cutting profit.",
    "UnitedHealth is valued on P/E. Its multiple fell sharply in 2025 on rising medical costs, government investigations and Medicare Advantage payment cuts. It recovers if the medical cost ratio comes back down.",
)
P["TMO"] = (
    "Thermo Fisher Scientific is the largest supplier of laboratory instruments, consumables and services, serving drug companies, hospitals, universities and industrial labs.",
    "It sells instruments, then the chemicals, reagents and consumables needed to use them, plus outsourced drug development and manufacturing services. Most revenue is recurring consumables and services, with drug companies the largest customers.",
    "Thermo Fisher is valued on P/E and free cash flow as a high-quality compounder. The multiple moves with biotech funding and pharmaceutical research spending.",
)
P["AMGN"] = (
    "Amgen is one of the largest biotechnology companies, selling medicines for bone health, cholesterol, inflammation, cancer and rare diseases (from its Horizon acquisition). It is developing an obesity drug, MariTide.",
    "It sells patented biologic medicines to hospitals, pharmacies and governments. Several older products face biosimilar competition, so growth depends on newer drugs and the obesity pipeline.",
    "Amgen is valued on P/E and dividend yield. Trailing earnings are depressed by amortisation from the Horizon deal. Results from the MariTide trials are the biggest potential driver of the multiple.",
)
P["ABT"] = (
    "Abbott Laboratories makes medical devices (FreeStyle Libre glucose monitors, heart devices), diagnostic tests, nutrition products (Similac, Ensure) and branded generic drugs sold outside the US.",
    "It sells products to hospitals, labs, pharmacies and consumers. Medical devices are the largest and fastest-growing segment, led by FreeStyle Libre continuous glucose monitors, which require recurring sensor purchases.",
    "Abbott is valued on P/E as a diversified health-care compounder. The multiple depends on FreeStyle Libre growth.",
)
P["GILD"] = (
    "Gilead Sciences is a biotechnology company that dominates HIV treatment (Biktarvy) and prevention, and also sells liver-disease, cancer and cell-therapy medicines.",
    "HIV medicines are most of sales, sold to pharmacies and governments; they are taken daily for life, so revenue is recurring. Yeztugo (lenacapavir), a twice-yearly HIV prevention injection approved in 2025, is its main new product.",
    "Gilead is valued on P/E and dividend yield as a cash-rich drug company. The multiple rises with evidence that lenacapavir can extend the HIV franchise beyond the patent expiries of current drugs.",
)
P["ISRG"] = (
    "Intuitive Surgical makes the da Vinci robotic surgery systems used in minimally invasive operations, and the Ion system for lung biopsies. It has a large installed base in hospitals worldwide.",
    "A razor-and-blade model: it sells or leases robots, then earns more than 80% of revenue from the instruments and accessories used in every procedure and from annual service contracts. Revenue grows with the number of procedures performed.",
    "Intuitive trades at a very high P/E for its long runway of procedure growth and competitive position. The multiple depends on procedure growth staying in the mid-teens.",
)
P["PFE"] = (
    "Pfizer is one of the largest drug companies, selling vaccines (Prevnar, Comirnaty), cancer drugs (from its Seagen acquisition), Eliquis for blood clots (with Bristol Myers Squibb) and Vyndaqel for heart disease.",
    "It sells medicines and vaccines to hospitals, pharmacies and governments. Covid product sales have collapsed from their 2022 peak, and several large drugs lose patent protection by 2028. Pfizer is cutting costs and buying companies, including the obesity-drug developer Metsera.",
    "Pfizer is valued on a low P/E and a high dividend yield because investors expect earnings to fall as patents expire. The multiple depends on the new-drug pipeline filling that gap.",
)
P["DHR"] = (
    "Danaher owns life-science and diagnostics businesses: Cytiva and Pall (equipment and consumables for making biologic drugs), Beckman Coulter, Cepheid and Leica Biosystems (diagnostics), and SCIEX (mass spectrometers).",
    "Most revenue is recurring consumables and services used in drug manufacturing and clinical testing. It is known for the Danaher Business System, a disciplined way of running acquired companies.",
    "Danaher is valued on P/E and free cash flow as a high-quality acquirer. The multiple moves with demand for bioprocessing equipment from drug makers.",
)
P["BMY"] = (
    "Bristol Myers Squibb is a large drug company selling Eliquis (blood clots, with Pfizer), Opdivo (cancer), and medicines for immunology and blood cancers. It is developing Cobenfy for schizophrenia.",
    "It sells patented drugs to pharmacies and hospitals. Much of its revenue comes from drugs facing patent expiry by 2028, including Eliquis and Opdivo, so it is cutting costs and relying on newer drugs.",
    "Bristol Myers trades at a low P/E and high dividend yield because investors expect patent expiries to cut earnings. The multiple moves with results for new drugs such as Cobenfy.",
)
P["MDT"] = (
    "Medtronic is one of the largest medical-device makers, selling cardiac devices (pacemakers, heart valves), surgical tools, diabetes pumps, and spine and neuroscience products in about 150 countries.",
    "It sells devices to hospitals and surgeons, with a mix of one-off equipment and recurring products. Growth is mid-single-digit. In 2025 it announced plans to separate its diabetes business into a standalone company.",
    "Medtronic is valued on P/E and dividend yield as a slow-growth health-care company. The multiple depends on faster growth from new products such as its pulsed-field ablation system and surgical robot.",
)
P["CVS"] = (
    "CVS Health owns CVS pharmacies, the Caremark pharmacy-benefit manager and the Aetna health insurer, making it one of the largest US health-care companies by revenue.",
    "Three businesses: Aetna collects premiums and pays claims; Caremark manages prescription benefits for employers and health plans and earns fees and rebates; CVS pharmacies fill prescriptions and sell retail goods. Margins are thin, and medical costs at Aetna drive profit swings.",
    "CVS trades at a low P/E reflecting thin margins and political pressure on pharmacy-benefit managers. The multiple depends on Aetna's profitability recovering.",
)
