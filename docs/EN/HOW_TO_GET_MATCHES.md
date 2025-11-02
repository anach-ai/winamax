# How to Get Football Matches with Odds - Complete Guide

## ✅ WORKING SOLUTION

Use `serve_data.py` - A Flask API that serves captured Winamax Socket.IO data.

## Quick Start

### 1. Start the Server

```bash
python serve_data.py
```

Server will be running on: `http://localhost:5000`

### 2. Get Matches

**Using cURL:**
```bash
curl http://localhost:5000/api/matches
```

**Using Python:**
```python
import requests
response = requests.get('http://localhost:5000/api/matches')
matches = response.json()
print(f"Found {matches['count']} matches")
```

**Using JavaScript:**
```javascript
fetch('http://localhost:5000/api/matches')
    .then(res => res.json())
    .then(data => console.log(data.matches));
```

### 3. Example Output

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

## Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/matches` | GET | Get all matches (simplified) |
| `/api/matches?sportId=1` | GET | Filter by sport (1=Football) |
| `/api/matches?date=DD-MM-YYYY` | GET | Filter by date |
| `/api/matches?sportId=1&date=DD-MM-YYYY` | GET | Filter by sport + date |
| `/api/matches/verbose` | GET | Get all matches (full details) |
| `/api/matches/<id>` | GET | Get specific match |
| `/api/status` | GET | Server status |
| `/api/info` | GET | Capture info |
| `/api/data/raw` | GET | Raw data |

## Match ID Examples

- `56418335` - Slovénie vs Kosovo
- `56418336` - Suisse vs Suède  
- `56418337` - Luxembourg vs Allemagne
- `56418338` - Slovaquie vs Irlande du Nord
- `56418339` - Grèce vs Écosse

## Advanced Usage

### Filter by Sport

```python
import requests

# Get only football matches (sportId=1)
response = requests.get('http://localhost:5000/api/matches?sportId=1')
data = response.json()
print(f"Football matches: {data['count']}")
```

### Filter by Date

```python
import requests

# Get matches for a specific date (DD-MM-YYYY format)
response = requests.get('http://localhost:5000/api/matches?date=15-11-2025')
data = response.json()
print(f"Matches on 15-11-2025: {data['count']}")
```

### Filter by Sport + Date

```python
import requests

# Get football matches for a specific date
response = requests.get('http://localhost:5000/api/matches?sportId=1&date=15-11-2025')
data = response.json()
print(f"Football matches on 15-11-2025: {data['count']}")
```

### Get Specific Match

```python
match_id = "56418335"
response = requests.get(f'http://localhost:5000/api/matches/{match_id}')
match = response.json()['match']

print(f"Match: {match['competitor1Name']} vs {match['competitor2Name']}")
print(f"Status: {match['status']}")
print(f"Odds: {match.get('odds', {})}")
```

## Data Structure

### Simplified Match Object
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

## Real-Time Data (Optional)

To get fresh real-time data:

1. Run the capture tool:
```bash
python analyze_winamax_socketio.py 60
```

2. This will update `winamax_socketio_analysis.json`

3. Restart the API server:
```bash
python serve_data.py
```

## API Usage Examples

### Complete Python Example

```python
import requests
import json

# Get all matches
response = requests.get('http://localhost:5000/api/matches')
data = response.json()

if data['success']:
    print(f"Total matches: {data['count']}")
    
    for match in data['matches'][:10]:  # First 10
        print(f"\nMatch: {match['matchId']}")
        print(f"  {match['competitor1Name']} vs {match['competitor2Name']}")
        print(f"  Status: {match['status']}")
        if 'odds' in match:
            print(f"  Odds: {match['odds']}")
```

### cURL Examples

```bash
# Get all matches
curl http://localhost:5000/api/matches

# Get football matches
curl http://localhost:5000/api/matches?sportId=1

# Filter by date
curl http://localhost:5000/api/matches?date=15-11-2025

# Combined filters
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025

# Get specific match
curl http://localhost:5000/api/matches/56418335

# Get status
curl http://localhost:5000/api/status
```

## Troubleshooting

**No data?**
- Make sure `winamax_socketio_analysis.json` exists
- Check file has content

**Server not starting?**
```bash
pip install flask flask-cors
python serve_data.py
```

**Need fresh data?**
```bash
python analyze_winamax_socketio.py 60
```

## Next Steps

1. ✅ **Use current API** - Works with captured data
2. Optional: Integrate with real-time capture
3. Optional: Add filtering and querying
4. Optional: Store in database

## Summary

**Working Solution:**
- File: `serve_data.py`
- Endpoint: `GET /api/matches`
- Output: JSON with matches and metadata
- Status: ✅ Fully functional

**Command to use:**
```bash
python serve_data.py && curl http://localhost:5000/api/matches
```

