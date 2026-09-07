#!/usr/bin/env python3
"""
ALGO_SURFACE_CHANGED Detector

Monitors GitGoblin observations for changes in:
- Ranking fields (title, brand, category weights)
- Filter semantics (hard vs soft)
- Constraint weights
- Search context (eligibility, provenance)
- Agent checkout capabilities
- Dispatch objective functions

Runs every 6 hours against the SQLite database.
Outputs alerts to /tmp/algo_surface_alerts.log
"""

import sqlite3
import json
import hashlib
import time
import os
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = "/root/gitgoblin/data/gitgoblin.db"
ALERT_LOG = "/tmp/algo_surface_alerts.log"
STATE_FILE = "/tmp/algo_surface_state.json"

# Keywords that indicate an algorithm surface change
ALGO_SURFACE_KEYWORDS = [
    # Ranking
    "ranking", "relevance", "score", "weight", "tie-break", "cutoff",
    "ranker", "scoring", "field_weight", "text_weight",
    # Filtering
    "hard_filter", "soft_filter", "eligibility", "exclusion", "constraint",
    "filter_semantics", "hard_gate", "soft_ranking",
    # Constraints
    "constraint_weight", "objective_function", "solver", "optimization",
    "hard", "medium", "soft", "penalty", "reward",
    # Search
    "query_rewriting", "catalog_vocabulary", "synonym", "reformulate",
    "search_context", "intent", "natural_language",
    # Checkout/Transaction
    "checkout", "authorization", "purchase", "payment", "credential",
    "idempotent", "approval", "transaction",
    # Dispatch
    "dispatch", "scheduling", "assignment", "routing", "field_service",
    "technician", "skill_fit", "travel_time", "conversion_rate",
    # Provenance/Attribution
    "provenance", "freshness", "attribution", "citation", "retrieval",
    "content_hash", "source_url",
    # Agent-specific
    "agent", "agentic", "mcp", "ucp", "acp", "webmcp",
    "machine_readable", "structured_data", "product_feed",
]


def get_observation_delta(conn, since: str) -> list:
    """Get observations since last check."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT observation_id, entity_type, entity_id, action, payload_json
        FROM observations
        WHERE observed_at > ?
        ORDER BY observed_at ASC
    """, (since,))
    return cursor.fetchall()


def extract_algo_signals(observation: dict) -> list:
    """Extract algorithm surface signals from an observation."""
    signals = []
    payload_str = json.dumps(observation).lower()

    for keyword in ALGO_SURFACE_KEYWORDS:
        if keyword in payload_str:
            signals.append(keyword)

    return list(set(signals))


def compute_observation_hash(observation: dict) -> str:
    """Hash an observation for change detection."""
    return hashlib.sha256(
        json.dumps(observation, sort_keys=True).encode()
    ).hexdigest()[:16]


def detect_changes(conn, state: dict) -> list:
    """Detect algorithm surface changes since last state."""
    last_check = state.get("last_check", "1970-01-01T00:00:00Z")
    observations = get_observation_delta(conn, last_check)

    alerts = []
    for obs_id, entity_type, entity_id, action, payload_str in observations:
        try:
            payload = json.loads(payload_str)
        except json.JSONDecodeError:
            continue

        algo_signals = extract_algo_signals(payload)
        if algo_signals:
            alerts.append({
                "observation_id": obs_id,
                "entity_type": entity_type,
                "entity_id": entity_id,
                "action": action,
                "algo_signals": algo_signals,
                "observed_at": payload.get("observed_at", "unknown"),
                "source": payload.get("source", "unknown"),
            })

    return alerts


def write_alert(alerts: list, log_path: str):
    """Write alerts to log file."""
    with open(log_path, "a") as f:
        for alert in alerts:
            timestamp = datetime.utcnow().isoformat()
            f.write(f"[{timestamp}] ALGO_SURFACE_CHANGED\n")
            f.write(f"  entity: {alert['entity_id']}\n")
            f.write(f"  action: {alert['action']}\n")
            f.write(f"  signals: {', '.join(alert['algo_signals'])}\n")
            f.write(f"  source: {alert['source']}\n")
            f.write(f"  observed: {alert['observed_at']}\n")
            f.write("---\n")


def load_state() -> dict:
    """Load detector state."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"last_check": "1970-01-01T00:00:00Z", "total_alerts": 0}


def save_state(state: dict):
    """Save detector state."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def run_detection():
    """Run one detection cycle."""
    if not os.path.exists(DB_PATH):
        print(f"Database not found: {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    state = load_state()

    alerts = detect_changes(conn, state)

    if alerts:
        write_alert(alerts, ALERT_LOG)
        state["total_alerts"] = state.get("total_alerts", 0) + len(alerts)
        print(f"[ALGO_SURFACE_CHANGED] {len(alerts)} alerts detected")
        for alert in alerts[:5]:  # Show first 5
            print(f"  {alert['entity_id']}: {', '.join(alert['algo_signals'][:3])}")
    else:
        print("[ALGO_SURFACE_CHANGED] No changes detected")

    state["last_check"] = datetime.utcnow().isoformat() + "Z"
    save_state(state)
    conn.close()


if __name__ == "__main__":
    run_detection()
