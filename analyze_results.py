"""
Analyze Winamax Socket.IO captured data
Author: Anass EL
Description: Analyzes and summarizes captured Socket.IO data
"""
import json
from collections import Counter
from datetime import datetime

# Load the captured data
with open('winamax_socketio_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("="*100)
print("WINAMAX SOCKET.IO DETAILED ANALYSIS")
print("="*100)

# Basic statistics
print(f"\n[*] BASIC STATISTICS")
print(f"-" * 100)
print(f"URL: {data['url']}")
print(f"Capture timestamp: {data['timestamp']}")
print(f"Total messages captured: {data['message_count']}")

# WebSocket connection details
websocket_messages = [msg for msg in data['messages'] if msg.get('event') == 'websocket_open']
if websocket_messages:
    ws_url = websocket_messages[0]['data']['url']
    print(f"\n[*] WEBSOCKET CONNECTION")
    print(f"-" * 100)
    print(f"WebSocket URL: {ws_url}")
    print(f"\nConnection Details:")
    print(f"  - Protocol: Socket.IO v3")
    print(f"  - Engine.IO version: 3")
    print(f"  - Transport: WebSocket")
    print(f"  - Server: sports-eu-west-3.winamax.fr")
    print(f"  - Language: French (FR)")
    print(f"  - Version: 3.26.0")

# Message types
print(f"\n[*] MESSAGE TYPES")
print(f"-" * 100)
event_counts = Counter(msg.get('event', 'unknown') for msg in data['messages'])
for event, count in event_counts.most_common():
    print(f"  {event}: {count}")

# Parse Socket.IO messages (event 'm' with data)
socket_messages = []
for msg in data['messages']:
    if msg.get('event') == 'websocket_message':
        # Check if data is a dict before calling get
        data_obj = msg.get('data')
        if isinstance(data_obj, dict):
            raw_data = data_obj.get('raw', '')
            if raw_data.startswith('42["m"'):
                try:
                    # Parse Socket.IO packet: 42["m",{...}]
                    import json as json_lib
                    # Extract the JSON part after "42["m","
                    json_part = raw_data.split('42["m",', 1)[1].rstrip(']')
                    parsed = json_lib.loads(json_part)
                    socket_messages.append({
                        'timestamp': msg['timestamp'],
                        'data': parsed
                    })
                except Exception as e:
                    pass

print(f"\n[*] SOCKET.IO DATA MESSAGES")
print(f"-" * 100)
print(f"Total parsed Socket.IO 'm' messages: {len(socket_messages)}")

if socket_messages:
    # Analyze structure
    print(f"\n[*] MESSAGE STRUCTURE ANALYSIS")
    print(f"-" * 100)
    
    # Collect all keys from all messages
    all_keys = set()
    for msg in socket_messages:
        if isinstance(msg['data'], dict):
            all_keys.update(msg['data'].keys())
    
    print(f"\nTop-level keys in Socket.IO messages:")
    for key in sorted(all_keys):
        key_count = sum(1 for msg in socket_messages if isinstance(msg['data'], dict) and key in msg['data'])
        print(f"  - {key}: appears in {key_count} messages")
    
    # Analyze specific sections
    print(f"\n[*] SPORTS DATA ANALYSIS")
    print(f"-" * 100)
    
    sports_messages = [msg for msg in socket_messages if 'sports' in msg['data']]
    if sports_messages:
        sports_data = sports_messages[0]['data']['sports']
        for sport_id, sport_info in sports_data.items():
            print(f"\nSport ID {sport_id} (likely Football/Soccer):")
            if 'mainMatchCount' in sport_info:
                print(f"  - Total matches: {sport_info['mainMatchCount']}")
            if 'matches' in sport_info:
                print(f"  - Match IDs listed: {len(sport_info['matches'])}")
                print(f"  - Sample match IDs: {sport_info['matches'][:10]}")
    
    print(f"\n[*] MATCH UPDATES")
    print(f"-" * 100)
    
    match_updates = [msg for msg in socket_messages if 'matches' in msg['data'] and 'sports' not in msg['data']]
    print(f"Live match updates: {len(match_updates)} messages")
    
    if match_updates:
        # Collect unique match IDs
        match_ids = set()
        for msg in match_updates:
            for match_id in msg['data']['matches'].keys():
                match_ids.add(match_id)
        
        print(f"  - Unique matches updated: {len(match_ids)}")
        
        # Show sample match update
        if match_updates:
            sample = match_updates[0]['data']['matches']
            print(f"\nSample match update structure:")
            for match_id, match_data in list(sample.items())[:2]:
                print(f"  Match ID {match_id}:")
                if isinstance(match_data, dict):
                    for key, value in match_data.items():
                        print(f"    - {key}: {value}")
    
    print(f"\n[*] ODDS UPDATES")
    print(f"-" * 100)
    
    odds_messages = [msg for msg in socket_messages if 'odds' in msg['data']]
    print(f"Odds update messages: {len(odds_messages)}")
    
    if odds_messages:
        # Collect all odds
        all_odds = []
        for msg in odds_messages:
            if 'odds' in msg['data']:
                for outcome_id, odds_value in msg['data']['odds'].items():
                    all_odds.append((outcome_id, odds_value))
        
        print(f"  - Total odds updated: {len(all_odds)}")
        if all_odds:
            print(f"  - Sample odds:")
            for outcome_id, odds_value in all_odds[:5]:
                print(f"    Outcome {outcome_id}: {odds_value}")
    
    print(f"\n[*] HOT OUTCOMES")
    print(f"-" * 100)
    
    hot_outcomes = []
    for msg in socket_messages:
        if 'outcomes' in msg['data']:
            for outcome_id, outcome_data in msg['data']['outcomes'].items():
                if isinstance(outcome_data, dict) and 'hotUsers' in outcome_data:
                    hot_users = outcome_data['hotUsers']
                    if hot_users:
                        hot_outcomes.append((outcome_id, hot_users, msg['timestamp']))
    
    # Sort by hot users
    hot_outcomes.sort(key=lambda x: x[1] if isinstance(x[1], int) else 0, reverse=True)
    print(f"Hot outcomes tracked: {len(hot_outcomes)}")
    if hot_outcomes:
        print(f"  - Top 10 hottest outcomes:")
        for outcome_id, hot_users, timestamp in hot_outcomes[:10]:
            print(f"    Outcome {outcome_id}: {hot_users} users at {timestamp}")

print(f"\n[*] KEY FINDINGS")
print(f"-" * 100)
print(f"""
1. WEB SOCKET PROTOCOL:
   - Winamax uses Socket.IO v3 over WebSocket
   - Connection maintained at: wss://sports-eu-west-3.winamax.fr/uof-sports-server/socket.io/
   - Transport uses Engine.IO v3 protocol

2. MESSAGE FORMAT:
   - Main event type: 'm' (market/message updates)
   - Messages sent as: 42["m", {{data}}]
   - Real-time updates push-only (server to client)

3. DATA STRUCTURE:
   - Sports data with match listings
   - Live match updates (time, scores, etc.)
   - Odds updates for betting outcomes
   - Hot outcomes (users tracking specific bets)
   - Match filters and metadata

4. UPDATE FREQUENCY:
   - Live odds updated in real-time
   - Match time updated every few seconds
   - Sports overview pushed initially and on major changes
   - Hot user counts updated frequently

5. SECURITY:
   - WebSocket uses session ID (sid) in URL
   - CORS configured for https://www.winamax.fr
   - Access-Control-Allow-Credentials enabled

6. INFRASTRUCTURE:
   - Hosted on AWS (eu-west-3 region)
   - CloudFront CDN in front
   - Server location: Madrid (MAD53-P4)
""")

print("="*100)
print("Analysis complete!")
print("="*100)

