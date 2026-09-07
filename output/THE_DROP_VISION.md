# The Drop Vision: Fulfillment Layer Beneath Consumer Agents

*Generated: 2026-09-07*
*Status: STRATEGIC — Core thesis and business models*

---

## One Sentence

**We are adapters that turn messy real-world suppliers into reliable, transactable endpoints for AI agents.**

---

## The Problem

ChatGPT owns discovery. It can't own fulfillment.

```
CHATGPT: "Here are 3 EV installers in Nottingham"
CUSTOMER: "Which one is OZEV approved?"
CHATGPT: "... I don't know"
```

ChatGPT can't:
- Validate certifications
- Check real-time availability
- Generate accurate quotes
- Complete service transactions
- Track job completion
- Build supplier trust graphs

---

## The Architecture

```
USER INTENT
    │
    ├─── PRODUCT ──────── "need this pump"
    │         │
    │         ▼
    │    IDENTIFICATION
    │         │
    │         ▼
    │    COMPATIBILITY GRAPH
    │         │
    └─── SERVICE ──────── "install charger"
              │
              ▼
         QUALIFICATION
              │
              ▼
         SERVICE SKU
              │
    ┌─────────┴─────────┐
    ▼                   ▼
SUPPLIER GRAPH
    │
    ├── API/feed supplier
    ├── WhatsApp supplier
    └── phone supplier
         │
         ▼
    NORMALIZER
         ▼
 price / availability /
trust / compatibility / ETA
         ▼
    TRANSACTION
         ▼
payment / booking / PO
         ▼
    FULFILLMENT
         ▼
OBSERVED OUTCOME
         │
         └──────────► THE GRAPH
```

---

## Eleven Business Models

### 1. Supplier OS (AI Front Desk)
- Free tool for contractors
- Voice/SMS/WhatsApp/Web chat
- Qualify leads, check availability, draft quotes, book appointments
- We get: proprietary supply data
- Monetize: procurement affiliate, financing, payments

### 2. Compatibility Dropshipping
- Normalize supplier data (images, descriptions, shipping, compatibility)
- Provide structured feeds to Shopify Catalog
- One-click buy via agent
- We do inventory for suppliers who are shit at tech
- Margin = compensation for solving information entropy

### 3. Photo-to-PO for Tradesmen
- Electrician sends photo + "need two of these tomorrow"
- System identifies part, confirms characteristics, finds alternatives
- Queries Screwfix / wholesalers / independents
- Compares price, stock, distance, delivery, trade discount
- "2 × Hager ___ CEF Derby has stock. £42.80 ex VAT. Collect 07:30 tomorrow."
- Every procurement interaction improves parts graph

### 4. Agentic RFQ Broker
- Customer: "I need a 7kW charger installed at this house"
- System constructs one standardized job object
- Agents contact qualified suppliers via WhatsApp/API/email/phone
- Each response turns into structured quote
- Customer receives three actually executable offers, not three phone numbers
- Commission on outcome

### 5. API Virtualization for Analogue Businesses
- We become the plumber's API
- ChatGPT calls check_availability()
- System knows Jim has no API
- Internally: cache/calendar says maybe → WhatsApp Jim → Jim: 👍 → structured response returned
- Over time we learn his recurring schedule
- Human WhatsApp is just a slow backend adapter

### 6. Service SKUs
- Create standardized offerings: EV-INSTALL-7KW-STANDARD, BOILER-SERVICE-COMBINATION, etc.
- Each has: qualification fields, required certification, expected duration, parts, normal price range, exclusions, warranty, evidence required
- Supplier maps: Jim Electrical supports EV-INSTALL-7KW-STANDARD, £850–£980, 2.5h
- Now agents can transact services like products

### 7. Compatibility Graph as an API
- POST /resolve with manufacturer, model, component
- Returns: OEM number, supersessions, compatible models, alternatives, confidence, evidence
- Sell to: retailers, agents, repair companies, insurers, marketplaces, manufacturers, call centers
- Picks-and-shovels company, not just our own store

### 8. Agentic Aftersales-as-a-Service
- Tell mid-sized manufacturer: "Give us your PDFs, spreadsheets, distributor lists"
- We return: normalized product graph, compatibility graph, Shopify storefront, Catalog-ready data, MCP endpoint, AI parts assistant, photo lookup, checkout, returns, analytics
- Revenue: setup fee + monthly fee + transaction %

### 9. Installed-Base Graph
- Every transaction tells us a household owns something
- Household has: Bosch SMS46MI08E, Zappi v2 charger, Vaillant boiler, Tesla Model 3
- Agent knows: "Your dishwasher pump is failing again"
- Creates recurring demand rather than constantly reacquiring customers

### 10. Verification/Trust Graph
- Don't reduce to star ratings
- Store empirical outcomes: quoted £950, actually invoiced £975; promised Thursday, arrived Thursday; estimated 3h, took 2h47; 187 booked, 181 completed, 3 cancelled supplier-side, 3 customer-side
- Machine-useful trust that AI agents can rank on

### 11. Grants/Compliance/Financing
- EV is constrained by rules: customer eligible? property eligible? installer certification? charger eligible? grant? DNO notification?
- Agent handles paperwork
- Later: EV → solar → battery → heat pump → insulation
- Orchestrate home electrification transaction
- Financing becomes obvious: exact project, quote, supplier, historical performance, customer, asset

---

## Two Clean Experiments

### Experiment A: EV Charger Installers, Nottingham

Build:
- Phone forwarding
- WhatsApp operator interface
- Lead qualification
- Service-area rules
- Certification fields
- Availability
- Quote generation
- Slot hold
- Booking
- Job completion

Onboard **10 electricians for free**. Their dashboard is WhatsApp.

Measure:
- Calls handled
- Qualified leads
- Booking rate
- Time to confirmation
- Accepted jobs
- Actual price
- Completion rate
- Human interventions/job

### Experiment B: One Replacement-Parts Vertical

Choose something with disgusting compatibility complexity:
- Appliance spare parts
- Boiler/HVAC parts
- Coffee-machine parts
- Power-tool parts

Build only:
- Photo/model intake
- Exact part resolver
- Compatibility evidence
- 3 supplier feeds/pages
- Normalized Shopify SKU
- Agent-friendly PDP
- Checkout

100–500 products is enough.

Test: **higher certainty beats Amazon/generalist merchants**

### The Convergence

Someone asks: "My dishwasher isn't draining."

We identify the pump.

```
Would you like:

A. Pump only — £68, tomorrow
B. Pump + installation — £149, Wednesday 10–12
```

Product graph + service graph.

---

## What NOT to Build

- New TTS engine
- Generic voice-agent infrastructure
- Another generic trades CRM
- Another Thumbtack/Checkatrade directory
- Generic visual product search
- Generic chatbot builder
- Another Shopify theme
- Enormous contractor dashboard

All have serious incumbents. Integrate or sit above them.

---

## The Unified Architecture

One kernel. Not two unrelated codebases.

```
PRODUCT GRAPH ──────┐
                    │
SERVICE GRAPH ──────┤
                    │
SUPPLIER GRAPH ─────┼──► NORMALIZER ──► TRANSACTION ──► FULFILLMENT
                    │
COMPATIBILITY ──────┤
                    │
TRUST GRAPH ────────┘
```

---

## The Deepest Moat

Not the storefront. Not the receptionist.

> **For a real-world problem, what exact product/service combination will fix it, who can fulfill it, when, at what price, and with what probability of success?**

That graph does not currently exist.

---

## Crawl Log

1. Voice agents commoditized (Retell $0.07-0.31/min, ServiceTitan Voice Agent)
2. Supplier side missing from ChatGPT's architecture
3. WhatsApp primary operator interface for UK trades
4. Compatibility = fitment, not visual similarity
5. Photo-to-PO for tradesmen = same infrastructure, B2B
6. API virtualization: human WhatsApp as slow backend adapter
7. Service SKUs: how services become agent-readable
8. Compatibility Graph as picks-and-shovels company
9. Aftersales-as-a-Service for OEMs
10. Installed-Base Graph = household infrastructure memory
11. Verification = empirical outcomes, not star ratings
12. Grants/compliance/financing = orchestration layer
13. Two experiments: EV installers + replacement parts
14. Convergence: product graph + service graph
