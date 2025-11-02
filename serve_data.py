"""
Winamax Football Matches API
Author: Anass EL
Description: Flask REST API to serve captured Winamax Socket.IO data with filters
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

# Load captured data
try:
    with open('winamax_socketio_analysis.json', 'r', encoding='utf-8') as f:
        captured_data = json.load(f)
except Exception as e:
    print(f"Error loading data: {e}")
    captured_data = {"messages": []}


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
        'endpoints': {
            'GET /api/matches': 'Get all matches (simplified)',
            'GET /api/matches?sportId=1': 'Filter by sport (1=Football)',
            'GET /api/matches?date=DD-MM-YYYY': 'Filter by date',
            'GET /api/matches?sportId=1&date=DD-MM-YYYY': 'Filter by sport + date',
            'GET /api/matches/verbose': 'Get all matches (full details)',
            'GET /api/matches/<id>': 'Get specific match',
            'GET /api/status': 'Get API status',
            'GET /api/info': 'Get capture information'
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
        'message_count': captured_data.get('message_count', 0)
    })


@app.route('/api/matches')
def get_matches():
    """Get all matches - simplified version"""
    matches, odds, outcomes, bets, sports = extract_all_data_from_messages()
    
    # Get filter parameters
    sport_id = request.args.get('sportId', type=int)
    date_filter = request.args.get('date')
    
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
        if 'mainBetId' in match_data:
            bet_id = str(match_data['mainBetId'])
            if bet_id in bets:
                bet = bets[bet_id]
                bet_outcomes = bet.get('outcomes', [])
                
                # Get simplified odds for each outcome
                match_odds = {}
                for outcome_id in bet_outcomes:
                    outcome_id_str = str(outcome_id)
                    if outcome_id_str in odds:
                        outcome_info = outcomes.get(outcome_id_str, {})
                        label = outcome_info.get('label', f'Outcome {outcome_id}')
                        
                        match_odds[label] = odds[outcome_id_str]
                
                if match_odds:
                    match_item['odds'] = match_odds
        
        result.append(match_item)
    
    return jsonify({
        'success': True,
        'matches': result,
        'count': len(result)
    })

@app.route('/api/matches/verbose')
def get_matches_verbose():
    """Get all matches with full details"""
    matches, odds, outcomes, bets, sports = extract_all_data_from_messages()
    
    # Get filter parameter
    sport_id = request.args.get('sportId', type=int)
    
    result = []
    for match_id, match_data in matches.items():
        # Filter by sport if specified
        if sport_id is not None:
            if match_data.get('sportId') != sport_id:
                continue
        
        match_item = {
            'matchId': match_id,
            **match_data
        }
        
        # Try to find associated odds for this match
        if 'mainBetId' in match_data:
            bet_id = str(match_data['mainBetId'])
            if bet_id in bets:
                bet = bets[bet_id]
                bet_outcomes = bet.get('outcomes', [])
                
                # Get odds for each outcome
                match_odds = {}
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
        
        # Add sport info if available
        if 'sportId' in match_data:
            sport_id = match_data['sportId']
            if sport_id in sports:
                match_item['sportInfo'] = sports[sport_id]
        
        result.append(match_item)
    
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
    print("="*80)
    app.run(host='0.0.0.0', port=5000, debug=False)

