"""
Cyber Shield SIEM - Configuration Module
=========================================
Loads configuration from environment variables with sensible defaults.
For production, set environment variables via Render dashboard or .env file.
"""
import os
from dotenv import load_dotenv

# Load .env file if it exists (for local development)
load_dotenv()

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database
# In production (Render), the data dir is created automatically
DATABASE_PATH = os.getenv('DATABASE_PATH', os.path.join(BASE_DIR, 'data', 'cybershield.db'))

# Log settings
LOG_DIR = os.getenv('LOG_DIR', os.path.join(BASE_DIR, 'logs'))
SIMULATION_INTERVAL = int(os.getenv('SIMULATION_INTERVAL', 5))  # seconds between log generation

# Detection rules (thresholds)
BRUTE_FORCE_THRESHOLD = int(os.getenv('BRUTE_FORCE_THRESHOLD', 5))   # Failed logins in window
BRUTE_FORCE_WINDOW = int(os.getenv('BRUTE_FORCE_WINDOW', 60))        # Time window in seconds
PORT_SCAN_THRESHOLD = int(os.getenv('PORT_SCAN_THRESHOLD', 10))      # Unique ports accessed
PORT_SCAN_WINDOW = int(os.getenv('PORT_SCAN_WINDOW', 30))            # Time window in seconds

# Alert settings
ALERT_EMAIL_ENABLED = os.getenv('ALERT_EMAIL_ENABLED', 'False').lower() == 'true'
ALERT_EMAIL_SERVER = os.getenv('ALERT_EMAIL_SERVER', 'smtp.gmail.com')
ALERT_EMAIL_PORT = int(os.getenv('ALERT_EMAIL_PORT', 587))
ALERT_EMAIL_USER = os.getenv('ALERT_EMAIL_USER', '')
ALERT_EMAIL_PASS = os.getenv('ALERT_EMAIL_PASS', '')
ALERT_EMAIL_TO = os.getenv('ALERT_EMAIL_TO', '')

# Web server
SECRET_KEY = os.getenv('SECRET_KEY', 'cyber-shield-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'  # MUST be False in production to prevent Flask reloader from killing background threads
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))

# Ensure data directories exist on import
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
