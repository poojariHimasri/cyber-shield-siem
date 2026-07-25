"""
Database Models - Stores logs, alerts, and rules
"""
import sqlite3
import os
from datetime import datetime
from config import DATABASE_PATH

class Database:
    def __init__(self):
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                event_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                raw_log TEXT,
                parsed_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                source_ip TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                status TEXT DEFAULT 'NEW',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Rules table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                field TEXT NOT NULL,
                operator TEXT NOT NULL,
                value TEXT NOT NULL,
                severity TEXT DEFAULT 'MEDIUM',
                enabled INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
        print("✅ Database tables created")
    
    def insert_log(self, timestamp, source_ip, event_type, severity, message, raw_log=""):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO logs (timestamp, source_ip, event_type, severity, message, raw_log)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, source_ip, event_type, severity, message, raw_log))
        self.conn.commit()
        return cursor.lastrowid
    
    def insert_alert(self, timestamp, alert_type, source_ip, severity, description):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO alerts (timestamp, alert_type, source_ip, severity, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (timestamp, alert_type, source_ip, severity, description))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_recent_logs(self, limit=50):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM logs ORDER BY id DESC LIMIT ?', (limit,))
        return cursor.fetchall()
    
    def get_recent_alerts(self, limit=20):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM alerts ORDER BY id DESC LIMIT ?', (limit,))
        return cursor.fetchall()
    
    def get_log_count(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM logs')
        return cursor.fetchone()[0]
    
    def get_alert_count(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM alerts')
        return cursor.fetchone()[0]
    
    def get_logs_by_type(self, event_type, limit=50):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM logs WHERE event_type = ? ORDER BY id DESC LIMIT ?', (event_type, limit))
        return cursor.fetchall()
    
    def get_logs_by_ip(self, ip, limit=50):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM logs WHERE source_ip = ? ORDER BY id DESC LIMIT ?', (ip, limit))
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()
