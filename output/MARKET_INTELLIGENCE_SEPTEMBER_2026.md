# Market Intelligence Report — September 2026

*Generated: 2026-09-07*
*Status: STRATEGIC — Core thesis validation and competitive landscape*

---

## Executive Summary

The market research supports the thesis strongly—but it also tells us **where not to compete**. The broad ideas are already being built. The opportunity is to go much narrower and own the ugly data layer that the broad platforms cannot economically maintain.

---

## Key Shopify Data Points

| Metric | Value | Source |
|--------|-------|--------|
| AI-referred shoppers conversion rate | 2× organic in spec-led categories | Shopify Q2 2026 |
| AI-attributed orders from long-tail | 71% | Shopify 2025 |
| Catalog data vs scraped data conversion | 2× better | Shopify Q2 2026 |
| Categories outside top 100 | 55% of Shopify sales | Shopify 2025 |

**Core economic premise:** AI is disproportionately useful when the purchase requires reasoning about specifications, compatibility, context or suitability.

---

## Market Map

| Opportunity | Demand | Competitors | Gap | Score |
|-------------|--------|-------------|-----|-------|
| Agentic Job Broker | Very strong | Checkatrade, Bark, Taskrabbit, Thumbtack, Rightcharge | Accepted-job routing + agent-native + vertical UK supply | **9.5/10** |
| Free Front Desk → Supplier Graph | Extremely strong | Probook, Avoca, ServiceTitan | Free/WhatsApp-first for small UK trades as data acquisition | **9/10** |
| Agentic Replacement Broker | Extremely strong | FixPart, Partium, PartsNow | Cross-supplier fitment + local-language + geographical routing | **9.5/10** |
| Visual Compatibility Graph | Proven | Partium, PartsNow, Shopify image search | Exact compatibility + negative fitment + supersessions | **9/10 moat** |
| Photo → PO for trades | Proven | MRO Command, SpareFinder, Buyer24, Corivo | Small trades + local wholesalers instead of industrial enterprise | **8/10** |
| Supplier Normalization Layer | Huge established market | Akeneo, Pimcore, Plytix, Salsify | Tiny analogue suppliers → machine API automatically | **8.5/10 infra** |
| Compatibility/Fitment API | Proven category | ACES/PIES, Parts Resolve | Non-automotive vertical fitment | **9/10 asset** |
| Agentic Aftersales-as-a-Service | Strong | Partful, Partium, Akeneo | Smaller OEM/distributor long tail | **8/10** |
| Nordic Installed-Base Microverticals | Excellent structural demand | Vertical incumbents vary | Hyper-specific language + legacy + supersession niches | **9/10 research target** |
| Supplier Trust Graph | Clearly valuable | Checkatrade/Thumbtack ratings | Outcome-derived machine trust | **8.5/10 moat** |

---

## Competitor Intelligence

### Agentic Job Broker
- **Google AI Mode** handles local service pricing/availability but does NOT create final booking
- **Taskrabbit API** exposes Estimate → Availability → Bid → Book → Project status
- **Thumbtack** moving photo/voice → problem diagnosis → professional (87% find it valuable, 300K businesses)
- **GeraHome** claims REST + MCP for provider search/availability/insurance/pricing/booking (20-60 countries)
- **Checkatrade** starts at £59/month, sends job to up to 3 installers
- **Rated People** receives ~1M job posts annually
- **Bark** £1.80/credit, lead cost depends on service/scope
- **Rightcharge** combines charger recommendation + installer network + energy tariff

### Compatibility Dropship
- **FixPart** operates across Norway, Finland, Sweden, Denmark, UK. Claims 15M+ spare parts. Has model-based fitment and "guaranteed fit" feature. Photo identification service available.
- **Partium** image/OCR/semantic text/barcode/BoM search. Deutsche Bahn: 95 plants, 12,200 users, 46,800 person-days saved annually.
- **PartsNow** Photo Match launched July 2026 for heavy-duty truck parts
- **Shopify Catalog API** now supports image search + multimodal text+image search

### Supplier OS
- **Probook** $40M funding, 58K daily interactions, 82% automation, dispatch-focused
- **Avoca** $125M raised, inbound/outbound AI, 70% call volume handled
- **ServiceTitan** Voice Agent with booking, rescheduling, cancellation, real-time availability

### Photo-to-PO
- **MRO Command** photo/text/email → AI identifies part → constructs RFQ → sends to vendors → normalizes quotes → compares price/lead time/freight → generates PO. 5,000+ MRO suppliers.
- **Buyer24** urgent multi-supplier RFQs, cross-reference matching, automated supplier follow-ups
- **Corivo** connects component to asset history, previous suppliers, price, lead time, purchase history
- **Andustry** (YC) AI-native broker for industrial equipment

### Supplier Normalization
- **Akeneo** AI Supplier Data Manager extracts, maps, normalizes from arbitrary formats (spreadsheets, documents)
- **Shopify** says catalogs commonly begin as supplier spreadsheets, model numbers, sparse fields

### Compatibility/Fitment
- **ACES/PIES** automotive industry standard for fitment
- **Parts Resolve** evidence-backed supersession, cross-reference, fitment APIs for automotive
- **Walmart** requires manufacturer brand + exact MPN for fitment records

### Aftersales
- **Partful** converts CAD+BOM into interactive parts catalogs. Research claims: only 15% consumers find parts from manufacturer, 52% professionals difficulty identifying parts, 67% parts revenue leaks to third parties.

---

## Marketplaces Are Brutal Competitors

Similarweb September 2026: marketplaces receive ~46.8M monthly AI referral visits, up 237% YoY (33.2M June 2025 → 89.9M May 2026).

**Don't fight where Amazon is clearly better. Own the decision.**

---

## Right-to-Repair Tailwind

EU Right-to-Repair rules began July 31, 2026. Manufacturers must make repair information and spare parts more accessible. European Commission expects €4.8 billion in growth. EU-wide online repair platform due 2027.

More structured OEM parts information becomes legally available. We can normalize it.

---

## The Strategic Stack

```
PROBLEM
    │
    ▼
RESOLUTION GRAPH
    │
    ├─── PRODUCT ──────── compatibility
    │         │
    │         ▼
    │    SUPPLIER ROUTER
    │         │
    │         ▼
    │    best valid seller
    │
    └─── SERVICE ──────── qualification
              │
              ▼
         BID ROUTER
              │
              ▼
         accepted contractor
              │
              └──────► SOLVED
```

---

## What to Pursue

1. **Agentic Job Broker — Nottingham EV**: structured job intake → anonymized broadcast → contractor price/availability response → customer selects → contractor pays lead unlock → details revealed. Test £20/£35/£50 lead-unlock pricing.

2. **GeoDrop Replacement Probe — one Nordic installed-base subsystem**: Finnish heat-pump remotes/controllers/legacy electronics, Norwegian cabin pump/water-system components, robot-mower lifecycle components. Score 500–2,000 candidate SKUs.

3. **One shared graph underneath both**: `asset`, `part`, `compatibility`, `supplier`, `service`, `location`, `availability`, `price`, `credential`, `outcome`.

---

## The Opportunity

What I do NOT see as an established winner is the specific combination:

> **consumer problem/photo → exact machine-readable resolution → geographically optimal physical part or verified local human → transaction, with proprietary compatibility and fulfillment data accumulating underneath.**

That is the opportunity.

---

## Sources

1. Shopify Q2 2026 commerce data
2. Shopify 2025 AI-attributed orders
3. Google AI Mode local services
4. Taskrabbit Home Services API
5. Thumbtack AI experience
6. GeraHome platform
7. Checkatrade pricing
8. Rated People job posts
9. Bark credit system
10. Rightcharge installer network
11. FixPart parts catalog
12. Partium visual search
13. PartsNow Photo Match
14. MRO Command procurement
15. Buyer24 RFQ automation
16. Corivo asset history
17. Andustry industrial sourcing
18. Akeneo supplier normalization
19. ACES/PIES automotive standard
20. Parts Resolve cross-reference API
21. Partful OEM parts catalog
22. Similarweb AI referral traffic
23. EU Right-to-Repair regulation
