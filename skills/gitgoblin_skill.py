"""GitGoblin Skill for Hermes agents.

Usage in TASK.md:

SKILLS INSTALLED FOR THIS JOB:
- gitgoblin-scan

Then Hermes will:
1. Parse your intent
2. Find engineers
3. Run campaigns
4. Log everything
5. Report back
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone

# Add gg-as to path
GG_AS_PATH = Path("/root/gg-as")
sys.path.insert(0, str(GG_AS_PATH))

os.environ['GITHUB_TOKEN'] = os.environ.get('GITHUB_TOKEN', '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')


class GitGoblinSkill:
    """Hermes skill for frontier intelligence."""
    
    def __init__(self):
        from gitgoblin.settings import AppSettings
        from gitgoblin.db import Store
        from gitgoblin.cloudflare_ai import cloudflare_ai
        
        self.settings = AppSettings.load()
        self.store = Store(self.settings.database_path)
        self.ai = cloudflare_ai
    
    def parse_intent(self, dirty_intent: str) -> dict:
        """Parse dirty intent into structured data."""
        from gitgoblin.intent_engine import parse_intent
        return parse_intent(dirty_intent)
    
    def find_engineers(self, intent: dict) -> list[dict]:
        """Find engineers for this niche."""
        from gitgoblin.intent_engine import find_engineers_websearch
        return find_engineers_websearch(intent)
    
    def run_scan(self, seeds: list[str], mode: str = "quick") -> dict:
        """Run a scan with given seeds."""
        from gitgoblin.scan_modes import get_mode
        from gitgoblin.pipeline.scout import Scout
        from gitgoblin.settings import SectorProfile
        
        scan_mode = get_mode(mode)
        self.settings.rate_limits["github"] = scan_mode.github_rate_limit
        self.settings.github.pages_per_seed = scan_mode.pages_per_seed
        self.settings.scoring.min_signal_score = scan_mode.min_signal_score
        
        profile = SectorProfile(
            id="hermes-scan",
            description="Hermes-initiated scan",
            seed_builders=seeds,
            keywords=[],
            arxiv_queries=[],
            rss_feeds=[],
            ecosystems_repos=[],
            expertise_languages=["python"],
            primitive_rules={},
        )
        
        start = time.time()
        run = Scout(self.store, self.settings, profile).run(
            seeds, expand_per_seed=scan_mode.expand_per_seed, research=scan_mode.research_enabled
        )
        duration = time.time() - start
        
        return {
            "observations": run.observations_added,
            "signals": run.signals_added,
            "duration_seconds": round(duration, 1),
        }
    
    def get_signals(self, limit: int = 20) -> list[dict]:
        """Get current signals."""
        signals = self.store.signals(limit=limit)
        return [s.model_dump(mode="json") for s in signals]
    
    def analyze(self, signal_data: dict) -> str:
        """Analyze a signal with AI."""
        result = self.ai.analyze_signal(signal_data)
        return result.get("analysis", "No analysis")
    
    def run_mission(self, dirty_intent: str) -> dict:
        """Full mission: intent → engineers → scan → analysis."""
        print(f"\n{'='*60}")
        print(f"MISSION: {dirty_intent}")
        print(f"{'='*60}\n")
        
        # Step 1: Parse intent
        print("1. Parsing intent...")
        intent = self.parse_intent(dirty_intent)
        print(f"   Real intent: {intent['real_intent']}")
        print(f"   Niche: {intent['niche']}")
        print(f"   Market: {intent['market']}")
        
        # Step 2: Find engineers
        print("\n2. Finding engineers...")
        seeds = self.find_engineers(intent)
        for s in seeds:
            print(f"   @{s['handle']}: {s['reason']}")
        
        # Step 3: Run scan
        print("\n3. Running scan...")
        seed_handles = [s['handle'] for s in seeds]
        result = self.run_scan(seed_handles, mode="quick")
        print(f"   Observations: {result['observations']}")
        print(f"   Signals: {result['signals']}")
        
        # Step 4: Get and analyze signals
        print("\n4. Analyzing signals...")
        signals = self.get_signals(5)
        for s in signals[:3]:
            analysis = self.analyze(s)
            print(f"   {s.get('target_id', '')}: {analysis[:100]}...")
        
        return {
            "intent": intent,
            "seeds": seeds,
            "scan_result": result,
            "signals": signals,
        }


def run(task_description: str) -> str:
    """Main entry point for Hermes skill."""
    skill = GitGoblinSkill()
    result = skill.run_mission(task_description)
    return json.dumps(result, indent=2, default=str)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python gitgoblin_skill.py 'your mission'")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    result = run(task)
    print(result)
