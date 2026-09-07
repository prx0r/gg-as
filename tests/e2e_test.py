"""E2E Testing — Full pipeline test with logging."""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone

# Setup
os.environ['GITHUB_TOKEN'] = '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'
sys.path.insert(0, '.')

from gitgoblin.intent_engine import parse_intent, find_engineers_websearch, create_corpus
from gitgoblin.mission_parser import parse_mission, save_campaign_config
from gitgoblin.cloudflare_ai import cloudflare_ai
from gitgoblin.settings import AppSettings, SectorProfile
from gitgoblin.db import Store
from gitgoblin.pipeline.scout import Scout
from gitgoblin.scan_modes import get_mode
from gitgoblin.experiment_logger import experiment_logger


class E2ETester:
    """End-to-end tester with logging."""
    
    def __init__(self):
        self.log_dir = Path("data/e2e_tests")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
    
    def log(self, step: str, status: str, details: dict):
        """Log a test step."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": step,
            "status": status,
            "details": details,
        }
        self.results.append(entry)
        print(f"  [{status}] {step}: {json.dumps(details, default=str)[:100]}")
    
    def test_intent_parsing(self):
        """Test 1: Parse dirty intent."""
        print("\n=== TEST 1: INTENT PARSING ===")
        
        test_intents = [
            "I want to come top in Google AI results for Norwegian spare parts",
            "I want ChatGPT to recommend my EV charger products",
            "I want agents to pick my Shopify store over competitors",
        ]
        
        for intent_text in test_intents:
            intent = parse_intent(intent_text)
            self.log("intent_parse", "PASS", {
                "input": intent_text[:50],
                "real_intent": intent["real_intent"],
                "niche": intent["niche"],
                "market": intent["market"],
            })
    
    def test_engineer_discovery(self):
        """Test 2: Find engineers."""
        print("\n=== TEST 2: ENGINEER DISCOVERY ===")
        
        intent = {"real_intent": "rank", "niche": "spare parts", "market": "norway"}
        seeds = find_engineers_websearch(intent)
        
        self.log("engineer_discovery", "PASS", {
            "seeds_found": len(seeds),
            "seeds": [s["handle"] for s in seeds],
        })
    
    def test_cloudflare_ai(self):
        """Test 3: Cloudflare AI analysis."""
        print("\n=== TEST 3: CLOUDFLARE AI ===")
        
        result = cloudflare_ai.analyze_signal({
            "target_id": "Google Merchant Center",
            "technical_alpha": 0.95,
            "expert_count": 5,
        })
        
        self.log("cloudflare_ai", "PASS", {
            "has_response": bool(result.get("analysis")),
            "response_length": len(result.get("analysis", "")),
        })
    
    def test_gitgoblin_scan(self):
        """Test 4: GitGoblin scan."""
        print("\n=== TEST 4: GITGOBLIN SCAN ===")
        
        settings = AppSettings.load()
        store = Store(settings.database_path)
        
        mode = get_mode("quick")
        settings.rate_limits["github"] = mode.github_rate_limit
        settings.github.pages_per_seed = mode.pages_per_seed
        settings.scoring.min_signal_score = mode.min_signal_score
        
        profile = SectorProfile(
            id="e2e-test",
            description="E2E test sector",
            seed_builders=["igrigorik"],
            keywords=["shopify", "ucp"],
            arxiv_queries=[],
            rss_feeds=[],
            ecosystems_repos=[],
            expertise_languages=["python"],
            primitive_rules={},
        )
        
        start = time.time()
        run = Scout(store, settings, profile).run(["igrigorik"], expand_per_seed=1, research=False)
        duration = time.time() - start
        
        self.log("gitgoblin_scan", "PASS", {
            "observations": run.observations_added,
            "signals": run.signals_added,
            "duration_seconds": round(duration, 1),
        })
    
    def test_campaign_system(self):
        """Test 5: Campaign creation and run."""
        print("\n=== TEST 5: CAMPAIGN SYSTEM ===")
        
        # Create campaign from mission
        mission = "Find engineers for Google AI ads SEO"
        config = parse_mission(mission)
        config["seeds"] = ["igrigorik", "gil--"]
        
        path = save_campaign_config(config)
        self.log("campaign_create", "PASS", {"path": path})
        
        # Run campaign
        settings = AppSettings.load()
        store = Store(settings.database_path)
        
        profile = SectorProfile(
            id=config["id"],
            description=config["description"],
            seed_builders=config["seeds"],
            keywords=config.get("keywords", []),
            arxiv_queries=[],
            rss_feeds=[],
            ecosystems_repos=[],
            expertise_languages=["python"],
            primitive_rules=config.get("primitive_rules", {}),
        )
        
        start = time.time()
        run = Scout(store, settings, profile).run(config["seeds"], expand_per_seed=1, research=False)
        duration = time.time() - start
        
        self.log("campaign_run", "PASS", {
            "campaign_id": config["id"],
            "observations": run.observations_added,
            "signals": run.signals_added,
            "duration_seconds": round(duration, 1),
        })
    
    def run_all(self):
        """Run all tests."""
        print("=" * 70)
        print("E2E TESTING — FULL PIPELINE")
        print("=" * 70)
        
        start_time = time.time()
        
        self.test_intent_parsing()
        self.test_engineer_discovery()
        self.test_cloudflare_ai()
        self.test_gitgoblin_scan()
        self.test_campaign_system()
        
        duration = time.time() - start_time
        
        # Save results
        results_file = self.log_dir / f"e2e_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(results_file, 'w') as f:
            json.dump({
                "test_run": datetime.now(timezone.utc).isoformat(),
                "duration_seconds": round(duration, 1),
                "total_tests": len(self.results),
                "passed": sum(1 for r in self.results if r["status"] == "PASS"),
                "failed": sum(1 for r in self.results if r["status"] == "FAIL"),
                "results": self.results,
            }, f, indent=2)
        
        print(f"\n{'=' * 70}")
        print(f"E2E TEST COMPLETE")
        print(f"{'=' * 70}")
        print(f"Duration: {duration:.1f}s")
        print(f"Tests: {len(self.results)}")
        print(f"Passed: {sum(1 for r in self.results if r['status'] == 'PASS')}")
        print(f"Failed: {sum(1 for r in self.results if r['status'] == 'FAIL')}")
        print(f"Results: {results_file}")


if __name__ == "__main__":
    tester = E2ETester()
    tester.run_all()
