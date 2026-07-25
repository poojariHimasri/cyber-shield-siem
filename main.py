"""
🛡️ Cyber Shield SIEM - Main Entry Point
=========================================
Starts all components:
1. Database initialization
2. Log collector (background thread)
3. Correlation engine (background thread)
4. Web dashboard (Flask + Socket.IO)
"""

import threading
import time
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models import Database
from app.collector import LogCollector
from app.correlation_engine import CorrelationEngine
from app.alert_manager import AlertManager
from config import SIMULATION_INTERVAL


def print_banner():
    """Print the Cyber Shield banner"""
    print("""
╔══════════════════════════════════════════════╗
║        🛡️  CYBER SHIELD SIEM  🛡️            ║
║   Security Information & Event Management    ║
╚══════════════════════════════════════════════╝
    """)


def run_collector(db):
    """Run the log collector in a separate thread"""
    collector = LogCollector(db)
    collector.run_continuous(interval=SIMULATION_INTERVAL)


def run_correlation(db, alert_manager):
    """Run the correlation engine in a separate thread"""
    engine = CorrelationEngine(db)
    cycle = 0
    
    print("🔍 Correlation Engine started - analyzing logs every 10 seconds")
    
    while True:
        cycle += 1
        try:
            alerts = engine.run_analysis()
            if alerts:
                alert_manager.process_alerts(alerts)
        except Exception as e:
            print(f"❌ Correlation error: {e}")
        
        time.sleep(10)


def main():
    """Main function to start all components"""
    print_banner()
    print(f"⏰ System started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Step 1: Initialize database
    print("\n📦 Step 1: Initializing Database...")
    db = Database()
    print("✅ Database ready!")
    
    # Step 2: Create log collector and correlation engine
    alert_manager = AlertManager(db)
    
    # Step 3: Start background threads
    print("\n🚀 Step 2: Starting background services...")
    
    # Thread 1: Log collector
    collector_thread = threading.Thread(
        target=run_collector, 
        args=(db,),
        daemon=True,
        name="LogCollector"
    )
    collector_thread.start()
    print("  ✅ Log Collector thread started")
    
    # Thread 2: Correlation engine
    correlation_thread = threading.Thread(
        target=run_correlation,
        args=(db, alert_manager),
        daemon=True,
        name="CorrelationEngine"
    )
    correlation_thread.start()
    print("  ✅ Correlation Engine thread started")
    
    # Step 4: Start web dashboard
    print("\n🌐 Step 3: Starting Web Dashboard...")
    from dashboard.app import run_dashboard
    print("  ✅ Dashboard server ready!")
    
    # Run dashboard (this blocks)
    run_dashboard()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Cyber Shield SIEM shutting down...")
        print("👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)
