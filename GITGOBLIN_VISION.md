# GitGoblin Vision — The Intelligence Layer

**Date:** 2026-09-07
**Status:** OPERATIONAL — Building the frontier intelligence system

---

## What GitGoblin Is

**A frontier-intelligence system that watches high-signal engineers and finds convergence before it becomes obvious.**

NOT a trending repo tracker.
NOT a star counter.
NOT a content scraper.

**YES: A rabbit hole machine that follows engineers, finds convergence, and emits product opportunities.**

---

## The Six Modes

| Mode | Time | Use Case | API Calls |
|------|------|----------|-----------|
| **quick** | 2 min | Fast sweep, find signals | 100 |
| **standard** | 5 min | Balanced investigation | 300 |
| **thorough** | 10 min | Deep research | 500 |
| **deepdive** | 20 min | Maximum expansion | 1000 |
| **stealth** | 15 min | Avoid detection | 200 |
| **targeted** | 1 min | Single repo analysis | 50 |

---

## The Campaign System

Each campaign is a self-contained rabbit hole:

```
campaigns/
├── allaway-finland/
│   ├── config.yaml          # Seeds, keywords, thresholds
│   ├── signals/             # Detected signals
│   ├── opportunities/       # Derived opportunities
│   └── run_*.json           # Run logs
```

Campaigns:
1. **Remember where they left off**
2. **Store all observations**
3. **Track seeds and expansion**
4. **Can be resumed with fresh seeds**

---

## The Experiment Logger

Every run is logged with:
- Observations, signals, opportunities
- Duration, API calls
- Quality assessment (HIGH/MEDIUM/LOW/NOISE)
- Recommendation

**After enough runs, you can:**
1. Compare modes — Which gives best signals per minute?
2. Assess quality — Which seeds produce GOLD signals?
3. Optimize budgets — Use quick for testing, thorough for production
4. Track convergence — Are signals improving over time?

---

## What GitGoblin Finds

### Signals (Convergence Detection)

When **2+ independent experts** interact with the same target:

```
igrigorik → UCP
gil-- → UCP
tobi → UCP
        ↓
CONVERGENCE DETECTED
        ↓
This repo is important
```

### Opportunities (Product Derivation)

From signals, GitGoblin derives:
- **BUILD**: Strong convergence, ready to implement
- **RESEARCH**: Interesting, needs more investigation
- **WATCH**: Early signals, monitor

### Algo Surface Changes

Detects when:
- Ranking fields change
- Filter semantics change
- Constraint weights change
- Search context changes
- Checkout capabilities change

---

## The Intelligence Layer for Agent Commerce

GitGoblin watches:

| Layer | What It Tracks |
|-------|----------------|
| **Shopify/UCP** | Protocol changes, new capabilities |
| **Google/Merchant Center** | Feed attributes, AI Max features |
| **Timefold/dispatch** | Scheduling algorithms, constraints |
| **Anthropic/commerce-agents** | Ranking functions, tool schemas |
| **LiveKit/voice** | Booking patterns, turn detection |

**It finds the infrastructure before it ships.**

---

## The Campaign: Allaway Finland

**Goal:** Find the engineers building compatibility graphs for Nordic spare parts.

**Seeds:** igrigorik, gil--, ge0ffrey, alishazal

**What we're looking for:**
- Compatibility graph primitives
- Visual product identification
- Merchant Center feed optimization
- Spare parts database patterns

**Status:** Running

---

## Future Features

### 1. Cross-Repo Concept Pages

Instead of repo summaries, build concept pages:

```
/concepts/serviceability

UCP: serves + distance + filters
Timefold: travel + time window + skills
Probook: service location + tech history + ETA
Hearthline: business availability + booking
```

### 2. Algo Surface Detector

Monitors for changes in:
- Ranking fields
- Filter semantics
- Constraint weights
- Search context
- Checkout capabilities

### 3. MCP Integration

Expose GitGoblin as MCP tools:
- `run_campaign` — Run a focused rabbit hole
- `get_signals` — Get convergence signals
- `compare_modes` — Compare scan strategies

### 4. GraphQL Optimization

Use GitHub GraphQL API for 5-10x efficiency:
- Batch repo lookups
- Single-call graph traversal
- Reduced rate limit consumption

### 5. Historical Data via GH Archive

Use BigQuery/GH Archive for:
- Historical star/fork graphs
- Past contributor activity
- Social graph evolution

**Don't burn live API calls on historical data.**

---

## The Key Insight

**GitGoblin is not the product. It's the intelligence layer that makes the product possible.**

The product is:
- Compatibility graph API
- Supplier normalization
- Agent-native commerce

GitGoblin finds:
- Who's building it
- What they're building
- When it ships
- How to build on top of it

**Point it at geniuses. Repackage their tech. That's the game.**

---

*Vision document: 2026-09-07*
