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
- `morethan` (optionnel) : Filtrer les matches où les cotes domicile ET extérieur > valeur (ex: `morethan=2`)
- `anyonehas` (optionnel) : Filtrer les matches où un résultat (domicile/match nul/extérieur) a des cotes dans la plage [valeur, valeur+0.09] (ex: `anyonehas=1.4` correspond aux cotes 1.400-1.490)

**Note :** Les matches sont automatiquement triés par timestamp `matchStart` (les plus anciens en premier).

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

# Filtrer par cotes (domicile ET extérieur > 2)
curl http://localhost:5000/api/matches?morethan=2

# Filtrer par plage de cotes (tout résultat 1.400-1.490)
curl http://localhost:5000/api/matches?anyonehas=1.4

# Combiner tous les filtres
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025&morethan=2&anyonehas=1.4
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
  "message_count": 155,
  "last_capture_time": "2025-11-04T17:52:27.736042"
}
```

### GET `/api/capture/status`
**Description :** Obtenir le statut de la capture en arrière-plan

**Réponse :**
```json
{
  "auto_capture_enabled": true,
  "capture_in_progress": false,
  "interval_minutes": 30,
  "last_capture_time": "2025-11-04T17:52:27.736042",
  "message_count": 157
}
```

### POST `/api/capture/trigger`
**Description :** Déclencher manuellement une capture de données fraîches

**Utilisation :**
```bash
curl -X POST http://localhost:5000/api/capture/trigger
```

**Réponse :**
```json
{
  "success": true,
  "message": "Capture started in background"
}
```

**Note :** La capture s'exécute en arrière-plan (prend ~3 minutes). Utilisez `/api/capture/status` pour surveiller la progression.

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

- **630+ matches de football** avec noms des équipes et cotes
- **157 messages** capturés
- Données de capture avec défilement automatique
- Tous les matches incluent des données de cotes
- **Matches automatiquement triés par heure de début**

## Actualisation Automatique des Données

L'API capture automatiquement des données fraîches toutes les 1 minute en arrière-plan. Aucune intervention manuelle nécessaire !

**Configuration** (dans `serve_data.py`) :
- `CAPTURE_INTERVAL_MINUTES = 1` - Modifier la fréquence de capture (par défaut : 1 minute)
- `AUTO_CAPTURE_ENABLED = True` - Activer/désactiver la capture automatique
- `CAPTURE_DURATION_SECONDS = 180` - Durée par capture (3 minutes)

**Note :** Selenium s'exécute en mode headless (sans fenêtre de navigateur visible) pour de meilleures performances et compatibilité serveur.

**Capture Manuelle :**
```bash
# Déclencher une capture immédiatement
curl -X POST http://localhost:5000/api/capture/trigger

# Vérifier le statut de la capture
curl http://localhost:5000/api/capture/status
```

**Capture Manuelle (Ancienne Méthode) :**
```bash
# Capturer pendant 180 secondes avec défilement auto
python analyze_winamax_socketio.py

# Puis redémarrer le serveur API (pas nécessaire avec la capture auto)
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

# Matches où les cotes domicile ET extérieur > 2
curl http://localhost:5000/api/matches?morethan=2

# Matches où un résultat a des cotes 1.400-1.490
curl http://localhost:5000/api/matches?anyonehas=1.4

# Matches de football avec les deux cotes > 2
curl http://localhost:5000/api/matches?sportId=1&morethan=2

# Combiner tous les filtres
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025&morethan=2&anyonehas=1.4
```

## Tri des Matches

Tous les matches sont automatiquement triés par timestamp `matchStart` en ordre croissant (matches les plus anciens en premier). Les matches sans timestamp sont placés à la fin.

