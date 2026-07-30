"""
Web Dashboard - Flask server with real-time log and alert display
=================================================================
This module works with both:
1. Development: `python dashboard/app.py` (Flask dev server)
2. Production: `gunicorn -k eventlet wsgi:application` (via wsgi.py)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import threading
import time
from datetime import datetime
from app.models import Database
from app.collector import LogCollector
from app.correlation_engine import CorrelationEngine
from app.alert_manager import AlertManager
from config import SECRET_KEY, DEBUG, HOST, PORT, DATABASE_PATH, LOG_DIR

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# Ensure data directories exist
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# SocketIO with eventlet async_mode for production compatibility
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Initialize components
db = Database()
collector = LogCollector(db)
correlation_engine = CorrelationEngine(db)
alert_manager = AlertManager(db)

# Background thread control
running = True
_cycle_count = 0

def background_log_collection():
    """Run log collection in background (works with both dev and gunicorn)"""
    global running, _cycle_count
    _cycle_count = 0
    
    # Brief delay to ensure server is fully initialized
    time.sleep(2)
    
    while running:
        _cycle_count += 1
        try:
            attacker_mode = (_cycle_count % 5 == 0)
            num_logs = 8 if attacker_mode else 4
            logs = collector.collect_logs(num_logs, attacker_mode)
            
            # Emit new logs to dashboard via WebSocket
            socketio.emit('new_logs', {'logs': logs, 'count': len(logs)})
            
            # Run correlation analysis every 2 cycles
            if _cycle_count % 2 == 0:
                alerts = correlation_engine.run_analysis()
                if alerts:
                    alert_manager.process_alerts(alerts)
                    socketio.emit('new_alerts', {'alerts': alerts})
            
            # Update stats every cycle
            stats = {
                'log_count': db.get_log_count(),
                'alert_count': db.get_alert_count(),
                'recent_logs': [{
                    'id': l[0], 'timestamp': l[1], 'source_ip': l[2],
                    'event_type': l[3], 'severity': l[4], 'message': l[5]
                } for l in db.get_recent_logs(10)],
                'recent_alerts': [{
                    'id': a[0], 'timestamp': a[1], 'alert_type': a[2],
                    'source_ip': a[3], 'severity': a[4], 'description': a[5]
                } for a in db.get_recent_alerts(5)]
            }
            socketio.emit('stats_update', stats)
            
        except Exception as e:
            print(f"Background error: {e}")
        
        time.sleep(5)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/logs')
def logs():
    """Log viewer page"""
    return render_template('logs.html')

@app.route('/alerts')
def alerts():
    """Alert history page"""
    return render_template('alerts.html')

@app.route('/api/logs')
def api_logs():
    """API endpoint to get logs"""
    event_type = request.args.get('type')
    source_ip = request.args.get('ip')
    limit = int(request.args.get('limit', 50))
    
    if event_type:
        results = db.get_logs_by_type(event_type, limit)
    elif source_ip:
        results = db.get_logs_by_ip(source_ip, limit)
    else:
        results = db.get_recent_logs(limit)
    
    logs_data = [{
        'id': l[0], 'timestamp': l[1], 'source_ip': l[2],
        'event_type': l[3], 'severity': l[4], 'message': l[5]
    } for l in results]
    
    return jsonify(logs_data)

@app.route('/api/alerts')
def api_alerts():
    """API endpoint to get alerts"""
    limit = int(request.args.get('limit', 50))
    results = db.get_recent_alerts(limit)
    
    alerts_data = [{
        'id': a[0], 'timestamp': a[1], 'alert_type': a[2],
        'source_ip': a[3], 'severity': a[4], 'description': a[5]
    } for a in results]
    
    return jsonify(alerts_data)

@app.route('/api/log/<int:log_id>')
def api_log_detail(log_id):
    """API endpoint to get a single log by ID"""
    cursor = db.conn.cursor()
    cursor.execute('SELECT * FROM logs WHERE id = ?', (log_id,))
    l = cursor.fetchone()
    if l:
        return jsonify({
            'id': l[0], 'timestamp': l[1], 'source_ip': l[2],
            'event_type': l[3], 'severity': l[4], 'message': l[5],
            'raw_log': l[6], 'parsed_at': l[7]
        })
    return jsonify({'error': 'Log not found'}), 404

@app.route('/api/alert/<int:alert_id>')
def api_alert_detail(alert_id):
    """API endpoint to get a single alert by ID"""
    cursor = db.conn.cursor()
    cursor.execute('SELECT * FROM alerts WHERE id = ?', (alert_id,))
    a = cursor.fetchone()
    if a:
        return jsonify({
            'id': a[0], 'timestamp': a[1], 'alert_type': a[2],
            'source_ip': a[3], 'severity': a[4], 'description': a[5],
            'status': a[6], 'created_at': a[7]
        })
    return jsonify({'error': 'Alert not found'}), 404

@app.route('/api/stats')
def api_stats():
    """API endpoint to get dashboard stats"""
    return jsonify({
        'log_count': db.get_log_count(),
        'alert_count': db.get_alert_count()
    })

@socketio.on('connect')
def handle_connect():
    """Handle WebSocket client connection"""
    print(f"Dashboard client connected")
    emit('connected', {'message': 'Connected to Cyber Shield SIEM'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Dashboard client disconnected")

def start_background_thread():
    """Start the background log collection thread"""
    thread = threading.Thread(target=background_log_collection)
    thread.daemon = True
    thread.start()
    return thread

def run_dashboard():
    """Start the dashboard server (for local development)"""
    global running
    running = True
    
    # Start background thread
    start_background_thread()
    
    print("\n" + "="*60)
    print("  🛡️ CYBER SHIELD SIEM DASHBOARD")
    print("="*60)
    print(f"  🌐 Open in browser: http://localhost:{PORT}")
    print(f"  📊 Dashboard:       http://localhost:{PORT}/")
    print(f"  📋 Logs:            http://localhost:{PORT}/logs")
    print(f"  🚨 Alerts:          http://localhost:{PORT}/alerts")
    print(f"  📈 API Stats:       http://localhost:{PORT}/api/stats")
    print("="*60 + "\n")
    
    socketio.run(app, host=HOST, port=PORT, debug=DEBUG, allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    # For local development only
    # For production use: gunicorn -k eventlet -w 1 wsgi:application
    print("[DEV] Starting Cyber Shield SIEM in development mode...")
    run_dashboard()
