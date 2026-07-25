"""
Log Collector - Generates simulated security logs for testing
"""
import random
import time
from datetime import datetime
from app.models import Database

class LogCollector:
    def __init__(self, db):
        self.db = db
        
        # Simulated IP addresses
        self.normal_ips = [
            "192.168.1.10", "192.168.1.20", "192.168.1.30",
            "10.0.0.5", "10.0.0.10", "172.16.0.2"
        ]
        self.attacker_ips = [
            "192.168.1.105", "10.0.0.50", "203.0.113.5",
            "198.51.100.20", "185.220.101.1"
        ]
        
        self.log_templates = {
            "SSH": {
                "success": [
                    "Accepted password for root from {ip} port 22 ssh2",
                    "Accepted publickey for admin from {ip} port 22 ssh2"
                ],
                "failed": [
                    "Failed password for root from {ip} port 22 ssh2",
                    "Failed password for invalid user admin from {ip} port 22 ssh2",
                    "Connection closed by authenticating user root {ip} port 22"
                ]
            },
            "HTTP": {
                "success": [
                    'GET /index.html HTTP/1.1" 200',
                    'GET /about.html HTTP/1.1" 200',
                    'POST /login HTTP/1.1" 302',
                    'GET /dashboard HTTP/1.1" 200'
                ],
                "failed": [
                    'GET /admin HTTP/1.1" 403',
                    'POST /login HTTP/1.1" 401',
                    'GET /wp-admin HTTP/1.1" 404',
                    'GET /../../etc/passwd HTTP/1.1" 400'
                ]
            },
            "SYSTEM": {
                "info": [
                    "Firewall rule updated: block port 445",
                    "DNS query completed for google.com",
                    "DHCP lease renewed for {ip}",
                    "Service httpd restarted successfully"
                ],
                "warning": [
                    "Disk space warning: 85% used on /dev/sda1",
                    "High memory usage detected: 92%",
                    "Certificate for *.example.com expires in 7 days",
                    "Failed to connect to update server"
                ]
            },
            "FIREWALL": {
                "blocked": [
                    "BLOCKED: Incoming TCP packet from {ip}:5432 to port 3306",
                    "BLOCKED: ICMP flood detected from {ip}",
                    "BLOCKED: UDP packet from {ip}:12345 to port 53",
                    "DROPPED: SYN flood from {ip}"
                ],
                "allowed": [
                    "ALLOWED: Established connection from {ip}:443",
                    "ALLOWED: Outbound connection to 8.8.8.8:53"
                ]
            }
        }
    
    def generate_log(self, attacker_mode=False):
        """Generate a single random log entry"""
        timestamp = datetime.now().isoformat()
        
        if attacker_mode and random.random() < 0.7:
            # Generate attack-like logs
            source_ip = random.choice(self.attacker_ips)
            event_type = random.choice(["SSH", "HTTP", "FIREWALL"])
            
            if event_type == "SSH":
                severity = "CRITICAL"
                template = random.choice(self.log_templates["SSH"]["failed"])
                message = template.format(ip=source_ip)
            elif event_type == "HTTP":
                severity = "WARNING"
                template = random.choice(self.log_templates["HTTP"]["failed"])
                message = template.format(ip=source_ip)
            else:
                severity = "WARNING"
                template = random.choice(self.log_templates["FIREWALL"]["blocked"])
                message = template.format(ip=source_ip)
        else:
            # Generate normal traffic
            source_ip = random.choice(self.normal_ips)
            event_type = random.choice(["SSH", "HTTP", "SYSTEM", "FIREWALL"])
            
            if event_type == "SSH":
                severity = "INFO"
                template = random.choice(self.log_templates["SSH"]["success"])
                message = template.format(ip=source_ip)
            elif event_type == "HTTP":
                severity = "INFO"
                template = random.choice(self.log_templates["HTTP"]["success"])
                message = template.format(ip=source_ip)
            elif event_type == "SYSTEM":
                severity = random.choice(["INFO", "WARNING"])
                category = "warning" if severity == "WARNING" else "info"
                template = random.choice(self.log_templates["SYSTEM"][category])
                message = template.format(ip=source_ip)
            else:
                severity = "INFO"
                template = random.choice(self.log_templates["FIREWALL"]["allowed"])
                message = template.format(ip=source_ip)
        
        raw_log = f"{timestamp} {source_ip} {event_type}: {message}"
        
        return {
            "timestamp": timestamp,
            "source_ip": source_ip,
            "event_type": event_type,
            "severity": severity,
            "message": message,
            "raw_log": raw_log
        }
    
    def collect_logs(self, num_logs=5, attacker_mode=False):
        """Generate and store multiple log entries"""
        logs = []
        for _ in range(num_logs):
            log_data = self.generate_log(attacker_mode)
            self.db.insert_log(
                log_data["timestamp"],
                log_data["source_ip"],
                log_data["event_type"],
                log_data["severity"],
                log_data["message"],
                log_data["raw_log"]
            )
            logs.append(log_data)
        return logs

    def run_continuous(self, interval=5):
        """Run continuous log collection"""
        print("🔍 Log Collector started - generating logs every {} seconds".format(interval))
        cycle = 0
        while True:
            cycle += 1
            # Every 5th cycle, generate attack patterns
            attacker_mode = (cycle % 5 == 0)
            num_logs = 8 if attacker_mode else 4
            
            logs = self.collect_logs(num_logs, attacker_mode)
            status = "⚠️ ATTACK PATTERN" if attacker_mode else "✅ Normal"
            print(f"  [{datetime.now().strftime('%H:%M:%S')}] Generated {len(logs)} logs - {status}")
            
            time.sleep(interval)
