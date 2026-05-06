"""
Test rapide avec SQLite : valide le schéma et l'import des données.
N'EST PAS UTILISÉ EN PRODUCTION (MySQL est la cible).
Sert juste à vérifier la cohérence du modèle et des données.
"""
import os
import sqlite3
import pandas as pd

DATASET = os.path.join(os.path.dirname(__file__), "..", "dataset")
DB = "/tmp/test_agri.db"

if os.path.exists(DB):
    os.remove(DB)

conn = sqlite3.connect(DB)
cur = conn.cursor()

# Schéma SQLite (équivalent du MySQL)
cur.executescript("""
CREATE TABLE utilisateur (
    id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    mot_de_passe TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'agriculteur',
    date_creation TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE parcelle (
    id_parcelle INTEGER PRIMARY KEY,
    nom TEXT NOT NULL,
    localisation TEXT NOT NULL,
    surface_ha REAL NOT NULL CHECK (surface_ha > 0),
    id_utilisateur INTEGER,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur)
);

CREATE TABLE culture (
    id_culture INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    date_semis TEXT NOT NULL,
    id_parcelle INTEGER NOT NULL,
    FOREIGN KEY (id_parcelle) REFERENCES parcelle(id_parcelle)
);

CREATE TABLE meteo (
    date TEXT PRIMARY KEY,
    temperature REAL NOT NULL,
    humidite REAL NOT NULL,
    pluie_mm REAL NOT NULL DEFAULT 0
);

CREATE TABLE observation (
    id_observation INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    etat TEXT NOT NULL,
    commentaire TEXT,
    id_parcelle INTEGER NOT NULL,
    FOREIGN KEY (id_parcelle) REFERENCES parcelle(id_parcelle)
);

CREATE TABLE alerte (
    id_alerte INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    type TEXT NOT NULL,
    niveau INTEGER NOT NULL CHECK (niveau BETWEEN 1 AND 3),
    statut TEXT NOT NULL DEFAULT 'active',
    id_parcelle INTEGER NOT NULL,
    FOREIGN KEY (id_parcelle) REFERENCES parcelle(id_parcelle)
);
""")

# Insertion des utilisateurs de démo
cur.executemany(
    "INSERT INTO utilisateur (nom, email, mot_de_passe, role) VALUES (?, ?, ?, ?)",
    [
        ('Admin Démo',     'admin@chambre-agri.fr',     'demo', 'admin'),
        ('Jean Dupont',    'jean.dupont@ferme.fr',      'demo', 'agriculteur'),
        ('Marie Martin',   'marie.martin@ferme.fr',     'demo', 'agriculteur'),
        ('Tech Conseil',   'conseil@chambre-agri.fr',   'demo', 'technicien'),
    ]
)

# Import CSV
parcelles = pd.read_csv(os.path.join(DATASET, "parcelles.csv"))
cultures = pd.read_csv(os.path.join(DATASET, "cultures.csv"))
meteo = pd.read_csv(os.path.join(DATASET, "meteo.csv"))
observations = pd.read_csv(os.path.join(DATASET, "observations.csv"))
alertes = pd.read_csv(os.path.join(DATASET, "alertes.csv"))

# parcelles
for _, r in parcelles.iterrows():
    cur.execute(
        "INSERT INTO parcelle (id_parcelle, nom, localisation, surface_ha, id_utilisateur) VALUES (?, ?, ?, ?, ?)",
        (int(r["id"]), r["nom"], r["localisation"], float(r["surface_ha"]),
         2 if int(r["id"]) % 2 == 0 else 3)
    )

# cultures
for _, r in cultures.iterrows():
    cur.execute(
        "INSERT INTO culture (id_culture, type, date_semis, id_parcelle) VALUES (?, ?, ?, ?)",
        (int(r["id"]), r["type"], r["date_semis"], int(r["parcelle_id"]))
    )

# meteo
for _, r in meteo.iterrows():
    cur.execute(
        "INSERT INTO meteo (date, temperature, humidite, pluie_mm) VALUES (?, ?, ?, ?)",
        (r["date"], float(r["temperature"]), float(r["humidite"]), float(r["pluie_mm"]))
    )

# observations
for _, r in observations.iterrows():
    cur.execute(
        "INSERT INTO observation (date, etat, commentaire, id_parcelle) VALUES (?, ?, ?, ?)",
        (r["date"], r["etat"], r["commentaire"], int(r["parcelle_id"]))
    )

# alertes
for _, r in alertes.iterrows():
    cur.execute(
        "INSERT INTO alerte (date, type, niveau, statut, id_parcelle) VALUES (?, ?, ?, ?, ?)",
        (r["date"], r["type"], int(r["niveau"]), 'active', int(r["parcelle_id"]))
    )

conn.commit()

# Vérifications
print("=== Lignes par table ===")
for t in ["utilisateur","parcelle","culture","meteo","observation","alerte"]:
    cur.execute(f"SELECT COUNT(*) FROM {t}")
    print(f"  {t:14s} : {cur.fetchone()[0]}")

print("\n=== Test FK (jointure) ===")
cur.execute("""
SELECT p.nom, c.type, c.date_semis
FROM parcelle p
JOIN culture c ON c.id_parcelle = p.id_parcelle
ORDER BY p.id_parcelle
""")
for row in cur.fetchall():
    print(" ", row)

conn.close()
print("\n[OK] Schéma et données validés.")
