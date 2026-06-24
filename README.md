# 🚀 ATS AI Matcher

## 📝 Description
**ATS AI Matcher** est un outil complet d'analyse de CV propulsé par l'intelligence artificielle **Google Gemini**. Cette plateforme permet d'automatiser le tri et l'évaluation des candidatures en extrayant intelligemment les compétences, les expériences et les informations clés des fichiers PDF pour les faire correspondre aux besoins de l'entreprise via une interface moderne et intuitive.

## 🛠 Stack Technique
L'application repose sur une architecture moderne et performante :
- **Backend :** FastAPI (Python) - Pour une API asynchrone rapide et robuste.
- **Base de données :** SQLite - Stockage léger et efficace des profils.
- **Frontend :** Vanilla JS / HTML5 / Tailwind CSS - Une interface utilisateur fluide avec support natif du Drag & Drop.
- **Conteneurisation :** Docker & Docker Compose - Pour un déploiement simplifié et reproductible.
- **IA :** Google Gemini API - Large Language Model utilisé pour le parsing sémantique des CV.

## 📋 Prérequis
Avant de lancer l'application, assurez-vous de disposer de :
- **Docker** et **Docker Compose** installés sur votre système.
- Une **Clé API Google Gemini** (obtenue via Google AI Studio).

## 🚀 Comment lancer le projet
Le projet est entièrement automatisé pour un démarrage rapide :

1. **Configuration de l'environnement :**
   Créez un fichier nommé `.env` à la racine du projet et insérez-y votre clé API :
   ```env
   GEMINI_API_KEY=votre_cle_api_ici
   ```

2. **Lancement de l'application :**
   Utilisez le Makefile fourni pour construire et démarrer tous les services en une seule commande :
   ```bash
   make up
   ```
   *(Note : Si vous n'avez pas l'utilitaire Make, vous pouvez utiliser `docker-compose up --build`)*

3. **Accès :**
   - L'interface utilisateur est accessible sur : `http://localhost:8080`
   - La documentation interactive de l'API (Swagger) est disponible sur : `http://localhost:8000/docs`

---
**ATS AI Matcher** est prêt à transformer votre processus de recrutement grâce à la puissance de l'IA générative. Profitez d'un gain de temps sans précédent et concentrez-vous sur ce qui compte vraiment : trouver le talent idéal. 🚀