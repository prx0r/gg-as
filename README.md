# GG-AS — GitGoblin Agent Commerce

*Technical alpha for agent-native commerce. Watches Shopify/UCP, Google/Merchant Center, Timefold/dispatch, and Anthropic/commerce-agents to find capabilities before they ship.*

---

## What Is This?

GG-AS is a frontier-intelligence system focused on the agent-commerce stack. It watches high-signal engineers, repositories, and protocol changes to detect:

- New ranking signals
- Filter semantics changes
- Compatibility primitives
- Voice/dispatch patterns
- Attribution mechanisms

**It is NOT a content scraper.** It is a frontier-intelligence system.

---

## Quick Start

```bash
# 1. Setup
cd /root/gg-as
pip install -e '.[dev]'
cp .env.example .env
# Add GITHUB_TOKEN to .env

# 2. Initialize
python3 -m gitgoblin.cli init

# 3. Run a scan
python3 -m gitgoblin.cli scan high-certainty-agentic-commerce \
    --seed igrigorik --seed gil-- --mode quick

# 4. Check results
python3 -m gitgoblin.cli rank --sector high-certainty-agentic-commerce
```

---

## Commands

### `scan` — Run a frontier scan

```bash
# Quick mode (GitHub only, fast)
python3 -m gitgoblin.cli scan <sector> --seed <builder> --mode quick

# Thorough mode (GitHub + arXiv)
python3 -m gitgoblin.cli scan <sector> --seed <builder> --mode thorough

# Full mode (everything)
python3 -m gitgoblin.cli scan <sector> --seed <builder> --mode full
```

### `rank` — View signals

```bash
python3 -m gitgoblin.cli rank --sector <sector> --limit 20
```

### `campaign` — Run a focused rabbit hole

```bash
# Run a campaign
python3 -m gitgoblin.cli campaign run allaway-finland

# Add fresh seeds
python3 -m gitgoblin.cli campaign run allaway-finland --seed newaccount

# List campaigns
python3 -m gitgoblin.cli campaign list
```

### `serve` — Start API/dashboard

```bash
python3 -m gitgoblin.cli serve --port 8787
# Dashboard: http://localhost:8787
# API docs: http://localhost:8787/docs
```

### Background Mode

```bash
# Watch mode (scans every 6 hours)
./run.sh watch high-certainty-agentic-commerce

# Or use scheduler directly
nohup python3 -m gitgoblin.scheduler \
    --sector high-certainty-agentic-commerce \
    --interval 3600 &
```

---

## Campaigns

Campaigns are self-contained rabbit holes for specific topics.

```bash
# Create campaign
mkdir -p campaigns/my-campaign
cat > campaigns/my-campaign/config.yaml << 'EOF'
id: my-campaign
description: "What we're investigating"
seeds:
  - engineer1
  - engineer2
keywords:
  - compatibility
  - spare part
status: ACTIVE
EOF

# Run campaign
python3 -m gitgoblin.cli campaign run my-campaign

# Add fresh seeds
python3 -m gitgoblin.cli campaign run my-campaign --seed newaccount
```

---

## MCP Server

GG-AS exposes tools via MCP for agent integration:

```bash
# Start MCP server
python3 -m gitgoblin.mcp_server
```

### Available Tools

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

## What GitGoblin Finds

| Signal Type | What It Means |
|-------------|---------------|
| **BUILD** | Strong convergence, ready to implement |
| **RESEARCH** | Interesting but needs more investigation |
| **WATCH** | Early signals, monitor for changes |

### Scoring

| Metric | Range | Meaning |
|--------|-------|---------|
| technical_alpha | 0-1 | How important is this convergence? |
| confidence | 0-1 | How sure are we? |
| novelty | 0-1 | How new is this? |
| momentum | 0-1 | Is activity accelerating? |

---

## Rate Limits

| Mode | GitHub Calls | Time |
|------|--------------|------|
| quick | ~100 | 1-2 min |
| thorough | ~300 | 3-5 min |
| full | ~500 | 5-10 min |

**Always use `--mode quick` for testing.**

---

## File Structure

```
gg-as/
├── gitgoblin/
│   ├── cli.py              # Command-line interface
│   ├── api.py              # REST API
│   ├── mcp_server.py       # MCP tools
│   ├── pipeline/
│   │   ├── scout.py        # Main scan orchestrator
│   │   ├── signals.py      # Signal detection
│   │   └── opportunities.py
│   ├── sources/
│   │   ├── github.py       # GitHub collector
│   │   ├── arxiv.py        # arXiv collector
│   │   └── openalex.py     # OpenAlex collector
│   └── db.py               # SQLite store
├── configs/sectors/         # Sector configurations
├── campaigns/               # Focused rabbit holes
├── scripts/
│   ├── algo_surface_detector.py  # Detect ranking changes
│   └── resource_monitor.py       # RAM/CPU protection
├── output/                  # Intelligence reports
├── data/                    # SQLite + cache
└── logs/                    # Run logs
```

---

## Why This Matters for Agent Commerce

GitGoblin finds the engineers building the infrastructure we need:

| What We Need | Who Builds It | GitGoblin Finds |
|--------------|---------------|-----------------|
| Compatibility graphs | Shopify/UCP engineers | PRs, schemas, capabilities |
| Ranking signals | Google/Merchant Center | Feed attributes, AI Max |
| Voice/dispatch | LiveKit, Timefold | Booking patterns, constraints |
| Attribution | OpenAttribution | Content tracking protocols |

**The alpha is in the implementation details, not the repos themselves.**

---

*Documentation generated: 2026-09-07*
