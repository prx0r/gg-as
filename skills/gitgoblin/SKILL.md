---
name: gitgoblin
description: "Frontier intelligence for agent-commerce. Finds engineers, detects convergence, tracks capability shipping."
version: 1.0.0
author: dropintel
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [research, intelligence, github, ecommerce]
    related_skills: [web-search]
    requires_tools: [terminal]
---

# GitGoblin — Frontier Intelligence

Find engineers building infrastructure before it ships. Detect convergence. Track capability shipping.

## When to Use

- User wants to find who's building something specific
- User wants to track a niche or technology
- User wants to detect when capabilities ship
- User wants to find hidden practitioners (not just famous builders)

## How It Works

### Step 1: Parse the User's Intent

The user will give you a dirty intent like:
> "I want to come top in Google AI results for Norwegian spare parts"

Parse this into structured data:
- Real intent: rank
- Niche: spare parts  
- Market: norway

### Step 2: Find Engineers

Search for practitioners who TEST agent preferences, not just builders.

```bash
cd /root/gg-as
python3 -c "
import sys
sys.path.insert(0, '.')
from gitgoblin.intent_engine import find_engineers_websearch
seeds = find_engineers_websearch({'real_intent': 'rank', 'niche': 'spare parts', 'market': 'norway'})
for s in seeds:
    print(f'@{s[\"handle\"]}: {s[\"reason\"]}')
"
```

### Step 3: Run GitGoblin Scan

```bash
cd /root/gg-as
export GITHUB_TOKEN=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

python3 -m gitgoblin.cli scan high-certainty-agentic-commerce \
    --seed <engineer1> --seed <engineer2> \
    --mode quick
```

### Step 4: Check Results

```bash
python3 -m gitgoblin.cli rank --sector high-certainty-agentic-commerce
```

### Step 5: Analyze with AI

```bash
python3 -c "
import sys
sys.path.insert(0, '.')
from gitgoblin.cloudflare_ai import cloudflare_ai
result = cloudflare_ai.analyze_signal({
    'target_id': '<repo>',
    'technical_alpha': <score>,
    'expert_count': <count>
})
print(result['analysis'])
"
```

## What GitGoblin Finds

| Signal Type | What It Means |
|-------------|---------------|
| BUILD | Strong convergence, ready to implement |
| RESEARCH | Interesting, needs more investigation |
| WATCH | Early signals, monitor |

## Rate Limits

- GitHub: 5,000/hr with token
- Use `--mode quick` for testing (100 calls, 2 min)
- Use `--mode standard` for real runs (300 calls, 5 min)

## Output Format

Always report:
1. Engineers found
2. Signals detected
3. Opportunities derived
4. Quality assessment (HIGH/MEDIUM/LOW)
5. Recommendation

## Pitfalls

- Seeds must be in same niche for convergence
- GitHub accounts with no public activity return 0 observations
- Don't burn all API calls on one run

## Verification

Check that:
- Observations > 0
- At least 1 signal detected (or explain why not)
- Quality assessment is reasonable
