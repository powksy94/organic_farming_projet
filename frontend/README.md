# Frontend — Organic Farming

Front React + Vite + Tailwind branché sur l'API FastAPI du back.

## Lancer en local

```bash
# 1. Installer les deps
npm install

# 2. Lancer le serveur de dev
npm run dev
```

Le front démarre sur **http://localhost:5173** et tape sur le back via un proxy
configuré dans `vite.config.js` (toutes les requêtes `/api/*` sont redirigées
vers `http://localhost:8000`).

⚠️ Pense à lancer le back FastAPI **avant** :
```bash
cd ../backend
uvicorn main:app --reload
```

## Structure

```
src/
├── main.jsx           # entrée + router
├── App.jsx            # routes
├── api.js             # client fetch
├── index.css          # Tailwind
├── components/
│   ├── Navbar.jsx
│   └── Layout.jsx
└── pages/
    ├── Dashboard.jsx
    ├── Plots.jsx       # parcelles
    ├── Crops.jsx       # cultures
    ├── Observations.jsx
    └── Alerts.jsx
```

## Build prod

```bash
npm run build
```

→ génère `dist/` à servir derrière nginx ou un autre statique.
