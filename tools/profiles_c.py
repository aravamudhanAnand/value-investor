"""Business profiles, part C: financials, industrials, energy, materials, utilities, real estate. See profiles_a.py."""

P = {}

P["JPM"] = (
    "JPMorgan Chase is the largest US bank, with leading positions in consumer banking (Chase), credit cards, investment banking, trading, commercial banking and asset and wealth management.",
    "Net interest income, the gap between what it earns on loans and securities and what it pays depositors, is roughly half of revenue. The rest is fees: card interchange, investment-banking advice and underwriting, trading, and asset-management fees. Its huge low-cost deposit base keeps funding costs down.",
    "Banks are valued on price to book value (or tangible book) relative to their return on equity, and on P/E. JPMorgan earns the highest premium among large US banks because its return on equity has stayed near 20% through cycles.",
)
P["BAC"] = (
    "Bank of America is the second-largest US bank, with about 70 million consumer and small-business clients, the Merrill Lynch wealth business, and a large investment bank.",
    "Net interest income from loans and securities funded by its large deposit base is the largest source of profit, so earnings rise with interest rates. Fees come from wealth management, cards, investment banking and trading.",
    "Valued on price to tangible book and P/E. Its multiple has lagged JPMorgan's because it bought long-dated bonds at low yields in 2020-21, which cut returns when rates rose; the discount narrows as those bonds mature.",
)
P["WFC"] = (
    "Wells Fargo is a large US consumer and commercial bank, with the biggest branch network in the country, mortgage and auto lending, cards and a wealth-management business.",
    "Mostly net interest income from loans funded by deposits, plus fees from wealth management, cards and banking. In 2025 the Federal Reserve lifted the cap on its asset size imposed after its fake-accounts scandal, freeing it to grow its balance sheet again.",
    "Valued on price to tangible book and P/E. The multiple has risen with the removal of the asset cap and depends on reaching its target return on tangible equity.",
)
P["C"] = (
    "Citigroup is the most global US bank, serving multinational companies in about 90 countries through treasury, trade and securities services, plus US credit cards and wealth management. It is in a multi-year restructuring and is exiting most consumer banking outside the US.",
    "Net interest income and fees from moving money for multinationals (its treasury and trade business), plus card interest, investment banking and trading. Restructuring costs and regulatory penalties have kept returns below its peers'.",
    "Citi trades at a discount to tangible book value because its returns have been below its cost of capital. The stock rises with progress toward its return target, which would close that discount.",
)
P["GS"] = (
    "Goldman Sachs is the leading global investment bank, advising on mergers, underwriting stock and bond issues, trading for institutional clients, and managing assets and wealth for wealthy individuals and institutions.",
    "Fees from advising on deals and underwriting, trading revenue from making markets in stocks, bonds and commodities for hedge funds and institutions, and asset- and wealth-management fees. Revenue swings with deal activity and market volatility; it has largely exited consumer banking.",
    "Investment banks are valued on price to book and P/E. Goldman's multiple rises when deal-making recovers and when the steadier asset- and wealth-management business grows as a share of earnings.",
)
P["MS"] = (
    "Morgan Stanley is a global investment bank and one of the largest wealth managers in the world, after acquiring Smith Barney, E*Trade and Eaton Vance.",
    "Wealth and investment management now earns roughly half of revenue from steady fees on client assets. The rest is investment banking and trading, which swing with markets.",
    "Valued on P/E and price to book. Morgan Stanley earns a higher multiple than pure investment banks because recurring wealth-management fees make earnings more stable.",
)
P["AXP"] = (
    "American Express runs a card network and issues its own premium charge and credit cards to affluent consumers and businesses. It is both the network and the lender.",
    "Discount fees from merchants (a percentage of every purchase) are the largest revenue source, followed by annual card fees and interest on card balances. Its cardholders spend heavily, and premium cards such as Platinum charge high annual fees.",
    "Amex is valued on P/E and return on equity. It earns a premium over card lenders because most revenue comes from spending fees rather than lending, but less than Visa and Mastercard because it carries credit risk.",
)
P["SCHW"] = (
    "Charles Schwab is the largest US brokerage by client assets, serving individual investors and the independent financial advisers who custody client money with it. It absorbed TD Ameritrade in 2020.",
    "Net interest income from investing client cash balances is about half of revenue; the rest is asset-management fees, trading revenue and bank deposit fees. It makes more money when interest rates are higher and when clients keep more cash with it.",
    "Schwab is valued on P/E. The multiple moves with interest rates and with client cash balances, which shrank when rates rose and clients moved money into higher-yielding funds.",
)
P["BLK"] = (
    "BlackRock is the largest asset manager in the world, running more than $10 trillion through iShares exchange-traded funds, index and active funds, and growing private-markets businesses bought through GIP and HPS. It also sells the Aladdin investment-management software.",
    "Management fees charged as a percentage of assets, so revenue rises with markets and new money. Index funds and ETFs charge low fees on enormous volumes; private markets and Aladdin carry higher fees.",
    "BlackRock is valued on P/E, at a premium to other asset managers because ETFs keep attracting money while active managers lose it. The stock moves with markets, since fees follow asset values.",
)
P["COF"] = (
    "Capital One is a large credit-card lender and consumer bank, with auto loans and commercial banking. It bought Discover Financial in 2025, gaining its own payment network.",
    "Mostly interest on credit-card balances and auto loans, funded by online and branch deposits, plus card interchange fees. Credit losses are the main swing factor. Moving its debit cards and some credit cards onto the Discover network saves fees paid to Visa and Mastercard.",
    "Valued on P/E and price to tangible book. The multiple depends on the Discover integration and on consumer credit losses staying under control.",
)
P["BNY"] = (
    "BNY (formerly Bank of New York Mellon) is the world's largest custodian bank, holding and servicing over $50 trillion of assets for pension funds, asset managers and governments. It also runs the Pershing brokerage platform.",
    "Fees for safekeeping assets, settling trades, clearing, payments and fund administration, plus net interest income on client deposits. Fees rise with market values and transaction volumes.",
    "BNY is valued on P/E and price to tangible book. The multiple has risen as returns improved under a cost and growth programme; it is more stable than other banks because it does little lending.",
)
P["USB"] = (
    "U.S. Bancorp is the fifth-largest US commercial bank, with a regional branch network in the West and Midwest, payments processing (Elavon) and corporate trust services.",
    "Net interest income from loans funded by deposits, plus fees from payments, cards, trust services and wealth management. The 2022 acquisition of MUFG Union Bank added West Coast branches.",
    "Valued on P/E and price to tangible book. The multiple depends on interest margins and on rebuilding capital after rate rises cut the value of its bond holdings.",
)
P["CAT"] = (
    "Caterpillar is the largest maker of construction and mining equipment, and of diesel and gas engines and turbines used in power generation, oil and gas, and data centres.",
    "It sells machines through independent dealers, then earns recurring revenue from parts and service on more than a million machines in use. Power generation for data centres is a fast-growing part. Its finance arm lends to buyers.",
    "Caterpillar is valued on P/E across the economic cycle. Its multiple has risen because data-centre power demand and services make earnings steadier than in past cycles.",
)
P["GE"] = (
    "GE Aerospace makes jet engines for commercial and military aircraft, through its own engines and CFM International, its joint venture with France's Safran that powers most narrow-body jets.",
    "It sells engines to aircraft makers, often at low or negative margins, then earns most of its profit over decades from spare parts and services as those engines fly. More than two-thirds of revenue comes from services.",
    "GE Aerospace is valued on P/E and free cash flow at a premium for its long, predictable aftermarket. The multiple depends on airline flying hours and on the supply chain keeping up with demand.",
)
P["RTX"] = (
    "RTX (formerly Raytheon Technologies) makes jet engines (Pratt & Whitney), aircraft systems (Collins Aerospace) and missiles and defence systems (Raytheon).",
    "Revenue is split roughly between commercial aerospace (engines and parts, with high-margin aftermarket service) and defence (missiles, radars and air defence sold to the US and allied governments). A large engine recall in 2023 is still costing it money.",
    "RTX is valued on P/E and free cash flow. The multiple moves with commercial air traffic and defence budgets, including European rearmament.",
)
P["GEV"] = (
    "GE Vernova makes gas turbines, wind turbines and electrical grid equipment. It was spun off from General Electric in 2024 and is one of the main suppliers for new power plants and grid upgrades.",
    "It sells turbines and grid equipment under long-term contracts, then earns service revenue for decades. Gas-turbine orders have surged on data-centre power demand; wind has been losing money.",
    "GE Vernova is valued on forward earnings and free cash flow at a high multiple, reflecting its large order backlog for gas turbines and grid equipment. Customer deposits inflate current cash flow, so investors look at the backlog and future margins.",
)
P["BA"] = (
    "Boeing is one of two makers of large commercial jets (with Airbus) and a major defence and space contractor.",
    "It sells aircraft to airlines and leasing companies, which pay most of the price on delivery, plus military aircraft, services and spare parts. Production problems and the 737 MAX crisis have caused years of losses and heavy debt.",
    "Boeing cannot be valued on current earnings, which are negative. Investors value it on the free cash flow it should earn once production recovers, so the stock moves with monthly 737 production rates.",
)
P["DE"] = (
    "Deere & Company is the world's largest maker of farm equipment (John Deere tractors and combines) and a major maker of construction and forestry machinery.",
    "It sells machines through dealers to farmers and contractors, and earns financing income from loans to buyers. Farm equipment demand follows crop prices and farm income. Precision-agriculture technology and software subscriptions are a growing part.",
    "Deere is valued on P/E across the farm cycle. The multiple has stayed fairly high through the current downturn because investors expect precision-agriculture technology to lift margins.",
)
P["UNP"] = (
    "Union Pacific runs the largest US railroad network west of the Mississippi, carrying coal, grain, chemicals, cars and shipping containers. It has agreed to merge with Norfolk Southern to create the first coast-to-coast US railroad, pending regulatory approval.",
    "It charges shippers for moving freight; railroads cannot easily be duplicated, which gives it pricing power. Profit grows with volumes, price increases and running the network more efficiently.",
    "Union Pacific is valued on P/E and free cash flow as a durable duopoly asset. The multiple depends on the Norfolk Southern merger review and on freight volumes.",
)
P["HON"] = (
    "Honeywell is an industrial technology company splitting into three. It spun off Solstice Advanced Materials in 2025 and has announced the separation of Honeywell Aerospace, which leaves Honeywell Automation (building and industrial controls).",
    "It sells aircraft systems and services, building controls, industrial automation and process software to aircraft makers, airlines, building owners and factories. The aerospace aftermarket and software are the highest-margin parts.",
    "Until the separations finish, investors value Honeywell on a sum of the parts, valuing each business separately. Its published figures are not comparable with the company that trades today.",
)
P["UBER"] = (
    "Uber runs the largest ride-hailing and food-delivery marketplace in the world, in about 70 countries, plus a freight brokerage.",
    "It takes a share of each ride and delivery booking (its take rate) and charges restaurants and advertisers. Mobility earns most of the profit; delivery is growing; advertising and the Uber One membership add higher-margin revenue. It partners with robotaxi companies rather than building its own cars.",
    "Uber is valued on free cash flow and forward earnings. Its multiple depends on whether robotaxis strengthen its network or bypass it.",
)
P["LMT"] = (
    "Lockheed Martin is the largest US defence contractor, making the F-35 and F-16 fighters, missiles and missile defence (PAC-3, THAAD), helicopters (Sikorsky) and space systems.",
    "Almost all revenue comes from government contracts, mainly the US Department of Defense, plus allied governments. Contracts are long-term, with set profit margins. The F-35 programme is the largest part.",
    "Lockheed is valued on P/E and free cash flow as a steady defence contractor. The multiple moves with US defence budgets and with charges on fixed-price contracts.",
)
P["GD"] = (
    "General Dynamics makes Gulfstream business jets, nuclear submarines (Electric Boat) and warships, combat vehicles, munitions and government IT services.",
    "Defence contracts with the US government are most of revenue, especially submarines. Gulfstream sells business jets to companies and wealthy individuals and services the existing fleet.",
    "General Dynamics is valued on P/E and free cash flow. The multiple moves with Gulfstream deliveries and with defence spending on submarines.",
)
P["FDX"] = (
    "FedEx runs one of the largest express and ground parcel delivery networks in the world, plus FedEx Freight, its less-than-truckload trucking business, which FedEx decided in 2024 to spin off as a separate company.",
    "It charges shippers by package, weight, distance and speed. Express (air) and Ground are the largest parts, with e-commerce a major volume source. It is merging its air and ground networks to cut costs.",
    "FedEx trades at a low P/E for a transport company because volumes are cyclical and margins thin. The multiple depends on cost savings and the value unlocked by separating FedEx Freight.",
)
P["UPS"] = (
    "United Parcel Service is the largest parcel delivery company in the world, with unionised US delivery operations, international express and supply-chain services.",
    "It charges shippers by package. It is cutting low-margin Amazon volume by about half and closing facilities to improve profitability. Labour costs rose sharply under the 2023 Teamsters contract.",
    "UPS is valued on P/E and dividend yield. The multiple has fallen as volumes shrank and investors questioned whether free cash flow covers the dividend.",
)
P["EMR"] = (
    "Emerson Electric makes industrial automation equipment: control systems, valves, measurement instruments and test equipment. It now owns AspenTech's industrial software and National Instruments.",
    "It sells automation hardware and software to oil and gas, chemical, power, pharmaceutical and factory customers, with recurring software and service revenue. It has sold its consumer and climate businesses to become a pure automation company.",
    "Emerson is valued on P/E and free cash flow. The multiple has risen as software became a larger share of earnings.",
)
P["MMM"] = (
    "3M makes industrial adhesives and abrasives, safety equipment, electronics materials and consumer products such as Post-it notes and Scotch tape. It spun off its health-care business (Solventum) in 2024.",
    "It sells thousands of products to factories, construction firms, electronics makers and retailers. Settlements over PFAS chemicals and earplug lawsuits cost billions of dollars, and it is cutting costs under a new chief executive.",
    "3M is valued on P/E. The multiple has recovered as legal liabilities were settled and margins improved.",
)
P["CVX"] = (
    "Chevron is one of the largest integrated oil and gas companies, producing oil and gas worldwide (Permian Basin, Kazakhstan, Australia) and refining fuels. It acquired Hess in 2025, gaining a stake in Guyana's large oil discoveries.",
    "Most profit comes from producing and selling crude oil and natural gas, so earnings rise and fall with oil prices. Refining and chemicals add profit that moves with fuel margins.",
    "Oil companies are valued on EV/EBITDA, free cash flow yield and dividend yield at mid-cycle oil prices. Chevron's multiple depends on oil prices and on production growth from Guyana and the Permian.",
)
P["COP"] = (
    "ConocoPhillips is the largest US independent oil and gas producer, with operations in the Permian Basin, Alaska, Norway and LNG projects. It acquired Marathon Oil in 2024.",
    "It produces and sells oil and gas, so earnings move almost directly with energy prices. It has no refining business.",
    "ConocoPhillips is valued on EV/EBITDA, free cash flow yield and cash returned to shareholders at mid-cycle oil prices. The stock moves with oil prices.",
)
P["LIN"] = (
    "Linde is the largest industrial-gas company in the world, producing oxygen, nitrogen, hydrogen, argon and specialty gases for steel, chemicals, health care, electronics and food.",
    "Most revenue comes from long-term contracts, often 15-20 years with minimum purchase commitments, to supply gases by pipeline or onsite plants, plus deliveries in cylinders and tankers. Pricing power in a consolidated industry and long contracts make earnings unusually stable.",
    "Linde is valued on P/E at a premium to industrial companies for the stability of its contracted earnings.",
)
P["NEE"] = (
    "NextEra Energy owns Florida Power & Light, the largest US electric utility, and NextEra Energy Resources, the world's largest generator of wind and solar power.",
    "Florida Power & Light earns a regulated return on the power grid and plants it builds. NextEra Energy Resources sells renewable power under long-term contracts, often to data centres and utilities. Earnings grow by investing heavily in new assets.",
    "Utilities are valued on P/E and dividend yield. NextEra earns a premium for faster growth, but its multiple falls when interest rates rise or renewable-energy tax credits are cut.",
)
P["SO"] = (
    "Southern Company is a regulated electric and gas utility serving about 9 million customers in Georgia, Alabama and Mississippi, and owns the new Vogtle nuclear units.",
    "It earns a return set by state regulators on the power plants and grid it builds, recovered through customer bills. Data-centre demand in Georgia is driving large new investment.",
    "Southern is valued on P/E and dividend yield like other utilities. The multiple moves with interest rates and with regulatory decisions in Georgia.",
)
P["DUK"] = (
    "Duke Energy is one of the largest US regulated utilities, supplying electricity to about 8 million customers in the Carolinas, Florida and the Midwest, and natural gas to about 1.7 million.",
    "It earns a regulated return on its power plants and grid. Earnings grow by investing in new generation, grid upgrades and capacity for data centres, with rates approved by state regulators.",
    "Duke is valued on P/E and dividend yield. The multiple moves with interest rates and with the outcome of rate cases.",
)
P["AMT"] = (
    "American Tower is one of the largest owners of cell towers in the world, with about 150,000 sites in the US, Latin America, Europe and Africa, and data centres through CoreSite.",
    "It leases space on towers to wireless carriers under long-term contracts with built-in annual rent increases. Adding a second or third carrier to a tower costs little, so each extra tenant is very profitable.",
    "Tower companies are real estate investment trusts, valued on funds from operations (FFO, cash earnings before depreciation) rather than P/E. Operating cash flow is used here as an approximation of FFO. The multiple moves with interest rates and carrier spending.",
)
P["SPG"] = (
    "Simon Property Group is the largest US owner of shopping malls and premium outlet centres, with about 230 properties, and interests in retailers and international outlets.",
    "Rent from retailers, mostly fixed base rent plus some rent tied to tenant sales. Top-tier malls have held occupancy above 95% even as weaker malls closed.",
    "Simon is a real estate investment trust valued on funds from operations (FFO) and dividend yield rather than P/E. Operating cash flow is used here as an approximation of FFO. The stock moves with interest rates and retail health.",
)
