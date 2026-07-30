"""
Cyber Shield SIEM - WSGI Entry Point for Gunicorn
==================================================
This module is used by Gunicorn to serve the application in production.
It also starts background threads (log collection & correlation engine).

Usage:
    gunicorn -k eventlet -w 1 wsgi:application --bind 0.0.0.0:$PORT
"""

import sys
import os
import threading
import time
from datetime import datetime

# Ensure project root is in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dashboard.app import app, socketio, db, collector, correlation_engine, alert_manager, background_log_collection

def start_background_threads():
    """Start background services in a separate thread"""
    print("[DEPLOY] Starting background services (log collection & threat detection)...")
    
    def bg_worker():
        """Wrapper to run background_log_collection"""
        background_log_collection()
    
    thread = threading.Thread(target=bg_worker, daemon=True)
    thread.start()
    print(f"[DEPLOY] Background thread started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return thread

# Initialize database on import
print("[DEPLOY] Initializing Database...")
db.create_tables()
print("[DEPLOY] Database ready!")

# Start background threads immediately when this module loads
print("[DEPLOY] Starting background services (log collection & threat detection)...")
background_thread = start_background_threads()
print("[DEPLOY] Log Collector thread started")
print("[DEPLOY] Correlation Engine thread started (runs every 2 cycles)")
print("[DEPLOY] Dashboard server ready!")

# Create the application object that Gunicorn will use
application = app

if __name__ == "__main__":
    # For local development - use Flask's built-in server
    socketio.run(app, host="0.0.0.0", port=5000, debug=False, allow_unsafe_werkzeug=True)

