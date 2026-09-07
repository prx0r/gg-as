from __future__ import annotations

import argparse
import json
from pathlib import Path

import uvicorn

from .api import create_app
from .db import Store
from .integrations.cuntgoblin import opportunity_to_cuntgoblin, signal_to_market_observations
from .pipeline.scout import Scout
from .settings import AppSettings, SectorProfile


def _profile(config_root: Path, sector: str) -> SectorProfile:
    path = config_root / "sectors" / f"{sector}.yaml"
    if not path.exists():
        raise SystemExit(f"Unknown sector profile: {path}")
    return SectorProfile.load(path)


def main() -> None:
    parser = argparse.ArgumentParser(prog="gitgoblin", description="Frontier technical-attention intelligence")
    parser.add_argument("--config", default="configs/default.yaml")
    parser.add_argument("--config-root", default="configs")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Initialize the local store")

    p_seed = sub.add_parser("seed", help="Add a seed builder")
    p_seed.add_argument("sector")
    p_seed.add_argument("username")

    p_scan = sub.add_parser("scan", help="Run a live bounded scan")
    p_scan.add_argument("sector")
    p_scan.add_argument("--seed", action="append", default=[])
    p_scan.add_argument("--expand", type=int, default=1)
    p_scan.add_argument("--no-research", action="store_true")
    p_scan.add_argument("--mode", choices=["quick", "standard", "thorough", "deepdive", "stealth", "targeted"], 
                       default="standard",
                       help="Scan mode: quick(2min), standard(5min), thorough(10min), deepdive(20min), stealth(15min), targeted(1min)")
    
    p_modes = sub.add_parser("modes", help="List available scan modes")

    p_rank = sub.add_parser("rank", help="Show current signals")
    p_rank.add_argument("--sector")
    p_rank.add_argument("--limit", type=int, default=20)

    p_export = sub.add_parser("export", help="Export VentureLab-compatible JSON")
    p_export.add_argument("--sector")
    p_export.add_argument("--out", default="build/cuntgoblin-export.json")

    p_experiments = sub.add_parser("experiments", help="View experiment history")
    p_experiments.add_argument("--sector", default=None)
    p_experiments.add_argument("--limit", type=int, default=10)
    
    p_compare = sub.add_parser("compare", help="Compare scan modes")
    p_compare.add_argument("sector")
    
    p_serve = sub.add_parser("serve", help="Serve API and dashboard")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8787)

    args = parser.parse_args()
    settings = AppSettings.load(args.config if Path(args.config).exists() else None)
    store = Store(settings.database_path)
    root = Path(args.config_root)

    if args.cmd == "init":
        print(json.dumps({"database": str(store.path), "status": "initialized"}, indent=2))
    elif args.cmd == "seed":
        _profile(root, args.sector)
        store.add_seed(args.sector, args.username.lower())
        print(json.dumps({"sector": args.sector, "seeds": store.seeds(args.sector)}, indent=2))
    elif args.cmd == "scan":
        from .scan_modes import get_mode
        from .experiment_logger import experiment_logger
        import time
        
        mode = get_mode(args.mode)
        profile = _profile(root, args.sector)
        
        # Apply mode settings
        settings.rate_limits["github"] = mode.github_rate_limit
        settings.github.pages_per_seed = mode.pages_per_seed
        settings.scoring.min_signal_score = mode.min_signal_score
        expand = min(args.expand, mode.expand_per_seed)
        
        print(f"Mode: {mode.name} | Expand: {expand} | Research: {mode.research_enabled}")
        print(f"Estimated: {mode.estimated_minutes} minutes")
        print()
        
        start_time = time.time()
        run = Scout(store, settings, profile).run(
            args.seed or None, expand_per_seed=expand, research=mode.research_enabled and not args.no_research
        )
        duration = time.time() - start_time
        
        # Log experiment
        experiment = experiment_logger.log_run(
            run_id=run.run_id,
            sector=args.sector,
            mode=mode.name,
            seeds=args.seed or profile.seed_builders,
            observations=run.observations_added,
            signals=[],  # Will be populated from DB
            opportunities=[],
            duration_seconds=duration,
            api_calls={"github": run.observations_added},  # Rough estimate
        )
        
        print(run.model_dump_json(indent=2))
        print(f"\nDuration: {duration:.1f}s")
        print(f"Assessment: {experiment['assessment']['quality']}")
        print(f"Recommendation: {experiment['assessment']['recommendation']}")
    
    elif args.cmd == "modes":
        from .scan_modes import list_modes
        modes = list_modes()
        print(f"{'Mode':<12} {'Est. Time':<12} {'GitHub Calls':<15} {'Description'}")
        print("-" * 70)
        for m in modes:
            print(f"{m['name']:<12} {m['estimated_minutes']:<12} {m['github_calls_limit']:<15} {m['description']}")
    elif args.cmd == "rank":
        print(json.dumps([s.model_dump(mode="json") for s in store.signals(args.sector, args.limit)], indent=2))
    elif args.cmd == "export":
        payload = {
            "market_observations": [o for s in store.signals(args.sector, 1000) for o in signal_to_market_observations(s)],
            "opportunities": [opportunity_to_cuntgoblin(o) for o in store.opportunities(args.sector, 1000)],
        }
        out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        print(out)
    elif args.cmd == "experiments":
        from .experiment_logger import experiment_logger
        experiments = experiment_logger.get_experiment_history(args.limit)
        if args.sector:
            experiments = [e for e in experiments if e.get("sector") == args.sector]
        
        print(f"{'Run ID':<20} {'Sector':<25} {'Mode':<12} {'Signals':<10} {'Quality':<10}")
        print("-" * 80)
        for exp in experiments:
            assessment = exp.get("assessment", {})
            print(f"{exp.get('run_id', ''):<20} {exp.get('sector', ''):<25} {exp.get('mode', ''):<12} {exp.get('signals_count', 0):<10} {assessment.get('quality', ''):<10}")
    
    elif args.cmd == "compare":
        from .experiment_logger import experiment_logger
        comparison = experiment_logger.compare_modes(args.sector)
        
        print(f"Mode comparison for: {args.sector}")
        print()
        print(f"{'Mode':<12} {'Runs':<8} {'Avg Signals':<12} {'Avg Time':<12} {'Efficiency':<12}")
        print("-" * 60)
        for mode, stats in comparison.items():
            print(f"{mode:<12} {stats['runs']:<8} {stats['avg_signals']:<12} {stats['avg_duration_seconds']:<12}s {stats['signal_efficiency']:<12}")
    
    elif args.cmd == "serve":
        uvicorn.run(create_app(settings_path=args.config if Path(args.config).exists() else None, config_root=root), host=args.host, port=args.port)


if __name__ == "__main__":
    main()
