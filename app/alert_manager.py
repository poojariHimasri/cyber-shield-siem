"""
Alert Manager - Sends notifications when threats are detected
"""
import smtplib
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import (
    ALERT_EMAIL_ENABLED, ALERT_EMAIL_SERVER, ALERT_EMAIL_PORT,
    ALERT_EMAIL_USER, ALERT_EMAIL_PASS, ALERT_EMAIL_TO
)

class AlertManager:
    def __init__(self, db):
        self.db = db
        self.alert_log = []  # Keep recent alerts in memory
    
    def process_alert(self, alert):
        """Process and dispatch an alert"""
        timestamp = alert.get("timestamp", datetime.now().isoformat())
        alert_type = alert.get("alert_type", "UNKNOWN")
        source_ip = alert.get("source_ip", "0.0.0.0")
        severity = alert.get("severity", "LOW")
        description = alert.get("description", "No description")
        
        # Store in memory
        self.alert_log.append({
            "timestamp": timestamp,
            "alert_type": alert_type,
            "source_ip": source_ip,
            "severity": severity,
            "description": description
        })
        
        # Keep last 100 alerts in memory
        if len(self.alert_log) > 100:
            self.alert_log.pop(0)
        
        # Print to console
        severity_icon = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🔵"
        }.get(severity, "⚪")
        
        print(f"\n{severity_icon} ALERT [{severity}] {alert_type}")
        print(f"   Source: {source_ip}")
        print(f"   Time: {timestamp}")
        print(f"   Details: {description}")
        
        # Send email if enabled
        if ALERT_EMAIL_ENABLED and severity in ["CRITICAL", "HIGH"]:
            self._send_email_alert(alert)
        
        return True
    
    def process_alerts(self, alerts):
        """Process multiple alerts"""
        for alert in alerts:
            self.process_alert(alert)
        return len(alerts)
    
    def _send_email_alert(self, alert):
        """Send alert via email"""
        if not ALERT_EMAIL_USER or not ALERT_EMAIL_PASS:
            print("   📧 Email alerts disabled - no credentials configured")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = ALERT_EMAIL_USER
            msg['To'] = ALERT_EMAIL_TO
            msg['Subject'] = f"🚨 Cyber Shield SIEM Alert: {alert['alert_type']} [{alert['severity']}]"
            
            body = f"""
            🛡️ CYBER SHIELD SIEM ALERT
            
            Alert Type: {alert['alert_type']}
            Severity: {alert['severity']}
            Source IP: {alert['source_ip']}
            Timestamp: {alert['timestamp']}
            
            Description:
            {alert['description']}
            
            ---
            This is an automated alert from Cyber Shield SIEM
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(ALERT_EMAIL_SERVER, ALERT_EMAIL_PORT)
            server.starttls()
            server.login(ALERT_EMAIL_USER, ALERT_EMAIL_PASS)
            server.send_message(msg)
            server.quit()
            
            print(f"   📧 Email alert sent to {ALERT_EMAIL_TO}")
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to send email alert: {e}")
            return False
    
    def get_recent_alerts(self, limit=20):
        """Get recent alerts from memory"""
        return self.alert_log[-limit:]
