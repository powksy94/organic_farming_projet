# Organic Farming — Projet Agriculture

Application de gestion agricole avec un backend FastAPI et un frontend React.

## Structure du projet

```
projet-agriculture/
├── backend/                  # API FastAPI (Python)
│   ├── main.py               # Point d'entrée
│   ├── data/                 # Base de données SQLite + seeding
│   ├── model/                # Modèles SQLAlchemy
│   ├── routes/               # Endpoints REST (plots, crops, observations, alerts, weather, dashboard)
│   ├── services/             # Services métier
│   └── schemas.py            # Schémas Pydantic
├── frontend/                 # App React (Vite + Tailwind)
│   ├── src/
│   │   ├── api.js            # Client fetch vers le backend
│   │   ├── App.jsx           # Routes
│   │   ├── components/       # Navbar, Layout
│   │   └── pages/            # Dashboard, Plots, Crops, Observations, Alerts
├── terraview/                # Interface cartographique TerraView
├── bdd/                      # Documentation BDD (MCD, MLD, Word)
└── dataset_agriculture (2)/  # Données CSV de seed
```

## Lancer en local

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

L'API démarre sur **http://localhost:8000**.  
La base de données SQLite est créée et seedée automatiquement au premier démarrage.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Le frontend démarre sur **http://localhost:5173**.  
Les requêtes `/api/*` sont automatiquement redirigées vers le backend via le proxy Vite.

## Routes API

| Méthode | Endpoint | Description |
|---|---|---|
| GET | `/api/plots/` | Liste des parcelles |
| GET | `/api/crops/` | Liste des cultures |
| GET | `/api/observations/` | Liste des observations |
| GET | `/api/alerts/` | Liste des alertes |
| GET | `/api/weather/` | Données météo |
| GET | `/api/dashboard/` | Données agrégées dashboard |

## Déploiement sur Railway

Le projet se déploie en **deux services séparés** dans un même projet Railway, depuis le même repo.

### Service Backend

- **Root Directory** : `backend`
- **Start Command** : `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Service Frontend

- **Root Directory** : `frontend`
- **Build Command** : `npm run build`
- **Start Command** : `npx serve dist`

> Après déploiement, mettre à jour la variable `VITE_API_URL` dans le frontend avec l'URL publique du service backend Railway.
