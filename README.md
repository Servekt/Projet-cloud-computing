# 📌 Projet Cloud Computing – Application Flask déployée sur AKS

Ce projet est une application Flask qui affiche les **actualités** et **événements** en France, récupérés dynamiquement depuis des APIs.  
Les données sont stockées dans **Azure Blob Storage**, mises à jour toutes les 30 minutes, et servies via une interface web dynamique.

---

## 🧱 Stack Technique

- **Python 3 + Flask**
- **Azure Blob Storage** (stockage des fichiers JSON)
- **Docker** (conteneurisation)
- **Azure Kubernetes Service (AKS)** (déploiement)
- **GitHub** (CI/CD)
- **Azure Container Registry (ACR)** (stockage des images)

---

## 🚀 Fonctionnalités

### 📅 API Endpoints

| Endpoint       | Méthode | Description |
|----------------|---------|-------------|
| `/api/news`    | GET     | Dernières actualités |
| `/api/events`  | GET     | Événements culturels à venir |
| `/`            | GET     | Interface HTML dynamique |

### 🔄 Mise à jour automatique
- Les données sont mises à jour toutes les 90 minutes via `APScheduler`
- Les fichiers sont uploadés vers Azure Blob automatiquement

### 🌐 Interface web responsive
- Actualités à gauche
- Événements à droite
- Affichage en grille avec images, lieux, liens
- Boutons 🔄 pour rafraîchir les données via JS

---

## ⚙️ Lancement en local

### 1. Prérequis

- Python 3.10+
- Docker (optionnel)
- Azure Storage Account

### 2. Installation

```bash
git clone https://github.com/Servekt/Projet-cloud-computing.git
cd Projet-cloud-computing
pip install -r app/requirements.txt
