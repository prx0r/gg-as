"""Cache layer for GitHub data — avoids re-fetching same repos."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path
from typing import Any, Optional
from datetime import datetime, timedelta, timezone


class GitHubCache:
    """Cache GitHub API responses to avoid duplicate calls."""
    
    def __init__(self, cache_dir: str = "data/cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
        self.stats = {"hits": 0, "misses": 0}
    
    def _key(self, url: str) -> str:
        """Generate cache key from URL."""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _path(self, key: str) -> Path:
        """Get cache file path."""
        return self.cache_dir / f"{key}.json"
    
    def get(self, url: str) -> Optional[dict]:
        """Get cached response if fresh."""
        key = self._key(url)
        path = self._path(key)
        
        if not path.exists():
            self.stats["misses"] += 1
            return None
        
        try:
            with open(path) as f:
                cached = json.load(f)
            
            # Check TTL
            cached_at = datetime.fromisoformat(cached["timestamp"])
            if datetime.now(timezone.utc) - cached_at > self.ttl:
                self.stats["misses"] += 1
                return None
            
            self.stats["hits"] += 1
            return cached["data"]
        except Exception:
            self.stats["misses"] += 1
            return None
    
    def set(self, url: str, data: Any):
        """Cache a response."""
        key = self._key(url)
        path = self._path(key)
        
        cached = {
            "url": url,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data,
        }
        
        with open(path, 'w') as f:
            json.dump(cached, f, default=str)
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        total = self.stats["hits"] + self.stats["misses"]
        hit_rate = self.stats["hits"] / total if total > 0 else 0
        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "hit_rate": f"{hit_rate:.1%}",
            "cache_files": len(list(self.cache_dir.glob("*.json"))),
        }


class DedupeTracker:
    """Track which repos we've already visited to avoid re-fetching."""
    
    def __init__(self, tracker_file: str = "data/crawl_graph.json"):
        self.tracker_file = Path(tracker_file)
        self.visited = self._load()
    
    def _load(self) -> dict:
        """Load visited repos."""
        if self.tracker_file.exists():
            with open(self.tracker_file) as f:
                return json.load(f)
        return {"repos": {}, "users": {}, "edges": []}
    
    def _save(self):
        """Save visited repos."""
        with open(self.tracker_file, 'w') as f:
            json.dump(self.visited, f, indent=2)
    
    def is_repo_visited(self, repo: str) -> bool:
        """Check if we've already fetched this repo."""
        return repo in self.visited["repos"]
    
    def mark_repo(self, repo: str, metadata: dict = None):
        """Mark a repo as visited."""
        self.visited["repos"][repo] = {
            "visited_at": datetime.now(timezone.utc).isoformat(),
            "metadata": metadata or {},
        }
        self._save()
    
    def is_user_visited(self, username: str) -> bool:
        """Check if we've already fetched this user."""
        return username in self.visited["users"]
    
    def mark_user(self, username: str):
        """Mark a user as visited."""
        self.visited["users"][username] = {
            "visited_at": datetime.now(timezone.utc).isoformat(),
        }
        self._save()
    
    def add_edge(self, source: str, target: str, edge_type: str):
        """Record a relationship edge."""
        edge = {
            "source": source,
            "target": target,
            "type": edge_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        if edge not in self.visited["edges"]:
            self.visited["edges"].append(edge)
            self._save()
    
    def get_stats(self) -> dict:
        """Get tracking statistics."""
        return {
            "repos_visited": len(self.visited["repos"]),
            "users_visited": len(self.visited["users"]),
            "edges_recorded": len(self.visited["edges"]),
        }
