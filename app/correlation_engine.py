"""
Correlation Engine - Detects security threats by analyzing log patterns
"""
from datetime import datetime, timedelta
from config import BRUTE_FORCE_THRESHOLD, BRUTE_FORCE_WINDOW, PORT_SCAN_THRESHOLD, PORT_SCAN_WINDOW

class CorrelationEngine:
    def __init__(self, db):
        self.db = db
        self.detected_alerts = set()  # Track recent alerts to avoid duplicates
    
    def check_brute_force(self):
        """Detect brute force attacks: multiple failed SSH logins from same IP"""
        print("  🔍 Checking for brute force attacks...")
        
        # Get failed SSH logs in the time window
        cursor = self.db.conn.cursor()
        time_threshold = (datetime.now() - timedelta(seconds=BRUTE_FORCE_WINDOW)).isoformat()
        
        cursor.execute('''
            SELECT source_ip, COUNT(*) as attempt_count 
            FROM logs 
            WHERE event_type = 'SSH' 
            AND severity IN ('CRITICAL', 'WARNING')
            AND message LIKE '%Failed%'
            AND timestamp > ?
            GROUP BY source_ip
            HAVING attempt_count >= ?
        ''', (time_threshold, BRUTE_FORCE_THRESHOLD))
        
        results = cursor.fetchall()
        alerts = []
        
        for row in results:
            source_ip = row[0]
            count = row[1]
            alert_key = f"BRUTE_FORCE_{source_ip}"
            
            if alert_key not in self.detected_alerts:
                alert = {
                    "timestamp": datetime.now().isoformat(),
                    "alert_type": "BRUTE_FORCE",
                    "source_ip": source_ip,
                    "severity": "CRITICAL",
                    "description": f"Brute force attack detected! {count} failed SSH attempts from {source_ip} in {BRUTE_FORCE_WINDOW}s"
                }
                self.db.insert_alert(**alert)
                alerts.append(alert)
                self.detected_alerts.add(alert_key)
                print(f"  🚨 BRUTE FORCE DETECTED from {source_ip} - {count} attempts!")
        
        return alerts
    
    def check_port_scan(self):
        """Detect port scanning: connections to many different ports from same IP"""
        print("  🔍 Checking for port scans...")
        
        cursor = self.db.conn.cursor()
        time_threshold = (datetime.now() - timedelta(seconds=PORT_SCAN_WINDOW)).isoformat()
        
        cursor.execute('''
            SELECT source_ip, COUNT(DISTINCT message) as unique_targets
            FROM logs 
            WHERE event_type = 'FIREWALL'
            AND severity IN ('WARNING', 'CRITICAL')
            AND timestamp > ?
            GROUP BY source_ip
            HAVING unique_targets >= ?
        ''', (time_threshold, PORT_SCAN_THRESHOLD))
        
        results = cursor.fetchall()
        alerts = []
        
        for row in results:
            source_ip = row[0]
            count = row[1]
            alert_key = f"PORT_SCAN_{source_ip}"
            
            if alert_key not in self.detected_alerts:
                alert = {
                    "timestamp": datetime.now().isoformat(),
                    "alert_type": "PORT_SCAN",
                    "source_ip": source_ip,
                    "severity": "HIGH",
                    "description": f"Port scan detected! {count} unique targets from {source_ip} in {PORT_SCAN_WINDOW}s"
                }
                self.db.insert_alert(**alert)
                alerts.append(alert)
                self.detected_alerts.add(alert_key)
                print(f"  🚨 PORT SCAN DETECTED from {source_ip} - {count} target variations!")
        
        return alerts
    
    def check_suspicious_http(self):
        """Detect suspicious HTTP requests (directory traversal, admin access attempts)"""
        print("  🔍 Checking for suspicious HTTP requests...")
        
        cursor = self.db.conn.cursor()
        time_threshold = (datetime.now() - timedelta(minutes=5)).isoformat()
        
        cursor.execute('''
            SELECT source_ip, message, COUNT(*) as request_count
            FROM logs 
            WHERE event_type = 'HTTP'
            AND (message LIKE '%/admin%' OR message LIKE '%/wp-admin%' OR message LIKE '%../%' OR message LIKE '%passwd%')
            AND timestamp > ?
            GROUP BY source_ip, message
        ''', (time_threshold,))
        
        results = cursor.fetchall()
        alerts = []
        
        for row in results:
            source_ip = row[0]
            message = row[1]
            count = row[2]
            alert_key = f"SUSPICIOUS_HTTP_{source_ip}_{message[:20]}"
            
            if alert_key not in self.detected_alerts:
                alert = {
                    "timestamp": datetime.now().isoformat(),
                    "alert_type": "SUSPICIOUS_HTTP",
                    "source_ip": source_ip,
                    "severity": "MEDIUM",
                    "description": f"Suspicious HTTP request from {source_ip}: {message} (seen {count}x)"
                }
                self.db.insert_alert(**alert)
                alerts.append(alert)
                self.detected_alerts.add(alert_key)
                print(f"  ⚠️ SUSPICIOUS HTTP from {source_ip}: {message}")
        
        return alerts
    
    def run_analysis(self):
        """Run all correlation checks"""
        print("\n🔄 Running correlation analysis...")
        all_alerts = []
        
        all_alerts.extend(self.check_brute_force())
        all_alerts.extend(self.check_port_scan())
        all_alerts.extend(self.check_suspicious_http())
        
        if not all_alerts:
            print("  ✅ No threats detected in this cycle")
        
        # Clean old alert cache (keep last 1000)
        if len(self.detected_alerts) > 1000:
            self.detected_alerts.clear()
        
        return all_alerts
