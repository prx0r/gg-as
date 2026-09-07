#!/bin/bash
# GG-AS background runner
# Usage: ./run.sh [command] [args...]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Load env if exists
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Default to serve if no command
CMD="${1:-serve}"
shift 2>/dev/null || true

case "$CMD" in
    scan)
        # Run scan in foreground (for testing)
        python3 -m gitgoblin.cli scan "$@"
        ;;
    serve)
        # Run API server in background
        echo "Starting GG-AS server..."
        nohup setsid python3 -m uvicorn gitgoblin.api:create_app \
            --host 0.0.0.0 \
            --port 8787 \
            --log-level info \
            > logs/server.log 2>&1 &
        echo $! > logs/server.pid
        echo "Server PID: $(cat logs/server.pid)"
        echo "Logs: logs/server.log"
        echo "API: http://localhost:8787"
        echo "Docs: http://localhost:8787/docs"
        ;;
    watch)
        # Run scheduler in background (continuous scanning)
        SECTOR="${1:-shopify-agent-commerce}"
        INTERVAL="${2:-21600}"  # Default 6 hours
        echo "Starting GG-AS watcher for sector: $SECTOR (interval: ${INTERVAL}s)"
        nohup setsid python3 -m gitgoblin.scheduler \
            --sector "$SECTOR" \
            --interval "$INTERVAL" \
            > logs/watcher.log 2>&1 &
        echo $! > logs/watcher.pid
        echo "Watcher PID: $(cat logs/watcher.pid)"
        echo "Logs: logs/watcher.log"
        ;;
    stop)
        # Stop all background processes
        for pidfile in logs/*.pid; do
            if [ -f "$pidfile" ]; then
                PID=$(cat "$pidfile")
                if kill -0 "$PID" 2>/dev/null; then
                    kill "$PID"
                    echo "Stopped $(basename $pidfile .pid) (PID: $PID)"
                fi
                rm -f "$pidfile"
            fi
        done
        ;;
    status)
        # Check all background processes
        for pidfile in logs/*.pid; do
            if [ -f "$pidfile" ]; then
                PID=$(cat "$pidfile")
                NAME=$(basename "$pidfile" .pid)
                if kill -0 "$PID" 2>/dev/null; then
                    echo "$NAME running (PID: $PID)"
                else
                    echo "$NAME not running (stale PID)"
                fi
            fi
        done
        # Check API if running
        if curl -s http://localhost:8787/health > /dev/null 2>&1; then
            echo "API accessible at http://localhost:8787"
        fi
        ;;
    logs)
        # Tail logs
        LOG="${1:-server}"
        tail -f "logs/${LOG}.log"
        ;;
    *)
        echo "Usage: $0 {scan|serve|watch|stop|status|logs} [args...]"
        echo ""
        echo "Commands:"
        echo "  scan [sector]     - Run scan in foreground"
        echo "  serve             - Start API server in background"
        echo "  watch [sector]    - Start watcher in background (default: shopify-agent-commerce)"
        echo "  stop              - Stop all background processes"
        echo "  status            - Check status of all processes"
        echo "  logs [server|watcher] - Tail logs"
        exit 1
        ;;
esac
