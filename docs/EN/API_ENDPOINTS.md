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
- `morethan` (optional): Filter matches where both home & away odds > value (e.g., `morethan=2`)
- `anyonehas` (optional): Filter matches where any outcome (home/draw/away) has odds in range [value, value+0.09] (e.g., `anyonehas=1.4` matches odds 1.400-1.490)

**Note:** Matches are automatically sorted by `matchStart` timestamp (earliest first).

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

# Filter by odds (both home & away > 2)
curl http://localhost:5000/api/matches?morethan=2

# Filter by odds range (any outcome 1.400-1.490)
curl http://localhost:5000/api/matches?anyonehas=1.4

# Combine all filters
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025&morethan=2&anyonehas=1.4
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
  "message_count": 155,
  "last_capture_time": "2025-11-04T17:52:27.736042"
}
```

### GET `/api/capture/status`
**Description:** Get background capture status

**Response:**
```json
{
  "auto_capture_enabled": true,
  "capture_in_progress": false,
  "interval_minutes": 30,
  "last_capture_time": "2025-11-04T17:52:27.736042",
  "message_count": 157
}
```

### POST `/api/capture/trigger`
**Description:** Manually trigger a fresh data capture

**Usage:**
```bash
curl -X POST http://localhost:5000/api/capture/trigger
```

**Response:**
```json
{
  "success": true,
  "message": "Capture started in background"
}
```

**Note:** Capture runs in background (takes ~3 minutes). Use `/api/capture/status` to monitor progress.

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

- **630+ football matches** with competitor names and odds
- **157 messages** captured
- Data from auto-scrolling capture
- All matches include odds data
- **Matches automatically sorted by start time**

## Automatic Data Refresh

The API automatically captures fresh data every 30 minutes in the background. No manual intervention needed!

**Configuration** (in `serve_data.py`):
- `CAPTURE_INTERVAL_MINUTES = 30` - Change capture frequency
- `AUTO_CAPTURE_ENABLED = True` - Enable/disable auto-capture
- `CAPTURE_DURATION_SECONDS = 180` - Duration per capture (3 minutes)

**Manual Capture:**
```bash
# Trigger a capture immediately
curl -X POST http://localhost:5000/api/capture/trigger

# Check capture status
curl http://localhost:5000/api/capture/status
```

**Manual Capture (Old Method):**
```bash
# Capture for 180 seconds with auto-scroll
python analyze_winamax_socketio.py

# Then restart the API server (not needed with auto-capture)
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

# Matches where both home & away odds > 2
curl http://localhost:5000/api/matches?morethan=2

# Matches where any outcome has odds 1.400-1.490
curl http://localhost:5000/api/matches?anyonehas=1.4

# Football matches with both odds > 2
curl http://localhost:5000/api/matches?sportId=1&morethan=2

# Combine all filters
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025&morethan=2&anyonehas=1.4
```

## Match Sorting

All matches are automatically sorted by `matchStart` timestamp in ascending order (earliest matches first). Matches without a timestamp are placed at the end.
