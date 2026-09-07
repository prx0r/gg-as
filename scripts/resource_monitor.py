#!/usr/bin/env python3
"""
System Resource Monitor for GitGoblin

Monitors RAM and CPU usage, kills background GitGoblin processes if needed.
Never kills opencode processes (PIDs tracked in /tmp/opencode_*.pid).
"""

import os
import sys
import time
import signal
import subprocess
from datetime import datetime

# Resource thresholds
MAX_RAM_PERCENT = 85  # Kill GitGoblin if RAM usage > 85%
MAX_CPU_PERCENT = 90  # Kill GitGoblin if CPU usage > 90%
CHECK_INTERVAL = 60   # Check every 60 seconds

# Processes to NEVER kill
PROTECTED_PROCESSES = ["opencode"]

# PID files to track
GITGOBLIN_PID_FILE = "/tmp/gitgoblin_scan.pid"
MONITOR_PID_FILE = "/tmp/gitgoblin_monitor.pid"


def get_memory_usage() -> dict:
    """Get system memory usage."""
    result = subprocess.run(
        ["free", "-m"],
        capture_output=True,
        text=True
    )
    lines = result.stdout.strip().split("\n")
    parts = lines[1].split()

    total = int(parts[1])
    used = int(parts[2])
    available = int(parts[6])

    return {
        "total": total,
        "used": used,
        "available": available,
        "percent": (used / total) * 100
    }


def get_cpu_usage() -> float:
    """Get CPU usage percentage."""
    result = subprocess.run(
        ["top", "-bn1"],
        capture_output=True,
        text=True
    )
    for line in result.stdout.split("\n"):
        if "Cpu(s)" in line:
            # Extract idle percentage
            parts = line.split()
            for part in parts:
                if "id" in part:
                    idle = float(part.replace("id,", ""))
                    return 100 - idle
    return 0.0


def is_process_running(pid: int) -> bool:
    """Check if a process is running."""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def is_protected(pid: int) -> bool:
    """Check if a process is protected (opencode)."""
    try:
        with open(f"/proc/{pid}/cmdline", "r") as f:
            cmdline = f.read().lower()
            for protected in PROTECTED_PROCESSES:
                if protected in cmdline:
                    return True
    except (FileNotFoundError, PermissionError):
        pass
    return False


def kill_gitgoblinProcesses(pid_file: str, reason: str):
    """Kill GitGoblin processes tracked by PID file."""
    if not os.path.exists(pid_file):
        return

    with open(pid_file) as f:
        pids = [int(line.strip()) for line in f if line.strip()]

    for pid in pids:
        if is_process_running(pid) and not is_protected(pid):
            print(f"[MONITOR] Killing GitGoblin PID {pid} — {reason}")
            try:
                os.kill(pid, signal.SIGTERM)
                time.sleep(2)
                if is_process_running(pid):
                    os.kill(pid, signal.SIGKILL)
            except OSError:
                pass


def log_status(mem: dict, cpu: float):
    """Log current status."""
    timestamp = datetime.utcnow().isoformat()
    log_line = f"[{timestamp}] RAM: {mem['percent']:.1f}% ({mem['used']}/{mem['total']}MB) CPU: {cpu:.1f}%\n"

    with open("/tmp/gitgoblin_monitor.log", "a") as f:
        f.write(log_line)


def monitor_loop():
    """Main monitoring loop."""
    print("[MONITOR] Resource monitor started")
    print(f"[MONITOR] Thresholds: RAM > {MAX_RAM_PERCENT}%, CPU > {MAX_CPU_PERCENT}%")
    print(f"[MONITOR] Check interval: {CHECK_INTERVAL}s")
    print(f"[MONITOR] Protected: {PROTECTED_PROCESSES}")

    # Write our own PID
    with open(MONITOR_PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    while True:
        mem = get_memory_usage()
        cpu = get_cpu_usage()

        log_status(mem, cpu)

        # Check if GitGoblin scan is running
        scan_running = False
        if os.path.exists(GITGOBLIN_PID_FILE):
            with open(GITGOBLIN_PID_FILE) as f:
                for line in f:
                    pid = int(line.strip())
                    if is_process_running(pid):
                        scan_running = True

        # Kill GitGoblin if resources critical
        if mem["percent"] > MAX_RAM_PERCENT:
            print(f"[MONITOR] CRITICAL: RAM {mem['percent']:.1f}% > {MAX_RAM_PERCENT}%")
            kill_gitgoblinProcesses(GITGOBLIN_PID_FILE, f"RAM {mem['percent']:.1f}%")
        elif cpu > MAX_CPU_PERCENT:
            print(f"[MONITOR] CRITICAL: CPU {cpu:.1f}% > {MAX_CPU_PERCENT}%")
            kill_gitgoblinProcesses(GITGOBLIN_PID_FILE, f"CPU {cpu:.1f}%")
        else:
            if scan_running:
                print(f"[MONITOR] OK: RAM {mem['percent']:.1f}% CPU {cpu:.1f}%")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor_loop()
