# Comment Obtenir les Matches de Football avec Cotes - Guide Complet

## ✅ SOLUTION FONCTIONNELLE

Utilisez `serve_data.py` - Une API Flask qui sert les données Socket.IO Winamax capturées.

## Démarrage Rapide

### 1. Démarrer le Serveur

```bash
python serve_data.py
```

Le serveur sera accessible sur : `http://localhost:5000`

### 2. Obtenir les Matches

**Avec cURL :**
```bash
curl http://localhost:5000/api/matches
```

**Avec Python :**
```python
import requests
response = requests.get('http://localhost:5000/api/matches')
matches = response.json()
print(f"Trouvé {matches['count']} matches")
```

**Avec JavaScript :**
```javascript
fetch('http://localhost:5000/api/matches')
    .then(res => res.json())
    .then(data => console.log(data.matches));
```

### 3. Exemple de Résultat

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

## Endpoints Disponibles

| Endpoint | Méthode | Description |
|----------|--------|-------------|
| `/api/matches` | GET | Obtenir tous les matches (simplifié, triés par heure) |
| `/api/matches?sportId=1` | GET | Filtrer par sport (1=Football) |
| `/api/matches?date=DD-MM-YYYY` | GET | Filtrer par date |
| `/api/matches?morethan=2` | GET | Filtrer où les deux cotes > 2 |
| `/api/matches?anyonehas=1.4` | GET | Filtrer où un résultat a des cotes 1.400-1.490 |
| `/api/matches?sportId=1&date=DD-MM-YYYY&morethan=2&anyonehas=1.4` | GET | Combiner tous les filtres |
| `/api/matches/verbose` | GET | Obtenir tous les matches (détails complets) |
| `/api/matches/<id>` | GET | Obtenir un match spécifique |
| `/api/status` | GET | Statut du serveur |
| `/api/info` | GET | Informations de capture |
| `/api/capture/status` | GET | Statut de la capture en arrière-plan |
| `/api/capture/trigger` | POST | Déclencher manuellement une capture |
| `/api/data/raw` | GET | Données brutes |

## Exemples d'IDs de Match

- `56418335` - Slovénie vs Kosovo
- `56418336` - Suisse vs Suède  
- `56418337` - Luxembourg vs Allemagne
- `56418338` - Slovaquie vs Irlande du Nord
- `56418339` - Grèce vs Écosse

## Utilisation Avancée

### Filtrer par Sport

```python
import requests

# Obtenir uniquement les matches de football (sportId=1)
response = requests.get('http://localhost:5000/api/matches?sportId=1')
data = response.json()
print(f"Matches de football : {data['count']}")
```

### Filtrer par Date

```python
import requests

# Obtenir les matches pour une date spécifique (format DD-MM-YYYY)
response = requests.get('http://localhost:5000/api/matches?date=15-11-2025')
data = response.json()
print(f"Matches du 15-11-2025 : {data['count']}")
```

### Filtrer par Sport + Date

```python
import requests

# Obtenir les matches de football pour une date spécifique
response = requests.get('http://localhost:5000/api/matches?sportId=1&date=15-11-2025')
data = response.json()
print(f"Matches de football du 15-11-2025 : {data['count']}")
```

### Filtrer par Cotes (morethan)

```python
import requests

# Obtenir les matches où les cotes domicile ET extérieur sont supérieures à 2
response = requests.get('http://localhost:5000/api/matches?morethan=2')
data = response.json()
print(f"Matches avec les deux cotes > 2 : {data['count']}")
```

### Filtrer par Plage de Cotes (anyonehas)

```python
import requests

# Obtenir les matches où un résultat (domicile/match nul/extérieur) a des cotes dans la plage 1.400-1.490
response = requests.get('http://localhost:5000/api/matches?anyonehas=1.4')
data = response.json()
print(f"Matches avec cotes dans la plage 1.4-1.49 : {data['count']}")
```

### Combiner Tous les Filtres

```python
import requests

# Obtenir les matches de football sur une date spécifique avec les deux cotes > 2 et un résultat dans la plage 1.4-1.49
response = requests.get('http://localhost:5000/api/matches?sportId=1&date=15-11-2025&morethan=2&anyonehas=1.4')
data = response.json()
print(f"Matches filtrés : {data['count']}")
```

### Obtenir un Match Spécifique

```python
match_id = "56418335"
response = requests.get(f'http://localhost:5000/api/matches/{match_id}')
match = response.json()['match']

print(f"Match : {match['competitor1Name']} vs {match['competitor2Name']}")
print(f"Statut : {match['status']}")
print(f"Cotes : {match.get('odds', {})}")
```

## Structure des Données

### Objet Match Simplifié
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

## Actualisation Automatique des Données

L'API **capture automatiquement des données fraîches toutes les 30 minutes** en arrière-plan. Aucune intervention manuelle nécessaire !

**Configuration** (dans `serve_data.py`) :
- `CAPTURE_INTERVAL_MINUTES = 30` - Modifier la fréquence de capture
- `AUTO_CAPTURE_ENABLED = True` - Activer/désactiver la capture automatique
- `CAPTURE_DURATION_SECONDS = 180` - Durée par capture (3 minutes)

**Vérifier le Statut de la Capture :**
```python
import requests
status = requests.get('http://localhost:5000/api/capture/status').json()
print(f"Capture automatique activée : {status['auto_capture_enabled']}")
print(f"Dernière capture : {status['last_capture_time']}")
print(f"Capture en cours : {status['capture_in_progress']}")
```

**Déclencher Manuellement une Capture :**
```python
import requests
response = requests.post('http://localhost:5000/api/capture/trigger')
print(response.json())  # {"success": true, "message": "Capture started in background"}
```

## Tri des Matches

Tous les matches sont **automatiquement triés par timestamp `matchStart`** (matches les plus anciens en premier). Cela garantit un ordre cohérent entre les requêtes.

## Données en Temps Réel (Méthode Manuelle - Optionnel)

Si vous souhaitez capturer manuellement des données :

1. Exécuter l'outil de capture :
```bash
python analyze_winamax_socketio.py
```

2. Cela mettra à jour `winamax_socketio_analysis.json`

3. L'API recharge automatiquement les données après la capture (pas besoin de redémarrer) :
```bash
python serve_data.py
```

## Exemples d'Utilisation de l'API

### Exemple Python Complet

```python
import requests
import json

# Obtenir tous les matches
response = requests.get('http://localhost:5000/api/matches')
data = response.json()

if data['success']:
    print(f"Total de matches : {data['count']}")
    
    for match in data['matches'][:10]:  # 10 premiers
        print(f"\nMatch : {match['matchId']}")
        print(f"  {match['competitor1Name']} vs {match['competitor2Name']}")
        print(f"  Statut : {match['status']}")
        if 'odds' in match:
            print(f"  Cotes : {match['odds']}")
```

### Exemples cURL

```bash
# Obtenir tous les matches
curl http://localhost:5000/api/matches

# Obtenir les matches de football
curl http://localhost:5000/api/matches?sportId=1

# Filtrer par date
curl http://localhost:5000/api/matches?date=15-11-2025

# Filtres combinés
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025

# Obtenir un match spécifique
curl http://localhost:5000/api/matches/56418335

# Obtenir le statut
curl http://localhost:5000/api/status
```

## Dépannage

**Pas de données ?**
- Assurez-vous que `winamax_socketio_analysis.json` existe
- Vérifiez que le fichier a du contenu

**Le serveur ne démarre pas ?**
```bash
pip install flask flask-cors
python serve_data.py
```

**Besoin de données fraîches ?**
```bash
python analyze_winamax_socketio.py 60
```

## Prochaines Étapes

1. ✅ **Utiliser l'API actuelle** - Fonctionne avec les données capturées
2. Optionnel : Intégrer avec capture en temps réel
3. Optionnel : Ajouter filtrage et requêtes
4. Optionnel : Stocker dans une base de données

## Résumé

**Solution Fonctionnelle :**
- Fichier : `serve_data.py`
- Endpoint : `GET /api/matches`
- Sortie : JSON avec matches et métadonnées
- Statut : ✅ Entièrement fonctionnel

**Commande à utiliser :**
```bash
python serve_data.py && curl http://localhost:5000/api/matches
```

