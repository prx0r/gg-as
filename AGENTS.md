# AGENTS.md — GG-AS

*For agents using GG-AS to monitor the agent-commerce frontier.*

---

## Mission

GG-AS converts public technical activity in agent-native commerce into **evidence-backed frontier signals**, then into falsifiable product hypotheses.

It watches Shopify/UCP, Google/Merchant Center, Timefold/dispatch, and Anthropic/commerce-agents to find capabilities before they ship.

---

## How GG-AS Works

### 1. Seeding

Start with known high-signal engineers:

```bash
python3 -m gitgoblin.cli seed high-certainty-agentic-commerce igrigorik
python3 -m gitgoblin.cli seed high-certainty-agentic-commerce gil--
```

### 2. Scanning

GG-AS follows their GitHub activity:
- Repos they star
- PRs they review
- Issues they comment on
- People they follow
- Dependencies they add

### 3. Convergence Detection

When **2+ independent experts** interact with the same target, it's a signal.

### 4. Opportunity Emission

Signals are scored and classified:
- **BUILD**: Strong convergence, ready to implement
- **RESEARCH**: Interesting, needs more investigation
- **WATCH**: Early signals, monitor

---

## Campaign System

Campaigns are self-contained rabbit holes for specific topics.

### Creating a Campaign

```bash
mkdir -p campaigns/allaway-finland
cat > campaigns/allaway-finland/config.yaml << 'EOF'
id: allaway-finland
description: "Norwegian maritime spare parts"
seeds:
  - uqp_no
  - copra_no
keywords:
  - maritime
  - spare part
  - Norwegian
status: ACTIVE
EOF
```

### Running a Campaign

```bash
python3 -m gitgoblin.cli campaign run allaway-finland
```

### Adding Fresh Seeds

```bash
python3 -m gitgoblin.cli campaign run allaway-finland --seed newaccount
```

---

## What GitGoblin Is NOT

- ❌ Not a trending repo tracker
- ❌ Not a star counter
- ❌ Not a content scraper
- ❌ Not a startup idea generator

## What GitGoblin IS

- ✅ Frontier-intelligence system
- ✅ Convergence detector
- ✅ Capability tracker
- ✅ Product opportunity engine

---

## Rate Limits

| Source | Limit | Strategy |
|--------|-------|----------|
| GitHub REST | 5,000/hr | Use token, cache aggressively |
| GitHub GraphQL | 5,000 pts/hr | Batch queries |
| OpenAlex | 10 req/sec | Polite pool |
| arXiv | 1 req/3.5s | Required delay |

---

## Protected Processes

**NEVER kill opencode processes.**

The resource monitor (`scripts/resource_monitor.py`) tracks:
- RAM usage (kill GitGoblin if > 85%)
- CPU usage (kill GitGoblin if > 90%)

---

## Key Files

| File | Purpose |
|------|---------|
| `configs/sectors/*.yaml` | Sector configurations |
| `campaigns/*/config.yaml` | Campaign configurations |
| `data/gitgoblin.db` | SQLite database |
| `data/crawl_graph.json` | Visited repos/users/edges |
| `logs/*.log` | Run logs |
| `output/*.md` | Intelligence reports |

---

## MCP Tools

| Tool | Description |
|------|-------------|
| `scan_sector` | Run a frontier scan |
| `get_signals` | Get convergence signals |
| `get_opportunities` | Get product opportunities |
| `run_campaign` | Run a focused campaign |
| `list_campaigns` | List all campaigns |
| `add_seed` | Add a seed builder |
| `search_entities` | Search repos/papers/developers |

---

*For agents, by agents.*
