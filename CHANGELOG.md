# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-11-02

### Added
- Initial release of Winamax Football Matches API
- Selenium-based Socket.IO traffic capture with stealth mode
- Auto-scrolling to capture all matches dynamically
- Flask REST API with comprehensive endpoints
- Filter by sport (sportId)
- Filter by date (DD-MM-YYYY format)
- Combined filters (sport + date)
- Simplified and verbose JSON output formats
- Analyzer tool for captured data
- Comprehensive documentation in English and French
- Project structure cleanup and organization

### Features
- 624 football matches captured with odds
- Bot detection bypass using selenium-stealth
- Real-time Socket.IO traffic monitoring
- RESTful API endpoints
- CORS enabled for web applications
- Complete match data with competitor names
- Support for live and upcoming matches

### Documentation
- README.md - Main project documentation
- README_FR.md - Documentation principale en français
- START_HERE.md - Quick start guide
- START_HERE_FR.md - Guide de démarrage rapide
- HOW_TO_GET_MATCHES.md - Complete usage guide
- HOW_TO_GET_MATCHES_FR.md - Guide complet
- API_ENDPOINTS.md - API reference
- API_ENDPOINTS_FR.md - Référence API
- PROJECT_COMPLETE.md - Project summary
- API_COMPLETE.md - API summary
- GET_MORE_MATCHES.md - Capture guide
- FINAL_ANSWER.md - Final summary
- FINAL_ANSWER_FR.md - Résumé final
- CLEAN_PROJECT_SUMMARY.md - Cleanup summary
- Technical documentation for Socket.IO analysis

### Technical
- Socket.IO v3 + Engine.IO v3 protocol support
- WebSocket transport for real-time data
- JSON data storage and retrieval
- Flask web framework
- Chrome DevTools Protocol integration
- Auto-scrolling for dynamic content loading

### Dependencies
- selenium==4.16.0
- selenium-stealth==1.0.6
- webdriver-manager==4.0.2
- flask==3.0.0
- flask-cors==4.0.0

## [1.1.0] - 2025-11-04

### Added
- **Background auto-capture** - Automatically captures fresh data every 30 minutes
- **Manual capture trigger** - `POST /api/capture/trigger` endpoint to trigger captures on demand
- **Capture status endpoint** - `GET /api/capture/status` to monitor capture status
- **Match sorting** - All matches automatically sorted by `matchStart` timestamp (earliest first)
- **Odds filter (morethan)** - Filter matches where both home & away odds are greater than a value
- **Odds range filter (anyonehas)** - Filter matches where any outcome (home/draw/away) has odds in a specific range
- Automatic data reload after each capture
- Capture progress monitoring

### Changed
- Updated match count to 630+ matches (after filtering)
- Improved data extraction reliability
- Enhanced error handling for capture operations

### Configuration
- `CAPTURE_INTERVAL_MINUTES = 30` - Configurable capture frequency
- `AUTO_CAPTURE_ENABLED = True` - Enable/disable auto-capture
- `CAPTURE_DURATION_SECONDS = 180` - Duration per capture

### Documentation
- Updated all documentation with new features
- Added examples for all new filters
- Added capture management documentation
- Updated match count and statistics

## [Unreleased]

### Planned
- Database storage option
- WebSocket real-time streaming
- Historical odds tracking
- Additional sports support
- Authentication and rate limiting

---

**Format**: [Semantic Versioning](https://semver.org/)

