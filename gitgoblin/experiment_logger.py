"""Experiment logger — tracks all runs and assesses validity."""

from __future__ import annotations

import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

from .api_tracker import tracker


class ExperimentLogger:
    """Log every run and assess signal quality."""
    
    def __init__(self, log_dir: str = "data/experiments"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def log_run(
        self,
        run_id: str,
        sector: str,
        mode: str,
        seeds: list[str],
        observations: int,
        signals: list[dict],
        opportunities: list[dict],
        duration_seconds: float,
        api_calls: dict,
    ) -> dict:
        """Log a complete experiment run."""
        
        # Assess signal quality
        assessment = self._assess_signals(signals, opportunities)
        
        # Create experiment record
        experiment = {
            "run_id": run_id,
            "sector": sector,
            "mode": mode,
            "seeds": seeds,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "duration_seconds": duration_seconds,
            "api_calls": api_calls,
            "observations": observations,
            "signals_count": len(signals),
            "opportunities_count": len(opportunities),
            "assessment": assessment,
            "signals": [
                {
                    "target_id": s.get("target_id", ""),
                    "alpha": s.get("technical_alpha", 0),
                    "experts": s.get("expert_count", 0),
                    "confidence": s.get("confidence", 0),
                }
                for s in signals[:20]  # Top 20
            ],
            "opportunities": [
                {
                    "title": o.get("title", ""),
                    "decision": o.get("decision", ""),
                    "score": o.get("scorecard", {}).get("total", 0),
                }
                for o in opportunities[:10]  # Top 10
            ],
        }
        
        # Save experiment log
        experiment_file = self.log_dir / f"{run_id}.json"
        with open(experiment_file, 'w') as f:
            json.dump(experiment, f, indent=2)
        
        # Record in API tracker
        tracker.record_run(
            run_id=run_id,
            sector=sector,
            observations=observations,
            signals=len(signals),
            api_calls=api_calls,
            duration_seconds=duration_seconds,
        )
        
        return experiment
    
    def _assess_signals(self, signals: list[dict], opportunities: list[dict]) -> dict:
        """Assess the quality of signals from a run."""
        if not signals:
            return {
                "quality": "NO_SIGNALS",
                "recommendation": "Try different seeds or lower threshold",
                "confidence": 0,
            }
        
        # Calculate metrics
        avg_alpha = sum(s.get("technical_alpha", 0) for s in signals) / len(signals)
        max_alpha = max(s.get("technical_alpha", 0) for s in signals)
        avg_experts = sum(s.get("expert_count", 0) for s in signals) / len(signals)
        
        # Count decisions
        build_count = sum(1 for o in opportunities if o.get("decision") == "BUILD")
        research_count = sum(1 for o in opportunities if o.get("decision") == "RESEARCH")
        
        # Assess quality
        if max_alpha > 0.7 and build_count > 0:
            quality = "HIGH"
            recommendation = "Strong signals found. Review BUILD opportunities."
        elif max_alpha > 0.5 or research_count > 2:
            quality = "MEDIUM"
            recommendation = "Promising signals. Continue investigation."
        elif avg_alpha > 0.3:
            quality = "LOW"
            recommendation = "Weak signals. Try different seeds."
        else:
            quality = "NOISE"
            recommendation = "Mostly noise. Reconsider approach."
        
        return {
            "quality": quality,
            "recommendation": recommendation,
            "avg_alpha": round(avg_alpha, 3),
            "max_alpha": round(max_alpha, 3),
            "avg_experts": round(avg_experts, 1),
            "build_count": build_count,
            "research_count": research_count,
            "confidence": min(1.0, max_alpha * avg_experts / 3),
        }
    
    def get_experiment_history(self, limit: int = 50) -> list[dict]:
        """Get experiment history sorted by timestamp."""
        experiments = []
        for f in self.log_dir.glob("*.json"):
            try:
                with open(f) as fh:
                    exp = json.load(fh)
                experiments.append(exp)
            except Exception:
                pass
        
        experiments.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        return experiments[:limit]
    
    def get_sector_stats(self, sector: str) -> dict:
        """Get aggregated stats for a sector."""
        experiments = self.get_experiment_history()
        sector_exps = [e for e in experiments if e.get("sector") == sector]
        
        if not sector_exps:
            return {"sector": sector, "runs": 0}
        
        total_observations = sum(e.get("observations", 0) for e in sector_exps)
        total_signals = sum(e.get("signals_count", 0) for e in sector_exps)
        avg_duration = sum(e.get("duration_seconds", 0) for e in sector_exps) / len(sector_exps)
        
        # Quality distribution
        qualities = Counter(e.get("assessment", {}).get("quality", "UNKNOWN") for e in sector_exps)
        
        return {
            "sector": sector,
            "runs": len(sector_exps),
            "total_observations": total_observations,
            "total_signals": total_signals,
            "avg_observations_per_run": round(total_observations / len(sector_exps)),
            "avg_signals_per_run": round(total_signals / len(sesector_exps)),
            "avg_duration_seconds": round(avg_duration, 1),
            "quality_distribution": dict(qualities),
            "last_run": sector_exps[0].get("timestamp") if sector_exps else None,
        }
    
    def compare_modes(self, sector: str) -> dict:
        """Compare different modes for a sector."""
        experiments = self.get_experiment_history()
        sector_exps = [e for e in experiments if e.get("sector") == sector]
        
        modes = {}
        for exp in sector_exps:
            mode = exp.get("mode", "unknown")
            if mode not in modes:
                modes[mode] = []
            modes[mode].append(exp)
        
        comparison = {}
        for mode, exps in modes.items():
            avg_observations = sum(e.get("observations", 0) for e in exps) / len(exps)
            avg_signals = sum(e.get("signals_count", 0) for e in exps) / len(exps)
            avg_duration = sum(e.get("duration_seconds", 0) for e in exps) / len(exps)
            
            comparison[mode] = {
                "runs": len(exps),
                "avg_observations": round(avg_observations),
                "avg_signals": round(avg_signals, 1),
                "avg_duration_seconds": round(avg_duration, 1),
                "signal_efficiency": round(avg_signals / max(avg_duration, 1), 3),
            }
        
        return comparison


# Global logger instance
experiment_logger = ExperimentLogger()
