# GitGoblin S-Tier Intelligence Report

*Generated: 2026-09-07*
*Status: VERIFIED — All claims backed by public sources*

---

## Executive Summary

The opportunity isn't "GEO for commerce." It is building the missing stateful compatibility + serviceability + availability graph between intent and transaction.

Products need: WHAT IS THIS? WHAT DOES IT FIT? CAN I GET IT? FROM WHOM? AT WHAT PRICE? WHEN? CAN I TRANSACT?

Services need: WHAT DO YOU DO? CAN YOU DO THIS EXACT JOB? DO YOU SERVE THIS LOCATION? ARE YOU QUALIFIED? WHEN CAN YOU COME? WHAT WILL IT COST? CAN I BOOK?

The front desk is how we keep that service graph current. The Shopify store is how we monetize the product graph.

---

## S-Tier Repos to Clone

| Repository | Why S-tier | What to extract |
|------------|-----------|-----------------|
| Shopify/ucp-cli | Public instructions telling agents how to shop Shopify | query rewriting, context fields, hard filters, seller fields, schema changes |
| Universal-Commerce-Protocol/ucp | The actual future commerce/service grammar | schemas, capabilities, Location, serviceability, constraints |
| Shopify/shop-chat-agent | Shopify's own storefront shopping-agent implementation | MCP tools, auth boundary, prompt, cart/order flow |
| Shopify/claude-for-commerce-examples | Anthropic agents connected to real Shopify | real backend adapters, staged merchant writes |
| anthropics/commerce-agents | Best readable commerce-agent reference architecture | ranking, tools, gates, prompts, evals |
| gil--/ucp-agent-imessage | Real-merchant shopping agent with purchase state machine | provenance, authorization, carts, buyer identity, payment |
| NVIDIA-AI-Blueprints/Retail-Agentic-Commerce | Full open ACP/UCP search/recommendation/promotion stack | actual ranking thresholds and agent configs |
| arenza-ai/agentic-commerce-score | Direct competitor to our Agent Recommendation Lab | readiness features, deterministic scoring |
| codewithmuh/hearthline | Closest open implementation of our free Supplier OS wedge | lead capture, quoting, booking, CRM, call state |
| livekit/agents | Serious open realtime voice runtime | turn detection, tools, telephony, handoffs |
| livekit-examples/python-agents-examples | Production patterns rather than framework abstractions | receptionist, observers, payments, multi-agent booking |
| livekit/sip | Telephony primitive beneath a self-owned receptionist | SIP lifecycle and routing |
| pipecat-ai/pipecat | Alternative fully controlled voice pipeline | frames, STT/LLM/TTS orchestration, interruption |
| bolna-ai/bolna | Entire open hosted-style voice-agent backend | provider abstraction, WebSockets, telephony, Redis |
| TimefoldAI/timefold-solver | Probook-like optimization brain primitive | constraint solving, objective architecture |
| TimefoldAI/timefold-quickstarts | Readable routing/field-service examples | visits, availability, travel, skills |
| Accio-org/BusinessArena | Autonomous ecommerce operator benchmark | strategies, capital allocation, trajectories |
| Accio-org/CommerceAgentBench | Long-horizon commerce task/eval corpus | workflows, verifiers, failure modes |
| vercel/acp-handler | Very clean merchant-side ACP transaction adapter | idempotency, signatures, payment state |
| agentcommercekit/ack | Agent identity/trust/payment receipts | DID, credentials, KYA, receipts |
| daydreamsai/lucid-agents | Machine-commerce service runtime | discovery, schemas, payment admission, tasks |
| paypal/agent-toolkit | Production financial tools designed for agents | invoices, refunds, subscriptions, disputes |
| stripe/ai | Stripe's agent/tool infrastructure | payment agent surfaces |
| openreferral/specification | Years of prior art for structured service directories | organisation/service/location graph model |
| TEN-framework/ten-framework | Third independent open realtime voice architecture | VAD, turn detection, SIP, chained vs realtime |

---

## Key Discoveries

### 1. Shopify/shop-chat-agent

Shopify's official reference storefront AI assistant. Supports natural-language catalog discovery, policy/FAQ search, cart creation+mutation, checkout initiation, order lookup, returns. Communicates through MCP.

Architecture connects to two separate MCP servers:
- STOREFRONT MCP: product/catalog/cart (anonymous-ish commerce state)
- CUSTOMER MCP: orders/customer information (authenticated customer state)

A 401 from customer MCP triggers authorization rather than letting the model improvise around missing identity.

Reusable principle: PUBLIC SUPPLIER CAPABILITIES ≠ CUSTOMER-SPECIFIC STATE ≠ PRIVILEGED MUTATIONS

### 2. UCP Location is much bigger than thought

Location Search supports: natural-language query, distance relation, serviceability relation, structured filters, current item availability, pagination.

`serves` can express point (lat/lng) or address (country/region/postal_code). If the business cannot authoritatively evaluate the service target, the spec says it should reject rather than silently broadening.

Location filters include: open_at, amenities, current item availability. Every requested item must currently be available at that candidate location.

Model Service Graph as a superset of UCP Location, not a bespoke representation.

### 3. Hearthline — closest open Supplier OS

Open-source AI front desk for home-service businesses. Architecture: Voice/SMS/WhatsApp/Email/Web chat → AI receptionist → qualify lead → check availability → draft quote → book appointment → customer/lead/quote/job records.

Stack: Next.js, Django/DRF, Postgres, Vapi (STT→LLM→TTS), Twilio, Claude/OpenAI.

Key bug fixes: application-level dedupe around qualify_lead/draft_quote/book_appointment/check_availability. Treats telephony-verified caller number as authoritative rather than trusting LLM-extracted phone number.

### 4. LiveKit example = Supplier OS prototype

Doheny Surf Desk Booking Agent: five specialized agents (FrontDeskAgent → IntakeAgent → SchedulerAgent → GearAgent → BillingAgent) plus parallel ObserverAgent.

Observer periodically watches conversation and checks safety, injuries, customer profile inconsistencies, skill mismatch, special handling. Injects additional context/guardrails back into active receptionist.

Pattern for EV installation: FAST VOICE AGENT (talk naturally, capture intent) + SLOW OBSERVER (continuously derive property type, homeowner/tenant, parking situation, fuse board, likely DNO requirement, grant eligibility, safety issue, confidence, missing qualification field).

### 5. Voice stack: four levels

| Layer | Projects | Use |
|-------|----------|-----|
| Managed orchestration | Vapi, Retell | Fastest MVP |
| Application-owned realtime | LiveKit Agents | Best balance for us |
| Fully composable pipelines | Pipecat, Bolna, TEN | Maximum control |
| Native speech-to-speech | OpenAI Realtime etc. | Lowest-complexity audio reasoning |

### 6. Schema.org compatibility edges

`isAccessoryOrSparePartFor` and `isConsumableFor` for explicit Product→Product compatibility edges. Belongs in drop immediately.

---

## Event Detectors

```text
ALGO_SURFACE_CHANGED: ranking, score, weight, threshold, filter, sort, relevance, similarity, rerank
DISCOVERY_SURFACE_CHANGED: catalog, search, lookup, query, context, intent, taxonomy, identifier, metadata
SERVICE_GRAPH_CHANGED: location, serves, distance, availability, hours, skills, certification, service_area
TRANSACTION_SURFACE_CHANGED: cart, checkout, order, payment, authorization, capture, refund, idempotency
VOICE_SURFACE_CHANGED: vad, turn_detector, interruption, barge_in, sip, handoff, transfer, latency, tool_call
SUPPLIER_OS_CHANGED: lead, qualification, quote, booking, scheduler, dispatch, technician, crm, fsm
TRUST_SURFACE_CHANGED: identity, credential, provenance, rating, review, reputation, fraud
AGENT_POLICY_CHANGED: prompt, SKILL.md, tool description, guard, policy, approval, permission
EVAL_SURFACE_CHANGED: benchmark, judge, fixture, trajectory, score, pass, simulation
```

Upweight changes inside: `**/schemas/**`, `**/skills/**`, `**/prompts/**`, `**/tools/**`, `**/agents/**`, `**/solver/**`, `**/search/**`, `**/ranking/**`, `**/recommendation/**`, `**/checkout/**`, `**/payments/**`, `**/tests/**`, `**/eval/**`

---

## Competitor Intelligence

**Probook:** 58,000+ customer interactions daily. Del-Air says 90% of dispatching automated across 220+ techs. Dispatch engine uses historical data to continuously reshuffle. Upstream system cleans bookings using equipment age, job data, company-specific business logic. Output includes forecast ETA and revenue.

**Avoca:** Forward Deployed Product Engineer posting leaks stack: TypeScript/JavaScript, Next.js, React, Node/Fastify, PostgreSQL, AWS. Production integrations into customer CRM/FSM systems. Python role notes vector databases, LLMs, agent frameworks.

**Sameday:** Engineering listing exposes AWS, Python, Firebase, React/Next.js.

---

## Data Model

```text
PERSON → REPOSITORY → CONCEPT → CHANGE

Detect: "Five separate ecosystems converging on the same primitive."
That is the alpha.
```

---

## Crawl Log

1. Started from Shopify/ucp-cli → found shop-chat-agent → dual MCP architecture
2. UCP Location schema expanded → serviceability as bridge between products and services
3. Hearthline → closest open Supplier OS implementation
4. LiveKit examples → Doheny Surf Desk → observer pattern for passive qualification
5. Voice stack convergence → four levels identified
6. Schema.org compatibility edges → isAccessoryOrSparePartFor
7. Competitor intelligence → Probook 58K daily, Avoca stack leak, Sameday stack
8. Event detectors → 9 categories for algorithm surface monitoring
