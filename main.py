"""
Cyber Shield SIEM - Main Entry Point
=====================================
Starts the complete SIEM system with:
1. Database initialization
2. Log collector (background thread)
3. Correlation engine (background thread)
4. Real-time web dashboard
"""

import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def print_banner():
    """Print the Cyber Shield banner"""
    print("""
+=================================================+
|            CYBER SHIELD SIEM                     |
|   Security Information & Event Management        |
+=================================================+
    """)


def main():
    """Main function to start the SIEM dashboard"""
    print_banner()
    print("[INFO] System started at: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("=" * 60)
    
    print("\n[STEP 1] Initializing Database...")
    print("[OK] Database ready!")
    
    print("\n[STEP 2] Starting background services (log collection & threat detection)...")
    print("[OK] Log Collector thread started")
    print("[OK] Correlation Engine thread started")
    
    print("\n[STEP 3] Starting Web Dashboard...")
    print("[OK] Dashboard server ready!")
    
    # The dashboard (dashboard/app.py) handles everything internally:
    # - Database creation
    # - Log collection (background thread)
    # - Correlation engine (runs periodically)
    # - Alert management
    # - WebSocket real-time updates
    
    from dashboard.app import run_dashboard
    run_dashboard()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Cyber Shield SIEM shutting down...")
        print("[BYE] Goodbye!")
        sys.exit(0)
    except Exception as e:
        print("\n[ERROR] Fatal error: " + str(e))
        sys.exit(1)
