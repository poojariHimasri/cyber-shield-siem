import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'cybershield.db')

# Log settings
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
SIMULATION_INTERVAL = 5  # seconds between log generation

# Detection rules (thresholds)
BRUTE_FORCE_THRESHOLD = 5      # Failed logins in window (seconds)
BRUTE_FORCE_WINDOW = 60         # Time window in seconds
PORT_SCAN_THRESHOLD = 10        # Unique ports accessed in window
PORT_SCAN_WINDOW = 30           # Time window in seconds

# Alert settings
ALERT_EMAIL_ENABLED = False
ALERT_EMAIL_SERVER = os.getenv('ALERT_EMAIL_SERVER', 'smtp.gmail.com')
ALERT_EMAIL_PORT = int(os.getenv('ALERT_EMAIL_PORT', 587))
ALERT_EMAIL_USER = os.getenv('ALERT_EMAIL_USER', '')
ALERT_EMAIL_PASS = os.getenv('ALERT_EMAIL_PASS', '')
ALERT_EMAIL_TO = os.getenv('ALERT_EMAIL_TO', '')

# Web server
SECRET_KEY = os.getenv('SECRET_KEY', 'cyber-shield-secret-key-change-in-production')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'  # MUST be False to prevent Flask reloader from killing background threads
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
