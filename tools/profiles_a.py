"""Business profiles, part A: technology and communication services.

Each entry: (what the company is, how it makes money, how the market values the stock).
These are analyst judgment. The calculated multiples and the fair value are added by build.py.
"""

P = {}

P["AVGO"] = (
    "Broadcom designs chips for networking, data-centre connectivity, broadband, wireless and storage, and since buying VMware in 2023 it is also one of the largest enterprise software companies. It is a central supplier of the networking and custom AI chips that hyperscale cloud providers build their AI clusters around.",
    "Two engines. Semiconductors (a little under 60% of fiscal 2025 revenue) sells chips to device makers and cloud giants, increasingly custom AI accelerators designed with a handful of very large customers. Infrastructure software (just over 40%) sells VMware, mainframe and security software on multi-year subscriptions with very high margins. Broadcom buys franchises, cuts costs hard and raises prices.",
    "The market prices Broadcom on forward earnings and free cash flow, and the multiple now rests on how fast its custom AI-chip business grows. Customer concentration in AI and the debt from VMware are the main reasons the multiple can fall.",
)
P["ORCL"] = (
    "Oracle sells the database software that runs much of the world's corporate data, business applications (Fusion ERP, NetSuite, Cerner health records), and Oracle Cloud Infrastructure (OCI), which it is expanding rapidly to rent computing capacity for AI training.",
    "Most revenue is recurring: annual support fees on software customers already own, plus cloud subscriptions. Cloud infrastructure was about a quarter of fiscal 2026 revenue and is the fastest-growing line, backed by very large multi-year contracts with AI companies. New licence sales and hardware are small and shrinking.",
    "Investors value Oracle on forward earnings and the size of its contracted cloud backlog rather than on today's cash flow, which is negative because data-centre spending exceeds operating cash. The key debate is whether those contracts earn a good return on the debt-funded build-out.",
)
P["AMD"] = (
    "AMD designs processors: EPYC server chips, Ryzen PC chips, Radeon graphics, Instinct AI accelerators, and embedded chips from its Xilinx acquisition. It owns no factories; TSMC manufactures its chips.",
    "It sells chips to server makers, cloud providers, PC makers and game-console makers (the PlayStation and Xbox use AMD chips). Data centre was about half of 2025 revenue, client PCs about 30%, with gaming and embedded the rest. Profit depends on winning share from Intel in CPUs and from Nvidia in AI accelerators.",
    "AMD is priced on forward earnings and on expected AI-accelerator growth; trailing earnings understate it because of large amortisation charges from the Xilinx deal. The multiple moves with each new data-centre customer win or loss.",
)
P["MU"] = (
    "Micron is one of three companies in the world that make DRAM memory at scale (with Samsung and SK Hynix), and a major maker of NAND flash storage. Its high-bandwidth memory (HBM) sits next to the processors in AI servers.",
    "Micron sells memory chips by the gigabyte to makers of servers, PCs, phones and cars. Memory is close to a commodity, so prices swing with supply and demand: in shortages margins are enormous, in gluts the company can lose money. HBM for AI has lifted prices and made the current upswing unusually strong.",
    "Memory stocks are valued on price to book value and on mid-cycle earnings, not on peak earnings: a low P/E at the top of the cycle is a warning, not a bargain. The stock moves with memory prices and AI-server demand.",
)
P["LRCX"] = (
    "Lam Research makes the machines that deposit and etch the microscopic layers on silicon wafers. Every leading chipmaker, including TSMC, Samsung, Intel and the memory makers, uses its equipment.",
    "It sells equipment costing millions of dollars per tool to chipmakers building or upgrading factories, then earns recurring revenue from spare parts, upgrades and service on its large installed base. New-equipment sales follow chipmakers' spending cycles; service revenue is steadier.",
    "Semiconductor-equipment stocks are valued on earnings across the cycle and on industry capital-spending forecasts. The multiple rises when chipmakers announce new factories and falls when memory spending is cut or export rules to China tighten.",
)
P["INTC"] = (
    "Intel designs and manufactures processors for PCs and servers and is trying to become a contract chipmaker for other companies (Intel Foundry). It is one of the few companies that both design and make leading-edge chips.",
    "Most revenue still comes from selling Core PC processors and Xeon server processors to computer makers; PCs are the largest group, data centre the second. The foundry business makes Intel's own chips and is trying to win outside customers; it is losing billions a year while it builds new factories.",
    "With earnings depressed, Intel is valued on price to book value and on hopes for its turnaround. P/E is not meaningful. The stock moves with progress on its new manufacturing processes and on landing outside foundry customers.",
)
P["CSCO"] = (
    "Cisco is the largest maker of corporate networking equipment (routers, switches, Wi-Fi) and sells security, collaboration (Webex) and observability software, including Splunk, acquired in 2024.",
    "It sells networking hardware to companies, governments, telecom carriers and increasingly cloud providers building AI networks, then charges for support contracts and software subscriptions. More than half of revenue is now recurring software and services.",
    "Cisco is valued as a mature cash generator: on P/E, free cash flow yield and its dividend and buybacks. Growth expectations are modest, so the multiple moves with signs that AI networking and Splunk can lift growth.",
)
P["PLTR"] = (
    "Palantir builds software that pulls together an organisation's data so that analysts and AI models can act on it. It started with US intelligence and defence agencies and now sells widely to companies through its AI Platform (AIP).",
    "Customers pay multi-year subscription fees. In 2025 government work was a little over half of revenue and commercial customers the rest, with US commercial the fastest-growing part. Revenue per customer rises as deployments spread across an organisation.",
    "Palantir is valued on a multiple of sales and on its growth rate, not on earnings: it trades at one of the highest valuations of any large company. The stock is driven by growth momentum and AI sentiment; any slowdown can cut the multiple sharply.",
)
P["AMAT"] = (
    "Applied Materials is the largest maker of chip-manufacturing equipment, covering deposition, etching, ion implantation and inspection. It also supplies equipment for display panels.",
    "It sells production tools to chipmakers expanding or upgrading factories, then earns service and spare-parts revenue from a large installed base. Sales follow chipmakers' spending, with China a large and politically sensitive customer.",
    "Like other equipment makers, it is valued on earnings through the cycle and on forecasts for industry wafer-equipment spending. Export controls on China are the most frequent cause of multiple swings.",
)
P["IBM"] = (
    "IBM is an enterprise technology company built around hybrid cloud software (Red Hat), automation, data and AI software, IT consulting, and mainframe computers that still run most of the world's bank transactions.",
    "Software is the largest and most profitable part, at a little under half of 2025 revenue, mostly subscriptions and support. Consulting is about 30%, sold by project. Infrastructure, mainly mainframes, rises and falls with the product cycle.",
    "IBM is valued on free cash flow and its dividend. The multiple has risen as software became most of the profit; investors pay up when software growth holds near double digits.",
)
P["TXN"] = (
    "Texas Instruments makes analog and embedded-processing chips: the tens of thousands of power-management, signal and control chips inside cars, factory equipment, appliances and electronics.",
    "It sells huge volumes of low-cost chips to more than 100,000 customers, mostly industrial and automotive, largely through its own website. It manufactures in its own factories on 300-millimetre wafers, which lowers unit cost, and is spending heavily to expand them.",
    "TI is valued on free cash flow per share, the measure management itself targets, and on its dividend record. Today's heavy factory spending depresses free cash flow, so the stock depends on investors believing that cash will return once spending falls.",
)
P["QCOM"] = (
    "Qualcomm designs the Snapdragon processors and modems used in most premium Android phones, and licenses the wireless patents that nearly every phone maker pays for. It is expanding into PCs, cars and connected devices.",
    "Two businesses. Chips (QCT) are most of revenue and are sold to phone makers, with Apple's modem business winding down. Licensing (QTL) is smaller but very profitable: phone makers pay a royalty on every handset sold. Automotive and IoT chips are the growth areas.",
    "Qualcomm trades on a low P/E for a chip company because of dependence on smartphones and the loss of Apple modem sales. The multiple moves with progress in cars and PCs.",
)
P["CRM"] = (
    "Salesforce is the largest provider of customer-relationship software: Sales Cloud, Service Cloud, marketing tools, Slack, Tableau and MuleSoft. It is pushing Agentforce, AI agents that handle customer service and sales tasks.",
    "Almost all revenue is subscriptions, priced per user per year, sold to companies of every size under multi-year contracts. Growth comes from adding users, selling more products to existing customers, and price increases.",
    "Salesforce has moved from being valued on sales growth to being valued on free cash flow and earnings now that growth has slowed to about 10%. The debate is whether AI agents grow seat-based revenue or cannibalise it.",
)
P["ACN"] = (
    "Accenture is the largest IT services and consulting firm in the world, with roughly 780,000 employees advising companies and governments on technology, operations and strategy.",
    "It sells people's time and expertise: consulting projects, plus multi-year managed-services contracts to run clients' IT and business processes. Revenue is spread across industries such as consumer products, health and public services, financial services and telecom.",
    "Accenture is valued on P/E and free cash flow as a high-quality but people-intensive business. The multiple has fallen on fears that generative AI shrinks the number of consultants clients need.",
)
P["INTU"] = (
    "Intuit makes TurboTax, QuickBooks accounting software, Credit Karma and Mailchimp. It serves consumers, the self-employed and small businesses in the US and a few other countries.",
    "Mostly subscriptions and fees. QuickBooks charges small businesses monthly and earns more from payroll and payments processing. TurboTax charges per tax return, so revenue is highly seasonal and concentrated in its fiscal third quarter. Credit Karma earns referral fees when members take out loans and cards.",
    "Intuit is valued on forward earnings and free cash flow as a high-quality compounder. The multiple depends on small-business platform growth and on whether free or AI-driven tax filing erodes TurboTax.",
)
P["ADBE"] = (
    "Adobe makes the standard software for creative professionals (Photoshop, Illustrator, Premiere), documents (Acrobat, PDF) and digital marketing (Experience Cloud). It is adding generative AI through its Firefly models.",
    "Nearly all revenue is subscriptions. Digital Media (Creative Cloud and Document Cloud) was about three-quarters of fiscal 2025 revenue; Digital Experience sells marketing and analytics software to large companies.",
    "Adobe is valued on forward earnings and free cash flow, and its multiple has fallen sharply on fears that AI image and video tools let users bypass Creative Cloud. Evidence of AI lifting revenue is what would re-rate it.",
)
P["NOW"] = (
    "ServiceNow sells a cloud platform that automates internal company workflows: IT service management, HR, customer service and security operations. Most of the Fortune 500 use it.",
    "Subscriptions are nearly all revenue, sold on multi-year contracts and priced by user and by module. Customers rarely leave (renewal rates near 98%) and expand by adding workflows and, now, AI agents.",
    "ServiceNow is valued on free cash flow and forward earnings at a high premium for its durable 20%-plus growth. Its high multiple makes it sensitive to any slowing in new contracts.",
)
P["META"] = (
    "Meta owns Facebook, Instagram, WhatsApp and Messenger, used by more than three billion people a day. It is spending heavily on AI models and data centres and on Reality Labs (virtual-reality headsets and smart glasses).",
    "Almost entirely advertising: about 98% of 2025 revenue. Businesses buy ads targeted by Meta's AI ranking systems. Revenue grows with the number of ads shown and the price per ad. Reality Labs loses more than $15 billion a year.",
    "Meta is valued on P/E and free cash flow, and the debate is about its spending: the market rewards it when ad growth outruns AI capital expenditure and punishes it when spending runs ahead of returns.",
)
P["NFLX"] = (
    "Netflix is the largest paid video-streaming service in the world, with more than 300 million paying households in over 190 countries. It makes and licenses films and series and has added live events and games.",
    "Monthly subscriptions are nearly all revenue; the US and Canada are the largest region at about 45%. Growth comes from new members, price increases, the crackdown on password sharing, and a cheaper ad-supported plan that also earns advertising revenue.",
    "Netflix is valued on forward earnings and free cash flow as a growth company. Investors watch operating margin expansion and ad revenue more than subscriber counts, which it no longer reports quarterly.",
)
P["TMUS"] = (
    "T-Mobile US is the second-largest US wireless carrier by subscribers and the leader in 5G coverage. It also sells home internet over its 5G network and is building fibre through joint ventures.",
    "Monthly service plans, mainly postpaid phone plans (about two-thirds of 2025 revenue), plus prepaid plans and phone sales. Profit grows by adding customers, selling premium plans, and spreading the cost of its network over more users.",
    "Carriers are valued on EV/EBITDA and free cash flow per share. T-Mobile earns a premium over AT&T and Verizon because it has been taking market share; that premium narrows if price competition increases.",
)
P["VZ"] = (
    "Verizon is a large US wireless carrier with a reputation for network quality, and a broadband provider through its Fios fibre network, expanded by the acquisition of Frontier Communications.",
    "Most revenue is monthly wireless service from consumers and businesses, plus phone sales and Fios internet. The business is mature: subscriber growth is slow, and profit growth comes from price increases and cost cuts.",
    "Verizon is valued like a bond: on its dividend yield, free cash flow and EV/EBITDA. Investors focus on whether free cash flow covers the dividend and pays down debt, and the stock moves with interest rates.",
)
P["DIS"] = (
    "Disney owns Disney, Pixar, Marvel, Star Wars and ESPN, the ABC network, Disney+ and Hulu, and theme parks and cruise ships around the world.",
    "Three segments. Experiences (parks, resorts, cruises, merchandise) earns most of the operating profit. Entertainment covers films, TV networks and streaming, with streaming now profitable. Sports is ESPN. The characters feed every segment: a hit film sells tickets, toys and park visits.",
    "Disney is valued on forward earnings and on a sum of the parts, with the parks valued separately. The multiple depends on streaming profits rising faster than traditional TV declines.",
)
P["T"] = (
    "AT&T is the third-largest US wireless carrier and the largest fibre broadband provider. It sold its media assets (WarnerMedia) in 2022 to concentrate on connectivity.",
    "Monthly wireless plans make up most revenue, plus fibre internet and business services. Legacy copper phone lines and business voice are shrinking. Profit growth comes from fibre subscribers and cost cutting.",
    "AT&T is valued on free cash flow, EV/EBITDA and dividend yield. Investors focus on debt reduction and buybacks, and the stock trades like an income investment sensitive to interest rates.",
)
P["CMCSA"] = (
    "Comcast is the largest US cable broadband provider (Xfinity) and owns NBCUniversal: the NBC network, Peacock streaming, Universal Pictures and Universal theme parks. In 2024 it decided to spin off most of its cable TV channels into a new company, Versant.",
    "Connectivity is most of the profit: monthly broadband, mobile and TV bills from homes and businesses. NBCUniversal earns advertising, licensing, box-office and theme-park revenue. Broadband customer numbers are now slowly falling as fibre and 5G home internet compete.",
    "Comcast is valued on free cash flow, EV/EBITDA and a low P/E because investors expect broadband to shrink. The multiple would rise only with evidence that broadband losses have stopped.",
)
