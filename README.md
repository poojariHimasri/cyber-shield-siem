# 🛡️ Cyber Shield SIEM

**A Mini Security Information and Event Management System**

Developed as a 4th Year Cybersecurity Project.

---

## 📋 Project Overview

Cyber Shield SIEM is a lightweight SIEM system that:
- Simulates and collects security logs
- Parses and normalizes log data
- Detects security threats using correlation rules
- Sends real-time alerts
- Provides a web dashboard for visualization

---

## 🧱 System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Log Generator   │────▶│  Log Collector   │────▶│  Parser/Normalizer│
│ (Simulates logs) │     │  (syslog/agent)  │     │  (JSON structured)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Dashboard UI    │◀────│  Alert Manager   │◀────│ Correlation Eng. │
│ (Flask + Chart.js)│    │  (Email/Slack)   │     │ (Rule matching)  │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
                                                  ┌─────────────────┐
                                                  │   Database       │
                                                  │  (SQLite/MySQL)  │
                                                  └─────────────────┘
```

---

## 🔧 Tech Stack

| Component      | Technology          |
|----------------|---------------------|
| Backend        | Python 3 + Flask    |
| Database       | SQLite              |
| Frontend       | HTML, CSS, Chart.js |
| Alerting       | SMTP / Webhook      |
| Log Format     | JSON                |

---

## 🚀 Features

1. **Log Simulation Engine** - Generates realistic SSH, HTTP, and system logs
2. **Log Collection & Parsing** - Ingests and normalizes raw logs
3. **Threat Detection Engine** - Rule-based correlation (Brute Force, Port Scan, Malware)
4. **Real-time Alerting** - Email and dashboard notifications
5. **Interactive Dashboard** - Real-time charts, log explorer, alert timeline
6. **Report Generation** - CSV/PDF summary reports

---

## 📁 Project Structure

```
cyber-shield-siem/
├── app/
│   ├── __init__.py
│   ├── collector.py          # Log collection module
│   ├── parser.py             # Log parsing & normalization
│   ├── correlation_engine.py # Threat detection rules
│   ├── alert_manager.py      # Alert dispatch
│   └── models.py             # Database models
├── dashboard/
│   ├── app.py                # Flask web server
│   ├── templates/
│   │   ├── index.html        # Main dashboard
│   │   ├── logs.html         # Log explorer
│   │   └── alerts.html       # Alert viewer
│   └── static/
│       └── style.css         # Dashboard styling
├── logs/                     # Simulated log storage
├── config.py                 # Configuration
├── main.py                   # Entry point
├── requirements.txt          # Dependencies
├── run.py                    # Launcher script
└── README.md                 # This file
```

---

## ⚙️ Installation & Setup

```bash
# 1. Navigate to project
cd cyber-shield-siem

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python run.py
```

---

## 🎓 Learning Outcomes

- Understand SIEM architecture and event correlation
- Work with log formats (Syslog, JSON, CSV)
- Build rule-based detection engines
- Develop real-time web dashboards
- Practice cybersecurity monitoring concepts

