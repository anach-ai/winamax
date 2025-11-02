# API Winamax - Matches de Football

Une boîte à outils complète pour capturer et servir les données de matches de football Winamax avec les cotes. Inclut des outils d'analyse Socket.IO, capture avec défilement automatique, API REST avec filtres, et documentation complète.

## 🚀 Démarrage Rapide - Obtenir les Matches de Football avec Cotes

**Vous voulez obtenir les matches MAINTENANT ?**

```bash
# Démarrer le serveur API
python serve_data.py

# Dans un autre terminal, obtenir les matches AVEC COTES
curl http://localhost:5000/api/matches
```

**Résultat :** JSON propre avec **624 matches de football** incluant les cotes :
- "Slovénie": 1.78
- "Match nul": 3.2
- "Kosovo": 3.9

**Dernière capture :** 624 matches de football avec cotes !

**Voir `HOW_TO_GET_MATCHES.md` pour le guide complet**

## 📚 Documentation

### 🇫🇷 Documentation Française (ce dossier)
- **`README.md`** ⭐ - Documentation principale
- **`START_HERE.md`** ⭐ - Guide de démarrage rapide
- **`HOW_TO_GET_MATCHES.md`** ⭐ - Guide complet pour obtenir les matches
- **`API_ENDPOINTS.md`** ⭐ - Référence API
- **`FINAL_ANSWER.md`** - Résumé final

### 🇬🇧 Documentation Anglaise
Located in [`../EN/`](../EN/)
- Tous les guides et références en anglais
- Setup, troubleshooting, et analyses techniques

## ✨ Ce Qui Est Inclus

### 1. Outils d'Analyse
- **`analyze_winamax_socketio.py`** - Capturer le trafic Socket.IO avec Selenium stealth [[memory:6983704]]
- **`analyze_results.py`** - Analyser les données capturées
- Contourne avec succès la détection de bot Winamax

### 2. Serveur API
- **`serve_data.py`** - API Flask fonctionnelle ⭐⭐⭐
- Sert les données Socket.IO capturées
- Endpoints JSON pour les matches avec filtres
- **C'est la solution qui fonctionne !**

## 🎯 Fonctionnalités Clés

✅ **Selenium Stealth** - Contourne la détection de bot  
✅ **Outil de Capture** - Défilement automatique pour obtenir tous les matches  
✅ **API REST** - Filtrer par sport, date ou les deux  
✅ **Données de Match** - 624 matches de football avec cotes  
✅ **JSON Propre** - Format simplifié  
✅ **Documentation Complète** - Tout documenté  

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🏗️ Architecture

```
Capture:    Selenium → Défilement auto → Socket.IO → JSON
Service:    Flask API → Endpoints REST → Votre App
Données:    Matches, Cotes, Scores, Résultats (624 matches)
```

## 📊 Données Accessibles

- **624 Matches de Football** avec noms des équipes et cotes
- **Matches en Direct** : scores en temps réel et progression du temps
- **Matches à Venir** : horaires et informations de match
- **Cotes de Pari** : mises à jour de cotes en temps réel
- **Données d'Équipes** : noms, métadonnées
- **Filtres** : par sport et date

## 🔌 Endpoints API

```
GET  /api/matches                 - Obtenir tous les matches (simplifié)
GET  /api/matches?sportId=1       - Filtrer par sport (1=Football)
GET  /api/matches?date=DD-MM-YYYY - Filtrer par date
GET  /api/matches?sportId=1&date=DD-MM-YYYY - Filtres combinés
GET  /api/matches/<id>            - Obtenir un match spécifique
GET  /api/matches/verbose         - Détails complets
GET  /api/status                  - Statut du serveur
GET  /api/info                    - Informations de capture
```

## 🔍 Ce Que Nous Avons Découvert

- **Protocole** : Engine.IO v3 + Socket.IO v3
- **Endpoint** : `wss://sports-eu-west-3.winamax.fr/uof-sports-server/socket.io/`
- **Transport** : WebSocket (pas de polling)
- **Taux de mise à jour** : Temps réel (toutes les quelques secondes)
- **Échelle** : 624 matches de football capturés

## 📁 Structure du Projet

```
winamax/
├── analyze_winamax_socketio.py       - Capturer le trafic Socket.IO
├── analyze_results.py                - Analyser les données capturées
├── serve_data.py                     - Serveur API Flask ⭐
├── winamax_socketio_analysis.json    - Données de matches capturées (624 matches)
├── requirements.txt                  - Dépendances Python
├── README.md                         - Ce fichier
├── START_HERE.md                     - Guide de démarrage rapide ⭐
├── HOW_TO_GET_MATCHES.md             - Guide complet ⭐
├── GET_MORE_MATCHES.md               - Capturer plus de matches
├── API_ENDPOINTS.md                  - Référence des endpoints ⭐
├── API_COMPLETE.md                   - Résumé API
├── PROJECT_COMPLETE.md               - Résumé du projet
├── FINAL_ANSWER.md                   - Résumé final
├── CLEAN_PROJECT_SUMMARY.md         - Résumé du nettoyage
├── ANALYZED_ENDPOINTS.md             - Analyse Socket.IO
└── SOCKET_IO_ANALYSIS_SUMMARY.md     - Résumé du protocole
```

## ⚡ Commandes Rapides

```bash
# Démarrer le serveur API
python serve_data.py

# Obtenir les matches
curl http://localhost:5000/api/matches

# Filtrer par football + date
curl http://localhost:5000/api/matches?sportId=1&date=15-11-2025

# Capturer de nouvelles données (120 secondes avec défilement auto)
python analyze_winamax_socketio.py 120

# Analyser les résultats
python analyze_results.py
```

## 🎓 En Savoir Plus

- Voir les données capturées : `../../winamax_socketio_analysis.json`
- Commencer : `START_HERE.md` ⭐
- Guide d'utilisation : `HOW_TO_GET_MATCHES.md` ⭐
- Documentation API : `API_ENDPOINTS.md` ⭐

## 🏆 Métriques de Succès

✅ Contourné la détection de bot Winamax  
✅ Capturé 624 matches de football  
✅ Défilement automatique pour obtenir toutes les données  
✅ API REST fonctionnelle  
✅ Filtrage par sport et date  
✅ Documentation complète  

---

**Prêt à commencer ?** → Voir `START_HERE.md` 🚀

