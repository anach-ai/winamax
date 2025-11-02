# COMMENCEZ ICI - Obtenir les Matches de Football avec Cotes

## 🎯 Votre Objectif

Obtenir les matches de football avec leurs cotes de pari Winamax.

## ✅ Solution (Fonctionne Maintenant)

### Étape 1 : Démarrer le Serveur API

```bash
python serve_data.py
```

Vous devriez voir :
```
Starting Winamax Data API...
Visit:
  http://localhost:5000/api/matches - Get all matches
  http://localhost:5000/api/status - Check status
  http://localhost:5000/api/info - Capture info
```

### Étape 2 : Obtenir les Matches

Ouvrez un autre terminal et exécutez :

```bash
curl http://localhost:5000/api/matches
```

**OU** utilisez Python :

```python
import requests
response = requests.get('http://localhost:5000/api/matches')
print(response.json())
```

## 📋 Ce Que Vous Obtenez

Réponse JSON avec les matches de football **AVEC COTES** :

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

## 📚 Plus d'Informations

- **Guide Complet :** `HOW_TO_GET_MATCHES.md`
- **Obtenir Plus de Matches :** `GET_MORE_MATCHES.md` ⭐
- **Référence API :** `API_ENDPOINTS.md`
- **Analyse :** `SOCKET_IO_ANALYSIS_SUMMARY.md`

## 🎓 Prochaines Étapes

1. ✅ Vous obtenez maintenant les matches !
2. Vous voulez PLUS de matches ? Voir `GET_MORE_MATCHES.md`
3. Personnalisez les requêtes selon vos besoins
4. Construisez votre application en utilisant l'API

**Note :** La capture actuelle contient 624 matches de football avec cotes ! Le défilement automatique capture tous les matches.

## 📊 Endpoints Disponibles

- `GET /api/matches` - Tous les matches (simplifié)
- `GET /api/matches?sportId=1` - Filtrer par sport (1=Football)
- `GET /api/matches?date=DD-MM-YYYY` - Filtrer par date
- `GET /api/matches?sportId=1&date=DD-MM-YYYY` - Filtrer par sport + date
- `GET /api/matches/verbose` - Tous les matches (détails complets)
- `GET /api/matches/<id>` - Match spécifique
- `GET /api/status` - Statut du serveur
- `GET /api/info` - Informations de données

## 🎉 C'est Tout !

Vous avez maintenant une API fonctionnelle pour obtenir les matches de football avec cotes !

**Voir `HOW_TO_GET_MATCHES.md` pour des exemples détaillés.**

