"""
Winamax Football Matches API
Author: Anass EL
Description: Flask REST API to serve captured Winamax Socket.IO data with filters
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import threading
import time
from datetime import datetime, timezone
from analyze_winamax_socketio import SocketIOCapture

app = Flask(__name__)
CORS(app)

# Configuration
CAPTURE_INTERVAL_MINUTES = 30  # Default: capture every 30 minutes
AUTO_CAPTURE_ENABLED = True  # Enable/disable automatic capture
CAPTURE_DURATION_SECONDS = 180  # Duration for each capture (3 minutes)

# Global state
captured_data = {"messages": []}
capture_in_progress = False
last_capture_time = None
capture_thread = None

def load_captured_data():
    """Load captured data from JSON file (thread-safe)"""
    global captured_data
    try:
        # Small delay to ensure file is fully written
        time.sleep(0.5)
        
        with open('winamax_socketio_analysis.json', 'r', encoding='utf-8') as f:
            new_data = json.load(f)
            captured_data = new_data
            message_count = len(captured_data.get('messages', []))
            timestamp = captured_data.get('timestamp', 'Unknown')
            print(f"✓ Reloaded {message_count} messages from capture file (timestamp: {timestamp})")
            return True
    except FileNotFoundError:
        print("⚠ No capture file found. Starting with empty data. Run capture manually or wait for auto-capture.")
        captured_data = {"messages": []}
        return False
    except json.JSONDecodeError as e:
        print(f"⚠ Error parsing JSON file: {e} - File may be incomplete, keeping existing data")
        return False
    except Exception as e:
        print(f"⚠ Error loading data: {e} - Keeping existing data")
        return False

# Load data on startup
load_captured_data()


def run_capture():
    """Run Selenium capture in background and reload data"""
    global capture_in_progress, last_capture_time, captured_data
    
    if capture_in_progress:
        print("⚠ Capture already in progress, skipping...")
        return
    
    capture_in_progress = True
    print(f"\n{'='*80}")
    print(f"🔄 Starting automatic data capture...")
    print(f"{'='*80}")
    
    try:
        # Store previous message count for comparison
        previous_count = len(captured_data.get('messages', []))
        
        # Run Selenium capture (this saves to winamax_socketio_analysis.json)
        capture = SocketIOCapture()
        capture.run(duration=CAPTURE_DURATION_SECONDS)
        
        # Update timestamp
        last_capture_time = datetime.now().isoformat()
        
        # Reload fresh data from file (thread-safe)
        print("📥 Reloading fresh data from capture file...")
        reload_success = load_captured_data()
        
        if reload_success:
            new_count = len(captured_data.get('messages', []))
            diff = new_count - previous_count
            if diff > 0:
                print(f"✅ Data reloaded! {new_count} messages (+{diff} new)")
            elif diff < 0:
                print(f"✅ Data reloaded! {new_count} messages ({abs(diff)} fewer)")
            else:
                print(f"✅ Data reloaded! {new_count} messages (no change)")
        else:
            print("⚠ Data reload failed, but capture completed")
        
        print(f"{'='*80}\n")
        
    except Exception as e:
        print(f"❌ Error during capture: {e}")
        import traceback
        traceback.print_exc()
    finally:
        capture_in_progress = False


def background_capture_loop():
    """Background thread that periodically captures data"""
    global AUTO_CAPTURE_ENABLED
    
    # Wait for initial interval before first capture
    print(f"⏳ Background capture will start in {CAPTURE_INTERVAL_MINUTES} minutes...")
    
    while AUTO_CAPTURE_ENABLED:
        try:
            # Wait for the interval
            time.sleep(CAPTURE_INTERVAL_MINUTES * 60)
            
            if AUTO_CAPTURE_ENABLED:
                run_capture()
        except Exception as e:
            print(f"❌ Error in background capture loop: {e}")
            time.sleep(60)  # Wait 1 minute before retrying


def start_background_capture():
    """Start the background capture thread"""
    global capture_thread, AUTO_CAPTURE_ENABLED
    
    if AUTO_CAPTURE_ENABLED and capture_thread is None:
        print(f"🚀 Starting background capture task (interval: {CAPTURE_INTERVAL_MINUTES} minutes)")
        capture_thread = threading.Thread(target=background_capture_loop, daemon=True)
        capture_thread.start()
    elif not AUTO_CAPTURE_ENABLED:
        print("⚠ Automatic capture is disabled")


def extract_all_data_from_messages():
    """Extract all data from captured messages including matches, odds, outcomes, etc."""
    matches = {}
    odds = {}
    outcomes = {}
    bets = {}
    sports = {}
    
    for msg in captured_data.get('messages', []):
        if msg.get('event') == 'websocket_message':
            data = msg.get('data', {})
            if isinstance(data, dict) and 'raw' in data:
                raw = data['raw']
                if raw.startswith('42["m"'):
                    # Parse Socket.IO message
                    try:
                        # Extract JSON after "42["m","
                        json_part = raw.split('42["m",', 1)[1].rstrip(']')
                        parsed = json.loads(json_part)
                        
                        # Extract all data types
                        if isinstance(parsed, dict):
                            if 'matches' in parsed:
                                for match_id, match_data in parsed['matches'].items():
                                    if isinstance(match_data, dict):
                                        if match_id not in matches:
                                            matches[match_id] = match_data.copy()
                                        else:
                                            matches[match_id].update(match_data)
                            
                            if 'odds' in parsed:
                                odds.update(parsed['odds'])
                            
                            if 'outcomes' in parsed:
                                for outcome_id, outcome_data in parsed['outcomes'].items():
                                    if isinstance(outcome_data, dict):
                                        if outcome_id not in outcomes:
                                            outcomes[outcome_id] = outcome_data.copy()
                                        else:
                                            outcomes[outcome_id].update(outcome_data)
                            
                            if 'bets' in parsed:
                                for bet_id, bet_data in parsed['bets'].items():
                                    if isinstance(bet_data, dict):
                                        bets[bet_id] = bet_data.copy()
                            
                            if 'sports' in parsed:
                                sports.update(parsed['sports'])
                    except Exception as e:
                        pass
    
    return matches, odds, outcomes, bets, sports


@app.route('/')
def index():
    """API documentation"""
    return jsonify({
        'name': 'Winamax Data API',
        'version': '1.0.0',
        'auto_capture': {
            'enabled': AUTO_CAPTURE_ENABLED,
            'interval_minutes': CAPTURE_INTERVAL_MINUTES,
            'capture_in_progress': capture_in_progress,
            'last_capture': last_capture_time
        },
        'endpoints': {
            'GET /api/matches': 'Get all matches (simplified)',
            'GET /api/matches?sportId=1': 'Filter by sport (1=Football)',
            'GET /api/matches?date=DD-MM-YYYY': 'Filter by date',
            'GET /api/matches?morethan=2': 'Filter matches where both home & away odds > 2',
            'GET /api/matches?anyonehas=1.4': 'Filter matches where any outcome (home/draw/away) has odds 1.400-1.490',
            'GET /api/matches?sportId=1&date=DD-MM-YYYY&morethan=2&anyonehas=1.4': 'Combine filters',
            'GET /api/matches/verbose': 'Get all matches (full details)',
            'GET /api/matches/<id>': 'Get specific match',
            'GET /api/status': 'Get API status',
            'GET /api/info': 'Get capture information',
            'POST /api/capture/trigger': 'Manually trigger a capture',
            'GET /api/capture/status': 'Get capture status'
        }
    })


@app.route('/api/status')
def status():
    """Get API status"""
    return jsonify({
        'status': 'running',
        'messages_count': len(captured_data.get('messages', [])),
        'server': 'Winamax Data Server'
    })


@app.route('/api/info')
def info():
    """Get capture information"""
    return jsonify({
        'url': captured_data.get('url'),
        'timestamp': captured_data.get('timestamp'),
        'message_count': captured_data.get('message_count', 0),
        'last_capture_time': last_capture_time
    })


@app.route('/api/capture/status')
def capture_status():
    """Get capture status"""
    return jsonify({
        'auto_capture_enabled': AUTO_CAPTURE_ENABLED,
        'capture_in_progress': capture_in_progress,
        'interval_minutes': CAPTURE_INTERVAL_MINUTES,
        'last_capture_time': last_capture_time,
        'message_count': len(captured_data.get('messages', []))
    })


@app.route('/api/capture/trigger', methods=['POST'])
def trigger_capture():
    """Manually trigger a capture"""
    global capture_thread
    
    if capture_in_progress:
        return jsonify({
            'success': False,
            'message': 'Capture already in progress'
        }), 400
    
    # Start capture in background thread
    thread = threading.Thread(target=run_capture, daemon=True)
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Capture started in background'
    })


@app.route('/api/matches')
def get_matches():
    """Get all matches - simplified version"""
    matches, odds, outcomes, bets, sports = extract_all_data_from_messages()
    
    # Get filter parameters
    sport_id = request.args.get('sportId', type=int)
    date_filter = request.args.get('date')
    morethan = request.args.get('morethan', type=float)
    anyonehas = request.args.get('anyonehas', type=float)
    
    result = []
    for match_id, match_data in matches.items():
        # Filter by sport if specified
        if sport_id is not None:
            if match_data.get('sportId') != sport_id:
                continue
        
        # Skip if no competitor names (tournament/outright bets)
        if not match_data.get('competitor1Name') or not match_data.get('competitor2Name'):
            continue
        
        # Filter by date if specified
        if date_filter:
            match_start = match_data.get('matchStart')
            if match_start:
                match_date = datetime.fromtimestamp(match_start, tz=timezone.utc).strftime('%d-%m-%Y')
                if match_date != date_filter:
                    continue
        
        # Simplified match item with only essential fields
        match_item = {
            'matchId': match_id,
            'title': match_data.get('title'),
            'status': match_data.get('status'),
            'competitor1Name': match_data.get('competitor1Name'),
            'competitor2Name': match_data.get('competitor2Name'),
            'matchStart': match_data.get('matchStart')
        }
        
        # Try to find associated odds for this match
        match_odds = {}
        if 'mainBetId' in match_data:
            bet_id = str(match_data['mainBetId'])
            if bet_id in bets:
                bet = bets[bet_id]
                bet_outcomes = bet.get('outcomes', [])
                
                # Get simplified odds for each outcome
                for outcome_id in bet_outcomes:
                    outcome_id_str = str(outcome_id)
                    if outcome_id_str in odds:
                        outcome_info = outcomes.get(outcome_id_str, {})
                        label = outcome_info.get('label', f'Outcome {outcome_id}')
                        
                        match_odds[label] = odds[outcome_id_str]
                
                if match_odds:
                    match_item['odds'] = match_odds
        
        # Filter by morethan: both home and away odds must be > morethan
        if morethan is not None:
            competitor1_name = match_data.get('competitor1Name')
            competitor2_name = match_data.get('competitor2Name')
            
            # Find odds for home and away teams
            home_odds = None
            away_odds = None
            
            for label, odds_value in match_odds.items():
                if competitor1_name in label or label == competitor1_name:
                    home_odds = odds_value
                elif competitor2_name in label or label == competitor2_name:
                    away_odds = odds_value
            
            # Both odds must exist and be > morethan
            if home_odds is None or away_odds is None:
                continue
            if home_odds <= morethan or away_odds <= morethan:
                continue
        
        # Filter by anyonehas: check if ANY of the three main outcomes (home, draw, away) 
        # has odds in range [value, value+0.09]
        # Example: anyonehas=1.4 matches odds from 1.400 to 1.490 (inclusive)
        # Example match: home=3.0, draw=2.0, away=1.42 → INCLUDED (away 1.42 is in range 1.400-1.490)
        if anyonehas is not None:
            # Calculate the range: [value, value+0.09]
            # For anyonehas=1.4: range is [1.400, 1.490] inclusive
            min_odds = anyonehas
            max_odds = round(anyonehas + 0.09, 3)  # Ensure precision (e.g., 1.4 + 0.09 = 1.490)
            
            # Must have odds to check this filter
            if not match_odds:
                continue
            
            # Check if any of the three main outcomes (home, draw, away) has odds in range
            found_match = False
            competitor1_name = match_data.get('competitor1Name')
            competitor2_name = match_data.get('competitor2Name')
            
            for label, odds_value in match_odds.items():
                # Identify if this is home, draw, or away
                is_main_outcome = False
                
                # Home: matches competitor1Name
                if competitor1_name and (competitor1_name in label or label == competitor1_name):
                    is_main_outcome = True
                # Away: matches competitor2Name
                elif competitor2_name and (competitor2_name in label or label == competitor2_name):
                    is_main_outcome = True
                # Draw: contains "nul" or "Match nul" (French for draw)
                elif 'nul' in label.lower() or 'draw' in label.lower():
                    is_main_outcome = True
                
                # If it's a main outcome AND odds are in range, match found
                # Example: away odds = 1.42, range = [1.400, 1.490] → 1.400 <= 1.42 <= 1.490 → True
                if is_main_outcome and min_odds <= odds_value <= max_odds:
                    found_match = True
                    break
            
            # If no main outcome found in range, exclude this match
            if not found_match:
                continue
        
        result.append(match_item)
    
    # Sort matches by matchStart timestamp (ascending - earliest first)
    # Matches without matchStart go to the end
    # Secondary sort by matchId for matches with same timestamp
    result.sort(key=lambda x: (
        float(x.get('matchStart')) if x.get('matchStart') is not None else float('inf'),
        str(x.get('matchId', ''))
    ))
    
    return jsonify({
        'success': True,
        'matches': result,
        'count': len(result)
    })

@app.route('/api/matches/verbose')
def get_matches_verbose():
    """Get all matches with full details"""
    matches, odds, outcomes, bets, sports = extract_all_data_from_messages()
    
    # Get filter parameters
    sport_id = request.args.get('sportId', type=int)
    morethan = request.args.get('morethan', type=float)
    anyonehas = request.args.get('anyonehas', type=float)
    
    result = []
    for match_id, match_data in matches.items():
        # Filter by sport if specified
        if sport_id is not None:
            if match_data.get('sportId') != sport_id:
                continue
        
        # Skip if no competitor names (tournament/outright bets)
        if not match_data.get('competitor1Name') or not match_data.get('competitor2Name'):
            continue
        
        match_item = {
            'matchId': match_id,
            **match_data
        }
        
        # Try to find associated odds for this match
        match_odds = {}
        if 'mainBetId' in match_data:
            bet_id = str(match_data['mainBetId'])
            if bet_id in bets:
                bet = bets[bet_id]
                bet_outcomes = bet.get('outcomes', [])
                
                # Get odds for each outcome
                for outcome_id in bet_outcomes:
                    outcome_id_str = str(outcome_id)
                    if outcome_id_str in odds:
                        # Get outcome info if available
                        outcome_info = outcomes.get(outcome_id_str, {})
                        label = outcome_info.get('label', f'Outcome {outcome_id}')
                        
                        match_odds[label] = {
                            'odds': odds[outcome_id_str],
                            'outcomeId': outcome_id,
                            **outcome_info
                        }
                
                if match_odds:
                    match_item['odds'] = match_odds
        
        # Filter by morethan: both home and away odds must be > morethan
        if morethan is not None:
            competitor1_name = match_data.get('competitor1Name')
            competitor2_name = match_data.get('competitor2Name')
            
            # Find odds for home and away teams
            home_odds = None
            away_odds = None
            
            for label, odds_data in match_odds.items():
                # Handle both dict format (verbose) and numeric format
                if isinstance(odds_data, dict):
                    odds_value = odds_data.get('odds')
                else:
                    odds_value = odds_data
                
                if competitor1_name in label or label == competitor1_name:
                    home_odds = odds_value
                elif competitor2_name in label or label == competitor2_name:
                    away_odds = odds_value
            
            # Both odds must exist and be > morethan
            if home_odds is None or away_odds is None:
                continue
            if home_odds <= morethan or away_odds <= morethan:
                continue
        
        # Filter by anyonehas: check if ANY of the three main outcomes (home, draw, away) 
        # has odds in range [value, value+0.09]
        # Example: anyonehas=1.4 matches odds from 1.400 to 1.490 (inclusive)
        # Example match: home=3.0, draw=2.0, away=1.42 → INCLUDED (away 1.42 is in range 1.400-1.490)
        if anyonehas is not None:
            # Calculate the range: [value, value+0.09]
            # For anyonehas=1.4: range is [1.400, 1.490] inclusive
            min_odds = anyonehas
            max_odds = round(anyonehas + 0.09, 3)  # Ensure precision (e.g., 1.4 + 0.09 = 1.490)
            
            # Must have odds to check this filter
            if not match_odds:
                continue
            
            # Check if any of the three main outcomes (home, draw, away) has odds in range
            found_match = False
            competitor1_name = match_data.get('competitor1Name')
            competitor2_name = match_data.get('competitor2Name')
            
            for label, odds_data in match_odds.items():
                # Handle both dict format (verbose) and numeric format
                if isinstance(odds_data, dict):
                    odds_value = odds_data.get('odds')
                else:
                    odds_value = odds_data
                
                # Identify if this is home, draw, or away
                is_main_outcome = False
                
                # Home: matches competitor1Name
                if competitor1_name and (competitor1_name in label or label == competitor1_name):
                    is_main_outcome = True
                # Away: matches competitor2Name
                elif competitor2_name and (competitor2_name in label or label == competitor2_name):
                    is_main_outcome = True
                # Draw: contains "nul" or "Match nul" (French for draw)
                elif 'nul' in label.lower() or 'draw' in label.lower():
                    is_main_outcome = True
                
                # If it's a main outcome AND odds are in range, match found
                # Example: away odds = 1.42, range = [1.400, 1.490] → 1.400 <= 1.42 <= 1.490 → True
                if is_main_outcome and min_odds <= odds_value <= max_odds:
                    found_match = True
                    break
            
            # If no main outcome found in range, exclude this match
            if not found_match:
                continue
        
        # Add sport info if available
        if 'sportId' in match_data:
            sport_id_match = match_data['sportId']
            if sport_id_match in sports:
                match_item['sportInfo'] = sports[sport_id_match]
        
        result.append(match_item)
    
    # Sort matches by matchStart timestamp (ascending - earliest first)
    # Matches without matchStart go to the end
    # Secondary sort by matchId for matches with same timestamp
    result.sort(key=lambda x: (
        float(x.get('matchStart')) if x.get('matchStart') is not None else float('inf'),
        str(x.get('matchId', ''))
    ))
    
    return jsonify({
        'success': True,
        'matches': result,
        'count': len(result),
        'total_odds': len(odds),
        'total_outcomes': len(outcomes)
    })


@app.route('/api/matches/<match_id>')
def get_match(match_id):
    """Get specific match by ID with odds"""
    matches, odds, outcomes, bets, sports = extract_all_data_from_messages()
    
    if match_id in matches:
        match_data = matches[match_id].copy()
        match_data['matchId'] = match_id
        
        # Try to find associated odds
        if 'mainBetId' in match_data:
            bet_id = str(match_data['mainBetId'])
            if bet_id in bets:
                bet = bets[bet_id]
                bet_outcomes = bet.get('outcomes', [])
                
                match_odds = {}
                for outcome_id in bet_outcomes:
                    outcome_id_str = str(outcome_id)
                    if outcome_id_str in odds:
                        outcome_info = outcomes.get(outcome_id_str, {})
                        label = outcome_info.get('label', f'Outcome {outcome_id}')
                        match_odds[label] = {
                            'odds': odds[outcome_id_str],
                            'outcomeId': outcome_id,
                            **outcome_info
                        }
                
                if match_odds:
                    match_data['odds'] = match_odds
        
        return jsonify({
            'success': True,
            'match': match_data
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Match not found'
        }), 404


@app.route('/api/data/raw')
def get_raw_data():
    """Get raw captured data"""
    return jsonify(captured_data)


if __name__ == '__main__':
    print("Starting Winamax Data API...")
    print("="*80)
    print("Visit:")
    print("  http://localhost:5000/api/matches - Get all matches")
    print("  http://localhost:5000/api/status - Check status")
    print("  http://localhost:5000/api/info - Capture info")
    print("  http://localhost:5000/api/capture/status - Capture status")
    print("  POST http://localhost:5000/api/capture/trigger - Trigger capture")
    print("="*80)
    
    # Start background capture if enabled
    if AUTO_CAPTURE_ENABLED:
        start_background_capture()
    
    app.run(host='0.0.0.0', port=5000, debug=False)

