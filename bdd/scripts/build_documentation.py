"""
Génère le document Word de documentation de la base de données.
Pour le projet B2 Sup de Vinci - Agriculture (P3 - Base de données).
"""
import os
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

ROOT = os.path.join(os.path.dirname(__file__), "..")
SCHEMA_DIR = os.path.join(ROOT, "schemas")
OUTPUT = os.path.join(ROOT, "Documentation_BDD.docx")

# ---------- Helpers ----------
PRIMARY = RGBColor(0x1A, 0x23, 0x7E)   # bleu foncé
SECONDARY = RGBColor(0x2E, 0x7D, 0x32) # vert
ACCENT = RGBColor(0xBF, 0x36, 0x0C)    # orange foncé
GREY = RGBColor(0x42, 0x42, 0x42)


def set_cell_shading(cell, fill_color_hex):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill_color_hex)
    tc_pr.append(shd)


def add_heading(doc, text, level=1, color=PRIMARY):
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.color.rgb = color
        run.font.name = "Calibri"
    return h


def add_paragraph(doc, text, bold=False, italic=False, size=11):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.name = "Calibri"
    run.bold = bold
    run.italic = italic
    return p


def add_bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    run = p.runs[0] if p.runs else p.add_run()
    p.add_run(text).font.name = "Calibri"
    return p


def add_code(doc, code, lang="sql"):
    """Bloc code en monospace dans un tableau 1x1 (fond gris)."""
    table = doc.add_table(rows=1, cols=1)
    table.autofit = True
    cell = table.rows[0].cells[0]
    set_cell_shading(cell, "F5F5F5")
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(code)
    run.font.name = "Consolas"
    run.font.size = Pt(9)
    # Petit espace après le bloc
    doc.add_paragraph()
    return table


def add_table_header(table, headers):
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        run = p.add_run(h)
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        run.font.size = Pt(10)
        run.font.name = "Calibri"
        set_cell_shading(hdr[i], "1A237E")
        hdr[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER


def add_dictionnaire_table(doc, lines):
    """lines = list of (col, type, contrainte, description)."""
    table = doc.add_table(rows=1, cols=4)
    table.style = "Light Grid Accent 1"
    add_table_header(table, ["Colonne", "Type", "Contrainte", "Description"])
    for col, typ, ctr, desc in lines:
        row = table.add_row().cells
        row[0].text = col
        row[1].text = typ
        row[2].text = ctr
        row[3].text = desc
        for c in row:
            for p in c.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)
                    r.font.name = "Calibri"
    # Largeurs de colonnes
    for row in table.rows:
        row.cells[0].width = Cm(3.5)
        row.cells[1].width = Cm(3.0)
        row.cells[2].width = Cm(3.5)
        row.cells[3].width = Cm(7.0)


# ============================================================
# Construction du document
# ============================================================
doc = Document()

# Style par défaut
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

# Marges
for section in doc.sections:
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)

# ---------- PAGE DE GARDE ----------
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run("\n\n\n\n")

t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("Documentation de la base de données")
r.font.size = Pt(28)
r.font.bold = True
r.font.color.rgb = PRIMARY
r.font.name = "Calibri"

t2 = doc.add_paragraph()
t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t2.add_run("Projet d'études Bachelor 2 — Agriculture")
r.font.size = Pt(18)
r.font.color.rgb = SECONDARY
r.font.name = "Calibri"

t3 = doc.add_paragraph()
t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t3.add_run("Suivi des cultures et aide à la décision")
r.font.size = Pt(14)
r.font.italic = True
r.font.color.rgb = GREY
r.font.name = "Calibri"

doc.add_paragraph("\n\n\n\n\n")

infos = doc.add_paragraph()
infos.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = infos.add_run("Sup de Vinci — Bachelor 2\n")
r.font.size = Pt(12); r.font.bold = True; r.font.name = "Calibri"
r = infos.add_run("Client : Chambre d'Agriculture\n")
r.font.size = Pt(12); r.font.name = "Calibri"
r = infos.add_run("Document réalisé par : P3 — Responsable Base de données\n")
r.font.size = Pt(12); r.font.name = "Calibri"
r = infos.add_run("Année 2025-2026")
r.font.size = Pt(12); r.font.name = "Calibri"

doc.add_page_break()

# ---------- SOMMAIRE (statique) ----------
add_heading(doc, "Sommaire", level=1)
sommaire = [
    "1. Contexte et périmètre",
    "2. Modèle Conceptuel de Données (MCD)",
    "3. Modèle Logique de Données (MLD)",
    "4. Dictionnaire des données",
    "5. Jeu de données fourni",
    "6. Procédure d'installation et d'import",
    "7. Requêtes SQL pour le tableau de bord",
    "8. Logique d'analyse et règles métier",
    "9. Limites, hypothèses et évolutions",
]
for item in sommaire:
    p = doc.add_paragraph(item)
    p.paragraph_format.space_after = Pt(2)
    for r in p.runs:
        r.font.size = Pt(11); r.font.name = "Calibri"

doc.add_page_break()

# ============================================================
# 1. CONTEXTE
# ============================================================
add_heading(doc, "1. Contexte et périmètre", level=1)

add_paragraph(doc,
    "Ce document décrit la base de données conçue pour le projet d'études B2 sur la "
    "thématique Agriculture. La solution numérique vise à aider les acteurs agricoles "
    "(agriculteurs, techniciens de la Chambre d'Agriculture) à suivre leurs cultures, "
    "exploiter des données météo et terrain, et améliorer leur prise de décision."
)

add_paragraph(doc, "Périmètre fonctionnel couvert par la base :", bold=True)
for puce in [
    "Gestion des parcelles et des cultures associées",
    "Saisie et historisation des observations terrain",
    "Stockage des données météo journalières",
    "Génération et suivi d'alertes basées sur des règles métier",
    "Authentification simple (utilisateurs avec rôles)",
]:
    add_bullet(doc, puce)

add_paragraph(doc, "Choix techniques :", bold=True)
add_bullet(doc, "SGBD relationnel : MySQL 8.0 (compatible MariaDB 10.x)")
add_bullet(doc, "Encodage : UTF-8 (utf8mb4)")
add_bullet(doc, "Moteur : InnoDB (transactions + intégrité référentielle)")
add_bullet(doc, "6 tables principales : utilisateur, parcelle, culture, meteo, observation, alerte")

doc.add_page_break()

# ============================================================
# 2. MCD
# ============================================================
add_heading(doc, "2. Modèle Conceptuel de Données (MCD)", level=1)

add_paragraph(doc,
    "Le MCD représente les entités du domaine et leurs associations en notation Merise. "
    "Il met en évidence le sens métier des données, indépendamment de l'implémentation."
)

# Insertion image MCD
mcd_path = os.path.join(SCHEMA_DIR, "MCD.png")
if os.path.exists(mcd_path):
    doc.add_picture(mcd_path, width=Cm(16))
    last_p = doc.paragraphs[-1]
    last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

caption = doc.add_paragraph()
caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = caption.add_run("Figure 1 — Modèle Conceptuel de Données")
r.font.italic = True; r.font.size = Pt(10); r.font.color.rgb = GREY; r.font.name = "Calibri"

add_paragraph(doc, "Lecture du MCD :", bold=True)
add_bullet(doc, "Un UTILISATEUR gère 0 ou plusieurs PARCELLES ; chaque parcelle est gérée par un seul utilisateur.")
add_bullet(doc, "Une PARCELLE peut accueillir plusieurs CULTURES dans le temps.")
add_bullet(doc, "Une PARCELLE est concernée par plusieurs OBSERVATIONS terrain.")
add_bullet(doc, "Une PARCELLE peut déclencher plusieurs ALERTES (basées sur règles métier).")
add_bullet(doc, "La METEO est journalière (clé = date) et croisée avec les observations.")

doc.add_page_break()

# ============================================================
# 3. MLD
# ============================================================
add_heading(doc, "3. Modèle Logique de Données (MLD)", level=1)

add_paragraph(doc,
    "Le MLD traduit le MCD en tables relationnelles avec leurs colonnes, "
    "clés primaires (PK) et clés étrangères (FK)."
)

mld_path = os.path.join(SCHEMA_DIR, "MLD.png")
if os.path.exists(mld_path):
    doc.add_picture(mld_path, width=Cm(16))
    last_p = doc.paragraphs[-1]
    last_p.alignment = WD_ALIGN_PARAGRAPH.CENTER

caption = doc.add_paragraph()
caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = caption.add_run("Figure 2 — Modèle Logique de Données")
r.font.italic = True; r.font.size = Pt(10); r.font.color.rgb = GREY; r.font.name = "Calibri"

add_paragraph(doc, "Règles d'intégrité référentielle :", bold=True)
add_bullet(doc, "parcelle.id_utilisateur → utilisateur.id_utilisateur (ON DELETE SET NULL)")
add_bullet(doc, "culture.id_parcelle → parcelle.id_parcelle (ON DELETE CASCADE)")
add_bullet(doc, "observation.id_parcelle → parcelle.id_parcelle (ON DELETE CASCADE)")
add_bullet(doc, "alerte.id_parcelle → parcelle.id_parcelle (ON DELETE CASCADE)")
add_bullet(doc, "meteo n'a pas de FK directe : la table est croisée par date avec les autres entités")

doc.add_page_break()

# ============================================================
# 4. DICTIONNAIRE DES DONNÉES
# ============================================================
add_heading(doc, "4. Dictionnaire des données", level=1)

add_paragraph(doc,
    "Description détaillée de chaque table, colonne par colonne. "
    "PK = clé primaire, FK = clé étrangère, NN = NOT NULL, U = UNIQUE."
)

# --- utilisateur ---
add_heading(doc, "4.1 Table utilisateur", level=2, color=SECONDARY)
add_dictionnaire_table(doc, [
    ("id_utilisateur", "INT",          "PK, AUTO_INCREMENT", "Identifiant unique du compte"),
    ("nom",            "VARCHAR(80)",  "NN",                 "Nom d'affichage"),
    ("email",          "VARCHAR(120)", "NN, U",              "Email de connexion (unique)"),
    ("mot_de_passe",   "VARCHAR(255)", "NN",                 "Hash bcrypt du mot de passe"),
    ("role",           "ENUM",         "NN, défaut 'agriculteur'", "agriculteur / technicien / admin"),
    ("date_creation",  "DATETIME",     "NN, défaut CURRENT_TIMESTAMP", "Date de création du compte"),
])

# --- parcelle ---
add_heading(doc, "4.2 Table parcelle", level=2, color=SECONDARY)
add_dictionnaire_table(doc, [
    ("id_parcelle",    "INT",          "PK, AUTO_INCREMENT", "Identifiant unique de la parcelle"),
    ("nom",            "VARCHAR(80)",  "NN",                 "Nom usuel (ex : Parcelle 3)"),
    ("localisation",   "VARCHAR(60)",  "NN",                 "Zone ou commune (ex : Zone A)"),
    ("surface_ha",     "DECIMAL(6,2)", "NN, > 0",            "Surface en hectares"),
    ("id_utilisateur", "INT",          "FK utilisateur",     "Utilisateur responsable (nullable)"),
])

# --- culture ---
add_heading(doc, "4.3 Table culture", level=2, color=SECONDARY)
add_dictionnaire_table(doc, [
    ("id_culture",    "INT",          "PK, AUTO_INCREMENT", "Identifiant unique de la culture"),
    ("type",          "VARCHAR(50)",  "NN",                 "Type de culture (Blé, Orge, Maïs, Colza, Tournesol)"),
    ("date_semis",    "DATE",         "NN",                 "Date de semis"),
    ("id_parcelle",   "INT",          "FK parcelle, NN",    "Parcelle où la culture est implantée"),
])

# --- meteo ---
add_heading(doc, "4.4 Table meteo", level=2, color=SECONDARY)
add_dictionnaire_table(doc, [
    ("date",          "DATE",         "PK",   "Date du relevé météo (1 ligne par jour)"),
    ("temperature",   "DECIMAL(4,1)", "NN",   "Température moyenne du jour, en °C"),
    ("humidite",      "DECIMAL(5,1)", "NN",   "Humidité moyenne du jour, en %"),
    ("pluie_mm",      "DECIMAL(5,1)", "NN, défaut 0", "Cumul de pluie du jour, en mm"),
])

# --- observation ---
add_heading(doc, "4.5 Table observation", level=2, color=SECONDARY)
add_dictionnaire_table(doc, [
    ("id_observation", "INT",          "PK, AUTO_INCREMENT", "Identifiant unique de l'observation"),
    ("date",           "DATE",         "NN",                 "Date de l'observation terrain"),
    ("etat",           "VARCHAR(40)",  "NN",                 "OK / Risque maladie / Stress hydrique / Maladie détectée"),
    ("commentaire",    "VARCHAR(255)", "",                   "Commentaire libre de l'agriculteur"),
    ("id_parcelle",    "INT",          "FK parcelle, NN",    "Parcelle observée"),
])

# --- alerte ---
add_heading(doc, "4.6 Table alerte", level=2, color=SECONDARY)
add_dictionnaire_table(doc, [
    ("id_alerte",     "INT",          "PK, AUTO_INCREMENT", "Identifiant unique de l'alerte"),
    ("date",          "DATE",         "NN",                 "Date de déclenchement"),
    ("type",          "VARCHAR(40)",  "NN",                 "Type d'alerte (Stress hydrique, Risque maladie, ...)"),
    ("niveau",        "TINYINT",      "NN, 1..3",           "Niveau de gravité (1=Faible, 2=Modéré, 3=Élevé)"),
    ("statut",        "VARCHAR(20)",  "NN, défaut 'active'", "active / résolue / ignorée"),
    ("id_parcelle",   "INT",          "FK parcelle, NN",    "Parcelle concernée"),
])

doc.add_page_break()

# ============================================================
# 5. JEU DE DONNÉES
# ============================================================
add_heading(doc, "5. Jeu de données fourni", level=1)

add_paragraph(doc,
    "Le dataset fourni avec le cahier des charges contient 5 fichiers CSV. "
    "Récapitulatif des volumes après nettoyage :"
)

t = doc.add_table(rows=1, cols=4)
t.style = "Light Grid Accent 1"
add_table_header(t, ["Fichier", "Lignes", "Période", "Description"])
for f, n, p, d in [
    ("parcelles.csv",    "10",  "—",                              "Liste des parcelles, zones et surfaces"),
    ("cultures.csv",     "10",  "—",                              "Cultures plantées sur chaque parcelle"),
    ("meteo.csv",        "60",  "01/03/2026 → 29/04/2026",        "Conditions météo journalières"),
    ("observations.csv", "100", "01/03/2026 → 29/04/2026",        "Observations terrain (4 états possibles)"),
    ("alertes.csv",      "50",  "01/03/2026 → 29/04/2026",        "Alertes générées (2 types, 3 niveaux)"),
]:
    row = t.add_row().cells
    row[0].text = f; row[1].text = n; row[2].text = p; row[3].text = d
    for c in row:
        for para in c.paragraphs:
            for run in para.runs:
                run.font.size = Pt(10); run.font.name = "Calibri"

add_paragraph(doc, "")
add_paragraph(doc, "Valeurs distinctes observées dans le dataset :", bold=True)
add_bullet(doc, "Cultures : Blé, Colza, Maïs, Orge, Tournesol")
add_bullet(doc, "Localisations : Zone A, B, C, D, E")
add_bullet(doc, "États d'observation : OK (26), Maladie détectée (25), Risque maladie (25), Stress hydrique (24)")
add_bullet(doc, "Types d'alerte : Stress hydrique (23), Risque maladie (27)")
add_bullet(doc, "Niveaux d'alerte : 1=Faible (15), 2=Modéré (23), 3=Élevé (12)")

doc.add_page_break()

# ============================================================
# 6. INSTALLATION
# ============================================================
add_heading(doc, "6. Procédure d'installation et d'import", level=1)

add_paragraph(doc, "Prérequis :", bold=True)
add_bullet(doc, "MySQL 8.0 ou MariaDB 10.x installé et démarré")
add_bullet(doc, "Python 3.9+ avec les libs : pandas, mysql-connector-python")

add_paragraph(doc, "Étape 1 — Création de la base et des tables", bold=True)
add_code(doc, "mysql -u root -p < scripts/01_create_tables.sql")

add_paragraph(doc, "Étape 2 — Configuration de la connexion", bold=True)
add_paragraph(doc, "Variables d'environnement à définir avant l'import :")
add_code(doc,
"export DB_HOST=localhost\n"
"export DB_PORT=3306\n"
"export DB_USER=root\n"
"export DB_PASSWORD=monMotDePasse\n"
"export DB_NAME=agri_db", lang="bash")

add_paragraph(doc, "Étape 3 — Import du dataset", bold=True)
add_code(doc,
"pip install pandas mysql-connector-python\n"
"python scripts/02_import_data.py", lang="bash")

add_paragraph(doc, "Le script effectue automatiquement :")
add_bullet(doc, "Lecture des 5 fichiers CSV")
add_bullet(doc, "Conversion des dates (format ISO YYYY-MM-DD)")
add_bullet(doc, "Suppression des doublons et lignes incomplètes")
add_bullet(doc, "Vidage des tables existantes (TRUNCATE) puis insertion en masse")
add_bullet(doc, "Affichage d'un récapitulatif (nb lignes par table)")

doc.add_page_break()

# ============================================================
# 7. REQUÊTES SQL
# ============================================================
add_heading(doc, "7. Requêtes SQL pour le tableau de bord", level=1)

add_paragraph(doc,
    "Le fichier scripts/03_dashboard_queries.sql regroupe les 12 requêtes utilisées "
    "par l'API backend pour alimenter le dashboard. Elles sont commentées et numérotées."
)

# Tableau des requêtes
t = doc.add_table(rows=1, cols=3)
t.style = "Light Grid Accent 1"
add_table_header(t, ["Code", "Objectif", "Usage"])
for c, o, u in [
    ("Q1",  "Indicateurs synthétiques",        "Cartes du haut du dashboard"),
    ("Q2",  "Météo des 7 derniers jours",      "Graphique courbe"),
    ("Q3",  "Météo moyenne sur 30 jours",      "Indicateur synthétique"),
    ("Q4",  "Dernier état de chaque parcelle", "Liste avec badges de statut"),
    ("Q5",  "Alertes actives triées",          "Widget alertes"),
    ("Q6",  "Répartition des cultures",        "Diagramme camembert"),
    ("Q7",  "Répartition par état d'observation", "Diagramme barres"),
    ("Q8",  "Historique d'une parcelle",       "Page détail parcelle"),
    ("Q9",  "Détection de risques (règles)",   "Génération automatique d'alertes"),
    ("Q10", "Top 5 parcelles les plus alertées", "Indicateur de pilotage"),
    ("Q11", "Évolution des alertes par jour",  "Graphique temporel"),
    ("Q12", "Trigger SQL observation→alerte",  "Création auto d'alertes"),
]:
    row = t.add_row().cells
    row[0].text = c; row[1].text = o; row[2].text = u
    for cell in row:
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.size = Pt(10); run.font.name = "Calibri"

add_paragraph(doc, "")
add_heading(doc, "Exemple : Q4 — Dernier état de chaque parcelle", level=2, color=SECONDARY)
add_code(doc, """SELECT
    p.id_parcelle,
    p.nom,
    p.localisation,
    p.surface_ha,
    c.type           AS culture,
    o.date           AS derniere_observation,
    o.etat           AS dernier_etat,
    o.commentaire
FROM parcelle p
LEFT JOIN culture c
       ON c.id_parcelle = p.id_parcelle
LEFT JOIN observation o
       ON o.id_observation = (
           SELECT o2.id_observation FROM observation o2
           WHERE o2.id_parcelle = p.id_parcelle
           ORDER BY o2.date DESC, o2.id_observation DESC
           LIMIT 1
       )
ORDER BY p.id_parcelle;""")

add_paragraph(doc, "Résultat sur le jeu de données fourni (10 lignes) :")
res = doc.add_table(rows=1, cols=5)
res.style = "Light Grid Accent 1"
add_table_header(res, ["Parcelle", "Zone", "Culture", "Dernière obs.", "État"])
for nom, zone, cult, d, etat in [
    ("Parcelle 1",  "Zone A", "Orge",      "2026-04-28", "OK"),
    ("Parcelle 2",  "Zone B", "Tournesol", "2026-04-19", "Maladie détectée"),
    ("Parcelle 3",  "Zone C", "Blé",       "2026-04-28", "Maladie détectée"),
    ("Parcelle 4",  "Zone D", "Maïs",      "2026-04-27", "Stress hydrique"),
    ("Parcelle 5",  "Zone E", "Blé",       "2026-04-28", "Stress hydrique"),
    ("Parcelle 6",  "Zone A", "Tournesol", "2026-04-15", "Stress hydrique"),
    ("Parcelle 7",  "Zone B", "Orge",      "2026-04-22", "Stress hydrique"),
    ("Parcelle 8",  "Zone C", "Tournesol", "2026-04-17", "OK"),
    ("Parcelle 9",  "Zone D", "Colza",     "2026-04-19", "Maladie détectée"),
    ("Parcelle 10", "Zone E", "Colza",     "2026-04-28", "OK"),
]:
    row = res.add_row().cells
    row[0].text = nom; row[1].text = zone; row[2].text = cult
    row[3].text = d; row[4].text = etat
    for c in row:
        for para in c.paragraphs:
            for run in para.runs:
                run.font.size = Pt(9); run.font.name = "Calibri"

doc.add_page_break()

# ============================================================
# 8. RÈGLES MÉTIER
# ============================================================
add_heading(doc, "8. Logique d'analyse et règles métier", level=1)

add_paragraph(doc,
    "La logique d'analyse repose sur un croisement entre les données météo et les "
    "observations terrain. Quatre règles principales sont implémentées dans la "
    "requête Q9 et peuvent générer automatiquement des alertes."
)

t = doc.add_table(rows=1, cols=4)
t.style = "Light Grid Accent 1"
add_table_header(t, ["Code", "Règle", "Condition", "Niveau"])
for c, n, cond, niv in [
    ("R1", "Stress hydrique probable",
        "pluie totale 14j < 10 mm ET temp moyenne > 20°C", "2 (Modéré)"),
    ("R2", "Risque maladie cryptogamique",
        "humidité moyenne 14j > 70% ET temp moyenne > 15°C", "2 (Modéré)"),
    ("R3", "Coup de chaleur",
        "au moins 1 jour à temp ≥ 30°C dans la période", "3 (Élevé)"),
    ("R4", "Excès d'eau",
        "pluie totale 14j > 60 mm", "2 (Modéré)"),
]:
    row = t.add_row().cells
    row[0].text = c; row[1].text = n; row[2].text = cond; row[3].text = niv
    for cell in row:
        for para in cell.paragraphs:
            for run in para.runs:
                run.font.size = Pt(10); run.font.name = "Calibri"

add_paragraph(doc, "")
add_paragraph(doc,
    "Exemple : sur les 14 derniers jours du dataset (15/04 → 29/04), la moyenne "
    "d'humidité est de 73,5 % et la température moyenne de 16,2 °C — la règle R2 "
    "(Risque maladie cryptogamique) se déclenche pour l'ensemble des parcelles. "
    "C'est cohérent avec les observations terrain : 25 cas de Risque maladie et "
    "25 cas de Maladie détectée sur 100 observations.")

add_paragraph(doc, "Trigger SQL associé :", bold=True)
add_paragraph(doc,
    "Un trigger MySQL est défini pour créer automatiquement une alerte chaque fois "
    "qu'une observation à risque est saisie (voir Q12).")

doc.add_page_break()

# ============================================================
# 9. LIMITES & ÉVOLUTIONS
# ============================================================
add_heading(doc, "9. Limites, hypothèses et évolutions", level=1)

add_paragraph(doc, "Hypothèses retenues dans le MVP :", bold=True)
add_bullet(doc, "La météo est journalière et globale (1 station par exploitation), pas par parcelle.")
add_bullet(doc, "Une seule culture active par parcelle à un instant T (extension possible : table de rotations).")
add_bullet(doc, "Les seuils des règles métier sont fixes (V2 : seuils par type de culture).")
add_bullet(doc, "L'authentification est simulée par hash bcrypt — JWT côté backend.")

add_paragraph(doc, "Limites du dataset :", bold=True)
add_bullet(doc, "Période courte (60 jours) : pas de saisonnalité observable.")
add_bullet(doc, "Échantillon réduit (10 parcelles) : statistiques peu robustes.")
add_bullet(doc, "Pas de coordonnées GPS : la géolocalisation reste textuelle (Zone A-E).")

add_paragraph(doc, "Évolutions possibles (V2 / V3) :", bold=True)
add_bullet(doc, "Ajout d'une table station_meteo et FK parcelle.id_station pour une météo locale.")
add_bullet(doc, "Table seuil_alerte paramétrable par type de culture et par règle.")
add_bullet(doc, "Table photo (FK observation) pour stocker les clichés terrain.")
add_bullet(doc, "Historisation des cultures (rotation : table parcelle_culture avec date_debut/date_fin).")
add_bullet(doc, "Géolocalisation GPS (lat, lng) pour la cartographie sur le dashboard.")
add_bullet(doc, "Connexion à une API météo externe (Météo France, Open-Meteo) pour l'auto-alimentation.")

# ---------- Footer ----------
add_paragraph(doc, "")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("— Fin du document —")
r.font.italic = True; r.font.size = Pt(10); r.font.color.rgb = GREY; r.font.name = "Calibri"

# Save
doc.save(OUTPUT)

# Post-traitement : retirer le w:zoom invalide qui empêche la validation OOXML
import zipfile, shutil, re
tmp_out = OUTPUT + ".tmp"
with zipfile.ZipFile(OUTPUT, "r") as zin, zipfile.ZipFile(tmp_out, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.namelist():
        data = zin.read(item)
        if item == "word/settings.xml":
            data = re.sub(rb'<w:zoom[^/]*/>', b'', data)
        zout.writestr(item, data)
shutil.move(tmp_out, OUTPUT)

print(f"Document généré : {OUTPUT}")
print(f"Taille : {os.path.getsize(OUTPUT) / 1024:.1f} KB")
