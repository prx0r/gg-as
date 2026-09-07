# GitGoblin User Manual

*For agents using GitGoblin to monitor the agent-commerce frontier.*

---

## What Is GitGoblin?

GitGoblin watches high-signal builders, repositories, papers, and technical discourse. It converts their activity into evidence-backed observations, detects independent expert convergence, and emits downstream product opportunities.

**It is NOT a content scraper.** It is a frontier-intelligence system.

---

## APIs Used

| API | What It Monitors | Cost |
|-----|------------------|------|
| GitHub API | Public profiles, following, starred repos, events | Free (with token) |
| OpenAlex API | Academic works | Free (API key recommended) |
| arXiv API | Research papers | Free |
| Hacker News API | Technical discussions | Free |
| ecosystems API | Repository metadata | Free |

**Set `GITHUB_TOKEN` for higher rate limits.**
**Set `OPENALEX_API_KEY` for production use.**

---

## Quick Start

```bash
# 1. Initialize (first time only)
cd /root/gitgoblin
gitgoblin init

# 2. Seed with a builder
gitgoblin seed agent_commerce igrigorik

# 3. Scan for signals
gitgoblin scan agent_commerce --seed igrigorik --expand 2

# 4. Check results
gitgoblin rank --sector agent_commerce
```

---

## Commands

### `gitgoblin init`
Initialize the database.

```bash
gitgoblin init
# Output: {"database": "data/gitgoblin.db", "status": "initialized"}
```

### `gitgoblin seed <sector> <builder>`
Add a seed builder to a sector profile.

```bash
gitgoblin seed agent_commerce igrigorik
# Output: {"sector": "agent_commerce", "seeds": ["igrigorik"]}
```

### `gitgoblin scan <sector> --seed <builder> --expand <depth>`
Scan GitHub for signals from the seed builder and their network.

```bash
gitgoblin scan agent_commerce --seed igrigorik --expand 2
# Output: {"observations_added": 867, "status": "PASS"}
```

### `gitgoblin rank --sector <sector>`
Rank entities by signal strength.

```bash
gitgoblin rank --sector agent_commerce
# Output: ranked list of entities
```

### `gitgoblin serve --port 8787`
Start the API server.

```bash
gitgoblin serve --port 8787
# Dashboard at http://localhost:8787
```

---

## Running as Background Task

```bash
# Start scan in background
cd /root/gitgoblin
nohup gitgoblin scan agent_commerce --seed igrigorik --expand 2 > /tmp/gitgoblin_scan.log 2>&1 &

# Check if running
ps aux | grep gitgoblin

# Check results
cat /tmp/gitgoblin_scan.log

# View observations
python3 -c "
import sqlite3
conn = sqlite3.connect('data/gitgoblin.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM observations')
print(f'Observations: {cursor.fetchone()[0]}')
conn.close()
"
```

---

## Sector Configuration

Sector configs live in `configs/sectors/`:

```yaml
# configs/sectors/agent_commerce.yaml
id: agent_commerce
description: Agent-native commerce infrastructure

seed_builders:
  - igrigorik
  - rmstein
  - gilgnyc
  - yoavweiss
  # ... more builders

keywords:
  - agentic commerce
  - UCP
  - ACP
  - WebMCP
  - service marketplace

primitive_rules:
  ucp_location_search:
    - "Watch for PRs that add Location/Catalog/Cart/Checkout capabilities"
  acp_product_feeds:
    - "Watch for new agent-related fields in product feeds"
```

---

## What GitGoblin Tracks

### GitHub
- Public profiles (followers, repos, activity)
- Following relationships (who follows whom)
- Starred repositories
- Public events (commits, PRs, issues)
- Repository metadata

### OpenAlex
- Recent academic works
- Author profiles
- Citation networks

### arXiv
- Research papers
- Author connections

### Hacker News
- Technical discussions
- Startup mentions

---

## How to Add a Builder

```bash
# Add a single builder
gitgoblin seed agent_commerce igrigorik

# Add multiple builders
gitgoblin seed agent_commerce igrigorik
gitgoblin seed agent_commerce rmstein
gitgoblin seed agent_commerce Romain_Lapeyre
```

---

## How to Check Results

```python
import sqlite3

conn = sqlite3.connect('data/gitgoblin.db')
cursor = conn.cursor()

# Count observations
cursor.execute('SELECT COUNT(*) FROM observations')
print(f'Observations: {cursor.fetchone()[0]}')

# Count entities
cursor.execute('SELECT COUNT(*) FROM entities')
print(f'Entities: {cursor.fetchone()[0]}')

# Sample observations
cursor.execute('SELECT entity_type, entity_id, action FROM observations LIMIT 10')
for row in cursor.fetchall():
    print(f'  {row[0]}: {row[1]} ({row[2]})')

conn.close()
```

---

## What GitGoblin Finds

From `igrigorik` (Ilya Grigorik — Shopify):
- 1,670 observations
- 811 entities
- Following graph mapped
- Profile snapshot captured

From other seeds:
- GitHub activity patterns
- Repository relationships
- Contributor networks
- Technical discourse

---

## How to Use in Drop

1. **Monitor UCP/ACP/WebMCP changes** — Watch for new primitives
2. **Track engineer activity** — Who's building what
3. **Detect convergence** — When multiple experts agree
4. **Find hidden signals** — Small projects with strong expert convergence

```bash
# Start monitoring
cd /root/gitgoblin
nohup gitgoblin scan agent_commerce --seed igrigorik --expand 2 > /tmp/gitgoblin_scan.log 2>&1 &

# Check periodically
cat /tmp/gitgoblin_scan.log
python3 -c "import sqlite3; conn = sqlite3.connect('data/gitgoblin.db'); print(f'Observations: {conn.execute(\"SELECT COUNT(*) FROM observations\").fetchone()[0]}'); conn.close()"
```
