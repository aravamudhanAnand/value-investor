"""Business profiles, part E: S&P 500 expansion, batch 1. See profiles_a.py for the format."""

P = {}

P["ANET"] = (
    "Arista Networks makes the high-speed switches and routers that connect servers inside large data centres, and the EOS software that runs them. Its largest customers are cloud and AI companies.",
    "It sells switching hardware bundled with its software, then earns service and support revenue. A few very large cloud customers account for a big share of sales, and AI clusters, which need far more networking than ordinary servers, are the main source of growth.",
    "Arista is valued on forward earnings and its growth rate. The multiple moves with cloud companies' data-centre spending and with how much of AI networking it wins against Nvidia and generic switches.",
)
P["PANW"] = (
    "Palo Alto Networks is one of the largest cybersecurity companies, selling network firewalls, cloud security and security-operations software to large organisations. It has grown through frequent acquisitions.",
    "Most revenue is subscriptions and support that renew each year; firewall hardware is a shrinking share. Its strategy is to persuade customers to replace many separate security tools with its platform.",
    "Investors value it on free cash flow and on growth in recurring revenue, not on reported earnings, which are held down by stock-based pay and acquisition charges. The debate is how much of that stock pay should count as a cost.",
)
P["CRWD"] = (
    "CrowdStrike sells cloud-based security software that protects laptops, servers and cloud workloads from attack. Its Falcon platform runs through a single small program on each device.",
    "Customers pay annual subscriptions per device and per module, and tend to add modules over time. A faulty software update in 2024 caused a worldwide computer outage and tested customer loyalty.",
    "CrowdStrike is valued on a multiple of sales and on recurring-revenue growth, because reported earnings are still close to zero. Its high valuation depends on growth continuing and on stock-based pay falling as a share of revenue.",
)
P["KLAC"] = (
    "KLA makes the inspection and measurement equipment that chipmakers use to find defects and control quality during manufacturing. It dominates this niche, known as process control.",
    "It sells machines to chipmakers building or upgrading factories, then earns recurring service revenue on its installed base. As chips become harder to make, factories need more inspection steps.",
    "Like other chip-equipment makers, KLA is valued on earnings across the cycle and on forecasts of chipmakers' spending. It usually earns a premium to peers for its market share and margins; export rules on China are the main swing in sentiment.",
)
P["ADI"] = (
    "Analog Devices designs chips that measure, convert and manage real-world signals such as temperature, sound, motion and power. It serves industrial, automotive, communications and consumer markets, and bought Maxim Integrated and Linear Technology.",
    "It sells tens of thousands of long-lived products to a very wide customer base. Each chip is a small part of the customer's cost and stays in a design for years, which supports high margins. Industrial customers are the largest group.",
    "ADI is valued on free cash flow and earnings through the chip cycle. The stock rises when industrial and automotive orders recover and falls when customers run down inventory.",
)
P["APH"] = (
    "Amphenol is one of the world's largest makers of connectors, cables, antennas and sensors: the parts that carry power and signals inside data centres, cars, aircraft, phones and factory equipment.",
    "It sells huge numbers of specialised components to equipment makers. Growth comes from content per device, from AI data centres, which need dense high-speed interconnects, and from a steady stream of acquisitions run by independent local managers.",
    "Amphenol is valued on P/E at a premium to industrial companies for its consistent margins and acquisition record. The multiple now leans on how long AI data-centre demand lasts.",
)
P["SNPS"] = (
    "Synopsys sells electronic design automation software, the tools engineers use to design and verify chips, and licenses pre-built circuit designs. It bought Ansys, a simulation software company, in 2025.",
    "Customers sign multi-year software licences and pay royalties on reused designs. Chipmakers, and increasingly large technology companies designing their own chips, depend on the tools for every new product.",
    "Synopsys is valued on forward earnings and free cash flow. Reported earnings are depressed by the cost of the Ansys deal, so investors watch debt reduction, integration and exposure to China.",
)
P["CDNS"] = (
    "Cadence Design Systems sells electronic design automation software and hardware used to design and test chips, circuit boards and whole electronic systems. With Synopsys it forms a duopoly.",
    "Revenue is mostly multi-year subscriptions, plus design blocks and emulation hardware. Demand grows as chips become more complex and as more companies design their own.",
    "Cadence is valued on forward earnings and free cash flow at a high multiple for its recurring revenue and steady growth. Export limits on China are the main risk to sentiment.",
)
P["SPGI"] = (
    "S&P Global owns one of the two dominant credit-rating agencies, the S&P Dow Jones indices, and large financial and commodity data businesses built up through its merger with IHS Markit.",
    "Borrowers pay for ratings when they issue debt; fund managers pay licence fees linked to assets tracking its indices; banks and companies subscribe to its data. Ratings revenue rises and falls with bond issuance; the rest is largely recurring.",
    "S&P Global is valued on P/E and free cash flow as a high-quality compounder. The multiple moves with debt-issuance volumes and interest-rate expectations.",
)
P["CB"] = (
    "Chubb is the largest publicly traded property and casualty insurer, covering companies, affluent households and farms in many countries, with a growing life insurance business in Asia.",
    "It collects premiums, pays claims and invests the money in between. Profit comes from underwriting, charging more than it pays out, and from investment income on a large bond portfolio.",
    "Insurers are valued on price to book value against their return on equity, and on P/E. Chubb earns a premium for the consistency of its underwriting results.",
)
P["PGR"] = (
    "Progressive is one of the largest car insurers in the United States, selling directly to drivers online and by phone and through independent agents. It also insures commercial vehicles and homes.",
    "It earns an underwriting margin on premiums and investment income on the money it holds. It adjusts prices quickly using detailed driving data, and reports its results every month.",
    "Progressive is valued on P/E and price to book, at a premium to other insurers for its growth and return on equity. The stock moves with the car-insurance pricing cycle.",
)
P["CME"] = (
    "CME Group operates the world's largest futures and options exchanges, including the Chicago Mercantile Exchange, CBOT, NYMEX and COMEX. Its contracts are the benchmarks for US interest rates, stock indices, oil, gold and grains.",
    "It charges a fee for every contract traded and cleared, and sells market data. Volumes rise when markets are volatile and when more debt needs hedging. Costs are largely fixed, so margins are very high.",
    "CME is valued on P/E and dividend yield, since it pays out most of its earnings. The stock tends to do well in volatile markets and is watched for new competition in interest-rate futures.",
)
P["ICE"] = (
    "Intercontinental Exchange owns the New York Stock Exchange, leading energy futures exchanges including the Brent crude contract, a fixed-income data business, and the largest US mortgage software platform.",
    "It earns trading and clearing fees, listing fees, recurring data subscriptions and fees from mortgage lenders.",
    "ICE is valued on P/E and free cash flow. The multiple depends on energy trading volumes and on a recovery in mortgage activity lifting its newest business.",
)
P["VRTX"] = (
    "Vertex Pharmaceuticals makes the medicines that treat the underlying cause of cystic fibrosis, and has launched a non-opioid pain drug and a gene-editing therapy for blood disorders.",
    "Almost all revenue comes from cystic fibrosis drugs that patients take for life. It is spending the cash to build new franchises in pain, kidney disease and diabetes.",
    "Vertex is valued on P/E and on the expected worth of its pipeline. The multiple moves with clinical-trial results outside cystic fibrosis.",
)
P["SYK"] = (
    "Stryker is one of the largest medical-technology companies, known for hip and knee implants, the Mako surgical robot, hospital beds and stretchers, and equipment for surgery and stroke treatment.",
    "It sells implants and single-use products for each procedure, and capital equipment to hospitals. Growth follows the number of operations, which rises as populations age, and its robots pull through implant sales.",
    "Stryker is valued on P/E at a premium for its steady high-single-digit growth. The multiple depends on procedure volumes and margin improvement.",
)
P["BSX"] = (
    "Boston Scientific makes devices for minimally invasive procedures, especially in cardiology: heart-rhythm ablation systems, implants that reduce stroke risk, stents, and tools for urology and endoscopy.",
    "It sells single-use devices to hospitals for each procedure. A small number of newer heart products have driven most of its recent growth.",
    "Boston Scientific was valued as a growth company on forward earnings. Its share price has fallen heavily over the past year, so the question for investors is whether growth in its key heart products has peaked.",
)
P["ELV"] = (
    "Elevance Health, formerly Anthem, is one of the largest US health insurers, operating Blue Cross Blue Shield plans and the Carelon business, which provides pharmacy, behavioural health and care services.",
    "It collects premiums from employers, individuals and government programmes such as Medicaid and Medicare, and pays medical claims. Profit is the small gap between the two, so results turn on the medical cost ratio.",
    "Health insurers are valued on P/E. Elevance trades at a low multiple because medical costs have outrun premiums and government payment rates are uncertain.",
)
P["MCK"] = (
    "McKesson is the largest pharmaceutical distributor in the United States, moving drugs from manufacturers to pharmacies, hospitals and clinics. It also runs a large network supporting community cancer practices.",
    "It earns a very thin margin on a very large volume of medicines, with higher margins on specialty drugs, oncology services and technology sold to drug makers.",
    "McKesson is valued on P/E and free cash flow. Margins look tiny, but returns on capital are high because it needs little capital; steady buybacks drive growth in earnings per share.",
)
P["TJX"] = (
    "TJX Companies is the world's largest off-price retailer, operating T.J. Maxx, Marshalls, HomeGoods and Sierra in the US, and T.K. Maxx and Homesense abroad.",
    "Its buyers purchase surplus branded goods from manufacturers and other retailers at low prices, and sell them well below regular retail prices. Stock changes constantly, which keeps shoppers returning to stores.",
    "TJX is valued on P/E at a premium to most retailers because sales have grown through recessions and online disruption. The multiple depends on steady comparable-store sales growth.",
)
P["ETN"] = (
    "Eaton is a power-management company. It makes the electrical equipment, such as switchgear, circuit breakers and backup power systems, that distributes electricity in data centres, buildings, factories and utilities, plus aerospace and vehicle components.",
    "It sells equipment and services to builders, utilities, data-centre operators and aircraft makers. Its electrical businesses earn most of the profit, with data centres the fastest-growing customer group.",
    "Eaton is valued on P/E. The multiple rose with enthusiasm for data-centre and grid spending and now moves with any sign that those orders are slowing.",
)
P["PH"] = (
    "Parker-Hannifin is the largest maker of motion and control technologies: hydraulic and pneumatic systems, filters, seals and connectors for factories and vehicles, and flight-control and engine components for aircraft.",
    "It sells to equipment makers and, more profitably, sells replacement parts through thousands of distributors. Aerospace, enlarged by its purchase of Meggitt, earns long-lived aftermarket revenue.",
    "Parker is valued on P/E and free cash flow. The multiple has risen as margins improved and aerospace became a larger share of profit; it still moves with the industrial cycle.",
)
P["ADP"] = (
    "Automatic Data Processing is the largest provider of payroll and human-resources services, handling pay, tax filings, benefits and compliance for employers from small firms to multinationals.",
    "Clients pay recurring fees per employee. ADP also earns interest on the client money it holds briefly before paying wages and taxes, so higher interest rates lift its profit.",
    "ADP is valued on P/E and dividend yield as a steady compounder. The multiple moves with employment growth and interest rates.",
)
P["MAR"] = (
    "Marriott International is the world's largest hotel company by rooms, with brands including Marriott, Ritz-Carlton, Sheraton, Westin and Courtyard, and the Marriott Bonvoy loyalty programme.",
    "It owns very few hotels. Property owners pay it franchise and management fees based on room revenue, and it earns fees from co-branded credit cards. The revenue it reports also includes costs reimbursed by hotel owners, which carry no profit.",
    "Marriott is valued on P/E and EV/EBITDA as a capital-light fee business. The multiple moves with room-revenue growth and the pace of new hotel openings.",
)
