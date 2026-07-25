"""
Cyber Shield SIEM - Launcher Script
====================================
Run this script to start the complete SIEM system.

Usage:
    python run.py
"""

import os
import sys

# Ensure we're in the project root
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("""
+=================================================+
|            CYBER SHIELD SIEM                     |
|   Security Information & Event Management        |
|              Launching...                        |
+=================================================+
    """)
    
    # Import and run main
    from main import main
    main()
