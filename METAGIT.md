# MetaGit — What We Learned About GitGoblin

**Date:** 2026-09-07
**Core Motivation:** I want my product to be the thing that Google AI talks about and recommends, and ChatGPT with Shopify/Etsy etc.

---

## What GitGoblin Is Actually Good At

### It's NOT good at:
- Finding trending repos (that's GitHub Trending)
- Predicting which startups will succeed (that's VC)
- Generating business ideas (that's ChatGPT)

### It IS good at:
- **Following engineers** → finding who they interact with
- **Detecting convergence** → 2+ experts on same thing = signal
- **Tracking capability shipping** → when PRs merge, when docs update
- **Finding the hidden practitioners** → not the famous ones, the ones actually testing

---

## The Key Insight from This Run

**The alpha is not in the infrastructure engineers (igrigorik, gil--).**

**The alpha is in the practitioners who TEST the infrastructure.**

| Type | Example | Value |
|------|---------|-------|
| Infrastructure engineer | igrigorik (builds UCP) | Medium — tells you what's shipping |
| Practitioner tester | AndrewLolk (tests AI Max) | **High** — tells you what actually works |
| Hidden expert | FeedArmy (identified 8 attributes) | **Highest** — found the signal before everyone else |

**GitGoblin should weight practitioners higher than builders.**

---

## What We Learned About Seeds

### Bad seed strategy:
```
Seed with famous engineers
    ↓
They work on different things
    ↓
No convergence detected
    ↓
0 signals
```

### Good seed strategy:
```
Seed with practitioners in SAME niche
    ↓
They interact with each other
    ↓
Convergence detected
    ↓
Real signals
```

**Example:**
- @AndrewLolk tests AI Max Shopping
- @mikeryanretail tests AI Max Shopping
- @FeedArmy identified the attributes
- They all interact on the same topics

**That's convergence. That's signal.**

---

## What We Learned About Modes

| Mode | Best For | Worst For |
|------|----------|-----------|
| quick | Testing if seeds work | Finding deep signals |
| standard | Balanced investigation | Time-critical research |
| thorough | Deep research | Quick questions |
| deepdive | Maximum expansion | Budget-conscious |
| stealth | Avoiding detection | Speed |
| targeted | Single repo analysis | Broad discovery |

**The insight:** Use `quick` to test seeds, then `standard` for real runs.

---

## What We Learned About Campaigns

### Campaigns work when:
- Seeds are in the same niche
- Seeds interact with each other
- The niche has active builders

### Campaigns don't work when:
- Seeds are from different domains
- Seeds don't overlap on repos
- The niche is too broad

**Example:**
- "Google AI ads" campaign → Works (AndrewLolk, mikeryanretail, FeedArmy all overlap)
- "Norwegian spare parts" campaign → Doesn't work (no GitHub presence)

---

## What We Learned About AI Analysis

**Cloudflare AI is useful for:**
- Analyzing signals (what does this convergence mean?)
- Generating hypotheses (what should we build?)
- Summarizing findings (what did we learn?)

**Cloudflare AI is NOT useful for:**
- Finding engineers (it doesn't know who they are)
- Predicting market size (it hallucinates numbers)
- Replacing human judgment (it's a tool, not an oracle)

---

## The Real Process That Works

```
1. START with dirty intent
   "I want to come top in Google AI results"

2. PARSE into structured data
   real_intent = rank
   niche = spare parts
   market = norway

3. FIND practitioners (not builders)
   Search for people who TEST agent preferences
   Look for experiment posts with data

4. CREATE corpus of 8 highest-signal people
   Weight by: empirical data, GitHub activity, recency

5. RUN GitGoblin on them
   Follow their activity
   Find convergence

6. ANALYZE with AI
   What does this convergence mean?
   What should we build?

7. LOG everything
   Every run, every signal, every opportunity
```

---

## What We Learned About the Product

### GitGoblin should become:
- **A campaign engine** — not just a scanner
- **An intent parser** — dirty intent → structured mission
- **A practitioner finder** — not just builder finder
- **An experiment logger** — track what works

### GitGoblin should NOT become:
- A content generator
- A business plan creator
- A market research tool
- A competitor analyzer

**It's a rabbit hole machine. Point it at the right problem.**

---

## The Core Motivation Connection

**I want my product to be the thing that Google AI talks about.**

To do that, I need to:
1. **Understand what agents actually pick** (not what Google says they pick)
2. **Build what agents want** (structured data, compatibility, Q&A)
3. **Test what works** (run experiments, measure results)
4. **Iterate fast** (wrong-part returns = graph corrections)

**GitGoblin helps with #1 and #2.**
**The campaign system helps with #3.**
**The outcome flywheel helps with #4.**

---

## The Meta-Insight

**GitGoblin is not a product. It's a lens.**

It shows you:
- Who's building what
- When it ships
- What they learned
- What you should build

**The product is what you build with that information.**

---

*Meta-learning document: 2026-09-07*
