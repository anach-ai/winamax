# Setup Guide - Winamax Football Matches API

Complete setup instructions for the Winamax Football Matches API by Anass EL.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Chrome browser installed
- Git (optional, for cloning)

## Quick Setup

### 1. Clone or Download

```bash
# If using Git
git clone https://github.com/anach-ai/winamax.git
cd winamax

# Or download ZIP and extract
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `selenium==4.16.0` - Browser automation
- `selenium-stealth==1.0.6` - Bot detection bypass
- `webdriver-manager==4.0.2` - ChromeDriver management
- `flask==3.0.0` - Web framework
- `flask-cors==4.0.0` - CORS support

### 3. Verify Installation

```bash
python --version  # Should be 3.8+
pip list  # Check installed packages
```

### 4. Run the API

```bash
python serve_data.py
```

You should see:
```
Starting Winamax Data API...
Visit:
  http://localhost:5000/api/matches - Get all matches
  http://localhost:5000/api/status - Check status
  http://localhost:5000/api/info - Capture info
```

### 5. Test the API

Open a new terminal:

```bash
curl http://localhost:5000/api/matches
```

Or visit in browser:
- http://localhost:5000/api/matches
- http://localhost:5000/api/status
- http://localhost:5000/api/info

## Data Capture (Optional)

To capture fresh data:

```bash
# Capture for 120 seconds with auto-scroll
python analyze_winamax_socketio.py 120

# Analyze captured data
python analyze_results.py
```

## Configuration

### API Port

Default port is 5000. To change:

Edit `serve_data.py` line 298:
```python
app.run(host='0.0.0.0', port=5000, debug=False)
```

### Capture URL

Default captures from football (sportId=1). To change:

Edit `analyze_winamax_socketio.py` line 46:
```python
self.url = "https://www.winamax.fr/paris-sportifs/sports/1"  # Football
```

## Troubleshooting

### ChromeDriver Issues

If you see ChromeDriver errors:
- The `webdriver-manager` package handles this automatically
- If issues persist, manually download ChromeDriver matching your Chrome version

### Port Already in Use

If port 5000 is busy:
```bash
# Find and kill the process
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill
```

### Import Errors

If you see import errors:
```bash
pip install --upgrade -r requirements.txt
```

### Data Not Loading

Ensure `winamax_socketio_analysis.json` exists:
```bash
ls winamax_socketio_analysis.json
```

If missing, run a capture first:
```bash
python analyze_winamax_socketio.py 60
```

## Development Environment

### Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### IDE Setup

Recommended IDEs:
- PyCharm
- VS Code with Python extension
- Sublime Text

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 serve_data:app
```

### Using Docker (Future)

Dockerfile coming soon!

## Environment Variables

Current configuration doesn't require environment variables. For future:
- `API_PORT` - Set custom port
- `LOG_LEVEL` - Set logging level
- `CORS_ORIGINS` - Configure CORS

## Support

- Documentation: See README.md
- Issues: Open on GitHub
- Questions: Check existing documentation

## Next Steps

1. Read `START_HERE.md` for quick start
2. Review `HOW_TO_GET_MATCHES.md` for complete guide
3. Explore `API_ENDPOINTS.md` for API reference
4. Check `CHANGELOG.md` for updates

---

**Happy coding!** 🚀

