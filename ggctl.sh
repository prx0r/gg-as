#!/bin/bash
# GG-AS Process Manager
# Enforces strict RAM/CPU/PID limits, kills stale runs
# NEVER kills opencode

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Configuration
MAX_RAM_MB=512
MAX_CPU_PERCENT=50
PID_DIR="logs/pids"
LOG_DIR="logs"

# Ensure directories exist
mkdir -p "$PID_DIR" "$LOG_DIR"

# Load env if exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Get opencode PIDs (NEVER kill these)
get_opencode_pids() {
    pgrep -f "opencode" 2>/dev/null || true
}

# Kill stale processes (excluding opencode)
kill_stale() {
    local killed=0
    for pidfile in "$PID_DIR"/*.pid; do
        [ -f "$pidfile" ] || continue
        PID=$(cat "$pidfile")
        NAME=$(basename "$pidfile" .pid)
        
        # Skip if opencode
        if echo "$(get_opencode_pids)" | grep -q "^${PID}$"; then
            echo "SKIP: $NAME (PID: $PID) is opencode"
            continue
        fi
        
        # Check if still running
        if ! kill -0 "$PID" 2>/dev/null; then
            echo "STALE: $NAME (PID: $PID) - removing"
            rm -f "$pidfile"
            ((killed++))
            continue
        fi
        
        # Check RAM usage
        RAM_KB=$(ps -o rss= -p "$PID" 2>/dev/null || echo "0")
        RAM_MB=$((RAM_KB / 1024))
        
        if [ "$RAM_MB" -gt "$MAX_RAM_MB" ]; then
            echo "OVER LIMIT: $NAME (PID: $PID) - ${RAM_MB}MB > ${MAX_RAM_MB}MB - killing"
            kill -9 "$PID" 2>/dev/null || true
            rm -f "$pidfile"
            ((killed++))
            continue
        fi
        
        # Check CPU usage (instantaneous sample)
        CPU=$(ps -o %cpu= -p "$PID" 2>/dev/null || echo "0" | tr -d ' ')
        if [ "${CPU%.*}" -gt "$MAX_CPU_PERCENT" ] 2>/dev/null; then
            echo "HIGH CPU: $NAME (PID: $PID) - ${CPU}% > ${MAX_CPU_PERCENT}% - killing"
            kill -9 "$PID" 2>/dev/null || true
            rm -f "$pidfile"
            ((killed++))
            continue
        fi
        
        echo "RUNNING: $NAME (PID: $PID) - RAM: ${RAM_MB}MB, CPU: ${CPU}%"
    done
    echo "Cleaned up $killed stale processes"
}

# Kill all GG-AS processes (excluding opencode)
kill_all() {
    local killed=0
    for pidfile in "$PID_DIR"/*.pid; do
        [ -f "$pidfile" ] || continue
        PID=$(cat "$pidfile")
        NAME=$(basename "$pidfile" .pid)
        
        # Skip if opencode
        if echo "$(get_opencode_pids)" | grep -q "^${PID}$"; then
            echo "SKIP: $NAME (PID: $PID) is opencode"
            continue
        fi
        
        echo "KILLING: $NAME (PID: $PID)"
        kill -9 "$PID" 2>/dev/null || true
        rm -f "$pidfile"
        ((killed++))
    done
    
    # Also kill any orphaned python processes running gitgoblin
    pkill -9 -f "gitgoblin" 2>/dev/null || true
    
    echo "Killed $killed processes"
}

# Show status
status() {
    echo "=== GG-AS Process Status ==="
    echo ""
    
    # Check opencode
    OPENCODE_PIDS=$(get_opencode_pids)
    if [ -n "$OPENCODE_PIDS" ]; then
        echo "OPENCODE (protected):"
        for pid in $OPENCODE_PIDS; do
            echo "  PID: $pid"
        done
        echo ""
    fi
    
    # Check GG-AS processes
    echo "GG-AS Processes:"
    for pidfile in "$PID_DIR"/*.pid; do
        [ -f "$pidfile" ] || continue
        PID=$(cat "$pidfile")
        NAME=$(basename "$pidfile" .pid)
        
        if kill -0 "$PID" 2>/dev/null; then
            RAM_KB=$(ps -o rss= -p "$PID" 2>/dev/null || echo "0")
            RAM_MB=$((RAM_KB / 1024))
            CPU=$(ps -o %cpu= -p "$PID" 2>/dev/null | tr -d ' ')
            echo "  $NAME (PID: $PID) - RAM: ${RAM_MB}MB, CPU: ${CPU}%"
        else
            echo "  $NAME (PID: $PID) - DEAD"
        fi
    done
    
    # System resources
    echo ""
    echo "System Resources:"
    free -h | grep Mem
    uptime | awk -F'load average:' '{print "Load:", $2}'
}

# Watch mode - auto-kill if resources exceeded
watch() {
    echo "Starting resource watcher (checking every 30s)..."
    while true; do
        kill_stale
        sleep 30
    done
}

case "${1:-status}" in
    kill-stale)
        kill_stale
        ;;
    kill-all)
        kill_all
        ;;
    status)
        status
        ;;
    watch)
        watch
        ;;
    *)
        echo "Usage: $0 {kill-stale|kill-all|status|watch}"
        exit 1
        ;;
esac
