# 📌 Projet-cloud-computing 

Ce projet est une application Flask permettant d'afficher les actualités et événements en France. Les données sont récupérées dynamiquement depuis des API et mises à jour automatiquement toutes les 30 minutes.

## 📦 Installation & Démarrage

### 1️⃣ Prérequis
- Python 3.x
- Pip installé
- Un accès à internet pour récupérer les données des API

### 2️⃣ Installation
Clonez ce dépôt et installez les dépendances nécessaires :
```sh
pip install flask requests apscheduler
```

### 3️⃣ Démarrer le serveur
Lancez le serveur Flask avec :
```sh
python app.py
```

L'application sera accessible sur **http://localhost:4123**.

## 🚀 Fonctionnalités
### 📅 API Endpoints
| Endpoint       | Méthode | Description |
|---------------|--------|-------------|
| `/api/news`   | GET    | Récupère les dernières actualités |
| `/api/events` | GET    | Récupère les événements à venir |

### 🔄 Mise à jour Automatique
Un **scheduler** met à jour les fichiers `news.json` et `events.json` toutes les 30 minutes en interrogeant les API.

### 🎨 Interface Web
L'interface est divisée en **deux colonnes** :
- 📌 **Gauche** : Actualités récentes
- 📅 **Droite** : Événements à venir (affichés sur deux colonnes)
- 🔄 **Bouton Refresh** : Permet de récupérer les dernières données sans recharger la page

## 🔧 Personnalisation
Vous pouvez modifier les API en éditant les fonctions `fetch_news()` et `fetch_events()` dans **app.py**.