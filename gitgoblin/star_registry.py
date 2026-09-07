"""Star Registry — tracks repos starred by multiple developers."""

from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict


class StarRegistry:
    """Track repos starred by multiple developers over time."""
    
    def __init__(self, registry_file: str = "data/star_registry.json"):
        self.registry_file = Path(registry_file)
        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()
    
    def _load(self) -> dict:
        if self.registry_file.exists():
            with open(self.registry_file) as f:
                return json.load(f)
        return {
            "repos": {},      # repo -> {stars, starrers, first_seen, last_seen}
            "developers": {},  # developer -> [repos they starred]
            "convergences": [],  # repos starred by 2+ devs
            "last_updated": None,
        }
    
    def _save(self):
        self.data["last_updated"] = datetime.now(timezone.utc).isoformat()
        with open(self.registry_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_star(self, developer: str, repo: str, repo_info: dict = None):
        """Record that a developer starred a repo."""
        # Add to repos
        if repo not in self.data["repos"]:
            self.data["repos"][repo] = {
                "starrers": [],
                "first_seen": datetime.now(timezone.utc).isoformat(),
                "last_seen": datetime.now(timezone.utc).isoformat(),
                "info": repo_info or {},
            }
        
        if developer not in self.data["repos"][repo]["starrers"]:
            self.data["repos"][repo]["starrers"].append(developer)
        
        self.data["repos"][repo]["last_seen"] = datetime.now(timezone.utc).isoformat()
        
        # Add to developers
        if developer not in self.data["developers"]:
            self.data["developers"][developer] = []
        
        if repo not in self.data["developers"][developer]:
            self.data["developers"][developer].append(repo)
    
    def find_convergences(self, min_starrers: int = 2) -> list[dict]:
        """Find repos starred by multiple developers."""
        convergences = []
        
        for repo, info in self.data["repos"].items():
            if len(info["starrers"]) >= min_starrers:
                convergences.append({
                    "repo": repo,
                    "starrers": info["starrers"],
                    "starrer_count": len(info["starrers"]),
                    "first_seen": info["first_seen"],
                    "info": info.get("info", {}),
                })
        
        return sorted(convergences, key=lambda x: x["starrer_count"], reverse=True)
    
    def find_developers_who_starred(self, repo: str) -> list[str]:
        """Find all developers who starred a specific repo."""
        return self.data["repos"].get(repo, {}).get("starrers", [])
    
    def find_repos_by_developer(self, developer: str) -> list[str]:
        """Find all repos a developer has starred."""
        return self.data["developers"].get(developer, [])
    
    def get_stats(self) -> dict:
        """Get registry statistics."""
        return {
            "total_repos": len(self.data["repos"]),
            "total_developers": len(self.data["developers"]),
            "convergences": len([r for r in self.data["repos"].values() if len(r["starrers"]) >= 2]),
            "last_updated": self.data.get("last_updated"),
        }
    
    def export_convergences(self) -> str:
        """Export convergences as markdown."""
        convergences = self.find_convergences()
        
        lines = ["# Star Registry — Convergences\n"]
        lines.append(f"Updated: {self.data.get('last_updated', 'never')}\n")
        lines.append(f"Total repos tracked: {len(self.data['repos'])}")
        lines.append(f"Total developers tracked: {len(self.data['developers'])}")
        lines.append(f"Convergences (2+ starrers): {len(convergences)}\n")
        
        lines.append("## Top Convergences\n")
        for c in convergences[:20]:
            lines.append(f"### {c['repo']}")
            lines.append(f"Starred by: {', '.join(c['starrers'])}")
            if c.get('info', {}).get('description'):
                lines.append(f"Description: {c['info']['description'][:100]}")
            lines.append("")
        
        return "\n".join(lines)


# Global instance
star_registry = StarRegistry()
