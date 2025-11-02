# START HERE - Get Football Matches with Odds

## 🎯 Your Goal

Get football matches with their betting odds from Winamax.

## ✅ Solution (Working Right Now)

### Step 1: Start the API Server

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

### Step 2: Get the Matches

Open another terminal and run:

```bash
curl http://localhost:5000/api/matches
```

**OR** use Python:

```python
import requests
response = requests.get('http://localhost:5000/api/matches')
print(response.json())
```

## 📋 What You Get

JSON response with football matches **WITH ODDS**:

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

## 📚 More Information

- **Complete Guide:** `HOW_TO_GET_MATCHES.md`
- **Get More Matches:** `GET_MORE_MATCHES.md` ⭐
- **API Reference:** `API_ENDPOINTS.md`
- **Analysis:** `SOCKET_IO_ANALYSIS_SUMMARY.md`

## 🎓 Next Steps

1. ✅ You're getting matches now!
2. Want MORE matches? See `GET_MORE_MATCHES.md`
3. Customize queries as needed
4. Build your application using the API

**Note:** Current capture has 624 football matches with odds! Auto-scrolling captures all matches.

## 📊 Available Endpoints

- `GET /api/matches` - All matches (simplified)
- `GET /api/matches?sportId=1` - Filter by sport (1=Football)
- `GET /api/matches?date=DD-MM-YYYY` - Filter by date
- `GET /api/matches?sportId=1&date=DD-MM-YYYY` - Filter by sport + date
- `GET /api/matches/verbose` - All matches (full details)
- `GET /api/matches/<id>` - Specific match
- `GET /api/status` - Server status
- `GET /api/info` - Data info

## 🎉 That's It!

You now have a working API to get football matches with odds!

**See `HOW_TO_GET_MATCHES.md` for detailed examples.**

