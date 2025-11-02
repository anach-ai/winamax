# Winamax Socket.IO Traffic Analysis Summary

## Overview
Successfully captured and analyzed Socket.IO traffic from Winamax sports betting website using Selenium with stealth technology.

## Connection Details

**WebSocket Endpoint:**
```
wss://sports-eu-west-3.winamax.fr/uof-sports-server/socket.io/
```

**Connection Parameters:**
- Protocol: Socket.IO v3
- Engine.IO version: 3
- Transport: WebSocket
- Language: French (FR)
- Version: 3.26.0
- Session ID: Generated dynamically on connection

**Infrastructure:**
- Server: AWS eu-west-3 (Paris region)
- CDN: CloudFront
- POP Location: Madrid (MAD53-P4)

## Message Protocol

**Format:**
```
42["m", {data}]
```
- `42`: Socket.IO packet type (event with data)
- `"m"`: Event name (market/message updates)
- `{data}`: JSON object with market data

**Engine.IO Control Messages:**
- `2probe` / `3probe`: Connection probing
- `2` / `3`: Ping/pong for keepalive
- `5`: Connection upgrade confirmation

## Data Structure

### 1. Sports Data
```json
{
  "sports": {
    "1": {
      "mainMatchCount": 628,
      "matches": [64692546, 64700620, ...]
    }
  }
}
```
- Sport ID 1 = Football/Soccer
- Total matches: 628
- Lists all match IDs for the sport

### 2. Match Updates
```json
{
  "matches": {
    "61065927": {
      "matchtime": 75,
      "matchtimeExtended": "74:05",
      "isHot": true
    }
  }
}
```
- Live time tracking
- Match status indicators
- Hot match flags

### 3. Odds Updates
```json
{
  "odds": {
    "1664709290": 1.58,
    "1664709291": 3.35
  }
}
```
- Real-time betting odds
- Decimal format
- Outcome IDs

### 4. Outcomes
```json
{
  "outcomes": {
    "1652947390": {
      "icon": "TXd-N_bP",
      "hotUsers": 1573
    }
  }
}
```
- Betting option identifiers
- Icons for teams/outcomes
- "Hot users" count (users tracking this outcome)

### 5. Filters
```json
{
  "moreBets": 227,
  "filters": [1, 2, 4, 5, 6, ...]
}
```
- Available bet types
- Filter categories

## Real-Time Updates

**Update Frequency:**
- Initial bulk data load on connection
- Live odds: Continuous (real-time)
- Match time: Every 1-3 seconds
- Hot outcomes: Frequently updated
- Sports overview: On major changes

**Message Statistics (60 second capture):**
- Total messages: 69
- Socket.IO data messages: 27
- Matches updated: 7 unique
- Odds updated: 12 outcomes
- Hot outcomes tracked: 101

## Top Hot Outcomes

Most tracked betting outcomes during capture:
1. Outcome 1652947390: 1,573 users
2. Outcome 1641373671: 1,403 users
3. Outcome 1639861626: 1,312 users
4. Outcome 1653153505: 890 users
5. Outcome 1653155843: 883 users

## Security & Authentication

- **CORS:** Configured for https://www.winamax.fr
- **Credentials:** Enabled (cookies/auth)
- **Session:** Managed via session ID in URL
- **SSL/TLS:** WebSocket over WSS

## Technical Implementation

**Captured using:**
- Selenium with Chrome driver
- selenium-stealth for anti-bot bypass
- WebDriver Manager for automatic driver management
- Chrome DevTools Protocol for network logging
- JavaScript injection for Socket.IO interception

**Detection bypass techniques:**
- Disabled automation flags
- Custom user agent
- Stealth browser fingerprinting
- WebGL vendor spoofing

## Sample Data Flow

1. **Initial Connection:**
   - WebSocket handshake
   - Session ID assigned
   - Authentication (if logged in)

2. **Bulk Data Load:**
   - Sports overview
   - Match listings
   - Initial odds
   - Filters and categories

3. **Real-Time Updates:**
   - Match time progression
   - Odds changes
   - Hot user counts
   - Match status updates

4. **Keepalive:**
   - Ping/pong every ~25 seconds
   - Connection monitoring

## Use Cases

This Socket.IO stream provides:
1. **Live Betting Data:** Real-time odds and outcomes
2. **Match Tracking:** Live scores, times, status
3. **Market Intelligence:** Popular bets (hot outcomes)
4. **Betting Options:** Available filters and bet types
5. **Sports Data:** Comprehensive match listings

## Files Generated

- `winamax_socketio_analysis.json`: Complete captured data
- `winamax_socketio.log`: Execution log
- `analyze_winamax_socketio.py`: Capture script
- `analyze_results.py`: Analysis script
- `SOCKET_IO_ANALYSIS_SUMMARY.md`: This summary

## Key Insights

1. **Push-Only Protocol:** Server pushes updates, client doesn't request data
2. **Efficient Updates:** Delta updates (only changed data)
3. **High Frequency:** Odds update in near real-time
4. **Scalable:** Uses standard Socket.IO for reliability
5. **Modern Infrastructure:** AWS with global CDN

## Conclusion

Winamax uses a sophisticated real-time data streaming system based on Socket.IO v3, providing live sports betting data with low latency. The protocol efficiently delivers match updates, odds changes, and social indicators (hot users) to keep bettors informed of the latest betting opportunities.

