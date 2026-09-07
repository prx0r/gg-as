"""Scan modes — different strategies for different use cases."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class ScanMode:
    """Configuration for a scan mode."""
    name: str
    description: str
    
    # API budget
    github_calls_limit: int
    openalex_enabled: bool
    arxiv_enabled: bool
    hn_enabled: bool
    rss_enabled: bool
    ecosystems_enabled: bool
    
    # Scan parameters
    expand_per_seed: int
    pages_per_seed: int
    min_signal_score: float
    research_enabled: bool
    
    # Rate limits (seconds between calls)
    github_rate_limit: float
    openalex_rate_limit: float
    
    # Expected runtime
    estimated_minutes: float


# Predefined modes
MODES = {
    "quick": ScanMode(
        name="quick",
        description="Fast sweep — GitHub only, minimal expansion",
        github_calls_limit=100,
        openalex_enabled=False,
        arxiv_enabled=False,
        hn_enabled=False,
        rss_enabled=False,
        ecosystems_enabled=False,
        expand_per_seed=1,
        pages_per_seed=1,
        min_signal_score=0.20,
        research_enabled=False,
        github_rate_limit=0.75,
        openalex_rate_limit=0.5,
        estimated_minutes=2,
    ),
    
    "standard": ScanMode(
        name="standard",
        description="Standard scan — GitHub + arXiv, moderate expansion",
        github_calls_limit=300,
        openalex_enabled=False,
        arxiv_enabled=True,
        hn_enabled=False,
        rss_enabled=False,
        ecosystems_enabled=False,
        expand_per_seed=2,
        pages_per_seed=2,
        min_signal_score=0.15,
        research_enabled=True,
        github_rate_limit=0.75,
        openalex_rate_limit=0.5,
        estimated_minutes=5,
    ),
    
    "thorough": ScanMode(
        name="thorough",
        description="Thorough scan — all sources, deep expansion",
        github_calls_limit=500,
        openalex_enabled=True,
        arxiv_enabled=True,
        hn_enabled=True,
        rss_enabled=True,
        ecosystems_enabled=True,
        expand_per_seed=3,
        pages_per_seed=2,
        min_signal_score=0.10,
        research_enabled=True,
        github_rate_limit=0.75,
        openalex_rate_limit=0.5,
        estimated_minutes=10,
    ),
    
    "deepdive": ScanMode(
        name="deepdive",
        description="Deep dive — maximum expansion, all sources",
        github_calls_limit=1000,
        openalex_enabled=True,
        arxiv_enabled=True,
        hn_enabled=True,
        rss_enabled=True,
        ecosystems_enabled=True,
        expand_per_seed=5,
        pages_per_seed=3,
        min_signal_score=0.05,
        research_enabled=True,
        github_rate_limit=0.5,
        openalex_rate_limit=0.3,
        estimated_minutes=20,
    ),
    
    "stealth": ScanMode(
        name="stealth",
        description="Stealth mode — minimal footprint, avoid detection",
        github_calls_limit=200,
        openalex_enabled=True,
        arxiv_enabled=True,
        hn_enabled=False,
        rss_enabled=False,
        ecosystems_enabled=False,
        expand_per_seed=2,
        pages_per_seed=1,
        min_signal_score=0.15,
        research_enabled=True,
        github_rate_limit=2.0,  # Slower
        openalex_rate_limit=1.0,
        estimated_minutes=15,
    ),
    
    "targeted": ScanMode(
        name="targeted",
        description="Targeted — single repo deep analysis",
        github_calls_limit=50,
        openalex_enabled=False,
        arxiv_enabled=False,
        hn_enabled=False,
        rss_enabled=False,
        ecosystems_enabled=False,
        expand_per_seed=0,
        pages_per_seed=3,
        min_signal_score=0.10,
        research_enabled=False,
        github_rate_limit=1.0,
        openalex_rate_limit=0.5,
        estimated_minutes=1,
    ),
}


def get_mode(name: str) -> ScanMode:
    """Get a scan mode by name."""
    if name not in MODES:
        raise ValueError(f"Unknown mode: {name}. Available: {list(MODES.keys())}")
    return MODES[name]


def list_modes() -> list[dict]:
    """List all available modes."""
    return [
        {
            "name": mode.name,
            "description": mode.description,
            "estimated_minutes": mode.estimated_minutes,
            "github_calls_limit": mode.github_calls_limit,
        }
        for mode in MODES.values()
    ]
