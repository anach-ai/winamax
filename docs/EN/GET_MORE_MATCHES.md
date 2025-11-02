# How to Get More Matches

## Current Status

The current capture has **624 football matches** with odds! This was achieved using:
1. **Auto-scrolling** to trigger lazy loading
2. **Longer capture** duration (120+ seconds)
3. Capturing complete match data with competitor names

## Solution: Run a Longer Capture

To get more complete match data:

```bash
# Capture for 2 minutes (120 seconds)
python analyze_winamax_socketio.py 120
```

This will:
- Capture more Socket.IO messages
- Get more complete match data with odds
- Save to `winamax_socketio_analysis.json`

Then restart the API:

```bash
# Stop current server (Ctrl+C)
python serve_data.py
```

## Quick Capture

Just run the capture directly:

```bash
python analyze_winamax_socketio.py 300
```

## What You'll Get

With a longer capture (120+ seconds) **with auto-scrolling**, you should get:
- **600+ complete matches** with full details
- **Team names, dates, status** for each match
- **Odds data** for all matches
- **More comprehensive data**

**Latest capture**: 624 football matches, all with odds!

## Alternative: Use Different Sports

You can also capture data for different sports:

1. Edit `analyze_winamax_socketio.py` line 46:
   ```python
   self.url = "https://www.winamax.fr/paris-sportifs/sports/4"  # Tennis
   self.url = "https://www.winamax.fr/paris-sportifs/sports/2"  # Basketball
   ```

2. Run the capture:
   ```bash
   python analyze_winamax_socketio.py 120
   ```

## Recommended Settings

For best results:
- **Duration**: 120-300 seconds (2-5 minutes)
- **Sports**: Football (sport 1) for most matches
- **Time of day**: Peak hours have more live matches

## Tips

1. Run captures during peak match times (evenings in Europe)
2. Capture for at least 2 minutes to get full data
3. Multiple short captures can be combined
4. The API will automatically parse all captured data

