# GG-AS — GitGoblin Agent Commerce

*Technical alpha for agent-native commerce. Finds engineers building infrastructure before it ships.*

---

## What Is This?

GG-AS is a frontier-intelligence system that watches high-signal engineers and finds convergence before it becomes obvious.

**It is NOT:**
- A trending repo tracker
- A star counter
- A content scraper

**It IS:**
- A rabbit hole machine
- A convergence detector
- A capability tracker
- A product opportunity engine

---

## The Core Loop

```
YOUR DIRTY INTENT
    ↓
INTENT ENGINE (parse what you REALLY want)
    ↓
ENGINEER DISCOVERY (web search for smart people)
    ↓
CORPUS (top 8 highest signal bets)
    ↓
CAMPAIGN (focused rabbit hole)
    ↓
SIGNALS + OPPORTUNITIES
    ↓
QUALITY ASSESSMENT
    ↓
LOG (for future runs)
```

---

## Quick Start

### 1. Parse your intent

```bash
python3 -m gitgoblin.cli mission "I want to come top in Google AI results for Norwegian spare parts"
```

### 2. Run the campaign

```bash
python3 -m gitgoblin.cli campaign run <campaign-id>
```

### 3. Check results

```bash
python3 -m gitgoblin.cli rank --sector <sector>
python3 -m gitgoblin.cli experiments
```

---

## Commands

| Command | Description |
|---------|-------------|
| `mission` | Parse dirty intent into campaign |
| `campaign run` | Run a campaign |
| `campaign list` | List all campaigns |
| `scan` | Run a frontier scan |
| `rank` | View signals |
| `modes` | List scan modes |
| `experiments` | View experiment history |
| `compare` | Compare scan modes |
| `serve` | Start API/dashboard |

---

## Scan Modes

| Mode | Time | Use Case |
|------|------|----------|
| `quick` | 2 min | Fast sweep |
| `standard` | 5 min | Balanced |
| `thorough` | 10 min | Deep research |
| `deepdive` | 20 min | Maximum expansion |
| `stealth` | 15 min | Avoid detection |
| `targeted` | 1 min | Single repo |

---

## Campaigns

Each campaign is a self-contained rabbit hole:

```bash
# Create from mission
python3 -m gitgoblin.cli mission "your intent" --save

# Run campaign
python3 -m gitgoblin.cli campaign run <id>

# Add fresh seeds
python3 -m gitgoblin.cli campaign run <id> --seed newaccount

# List campaigns
python3 -m gitgoblin.cli campaign list
```

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
| `parse_intent` | Parse dirty intent |
| `analyze_with_ai` | Analyze with Cloudflare AI |

---

## What GitGoblin Finds

| Signal Type | What It Means |
|-------------|---------------|
| **BUILD** | Strong convergence, ready to implement |
| **RESEARCH** | Interesting, needs more investigation |
| **WATCH** | Early signals, monitor |

---

## API Usage

| Mode | GitHub Calls | Time |
|------|--------------|------|
| quick | 100 | 2 min |
| standard | 300 | 5 min |
| thorough | 500 | 10 min |
| deepdive | 1000 | 20 min |

---

## Architecture

```
gg-as/
├── gitgoblin/
│   ├── cli.py              # Command-line interface
│   ├── api.py              # REST API
│   ├── mcp_server.py       # MCP tools
│   ├── intent_engine.py    # Dirty intent parser
│   ├── cloudflare_ai.py    # Free AI analysis
│   ├── mission_parser.py   # Mission → campaign
│   ├── scan_modes.py       # Different scan strategies
│   ├── experiment_logger.py # Track all runs
│   ├── api_tracker.py      # Monitor API usage
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
│   ├── algo_surface_detector.py
│   └── resource_monitor.py
├── output/                  # Intelligence reports
├── data/                    # SQLite + cache + experiments
└── logs/                    # Run logs
```

---

## Example: Norwegian Spare Parts

### Your dirty intent:
> "I want to come top in Google AI results and ChatGPT/Shopify listings to sell my dropshipped Norwegian spare parts"

### What GitGoblin parsed:
- **Real intent:** rank
- **Niche:** spare parts
- **Market:** norway
- **Mission:** Find engineers building: rank for spare parts in norway

### What it found:
- 757 observations from 6 engineers
- 0 signals (need more seeds)
- Campaign ready for fresh seeds

---

## The Vision

GitGoblin is the intelligence layer that finds engineers building infrastructure before it ships.

**Point it at geniuses. Repackage their tech. That's the game.**

---

*Documentation generated: 2026-09-07*
