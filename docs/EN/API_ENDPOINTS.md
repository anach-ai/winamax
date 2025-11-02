# Winamax API Endpoints Documentation

## Working API Server

**File:** `serve_data.py` - Serves captured Socket.IO data  
**Status:** ✅ **WORKING**  
**Port:** 5000

## Available Endpoints

### GET `/api/matches`
**Description:** Get all football matches with odds (simplified)

**Query Parameters:**
- `sportId` (optional): Filter by sport ID (1=Football)
- `date` (optional): Filter by date (format: DD-MM-YYYY)

**Response:**
```json
{
  "success": true,
  "matches": [
    {
      "matchId": "56418335",
      "title": "Slovénie - Kosovo",
      "status": "PREMATCH",
      "competitor1Name": "Slovénie",
      "competitor2Name": "Kosovo",
      "matchStart": 1763235900,
      "odds": {
        "Slovénie": 1.78,
        "Match nul": 3.2,
        "Kosovo": 3.9
      }
    }
  ],
  "count": 624
}
```

**Usage:**
```bash
# All matches
curl http://localhost:5000/api/matches

# Filter by football
curl http://localhost:5000/api/matches?sportId=1

# Filter by date
curl http://localhost:5000/api/matches?date=15-11-2025

# Combined filters
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025
```

### GET `/api/matches/verbose`
**Description:** Get all matches with full details

**Query Parameters:**
- `sportId` (optional): Filter by sport ID (1=Football)

**Response:** Full match data including all metadata

**Usage:**
```bash
curl http://localhost:5000/api/matches/verbose
curl http://localhost:5000/api/matches/verbose?sportId=1
```

### GET `/api/matches/<match_id>`
**Description:** Get specific match by ID

**Example:**
```bash
curl http://localhost:5000/api/matches/56418335
```

**Response:**
```json
{
  "success": true,
  "match": {
    "matchId": "56418335",
    "title": "Slovénie - Kosovo",
    "status": "PREMATCH",
    "competitor1Name": "Slovénie",
    "competitor2Name": "Kosovo",
    "matchStart": 1763235900,
    "odds": {
      "Slovénie": 1.78,
      "Match nul": 3.2,
      "Kosovo": 3.9
    }
  }
}
```

### GET `/api/status`
**Description:** Get API status

**Response:**
```json
{
  "status": "running",
  "messages_count": 155,
  "server": "Winamax Data Server"
}
```

### GET `/api/info`
**Description:** Get capture information

**Response:**
```json
{
  "url": "https://www.winamax.fr/paris-sportifs/sports/1",
  "timestamp": "2025-11-02T03:46:59.686006",
  "message_count": 155
}
```

### GET `/api/data/raw`
**Description:** Get complete raw captured data

## Quick Start

1. **Start the server:**
```bash
python serve_data.py
```

2. **Get matches:**
```bash
# Using curl
curl http://localhost:5000/api/matches

# Using Python
import requests
response = requests.get('http://localhost:5000/api/matches')
print(response.json())
```

3. **Get specific match:**
```bash
curl http://localhost:5000/api/matches/56418335
```

## Match Data Structure

### Simplified Format (default)
```json
{
  "matchId": "56418335",
  "title": "Slovénie - Kosovo",
  "status": "PREMATCH",
  "competitor1Name": "Slovénie",
  "competitor2Name": "Kosovo",
  "matchStart": 1763235900,
  "odds": {
    "Slovénie": 1.78,
    "Match nul": 3.2,
    "Kosovo": 3.9
  }
}
```

### Verbose Format
Full match data including all metadata, outcomes, bets, etc.

## Current Dataset

- **624 football matches** with competitor names and odds
- **155 messages** captured
- Data from auto-scrolling capture
- All matches include odds data

## For Fresh Data

Use the Selenium capture tool:
```bash
# Capture for 120 seconds with auto-scroll
python analyze_winamax_socketio.py 120
```

Then restart the API server to load new data:
```bash
python serve_data.py
```

## Filter Examples

```bash
# Football only
curl http://localhost:5000/api/matches?sportId=1

# Specific date
curl http://localhost:5000/api/matches?date=15-11-2025

# Football on specific date
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025
```
