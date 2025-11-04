# Winamax Football Matches API

**By Anass EL**

A complete toolkit for capturing and serving Winamax football match data with odds. Includes Socket.IO analysis tools, auto-scrolling capture, REST API with filters, and comprehensive documentation.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/Docs-EN%20%7C%20FR-red.svg)](README.md)

## 🚀 Quick Start - Get Football Matches with Odds

**Want to get matches NOW?**

```bash
# Start API server
python serve_data.py

# In another terminal, get matches WITH ODDS
curl http://localhost:5000/api/matches
```

**Returns:** Clean JSON with **630+ football matches** including odds (sorted by start time):
- "Slovénie": 1.78
- "Match nul": 3.2
- "Kosovo": 3.9

**Latest Capture**: 630+ football matches with odds!  
**Auto-Refresh**: Data automatically refreshes every 1 minute in the background (headless mode).

**See [docs/EN/HOW_TO_GET_MATCHES.md](docs/EN/HOW_TO_GET_MATCHES.md) for complete guide**

## 📚 Documentation

### 🇬🇧 English Documentation
Located in [`docs/EN/`](docs/EN/)
- **`START_HERE.md`** ⭐ - Quick start guide
- **`HOW_TO_GET_MATCHES.md`** ⭐ - Complete guide to get matches
- **`API_ENDPOINTS.md`** ⭐ - API reference
- **`SETUP.md`** - Installation guide
- **`PROJECT_COMPLETE.md`** - Complete solution summary
- **`API_COMPLETE.md`** - API summary
- **`GET_MORE_MATCHES.md`** - How to capture more matches
- **`FINAL_ANSWER.md`** - Final summary
- **`CLEAN_PROJECT_SUMMARY.md`** - Cleanup summary
- **`ANALYZED_ENDPOINTS.md`** - Socket.IO analysis
- **`SOCKET_IO_ANALYSIS_SUMMARY.md`** - Protocol summary

### 🇫🇷 Documentation Française
Located in [`docs/FR/`](docs/FR/)
- **`README.md`** ⭐ - Documentation principale
- **`START_HERE.md`** ⭐ - Guide de démarrage rapide
- **`HOW_TO_GET_MATCHES.md`** ⭐ - Guide complet
- **`API_ENDPOINTS.md`** ⭐ - Référence API
- **`FINAL_ANSWER.md`** - Résumé final

## ✨ What's Included

### 1. Analysis Tools
- **`analyze_winamax_socketio.py`** - Capture Socket.IO traffic with Selenium stealth [[memory:6983704]]
- **`analyze_results.py`** - Analyze captured data
- Successfully bypasses Winamax bot detection

### 2. API Server
- **`serve_data.py`** - Working Flask API ⭐⭐⭐
- Serves captured Socket.IO data
- JSON endpoints for matches with filters
- **Background auto-capture** - Automatically refreshes data every 1 minute
- **Headless mode** - Runs Selenium in background without visible browser
- **Manual capture trigger** - Trigger fresh captures on demand
- **Match sorting** - Results sorted by match start time
- **This is the working solution!**

## 🎯 Key Features

✅ **Stealth Selenium** - Bypasses bot detection  
✅ **Headless Mode** - Runs in background without visible browser  
✅ **Auto-scrolling Capture** - Captures all matches automatically  
✅ **Background Auto-Capture** - Automatically refreshes data every 1 minute  
✅ **REST API** - Filter by sport, date, odds, and more  
✅ **Match Sorting** - Results sorted by match start time  
✅ **Match Data** - 630+ football matches with odds  
✅ **Clean JSON** - Simplified output  
✅ **Complete Docs** - Everything documented  
✅ **Bilingual** - English & French documentation

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/anach-ai/winamax.git
cd winamax

# Install dependencies
pip install -r requirements.txt

# Run the API
python serve_data.py
```

**Detailed setup:** See [docs/EN/SETUP.md](docs/EN/SETUP.md) for complete installation guide.

## 🏗️ Architecture

```
Capture:    Selenium → Auto-scroll → Socket.IO → JSON
            ↓
Background: Auto-capture every 30 min → Auto-reload → Fresh data
            ↓
Serve:      Flask API → REST endpoints → Your App
Data:       Matches, Odds, Scores, Outcomes (630+ matches, sorted by time)
```

## 📊 Data You Can Access

- **630+ Football Matches** with competitor names and odds
- **Live Matches**: Real-time scores and time progression
- **Upcoming Matches**: Schedules and match info (sorted by start time)
- **Betting Odds**: Real-time odds updates
- **Team Data**: Names, metadata
- **Filters**: By sport, date, odds (morethan, anyonehas)
- **Auto-Refresh**: Data automatically updates every 1 minute
- **Headless Mode**: Runs in background without visible browser

## 🔌 API Endpoints

```
GET  /api/matches                              - Get all matches (sorted by start time)
GET  /api/matches?sportId=1                     - Filter by sport (1=Football)
GET  /api/matches?date=DD-MM-YYYY               - Filter by date
GET  /api/matches?morethan=2                   - Filter where both odds > 2
GET  /api/matches?anyonehas=1.4                - Filter where any outcome has odds 1.400-1.490
GET  /api/matches?sportId=1&date=DD-MM-YYYY&morethan=2&anyonehas=1.4 - Combine filters
GET  /api/matches/<id>                         - Get specific match
GET  /api/matches/verbose                      - Full details
GET  /api/status                               - Server status
GET  /api/info                                 - Capture info
GET  /api/capture/status                       - Background capture status
POST /api/capture/trigger                      - Manually trigger capture
```

## ⚡ Quick Commands

```bash
# Start API server (auto-capture enabled)
python serve_data.py

# Get matches (sorted by start time)
curl http://localhost:5000/api/matches

# Filter by football + date
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025

# Filter by odds
curl http://localhost:5000/api/matches?morethan=2
curl http://localhost:5000/api/matches?anyonehas=1.4

# Trigger manual capture
curl -X POST http://localhost:5000/api/capture/trigger

# Check capture status
curl http://localhost:5000/api/capture/status

# Manual capture (old method, optional)
python analyze_winamax_socketio.py

# Analyze results
python analyze_results.py
```

## 🔍 What We Discovered

- **Protocol**: Engine.IO v3 + Socket.IO v3
- **Endpoint**: `wss://sports-eu-west-3.winamax.fr/uof-sports-server/socket.io/`
- **Transport**: WebSocket (not polling)
- **Update Rate**: Real-time (every few seconds)
- **Scale**: 630+ football matches captured
- **Auto-Refresh**: Background capture every 1 minute
- **Headless Mode**: Runs without visible browser window

## 📁 Project Structure

```
winamax/
├── 🐍 Scripts
│   ├── analyze_winamax_socketio.py    - Capture Socket.IO traffic
│   ├── analyze_results.py             - Analyze captured data
│   └── serve_data.py                  - Flask API server ⭐
│
├── 📊 Data
│   ├── winamax_socketio_analysis.json - Captured match data (630+ matches, auto-updated)
│   └── winamax_socketio.log          - Capture log
│
├── 📝 Documentation
│   ├── README.md                      - This file (English)
│   ├── LICENSE                        - MIT License
│   ├── CONTRIBUTING.md                - Contribution guide
│   ├── CHANGELOG.md                   - Version history
│   │
│   ├── 📁 docs/
│   │   ├── 🇬🇧 EN/                     - English documentation
│   │   │   ├── START_HERE.md          - Quick start ⭐
│   │   │   ├── HOW_TO_GET_MATCHES.md  - Complete guide ⭐
│   │   │   ├── API_ENDPOINTS.md       - API reference ⭐
│   │   │   ├── SETUP.md               - Installation guide
│   │   │   ├── PROJECT_COMPLETE.md    - Project summary
│   │   │   ├── API_COMPLETE.md        - API summary
│   │   │   ├── GET_MORE_MATCHES.md    - Capture guide
│   │   │   ├── FINAL_ANSWER.md        - Final summary
│   │   │   ├── CLEAN_PROJECT_SUMMARY.md - Cleanup
│   │   │   ├── ANALYZED_ENDPOINTS.md  - Socket.IO analysis
│   │   │   ├── SOCKET_IO_ANALYSIS_SUMMARY.md - Protocol
│   │   │   └── PROJECT_README.md      - Project overview
│   │   │
│   │   └── 🇫🇷 FR/                     - Documentation française
│   │       ├── README.md              - Documentation principale ⭐
│   │       ├── START_HERE.md          - Guide démarrage ⭐
│   │       ├── HOW_TO_GET_MATCHES.md  - Guide complet ⭐
│   │       ├── API_ENDPOINTS.md       - Référence API ⭐
│   │       └── FINAL_ANSWER.md        - Résumé final
│   │
└── ⚙️ Config
    ├── requirements.txt               - Python dependencies
    └── .gitignore                    - Git ignore rules
```

## 🎓 Learn More

- See captured data: `winamax_socketio_analysis.json`
- Get started: [docs/EN/START_HERE.md](docs/EN/START_HERE.md) ⭐
- Setup guide: [docs/EN/SETUP.md](docs/EN/SETUP.md)
- Usage guide: [docs/EN/HOW_TO_GET_MATCHES.md](docs/EN/HOW_TO_GET_MATCHES.md) ⭐
- Capture guide: [docs/EN/GET_MORE_MATCHES.md](docs/EN/GET_MORE_MATCHES.md)
- API docs: [docs/EN/API_ENDPOINTS.md](docs/EN/API_ENDPOINTS.md)
- Protocol: [docs/EN/ANALYZED_ENDPOINTS.md](docs/EN/ANALYZED_ENDPOINTS.md)
- Changelog: [CHANGELOG.md](CHANGELOG.md)

## 🏆 Success Metrics

✅ Bypassed Winamax bot detection  
✅ Captured 624 football matches  
✅ Auto-scrolling to get all data  
✅ Working REST API  
✅ Filter by sport & date  
✅ Comprehensive documentation  
✅ Bilingual support (EN/FR)

## 📝 Example Usage

### Python

```python
import requests

# Get all matches
response = requests.get('http://localhost:5000/api/matches')
data = response.json()
print(f"Found {data['count']} matches")

# Filter by date
response = requests.get('http://localhost:5000/api/matches?date=15-11-2025')
data = response.json()
print(f"Matches on 15-11-2025: {data['count']}")
```

### JavaScript

```javascript
fetch('http://localhost:5000/api/matches')
    .then(res => res.json())
    .then(data => console.log(data.matches));
```

### cURL

```bash
# All matches
curl http://localhost:5000/api/matches

# Filtered
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This project is for educational purposes only. Always respect Winamax's terms of service and use responsibly.

## 👤 Author

**Anass EL**

- Project: Winamax Football Matches API
- Languages: Python, Flask, Selenium
- Documentation: English & French

## 🙏 Acknowledgments

- Built with Selenium for browser automation
- Flask for the REST API
- Stealth technologies to bypass bot detection

---

**Ready to get started?** → See [docs/EN/START_HERE.md](docs/EN/START_HERE.md) 🚀

**Questions?** Open an issue or check the documentation.

---

## 📞 Quick Links

- 🇬🇧 [English Documentation](docs/EN/) - Full documentation in English
- 🇫🇷 [Documentation Française](docs/FR/) - Documentation complète en français
- 📦 [Installation Guide](docs/EN/SETUP.md) - Complete setup instructions
- 🔌 [API Reference](docs/EN/API_ENDPOINTS.md) - All endpoints explained
- 🤝 [Contribute](CONTRIBUTING.md) - How to contribute to this project
- 📝 [Changelog](CHANGELOG.md) - Version history and updates
