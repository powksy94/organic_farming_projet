"""
Script d'import du dataset agricole dans MySQL/MariaDB.

Usage :
    pip install mysql-connector-python pandas
    python 02_import_data.py

Variables d'environnement :
    DB_HOST     (défaut : localhost)
    DB_PORT     (défaut : 3306)
    DB_USER     (défaut : root)
    DB_PASSWORD (défaut : "")
    DB_NAME     (défaut : agri_db)

Le script :
  1. Se connecte à MySQL
  2. Charge les 5 CSV (parcelles, cultures, meteo, observations, alertes)
  3. Nettoie les données (types, doublons, valeurs manquantes)
  4. Insère dans les tables, en respectant les contraintes
  5. Affiche un récapitulatif des lignes importées
"""

import os
import sys
import pandas as pd
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", "3306")),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "agri_db"),
}

DATASET_DIR = os.path.join(os.path.dirname(__file__), "..", "dataset")

CSV_FILES = {
    "parcelles":    "parcelles.csv",
    "cultures":     "cultures.csv",
    "meteo":        "meteo.csv",
    "observations": "observations.csv",
    "alertes":      "alertes.csv",
}


# ---------------------------------------------------------------------
# Étapes
# ---------------------------------------------------------------------
def load_csvs():
    """Charge les 5 CSV en DataFrames."""
    dfs = {}
    for key, filename in CSV_FILES.items():
        path = os.path.join(DATASET_DIR, filename)
        if not os.path.isfile(path):
            sys.exit(f"[ERREUR] Fichier introuvable : {path}")
        dfs[key] = pd.read_csv(path)
        print(f"  - {filename:25s} : {len(dfs[key])} lignes")
    return dfs


def clean_data(dfs):
    """Nettoie les données avant import."""
    # parcelles : id, nom, localisation, surface_ha
    df = dfs["parcelles"]
    df.drop_duplicates(subset=["id"], inplace=True)
    df["surface_ha"] = pd.to_numeric(df["surface_ha"], errors="coerce")
    df.dropna(subset=["nom", "localisation", "surface_ha"], inplace=True)

    # cultures : id, type, date_semis, parcelle_id
    df = dfs["cultures"]
    df.drop_duplicates(subset=["id"], inplace=True)
    df["date_semis"] = pd.to_datetime(df["date_semis"], errors="coerce").dt.date
    df.dropna(subset=["type", "date_semis", "parcelle_id"], inplace=True)

    # meteo : date, temperature, humidite, pluie_mm
    df = dfs["meteo"]
    df.drop_duplicates(subset=["date"], inplace=True)
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    for col in ["temperature", "humidite", "pluie_mm"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df.dropna(inplace=True)

    # observations : date, etat, parcelle_id, commentaire
    df = dfs["observations"]
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["commentaire"] = df["commentaire"].fillna("")
    df.dropna(subset=["date", "etat", "parcelle_id"], inplace=True)

    # alertes : date, type, parcelle_id, niveau
    df = dfs["alertes"]
    df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    df["niveau"] = pd.to_numeric(df["niveau"], errors="coerce").astype("Int64")
    df.dropna(subset=["date", "type", "parcelle_id", "niveau"], inplace=True)

    return dfs


def truncate_tables(cursor):
    """Vide les tables (sauf utilisateur, conservé pour démo)."""
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    for table in ["alerte", "observation", "meteo", "culture", "parcelle"]:
        cursor.execute(f"TRUNCATE TABLE {table};")
    cursor.execute("SET FOREIGN_KEY_CHECKS=1;")


def insert_parcelles(cursor, df):
    sql = ("INSERT INTO parcelle "
           "(id_parcelle, nom, localisation, surface_ha, id_utilisateur) "
           "VALUES (%s, %s, %s, %s, %s)")
    rows = [
        (int(r["id"]), r["nom"], r["localisation"],
         float(r["surface_ha"]),
         # On répartit fictivement les parcelles entre les utilisateurs 2 et 3
         2 if int(r["id"]) % 2 == 0 else 3)
        for _, r in df.iterrows()
    ]
    cursor.executemany(sql, rows)
    return len(rows)


def insert_cultures(cursor, df):
    sql = ("INSERT INTO culture (id_culture, type, date_semis, id_parcelle) "
           "VALUES (%s, %s, %s, %s)")
    rows = [
        (int(r["id"]), r["type"], r["date_semis"], int(r["parcelle_id"]))
        for _, r in df.iterrows()
    ]
    cursor.executemany(sql, rows)
    return len(rows)


def insert_meteo(cursor, df):
    sql = ("INSERT INTO meteo (date, temperature, humidite, pluie_mm) "
           "VALUES (%s, %s, %s, %s)")
    rows = [
        (r["date"], float(r["temperature"]),
         float(r["humidite"]), float(r["pluie_mm"]))
        for _, r in df.iterrows()
    ]
    cursor.executemany(sql, rows)
    return len(rows)


def insert_observations(cursor, df):
    sql = ("INSERT INTO observation (date, etat, commentaire, id_parcelle) "
           "VALUES (%s, %s, %s, %s)")
    rows = [
        (r["date"], r["etat"], r["commentaire"], int(r["parcelle_id"]))
        for _, r in df.iterrows()
    ]
    cursor.executemany(sql, rows)
    return len(rows)


def insert_alertes(cursor, df):
    sql = ("INSERT INTO alerte (date, type, niveau, statut, id_parcelle) "
           "VALUES (%s, %s, %s, %s, %s)")
    rows = [
        (r["date"], r["type"], int(r["niveau"]), "active", int(r["parcelle_id"]))
        for _, r in df.iterrows()
    ]
    cursor.executemany(sql, rows)
    return len(rows)


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------
def main():
    print("=" * 60)
    print("Import du dataset agricole dans MySQL")
    print("=" * 60)

    print("\n[1/4] Chargement des CSV…")
    dfs = load_csvs()

    print("\n[2/4] Nettoyage des données…")
    dfs = clean_data(dfs)
    for k, df in dfs.items():
        print(f"  - {k:13s} après nettoyage : {len(df)} lignes")

    print("\n[3/4] Connexion à la base de données…")
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print(f"  Connecté à {DB_CONFIG['host']}:{DB_CONFIG['port']} "
              f"(base : {DB_CONFIG['database']})")
    except Error as e:
        sys.exit(f"[ERREUR] Connexion impossible : {e}")

    print("\n[4/4] Insertion des données…")
    truncate_tables(cursor)

    counts = {
        "parcelles":    insert_parcelles(cursor,   dfs["parcelles"]),
        "cultures":     insert_cultures(cursor,    dfs["cultures"]),
        "meteo":        insert_meteo(cursor,       dfs["meteo"]),
        "observations": insert_observations(cursor, dfs["observations"]),
        "alertes":      insert_alertes(cursor,     dfs["alertes"]),
    }
    conn.commit()

    print("\nRécapitulatif :")
    for table, n in counts.items():
        print(f"  - {table:13s} : {n} lignes insérées")

    cursor.close()
    conn.close()
    print("\n[OK] Import terminé avec succès.")


if __name__ == "__main__":
    main()
