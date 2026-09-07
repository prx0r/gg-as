# Rabbit Hole Log — Google AI Max / Merchant Center

**Date:** 2026-09-07
**Depth:** 2 hops from seed repos

---

## The Path

```
START: igrigorik (Shopify UCP architect)
    ↓
FOLLOW: who does igrigorik watch?
    ↓
STAR: what repos do they star?
    ↓
FIND: repos starred by 2+ seeds
    ↓
DISCOVER: gmc-mcp, advertising-hub
    ↓
GO DEEPER: what's inside those repos
```

---

## Key Findings

### 1. kiwoongeom/gmc-mcp (14 stars)

**"The first free, open-source, self-hosted MCP server for Google Merchant Center"**

- 126 tools over Merchant API v1
- Products, inventory, reports, promotions, returns
- Account config, audit log + rollback, dry-run
- Free alternative to paid SaaS (Adzviser, Catchr, Windsor.ai)
- Created: 2026-05-02
- Updated: 2026-08-27

**This is exactly what we need.** It's the MCP bridge to Merchant Center.

### 2. itallstartedwithaidea/advertising-hub (39 stars)

**"The open-source one-stop shop for advertising platform APIs, MCP servers, AI agents"**

- 14 platforms (Google Ads, Meta, Microsoft, Amazon, LinkedIn, Pinterest, Reddit, Spotify, TTD, Criteo)
- 25+ specialized agents
- Production tooling for digital marketers
- Built by practitioners who manage real ad spend

**This is the advertising layer on top of Merchant Center.**

### 3. lukesnowden/google-shopping-feed (68 stars)

**PHP library for Google Shopping feed generation**

- MIT license
- Composer package
- Simple feed generation

**This is the feed layer.**

---

## The Architecture Emerging

```
MCP LAYER (gmc-mcp)
    ↓
FEED LAYER (google-shopping-feed)
    ↓
AGENT LAYER (advertising-hub)
    ↓
YOUR STORE (Shopify + Merchant Center)
```

**The stack is: MCP → Feed → Agent → Store.**

---

## What We Should Build

**Not another feed tool.**

Build the **compatibility graph** that sits on top of this stack:

```
USER: "What replacement pump fits my Bosch SMS46MI08E?"
    ↓
COMPATIBILITY GRAPH (our data)
    ↓
gmc-mcp (queries Merchant Center)
    ↓
google-shopping-feed (generates feed)
    ↓
advertising-hub (manages ads)
    ↓
RESULT: Our product appears first
```

**We own the data layer. They provide the infrastructure.**

---

## Next Steps

1. Clone gmc-mcp, study its API
2. Build compatibility graph on top
3. Test with real Merchant Center feed
4. Measure AI impression share
5. Iterate

---

*Rabbit hole logged: 2026-09-07*
