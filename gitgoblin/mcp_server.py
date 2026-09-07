"""GitGoblin MCP server — exposes frontier intelligence as agent tools.

Requires mcp[cli] or mcp<2 for FastMCP high-level API.
Falls back gracefully if MCP version is incompatible.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .db import Store
from .settings import AppSettings, SectorProfile
from .pipeline.scout import Scout
from .integrations.cuntgoblin import opportunity_to_cuntgoblin, signal_to_market_observations


def build_server(
    settings_path: str | None = None,
    db_path: str | None = None,
    config_root: str | Path = "configs",
):
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        raise ImportError(
            "MCP high-level API not available. Install with: pip install 'mcp[cli]>=1,<2'"
        )

    settings = AppSettings.load(settings_path)
    if db_path:
        settings.database_path = db_path
    store = Store(settings.database_path)
    config_root = Path(config_root)
    mcp = FastMCP("gitgoblin")

    def _load_profile(sector: str) -> SectorProfile:
        path = config_root / "sectors" / f"{sector}.yaml"
        if not path.exists():
            raise ValueError(f"Unknown sector: {sector}")
        return SectorProfile.load(path)

    @mcp.tool()
    def list_sectors() -> str:
        """List available intelligence sectors."""
        sectors = []
        sectors_dir = config_root / "sectors"
        if sectors_dir.exists():
            for f in sorted(sectors_dir.glob("*.yaml")):
                profile = SectorProfile.load(f)
                sectors.append({"id": profile.id, "description": profile.description, "seeds": len(profile.seed_builders)})
        return json.dumps(sectors)

    @mcp.tool()
    def scan_sector(sector: str, seeds: list[str] | None = None, expand_per_seed: int = 2, research: bool = True) -> str:
        """Run a frontier scan on a sector. Collects from GitHub, arXiv, OpenAlex, HN, RSS, ecosyste.ms."""
        profile = _load_profile(sector)
        run = Scout(store, settings, profile).run(seeds, expand_per_seed=expand_per_seed, research=research)
        return json.dumps(run.model_dump(mode="json"), default=str)

    @mcp.tool()
    def get_signals(sector: str | None = None, limit: int = 50) -> str:
        """Get frontier signals — convergence detections with technical alpha scores."""
        signals = store.signals(sector, limit)
        return json.dumps([s.model_dump(mode="json") for s in signals], default=str)

    @mcp.tool()
    def get_opportunities(sector: str | None = None, limit: int = 20) -> str:
        """Get derived product opportunities with BUILD/RESEARCH/WATCH/REJECT decisions."""
        opps = store.opportunities(sector, limit)
        return json.dumps([o.model_dump(mode="json") for o in opps], default=str)

    @mcp.tool()
    def search_entities(query: str, entity_type: str | None = None, sector: str | None = None, limit: int = 20) -> str:
        """Search entities (repos, papers, developers, discussions) by name or ID."""
        results = []
        seen = set()
        for e in store.observations(sector=sector):
            if query.lower() in e.entity_id.lower() or query.lower() in str(e.value).lower():
                if entity_type and e.entity_type != entity_type:
                    continue
                if e.entity_id in seen:
                    continue
                seen.add(e.entity_id)
                entity = store.get_entity(e.entity_id)
                if entity:
                    results.append(entity.model_dump(mode="json"))
            if len(results) >= limit:
                break
        return json.dumps(results, default=str)

    @mcp.tool()
    def get_entity(entity_id: str) -> str:
        """Get a single entity by ID with all its attributes."""
        entity = store.get_entity(entity_id)
        if not entity:
            return json.dumps({"error": "Entity not found"})
        return json.dumps(entity.model_dump(mode="json"), default=str)

    @mcp.tool()
    def export_cuntgoblin(sector: str | None = None) -> str:
        """Export VentureLab-compatible market observations and opportunities."""
        signals_out = [obs for s in store.signals(sector, 1000) for obs in signal_to_market_observations(s)]
        opps_out = [opportunity_to_cuntgoblin(o) for o in store.opportunities(sector, 1000)]
        return json.dumps({"market_observations": signals_out, "opportunities": opps_out}, default=str)

    @mcp.tool()
    def add_seed(sector: str, username: str) -> str:
        """Add a seed builder to a sector for monitoring."""
        _load_profile(sector)
        store.add_seed(sector, username.lower())
        return json.dumps({"sector": sector, "seeds": store.seeds(sector)})

    @mcp.tool()
    def list_seeds(sector: str) -> str:
        """List configured and persisted seeds for a sector."""
        profile = _load_profile(sector)
        return json.dumps({"sector": sector, "configured": profile.seed_builders, "persisted": store.seeds(sector)})

    @mcp.tool()
    def get_sector_stats(sector: str | None = None) -> str:
        """Get statistics: observation count, signal count, opportunity count, entity count."""
        signals = store.signals(sector, 10000)
        opps = store.opportunities(sector, 10000)
        return json.dumps({
            "sector": sector or "all",
            "signal_count": len(signals),
            "opportunity_count": len(opps),
            "avg_technical_alpha": sum(s.technical_alpha for s in signals) / max(1, len(signals)),
            "build_count": sum(1 for o in opps if o.decision == "BUILD"),
            "research_count": sum(1 for o in opps if o.decision == "RESEARCH"),
            "watch_count": sum(1 for o in opps if o.decision == "WATCH"),
        })

    @mcp.tool()
    def run_campaign(campaign_id: str, fresh_seeds: list[str] | None = None) -> str:
        """Run a focused rabbit-hole campaign. Resumes from where it left off."""
        import yaml
        from datetime import datetime
        
        campaign_path = config_root.parent / "campaigns" / campaign_id / "config.yaml"
        if not campaign_path.exists():
            return json.dumps({"error": f"Campaign not found: {campaign_id}"})
        
        with open(campaign_path) as f:
            campaign = yaml.safe_load(f)
        
        # Add fresh seeds if provided
        if fresh_seeds:
            for seed in fresh_seeds:
                if seed not in campaign['seeds']:
                    campaign['seeds'].append(seed)
        
        # Create profile for this campaign
        profile = SectorProfile(
            id=campaign['id'],
            description=campaign['description'],
            seed_builders=campaign['seeds'],
            keywords=campaign.get('keywords', []),
            arxiv_queries=[],
            rss_feeds=[],
            ecosystems_repos=[],
            expertise_languages=['python', 'typescript', 'rust'],
            primitive_rules=campaign.get('primitive_rules', {}),
        )
        
        # Run scan
        result = Scout(store, settings, profile).run(
            campaign['seeds'],
            expand_per_seed=campaign.get('expansion', {}).get('expand_per_seed', 2),
            research=False
        )
        
        # Update campaign config
        campaign['last_run'] = datetime.now(timezone.utc).isoformat()
        campaign['total_observations'] = campaign.get('total_observations', 0) + result.observations_added
        campaign['total_signals'] = campaign.get('total_signals', 0) + result.signals_added
        campaign['total_opportunities'] = campaign.get('total_opportunities', 0) + result.opportunities_added
        
        with open(campaign_path, 'w') as f:
            yaml.dump(campaign, f, default_flow_style=False)
        
        return json.dumps({
            "campaign": campaign_id,
            "observations_added": result.observations_added,
            "signals_added": result.signals_added,
            "opportunities_added": result.opportunities_added,
            "total_observations": campaign['total_observations'],
            "total_signals": campaign['total_signals'],
        }, default=str)

    @mcp.tool()
    def list_campaigns() -> str:
        """List all active campaigns."""
        import yaml
        campaigns_dir = config_root.parent / "campaigns"
        if not campaigns_dir.exists():
            return json.dumps({"campaigns": []})
        
        campaigns = []
        for d in campaigns_dir.iterdir():
            config_path = d / "config.yaml"
            if config_path.exists():
                with open(config_path) as f:
                    campaign = yaml.safe_load(f)
                campaigns.append({
                    "id": campaign.get('id'),
                    "description": campaign.get('description', '')[:80],
                    "seeds": len(campaign.get('seeds', [])),
                    "status": campaign.get('status', 'unknown'),
                    "total_observations": campaign.get('total_observations', 0),
                    "total_signals": campaign.get('total_signals', 0),
                })
        
        return json.dumps({"campaigns": campaigns})

    @mcp.tool()
    def get_campaign_log(campaign_id: str) -> str:
        """Get the run log for a campaign."""
        log_dir = config_root.parent / "campaigns" / campaign_id
        logs = sorted(log_dir.glob("run_*.json"))
        
        if not logs:
            return json.dumps({"error": "No run logs found"})
        
        # Get last 5 runs
        recent = []
        for log_file in logs[-5:]:
            with open(log_file) as f:
                recent.append(json.load(f))
        
        return json.dumps({"campaign": campaign_id, "recent_runs": recent})

    return mcp


def main():
    build_server().run()


if __name__ == "__main__":
    main()
