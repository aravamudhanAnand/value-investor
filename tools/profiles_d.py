"""Business profiles, part D: the original 20 companies. See profiles_a.py."""

P = {}

P["AAPL"] = (
    "Apple designs the iPhone, Mac, iPad, Apple Watch and AirPods, and runs the App Store, iCloud, Apple Music, Apple Pay and other services on more than two billion active devices.",
    "The iPhone is about half of revenue (fiscal 2025), sold at premium prices through carriers, retailers and Apple's own stores. Services are about a quarter of revenue but a much larger share of gross profit, because App Store commissions, Google's payments for default search, iCloud and subscriptions carry margins above 70%. Macs, iPads and wearables make up the rest.",
    "Apple is valued on P/E and free cash flow as the most profitable consumer franchise in the world. It trades at a high multiple for mid-single-digit growth because investors prize its services revenue and its buybacks; the risks to the multiple are antitrust rulings against App Store fees and Google payments.",
)
P["MSFT"] = (
    "Microsoft sells Azure cloud computing, Microsoft 365 (Office, Teams, Outlook), Windows, LinkedIn, GitHub, Dynamics business software and Xbox gaming. It is a large investor in OpenAI and is building AI into all its products through Copilot.",
    "Mostly subscriptions and usage fees from companies. Azure is the fastest-growing part, charging by computing used. Microsoft 365 charges per user per month. Windows earns licence fees from PC makers. It is spending well over $100 billion a year on data centres for AI.",
    "Microsoft is valued on P/E and free cash flow at a premium for its durable growth. The debate is whether AI spending earns an adequate return: its multiple moves with Azure growth and with the size of its capital spending.",
)
P["GOOGL"] = (
    "Alphabet owns Google Search, YouTube, Android, Chrome, Google Cloud and Gemini AI, plus long-term bets including Waymo self-driving cars.",
    "Advertising on Search and YouTube is about three-quarters of revenue: businesses pay when users click or view ads. Google Cloud sells computing and AI services and is now profitable. Subscriptions (YouTube Premium, Google One) and Pixel devices add the rest.",
    "Alphabet is valued on P/E and free cash flow. It has traded at a discount to other large tech companies because of fears that AI chatbots replace search and antitrust remedies; the multiple rises with evidence that Gemini and Cloud strengthen the business.",
)
P["AMZN"] = (
    "Amazon is the largest online retailer in the US and runs Amazon Web Services (AWS), the largest cloud-computing provider. It also sells advertising, Prime memberships and streaming video.",
    "Online retail is most of revenue but earns thin margins. AWS earns most of the operating profit, charging companies for computing and storage. Advertising on its shopping sites, fees from third-party sellers who use its warehouses, and Prime subscriptions are increasingly important profit sources.",
    "Amazon is valued on EV/EBITDA, operating cash flow and a sum of the parts, because heavy investment keeps reported earnings and free cash flow low. The multiple moves with AWS growth and the return on its AI capital spending.",
)
P["NVDA"] = (
    "Nvidia designs the GPUs and networking that power most AI training and inference in data centres, plus graphics chips for gaming and professional workstations. Its CUDA software is the standard for AI developers.",
    "Data centre is the vast majority of revenue: cloud providers, AI companies and governments buy complete AI systems. It owns no factories; TSMC makes its chips. Gaming GPUs, professional visualisation and automotive chips are small by comparison.",
    "Nvidia is valued on forward P/E, since earnings have grown so fast that trailing figures understate it. Its multiple depends on how long AI data-centre spending keeps growing and whether customers' own chips take share.",
)
P["BRK.B"] = (
    "Berkshire Hathaway is a conglomerate: insurance (GEICO, General Re, Berkshire Hathaway Reinsurance), the BNSF railroad, Berkshire Hathaway Energy, dozens of manufacturing and retail companies, and a large stock portfolio led by Apple and American Express. Greg Abel succeeded Warren Buffett as chief executive at the start of 2026.",
    "Insurance provides float, premiums received before claims are paid, which Berkshire invests. Operating businesses (railroad, utilities, manufacturing) earn steady profits. Dividends and gains on its stock portfolio, plus interest on a very large cash pile, add the rest.",
    "Berkshire is valued on price to book value, because reported earnings swing with stock-market gains and losses. Historically the shares have traded around 1.3 to 1.6 times book, and the company has historically bought back shares only when they traded near the low end of that range.",
)
P["V"] = (
    "Visa runs the largest card-payment network in the world, connecting billions of cards with tens of millions of merchants and thousands of banks.",
    "Visa does not lend money. It charges small fees on every payment: service fees on payment volume, data-processing fees per transaction, and higher fees for cross-border payments. Banks issue Visa-branded cards and take the credit risk.",
    "Visa is valued on P/E and free cash flow at a premium for its very high margins and durable growth. Threats to the multiple are regulation of card fees and new payment systems that bypass card networks.",
)
P["MA"] = (
    "Mastercard runs the second-largest card-payment network in the world, with a growing business in data, fraud prevention and other value-added services.",
    "Like Visa, it charges small fees on payment volume and transactions, with higher fees on cross-border payments, and lends no money. Value-added services such as cybersecurity, data analytics and loyalty programmes are growing faster than core payments.",
    "Mastercard is valued on P/E and free cash flow, at a premium similar to Visa's. The multiple depends on cross-border travel and on regulation of card fees.",
)
P["KO"] = (
    "Coca-Cola owns the world's most recognised drink brands: Coca-Cola, Sprite, Fanta, Powerade, smartwater and fairlife.",
    "It mostly sells concentrate and syrup to independent bottlers, who make, distribute and sell the drinks. This keeps Coca-Cola's capital needs low and margins high. Revenue grows through price increases and modest volume growth.",
    "Coca-Cola is valued on P/E and dividend yield as a defensive compounder. It trades at a premium for reliability; the multiple moves more with interest rates than with its own results.",
)
P["PEP"] = (
    "PepsiCo owns Pepsi, Gatorade, Mountain Dew, Frito-Lay (Lay's, Doritos, Cheetos) and Quaker. Snacks are a larger part of the business than drinks.",
    "Unlike Coca-Cola, it makes and distributes much of its product itself, through its own trucks and warehouses, which requires more capital. Frito-Lay North America earns the highest margins. Volumes have weakened as consumers trade down and as weight-loss drugs affect snacking.",
    "PepsiCo is valued on P/E and dividend yield. The multiple has fallen with weaker snack volumes and activist pressure to restructure.",
)
P["PG"] = (
    "Procter & Gamble is the largest consumer-products company, owning Tide, Pampers, Gillette, Charmin, Crest, Head & Shoulders and Olay.",
    "It sells everyday household and personal-care products to retailers in about 180 countries. Leading brands let it raise prices and invest heavily in innovation and advertising. Fabric and home care and baby and family care are its largest segments.",
    "P&G is valued on P/E and dividend yield as a defensive staple, with a premium for its consistent organic growth and decades of dividend increases.",
)
P["JNJ"] = (
    "Johnson & Johnson is a health-care company with two businesses: Innovative Medicine (prescription drugs for cancer, immunology and neuroscience) and MedTech (surgical, orthopaedic, heart and eye devices).",
    "Drugs are about two-thirds of revenue, with leading cancer drugs such as Darzalex and Carvykti; immunology drug Stelara has lost patent protection. MedTech sells devices to hospitals. Talc-related litigation remains a cost.",
    "J&J is valued on P/E and dividend yield as a defensive health-care company. The multiple depends on new drugs offsetting the Stelara patent loss.",
)
P["COST"] = (
    "Costco runs membership warehouse clubs selling groceries, household goods, electronics and fuel in bulk at low prices, with about 900 warehouses worldwide.",
    "It marks up goods only slightly over cost, so most of its profit comes from membership fees paid annually by about 80 million paid members, renewing at about 90% in the US and Canada. Low prices drive volume, and volume gives it buying power.",
    "Costco trades at one of the highest P/Es in retail because investors prize its steady growth and loyal members. The multiple leaves little room for disappointment.",
)
P["WMT"] = (
    "Walmart is the largest retailer in the world, with about 10,500 stores, Sam's Club, a fast-growing e-commerce business and Walmart International (including Flipkart in India).",
    "It earns thin margins on enormous volumes of groceries and general merchandise. Advertising, its Walmart+ membership and fees from marketplace sellers are newer, higher-margin sources of profit that are lifting overall margins.",
    "Walmart now trades at a high P/E for a retailer because investors see advertising and e-commerce turning it into a technology-enabled platform. The multiple depends on margins continuing to rise.",
)
P["MCD"] = (
    "McDonald's is the largest restaurant brand in the world, with more than 40,000 restaurants in over 100 countries, about 95% run by franchisees.",
    "It earns rent and royalties from franchisees, a percentage of each restaurant's sales, and owns or leases much of the land under its restaurants. This makes it effectively a real-estate and brand-licensing company with high, stable margins.",
    "McDonald's is valued on P/E and dividend yield as a defensive compounder. The multiple moves with sales growth, which slows when lower-income customers cut back.",
)
P["HD"] = (
    "Home Depot is the largest home-improvement retailer in the world, with about 2,300 stores in the US, Canada and Mexico. It acquired SRS Distribution and GMS to grow its business with professional contractors.",
    "It earns a retail margin on building materials, tools, appliances and garden products. Professional contractors are about half of sales. Sales follow home sales, home prices and renovation spending.",
    "Home Depot is valued on P/E and free cash flow. The stock moves with the housing market and mortgage rates.",
)
P["WM"] = (
    "Waste Management is the largest waste and recycling company in North America, collecting, transporting and disposing of household and business waste. It owns the largest network of landfills, and acquired Stericycle's medical-waste business in 2024.",
    "It charges homes, businesses and municipalities for collection and disposal under long-term contracts, with annual price increases. Owning landfills, which are very hard to permit, gives it pricing power. It also earns revenue from recycling and from turning landfill gas into energy.",
    "WM is valued on P/E and EV/EBITDA at a premium for its stable, recession-resistant earnings and pricing power.",
)
P["SHW"] = (
    "Sherwin-Williams is the largest paint and coatings company in the world, selling through about 5,000 of its own paint stores and to industrial customers.",
    "Paint Stores Group, which sells to professional painters and contractors, earns most of the profit. Consumer Brands sells through retailers such as Lowe's, and Performance Coatings sells industrial coatings. Owning its stores gives it pricing power and close contact with painters.",
    "Sherwin-Williams is valued on P/E at a premium for its pricing power and consistent growth. The multiple moves with housing and construction activity.",
)
P["XOM"] = (
    "ExxonMobil is the largest US oil and gas company, producing oil and gas worldwide (Permian Basin, Guyana, LNG) and running large refining and chemical businesses. It acquired Pioneer Natural Resources in 2024.",
    "Most profit comes from producing and selling oil and gas, so earnings move with energy prices. Refining and chemicals add profit that depends on fuel and chemical margins.",
    "ExxonMobil is valued on EV/EBITDA, free cash flow yield and dividend yield at mid-cycle oil prices. The stock moves with oil prices and production growth in Guyana and the Permian.",
)
P["NKE"] = (
    "Nike is the largest athletic footwear and apparel brand in the world, with Jordan and Converse. It is in a turnaround under chief executive Elliott Hill.",
    "It sells shoes and clothing through retailers such as Foot Locker and Dick's, and directly through its own stores and app. Footwear is about two-thirds of revenue. Discounting and a shift away from retailers hurt margins, and Nike is rebuilding its retail partnerships.",
    "Nike is valued on forward earnings, because current earnings are depressed by the turnaround. The multiple depends on evidence of renewed growth and margin recovery.",
)
