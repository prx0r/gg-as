"""Mission Engine — the real version.

Takes a dirty intent, finds the engineers, builds the corpus.
"""

from __future__ import annotations

import json
import re
import httpx
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


# The real intents people have (not the chatgpt version)
REAL_INTENTS = {
    "rank": "I want to rank #1 in AI search results",
    "sell": "I want to sell dropshipped products through agents",
    "shopify": "I want ChatGPT to recommend my Shopify store",
    "google": "I want to appear in Google AI Mode results",
    "seo": "I want to beat competitors in AI-powered search",
    "agent": "I want agents to pick my products over others",
    "feed": "I want my product feed to be the one agents use",
    "compatibility": "I want to own the compatibility graph for spare parts",
    "voice": "I want AI to answer my phone and book jobs",
    "dispatch": "I want AI to schedule my technicians",
}


def parse_intent(dirty_intent: str) -> dict:
    """Parse the real dirty intent into structured data."""
    intent_lower = dirty_intent.lower()
    
    # Detect what they REALLY want
    real_intent = detect_real_intent(intent_lower)
    
    # Extract the niche
    niche = detect_niche(intent_lower)
    
    # Extract the market
    market = detect_market(intent_lower)
    
    # Extract the competition
    competition = detect_competition(intent_lower)
    
    return {
        "dirty_intent": dirty_intent,
        "real_intent": real_intent,
        "niche": niche,
        "market": market,
        "competition": competition,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def detect_real_intent(text: str) -> str:
    """Detect what they REALLY want (not the chatgpt version)."""
    if any(w in text for w in ["rank", "#1", "top", "first"]):
        return "rank"
    if any(w in text for w in ["sell", "revenue", "money", "profit"]):
        return "sell"
    if any(w in text for w in ["shopify", "chatgpt", "agent"]):
        return "shopify"
    if any(w in text for w in ["google", "ai mode", "merchant center"]):
        return "google"
    if any(w in text for w in ["seo", "search", "listing"]):
        return "seo"
    if any(w in text for w in ["feed", "product data", "catalog"]):
        return "feed"
    if any(w in text for w in ["compatibility", "spare part", "replacement"]):
        return "compatibility"
    if any(w in text for w in ["voice", "phone", "call"]):
        return "voice"
    if any(w in text for w in ["dispatch", "schedule", "technician"]):
        return "dispatch"
    return "general"


def detect_niche(text: str) -> str:
    """Detect the specific niche."""
    niches = {
        "spare parts": ["spare", "replacement", "part", "filter", "pump"],
        "ev charger": ["ev", "charger", "electric vehicle", "zappi"],
        "heat pump": ["heat pump", "hvac", "boiler"],
        "cabin": ["cabin", "hytte", "cottage", "holiday home"],
        "marine": ["marine", "boat", "ship", "offshore"],
        "sauna": ["sauna", "steam", "helo", "harvia"],
    }
    
    for niche, keywords in niches.items():
        if any(kw in text for kw in keywords):
            return niche
    
    return "general"


def detect_market(text: str) -> str:
    """Detect the target market."""
    markets = {
        "finland": ["finland", "finnish", "suomi"],
        "norway": ["norway", "norwegian", "norsk"],
        "sweden": ["sweden", "swedish", "svenska"],
        "uk": ["uk", "united kingdom", "britain"],
        "us": ["us", "united states", "america"],
    }
    
    for market, keywords in markets.items():
        if any(kw in text for kw in keywords):
            return market
    
    return "global"


def detect_competition(text: str) -> str:
    """Detect the competitive landscape."""
    if any(w in text for w in ["nobody", "no competition", "empty"]):
        return "empty"
    if any(w in text for w in ["few sellers", "limited", "niche"]):
        return "limited"
    if any(w in text for w in ["crowded", "competitive", "amazon"]):
        return "crowded"
    return "unknown"


def find_engineers_websearch(intent: dict) -> list[dict]:
    """Web search to find the smartest engineers in this niche."""
    # This would call a web search API
    # For now, return seed suggestions based on intent
    seeds = []
    
    if intent["real_intent"] == "google":
        seeds.extend([
            {"handle": "AndrewLolk", "reason": "AI Max Shopping expert"},
            {"handle": "mikeryanretail", "reason": "Retail PPC operator"},
            {"handle": "rustybrick", "reason": "Google tests/features"},
            {"handle": "FeedArmy", "reason": "Identified 8 conversational attributes"},
        ])
    
    if intent["real_intent"] == "shopify":
        seeds.extend([
            {"handle": "igrigorik", "reason": "UCP architect"},
            {"handle": "gil--", "reason": "iMessage shopping agent"},
            {"handle": "yoavweiss", "reason": "Web standards"},
        ])
    
    if intent["niche"] == "spare parts":
        seeds.extend([
            {"handle": "ge0ffrey", "reason": "Timefold CTO (dispatch)"},
            {"handle": "alishazal", "reason": "Anthropic commerce agents"},
        ])
    
    return seeds[:8]  # Top 8


def create_corpus(intent: dict, seeds: list[dict]) -> dict:
    """Create a corpus of the top 8 highest signal bets."""
    return {
        "intent": intent,
        "seeds": seeds[:8],
        "mission": f"Find engineers building: {intent['real_intent']} for {intent['niche']} in {intent['market']}",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def run_mission(dirty_intent: str) -> dict:
    """Full mission pipeline: intent → seeds → corpus."""
    print(f"\n{'='*60}")
    print(f"MISSION: {dirty_intent}")
    print(f"{'='*60}\n")
    
    # Step 1: Parse intent
    print("1. Parsing intent...")
    intent = parse_intent(dirty_intent)
    print(f"   Real intent: {intent['real_intent']}")
    print(f"   Niche: {intent['niche']}")
    print(f"   Market: {intent['market']}")
    print()
    
    # Step 2: Find engineers
    print("2. Finding engineers...")
    seeds = find_engineers_websearch(intent)
    for seed in seeds:
        print(f"   @{seed['handle']}: {seed['reason']}")
    print()
    
    # Step 3: Create corpus
    print("3. Creating corpus...")
    corpus = create_corpus(intent, seeds)
    print(f"   Mission: {corpus['mission']}")
    print(f"   Seeds: {len(corpus['seeds'])}")
    print()
    
    return corpus


# CLI
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python intent_engine.py 'your real intent here'")
        print()
        print("Examples:")
        print("  python intent_engine.py 'I want to rank #1 in Google AI results for Norwegian spare parts'")
        print("  python intent_engine.py 'I want ChatGPT to recommend my EV charger products'")
        print("  python intent_engine.py 'I want agents to pick my Shopify store over competitors'")
        sys.exit(1)
    
    dirty_intent = " ".join(sys.argv[1:])
    corpus = run_mission(dirty_intent)
    
    print("\n" + "="*60)
    print("CORPUS")
    print("="*60)
    print(json.dumps(corpus, indent=2))
