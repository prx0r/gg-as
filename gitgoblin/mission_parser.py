"""Mission parser — converts natural language into structured campaign configs."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional
from datetime import datetime, timezone


def parse_mission(mission: str) -> dict:
    """Parse a natural language mission into structured campaign config.
    
    Example:
        "Find all engineers working on Google AI ads and find out how to make our SEO number 1"
    
    Returns:
        Campaign config dict ready to save
    """
    mission_lower = mission.lower()
    
    # Extract domain focus
    domain = extract_domain(mission_lower)
    
    # Extract keywords
    keywords = extract_keywords(mission_lower)
    
    # Extract target accounts (if mentioned)
    targets = extract_targets(mission_lower)
    
    # Generate campaign ID
    campaign_id = generate_campaign_id(domain, mission)
    
    # Generate description
    description = f"Mission: {mission}"
    
    # Generate primitive rules based on domain
    primitive_rules = generate_primitive_rules(domain)
    
    return {
        "id": campaign_id,
        "description": description,
        "mission": mission,
        "seeds": targets,
        "keywords": keywords,
        "domain": domain,
        "expansion": {
            "max_depth": 3,
            "expand_per_seed": 2,
            "follow_replies": True,
            "follow_quotes": True,
        },
        "thresholds": {
            "signal_score": 0.15,
            "opportunity_score": 0.3,
            "build_threshold": 0.7,
        },
        "primitive_rules": primitive_rules,
        "status": "ACTIVE",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_run": None,
        "total_observations": 0,
        "total_signals": 0,
        "total_opportunities": 0,
    }


def extract_domain(mission_lower: str) -> str:
    """Extract the primary domain from mission text."""
    domain_keywords = {
        "google ads": "google_ads",
        "google merchant": "google_merchant",
        "shopify": "shopify",
        "ai max": "ai_max",
        "shopping": "shopping",
        "voice": "voice",
        "dispatch": "dispatch",
        "compatibility": "compatibility",
        "spare parts": "spare_parts",
        "agent commerce": "agent_commerce",
        "ucp": "ucp",
        "mcp": "mcp",
        "seo": "seo",
        "feed": "feed",
        "merchant center": "merchant_center",
    }
    
    for keyword, domain in domain_keywords.items():
        if keyword in mission_lower:
            return domain
    
    return "general"


def extract_keywords(mission_lower: str) -> list[str]:
    """Extract relevant keywords from mission text."""
    # Common tech/commerce keywords
    keyword_patterns = [
        r'\b(seo|search|ranking|algorithm)\b',
        r'\b(google|merchant|shopping|ads)\b',
        r'\b(shopify|catalog|feed)\b',
        r'\b(agent|ai|llm|chatgpt|gemini)\b',
        r'\b(commerce|ecommerce|ecom)\b',
        r'\b(feed|attribute|schema)\b',
        r'\b(engineer|developer|builder)\b',
        r'\b(ranking|score|weight|filter)\b',
    ]
    
    keywords = []
    for pattern in keyword_patterns:
        matches = re.findall(pattern, mission_lower)
        keywords.extend(matches)
    
    # Add domain-specific keywords
    if "google" in mission_lower:
        keywords.extend(["google", "merchant center", "shopping"])
    if "shopify" in mission_lower:
        keywords.extend(["shopify", "catalog", "ucp"])
    if "agent" in mission_lower:
        keywords.extend(["agent", "agentic", "ai"])
    
    return list(set(keywords))


def extract_targets(mission: str) -> list[str]:
    """Extract target accounts mentioned in mission."""
    # Common patterns: @username, "username", username
    targets = []
    
    # Find @mentions
    mentions = re.findall(r'@(\w+)', mission)
    targets.extend(mentions)
    
    # Find quoted usernames
    quoted = re.findall(r'"(\w+)"', mission)
    targets.extend(quoted)
    
    return list(set(targets))


def generate_campaign_id(domain: str, mission: str) -> str:
    """Generate a campaign ID from domain and mission."""
    # Clean mission for ID
    clean = re.sub(r'[^a-z0-9]', '-', mission.lower())
    clean = re.sub(r'-+', '-', clean)
    clean = clean[:50].strip('-')
    
    return f"{domain}-{clean}"


def generate_primitive_rules(domain: str) -> dict:
    """Generate primitive rules based on domain."""
    rules = {
        "google_ads": {
            "ranking": ["rank", "score", "weight", "relevance", "quality"],
            "feeds": ["feed", "attribute", "product_detail", "related_product"],
            "ai_max": ["ai max", "text customization", "final url expansion"],
            "shopping": ["shopping", "product", "merchant", "catalog"],
        },
        "google_merchant": {
            "feeds": ["feed", "attribute", "product_detail", "related_product"],
            "conversational": ["question_and_answer", "document_link", "popularity_rank"],
            "ai_mode": ["ai mode", "ai overview", "conversational"],
        },
        "shopify": {
            "catalog": ["catalog", "product", "feed"],
            "ucp": ["ucp", "checkout", "cart", "agent"],
            "agentic": ["agentic", "agent", "mcp"],
        },
        "agent_commerce": {
            "ranking": ["rank", "score", "recommend", "filter"],
            "checkout": ["checkout", "cart", "payment", "transaction"],
            "identity": ["identity", "credential", "provenance"],
        },
        "compatibility": {
            "graph": ["compatible", "fit", "part", "model", "supersession"],
            "identification": ["photo", "image", "vision", "identify"],
            "spare_parts": ["spare", "replacement", "filter", "oem"],
        },
        "voice": {
            "telephony": ["voice", "call", "phone", "sip"],
            "booking": ["booking", "appointment", "schedule"],
            "dispatch": ["dispatch", "route", "assign", "optimize"],
        },
        "seo": {
            "ranking": ["rank", "score", "algorithm"],
            "content": ["content", "page", "schema", "json-ld"],
            "discovery": ["search", "crawl", "index"],
        },
    }
    
    # Find matching domain
    for domain_key, rules_dict in rules.items():
        if domain_key in domain:
            return rules_dict
    
    # Default rules
    return {
        "general": ["search", "rank", "score", "agent", "commerce"]
    }


def save_campaign_config(config: dict, campaigns_dir: str = "campaigns") -> str:
    """Save campaign config to file."""
    import yaml
    
    campaigns_path = Path(campaigns_dir)
    campaign_dir = campaigns_path / config["id"]
    campaign_dir.mkdir(parents=True, exist_ok=True)
    
    config_path = campaign_dir / "config.yaml"
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    return str(config_path)


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python mission_parser.py 'your mission here'")
        sys.exit(1)
    
    mission = " ".join(sys.argv[1:])
    config = parse_mission(mission)
    
    print(json.dumps(config, indent=2))
