# Winamax Socket.IO Analyzed Endpoints

## WebSocket Connections

### Primary Socket.IO Endpoint
```
wss://sports-eu-west-3.winamax.fr/uof-sports-server/socket.io/?language=FR&version=3.26.0&embed=false&EIO=3&transport=websocket&sid={SESSION_ID}
```

**Parameters:**
- `language`: FR (French)
- `version`: 3.26.0
- `embed`: false
- `EIO`: 3 (Engine.IO version)
- `transport`: websocket
- `sid`: Dynamic session ID

**Server Information:**
- Host: sports-eu-west-3.winamax.fr
- Region: AWS eu-west-3 (Paris)
- CDN: CloudFront
- POP: MAD53-P4 (Madrid)

---

## Socket.IO Events

### Event: `m` (Market/Message Updates)
**Format:** `42["m", {data}]`

**Payload Structure:**
```json
{
  "sports": {...},      // Sports data with match listings
  "matches": {...},     // Match updates
  "outcomes": {...},    // Betting outcomes
  "odds": {...},        // Betting odds
  "bets": {...},        // Bet types
  "categories": {...},  // Bet categories
  "tournaments": {...}, // Tournament data
  "mainMatchCount": 958 // Total matches
}
```

**Sample Endpoints in Payload:**

#### Sports Data
```
wss://sports-eu-west-3.winamax.fr/uof-sports-server/socket.io/
  -> sports["1"].matches // List of 628 match IDs
```

#### Match Updates
```
wss://sports-eu-west-3.winamax.fr/uof-sports-server/socket.io/
  -> matches["{matchId}"] // Real-time match data
```

**Match ID Examples:**
- 61065927
- 64700620
- 58053075
- 61098835
- 56523887
- 61735836
- 61065929

#### Outcome Tracking
```
wss://sports-eu-west-3.winamax.fr/uof-sports-server/socket.io/
  -> outcomes["{outcomeId}"] // Betting outcome data
```

**Top Outcome IDs (by users):**
- 1652947390: 1,573 users
- 1641373671: 1,403 users
- 1639861626: 1,312 users
- 1653153505: 890 users
- 1653155843: 883 users

#### Odds Updates
```
wss://sports-eu-west-3.winamax.fr/uof-sports-server/socket.io/
  -> odds["{outcomeId}"] // Decimal odds value
```

**Sample Odds:**
- Outcome 1664709290: 1.58
- Outcome 1664709291: 3.35
- Outcome 1664745687: 2.75

---

## Engine.IO Protocol Messages

### Connection Handshake
```
Message: 2probe
Response: 3probe
Purpose: Connection probing
```

### Keepalive (Ping/Pong)
```
Client: 2
Server: 3
Frequency: ~every 25 seconds
Purpose: Connection keepalive
```

### Connection Upgrade
```
Message: 5
Purpose: Upgrade from polling to WebSocket confirmed
```

---

## Data Streams

### 1. Initial Data Stream
**Trigger:** On connection
**Content:**
- Sports overview (628 matches for football)
- Match listings
- Initial odds
- Bet types and categories
- Tournament data

### 2. Live Match Stream
**Trigger:** Continuous
**Update Frequency:** Every 1-3 seconds
**Content:**
- Match time progression
- Live scores
- Match status
- Period changes

**Sample Match Update:**
```json
{
  "61065927": {
    "matchtime": 75,
    "matchtimeExtended": "74:05",
    "matchtimeExtended": "74:56" // Updated every few seconds
  }
}
```

### 3. Odds Stream
**Trigger:** Real-time on change
**Content:**
- Odds changes
- Market updates
- Availability changes

**Sample Odds Update:**
```json
{
  "1664709290": 1.56,  // Changed from 1.58
  "1664709291": 3.35   // Unchanged
}
```

### 4. Hot Outcomes Stream
**Trigger:** Frequent updates
**Content:**
- User tracking counts
- Popular bets
- Trend indicators

**Sample Hot Outcome:**
```json
{
  "1652947390": {
    "icon": "TXd-N_bP",
    "hotUsers": 1573
  }
}
```

### 5. Match Metadata Stream
**Trigger:** On changes
**Content:**
- Filter updates
- More bets availability
- Match flags (isHot, isBooked)
- Highlights availability

---

## API Structure Summary

### Connection Layer
- **Protocol:** Socket.IO v3
- **Transport:** WebSocket (WSS)
- **Engine:** Engine.IO v3
- **Server:** sports-eu-west-3.winamax.fr

### Data Model
- **Sports:** Organizing matches by sport
- **Matches:** Individual match data
- **Outcomes:** Betting options
- **Odds:** Pricing data
- **Bets:** Bet type definitions
- **Categories:** Betting categories
- **Tournaments:** Competition data

### Update Types
1. **Bulk Load:** Initial data on connection
2. **Delta Updates:** Only changed fields
3. **Real-time:** Continuous updates
4. **Event-driven:** On specific triggers

---

## Security Headers

**Request Headers:**
```
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Cache-Control: no-cache
Connection: Upgrade
Host: sports-eu-west-3.winamax.fr
Origin: https://www.winamax.fr
Pragma: no-cache
Sec-WebSocket-Extensions: permessage-deflate; client_max_window_bits
Sec-WebSocket-Key: {dynamic}
Sec-WebSocket-Version: 13
Upgrade: websocket
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
```

**Response Headers:**
```
Access-Control-Allow-Credentials: true
Access-Control-Allow-Origin: https://www.winamax.fr
Connection: upgrade
Date: {timestamp}
Sec-WebSocket-Accept: {key}
Upgrade: websocket
Vary: Origin
Via: 1.1 {cloudfront}.cloudfront.net (CloudFront)
X-Cache: Miss from cloudfront
X-Amz-Cf-Pop: MAD53-P4
Alt-Svc: h3=":443"; ma=86400
```

---

## WebSocket URL Patterns

### Main Pattern
```
wss://sports-eu-west-3.winamax.fr/uof-sports-server/socket.io/
```

### Query Parameters
- `language`: Language code (FR, EN, etc.)
- `version`: API version (3.26.0)
- `embed`: Embed mode (false)
- `EIO`: Engine.IO version (3)
- `transport`: Transport type (websocket)
- `sid`: Session identifier (dynamic)

### Full Example
```
wss://sports-eu-west-3.winamax.fr/uof-sports-server/socket.io/?language=FR&version=3.26.0&embed=false&EIO=3&transport=websocket&sid=BYWalRJIk-HLMALHAsEa
```

---

## Connection Flow

1. **Initial Request:** GET to Socket.IO endpoint
2. **Session Creation:** Server assigns session ID
3. **Upgrade to WebSocket:** Transport upgrade
4. **Handshake Probe:** `2probe` / `3probe`
5. **Connection Confirmed:** `5` message
6. **Data Streaming:** Continuous `m` events
7. **Keepalive:** Regular ping/pong
8. **Close:** On disconnect

---

## Summary

**Total Analyzed:**
- 1 Primary WebSocket endpoint
- 1 Main event type (`m`)
- 5 Data stream types
- 69 Total messages captured
- 27 Parsed Socket.IO messages
- 7 Unique matches tracked
- 101 Outcomes monitored

**Data Volume:**
- 628 Total football matches
- 12 Odds updated in 60 seconds
- 1,573 Peak concurrent viewers on single outcome

**Protocol:**
- Push-only architecture
- Delta update strategy
- Low latency real-time delivery
- Scalable via Socket.IO clusters

