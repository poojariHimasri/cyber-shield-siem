"""
Log Parser - Normalizes raw logs into structured format
"""
import re
from datetime import datetime

class LogParser:
    def __init__(self):
        # Patterns for different log types
        self.patterns = {
            "SSH_SUCCESS": r"Accepted (password|publickey) for (\w+) from ([\d\.]+)",
            "SSH_FAILED": r"Failed password for (\w+) from ([\d\.]+)",
            "HTTP_200": r'GET (\S+) HTTP.*" 200',
            "HTTP_403": r'GET (\S+) HTTP.*" 403',
            "HTTP_401": r'POST (\S+) HTTP.*" 401',
            "HTTP_404": r'GET (\S+) HTTP.*" 404',
            "FIREWALL_BLOCK": r"BLOCKED:.*from ([\d\.]+)",
            "FIREWALL_DROP": r"DROPPED:.*from ([\d\.]+)",
        }
    
    def parse_log(self, log_entry):
        """Parse a log entry and extract structured information"""
        parsed = {
            "timestamp": log_entry["timestamp"],
            "source_ip": log_entry["source_ip"],
            "event_type": log_entry["event_type"],
            "severity": log_entry["severity"],
            "message": log_entry["message"],
            "category": None,
            "user": None,
            "destination": None,
            "port": None,
            "is_suspicious": False
        }
        
        # Try to extract additional details based on event type
        if log_entry["event_type"] == "SSH":
            # Extract username
            user_match = re.search(r"for (\w+) from", log_entry["message"])
            if user_match:
                parsed["user"] = user_match.group(1)
            
            # Check if it's a failed attempt
            if "Failed" in log_entry["message"] or "failed" in log_entry["message"]:
                parsed["category"] = "AUTH_FAILURE"
                parsed["is_suspicious"] = True
            else:
                parsed["category"] = "AUTH_SUCCESS"
        
        elif log_entry["event_type"] == "HTTP":
            # Extract URL path
            path_match = re.search(r'GET (\S+) HTTP', log_entry["message"])
            if path_match:
                parsed["destination"] = path_match.group(1)
            
            # Check for suspicious paths
            suspicious_paths = ["/admin", "/wp-admin", "/../../", "/etc/passwd"]
            if any(path in log_entry["message"] for path in suspicious_paths):
                parsed["is_suspicious"] = True
                parsed["category"] = "SUSPICIOUS_REQUEST"
            
            if "403" in log_entry["message"] or "401" in log_entry["message"]:
                parsed["category"] = "ACCESS_DENIED"
                parsed["is_suspicious"] = True
        
        elif log_entry["event_type"] == "FIREWALL":
            # Extract port information
            port_match = re.search(r"port (\d+)", log_entry["message"])
            if port_match:
                parsed["port"] = int(port_match.group(1))
            
            if "BLOCKED" in log_entry["message"] or "DROPPED" in log_entry["message"]:
                parsed["category"] = "TRAFFIC_BLOCKED"
                parsed["is_suspicious"] = True
        
        elif log_entry["event_type"] == "SYSTEM":
            if "warning" in log_entry["message"].lower() or "high" in log_entry["message"].lower():
                parsed["category"] = "SYSTEM_WARNING"
            else:
                parsed["category"] = "SYSTEM_INFO"
        
        return parsed
    
    def batch_parse(self, log_entries):
        """Parse multiple log entries"""
        return [self.parse_log(entry) for entry in log_entries]
