"""API usage tracker — monitors GitHub/GraphQL consumption."""

from __future__ import annotations

import json
import httpx
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional


class APITracker:
    """Track API usage across all sources."""
    
    def __init__(self, tracker_file: str = "data/api_usage.json"):
        self.tracker_file = Path(tracker_file)
        self.tracker_file.parent.mkdir(parents=True, exist_ok=True)
        self.data = self._load()
    
    def _load(self) -> dict:
        if self.tracker_file.exists():
            with open(self.tracker_file) as f:
                return json.load(f)
        return {
            "github": {"core": 0, "search": 0, "graphql": 0},
            "openalex": 0,
            "arxiv": 0,
            "hackernews": 0,
            "total_cost_usd": 0.0,
            "runs": [],
        }
    
    def _save(self):
        with open(self.tracker_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def check_github_rate_limit(self, token: str) -> dict:
        """Query GitHub for current rate limit status."""
        try:
            resp = httpx.get(
                'https://api.github.com/rate_limit',
                headers={'Authorization': f'Bearer {token}'},
                timeout=10.0
            )
            data = resp.json()
            
            core = data['resources']['core']
            search = data['resources']['search']
            graphql = data['resources']['graphql']
            
            return {
                "core": {
                    "limit": core['limit'],
                    "remaining": core['remaining'],
                    "used": core['limit'] - core['remaining'],
                    "reset_at": core['reset'],
                },
                "search": {
                    "limit": search['limit'],
                    "remaining": search['remaining'],
                    "used": search['limit'] - search['remaining'],
                },
                "graphql": {
                    "limit": 5000,
                    "remaining": graphql['remaining'],
                    "used": graphql['used'],
                },
            }
        except Exception as e:
            return {"error": str(e)}
    
    def record_call(self, source: str, endpoint: str = "", points: int = 1):
        """Record an API call."""
        if source not in self.data:
            self.data[source] = {"calls": 0}
        
        self.data[source]["calls"] = self.data[source].get("calls", 0) + points
        self._save()
    
    def record_run(self, run_id: str, sector: str, observations: int, signals: int, 
                   api_calls: dict, duration_seconds: float):
        """Record a complete run for analysis."""
        run = {
            "run_id": run_id,
            "sector": sector,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "observations": observations,
            "signals": signals,
            "api_calls": api_calls,
            "duration_seconds": duration_seconds,
            "cost_estimate": self._estimate_cost(api_calls),
        }
        self.data["runs"].append(run)
        self._save()
        return run
    
    def _estimate_cost(self, api_calls: dict) -> float:
        """Estimate cost based on API calls."""
        # GitHub: free with token
        # OpenAlex: free
        # arXiv: free
        # Total: $0
        return 0.0
    
    def get_usage_summary(self) -> dict:
        """Get summary of API usage."""
        total_runs = len(self.data.get("runs", []))
        
        # Aggregate stats
        total_observations = sum(r.get("observations", 0) for r in self.data.get("runs", []))
        total_signals = sum(r.get("signals", 0) for r in self.data.get("runs", []))
        total_duration = sum(r.get("duration_seconds", 0) for r in self.data.get("runs", []))
        
        return {
            "total_runs": total_runs,
            "total_observations": total_observations,
            "total_signals": total_signals,
            "total_duration_minutes": round(total_duration / 60, 1),
            "avg_observations_per_run": round(total_observations / max(total_runs, 1)),
            "avg_signals_per_run": round(total_signals / max(total_runs, 1)),
        }
    
    def get_run_history(self, limit: int = 20) -> list[dict]:
        """Get recent run history."""
        return self.data.get("runs", [])[-limit:]


# Global tracker instance
tracker = APITracker()
