# Documentation API Winamax

## Serveur API Fonctionnel

**Fichier :** `serve_data.py` - Sert les données Socket.IO capturées  
**Statut :** ✅ **FONCTIONNEL**  
**Port :** 5000

## Endpoints Disponibles

### GET `/api/matches`
**Description :** Obtenir tous les matches de football avec cotes (simplifié)

**Paramètres de Requête :**
- `sportId` (optionnel) : Filtrer par ID sport (1=Football)
- `date` (optionnel) : Filtrer par date (format : DD-MM-YYYY)

**Réponse :**
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

**Utilisation :**
```bash
# Tous les matches
curl http://localhost:5000/api/matches

# Filtrer par football
curl http://localhost:5000/api/matches?sportId=1

# Filtrer par date
curl http://localhost:5000/api/matches?date=15-11-2025

# Filtres combinés
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025
```

### GET `/api/matches/verbose`
**Description :** Obtenir tous les matches avec détails complets

**Paramètres de Requête :**
- `sportId` (optionnel) : Filtrer par ID sport (1=Football)

**Réponse :** Données de match complètes incluant toutes les métadonnées

**Utilisation :**
```bash
curl http://localhost:5000/api/matches/verbose
curl http://localhost:5000/api/matches/verbose?sportId=1
```

### GET `/api/matches/<match_id>`
**Description :** Obtenir un match spécifique par ID

**Exemple :**
```bash
curl http://localhost:5000/api/matches/56418335
```

**Réponse :**
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
**Description :** Obtenir le statut de l'API

**Réponse :**
```json
{
  "status": "running",
  "messages_count": 155,
  "server": "Winamax Data Server"
}
```

### GET `/api/info`
**Description :** Obtenir les informations de capture

**Réponse :**
```json
{
  "url": "https://www.winamax.fr/paris-sportifs/sports/1",
  "timestamp": "2025-11-02T03:46:59.686006",
  "message_count": 155
}
```

### GET `/api/data/raw`
**Description :** Obtenir les données brutes complètes capturées

## Démarrage Rapide

1. **Démarrer le serveur :**
```bash
python serve_data.py
```

2. **Obtenir les matches :**
```bash
# Avec curl
curl http://localhost:5000/api/matches

# Avec Python
import requests
response = requests.get('http://localhost:5000/api/matches')
print(response.json())
```

3. **Obtenir un match spécifique :**
```bash
curl http://localhost:5000/api/matches/56418335
```

## Structure des Données de Match

### Format Simplifié (par défaut)
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

### Format Verbose
Données de match complètes incluant toutes les métadonnées, résultats, paris, etc.

## Jeu de Données Actuel

- **624 matches de football** avec noms des équipes et cotes
- **155 messages** capturés
- Données de capture avec défilement automatique
- Tous les matches incluent des données de cotes

## Pour des Données Fraîches

Utiliser l'outil de capture Selenium :
```bash
# Capturer pendant 120 secondes avec défilement auto
python analyze_winamax_socketio.py 120
```

Puis redémarrer le serveur API pour charger les nouvelles données :
```bash
python serve_data.py
```

## Exemples de Filtres

```bash
# Football uniquement
curl http://localhost:5000/api/matches?sportId=1

# Date spécifique
curl http://localhost:5000/api/matches?date=15-11-2025

# Football sur une date spécifique
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025
```

