"""
Génère les schémas MCD et MLD en SVG haute qualité.
Auteur : Projet B2 Sup de Vinci - Agriculture
"""
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "schemas")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== MCD (Modèle Conceptuel de Données) =====
MCD = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" font-family="Arial, sans-serif">
  <style>
    .entity { fill: #E3F2FD; stroke: #1565C0; stroke-width: 2; }
    .entity-header { fill: #1565C0; }
    .entity-title { fill: white; font-weight: bold; font-size: 14px; text-anchor: middle; }
    .entity-attr { fill: #0D47A1; font-size: 12px; }
    .entity-pk { font-weight: bold; text-decoration: underline; }
    .assoc { fill: #FFF3E0; stroke: #E65100; stroke-width: 2; }
    .assoc-text { fill: #BF360C; font-size: 12px; font-weight: bold; text-anchor: middle; }
    .link { stroke: #424242; stroke-width: 1.5; fill: none; }
    .card { fill: #424242; font-size: 11px; font-weight: bold; }
    .title { fill: #1A237E; font-size: 22px; font-weight: bold; text-anchor: middle; }
  </style>

  <text x="600" y="30" class="title">MCD - Modèle Conceptuel de Données</text>
  <text x="600" y="52" font-size="13" text-anchor="middle" fill="#555">Projet Agriculture - Suivi des cultures et aide à la décision</text>

  <!-- UTILISATEUR -->
  <rect x="40" y="100" width="180" height="130" rx="6" class="entity"/>
  <rect x="40" y="100" width="180" height="28" rx="6" class="entity-header"/>
  <text x="130" y="120" class="entity-title">UTILISATEUR</text>
  <text x="55" y="148" class="entity-attr entity-pk">id_utilisateur</text>
  <text x="55" y="168" class="entity-attr">nom</text>
  <text x="55" y="186" class="entity-attr">email</text>
  <text x="55" y="204" class="entity-attr">mot_de_passe</text>
  <text x="55" y="222" class="entity-attr">role</text>

  <!-- PARCELLE -->
  <rect x="500" y="100" width="180" height="130" rx="6" class="entity"/>
  <rect x="500" y="100" width="180" height="28" rx="6" class="entity-header"/>
  <text x="590" y="120" class="entity-title">PARCELLE</text>
  <text x="515" y="148" class="entity-attr entity-pk">id_parcelle</text>
  <text x="515" y="168" class="entity-attr">nom</text>
  <text x="515" y="186" class="entity-attr">localisation</text>
  <text x="515" y="204" class="entity-attr">surface_ha</text>

  <!-- CULTURE -->
  <rect x="960" y="100" width="180" height="115" rx="6" class="entity"/>
  <rect x="960" y="100" width="180" height="28" rx="6" class="entity-header"/>
  <text x="1050" y="120" class="entity-title">CULTURE</text>
  <text x="975" y="148" class="entity-attr entity-pk">id_culture</text>
  <text x="975" y="168" class="entity-attr">type</text>
  <text x="975" y="186" class="entity-attr">date_semis</text>

  <!-- OBSERVATION -->
  <rect x="40" y="430" width="180" height="130" rx="6" class="entity"/>
  <rect x="40" y="430" width="180" height="28" rx="6" class="entity-header"/>
  <text x="130" y="450" class="entity-title">OBSERVATION</text>
  <text x="55" y="478" class="entity-attr entity-pk">id_observation</text>
  <text x="55" y="498" class="entity-attr">date</text>
  <text x="55" y="516" class="entity-attr">etat</text>
  <text x="55" y="534" class="entity-attr">commentaire</text>

  <!-- ALERTE -->
  <rect x="500" y="600" width="180" height="130" rx="6" class="entity"/>
  <rect x="500" y="600" width="180" height="28" rx="6" class="entity-header"/>
  <text x="590" y="620" class="entity-title">ALERTE</text>
  <text x="515" y="648" class="entity-attr entity-pk">id_alerte</text>
  <text x="515" y="668" class="entity-attr">date</text>
  <text x="515" y="686" class="entity-attr">type</text>
  <text x="515" y="704" class="entity-attr">niveau</text>

  <!-- METEO -->
  <rect x="960" y="430" width="180" height="130" rx="6" class="entity"/>
  <rect x="960" y="430" width="180" height="28" rx="6" class="entity-header"/>
  <text x="1050" y="450" class="entity-title">METEO</text>
  <text x="975" y="478" class="entity-attr entity-pk">date</text>
  <text x="975" y="498" class="entity-attr">temperature</text>
  <text x="975" y="516" class="entity-attr">humidite</text>
  <text x="975" y="534" class="entity-attr">pluie_mm</text>

  <!-- Association GERE (Utilisateur - Parcelle) -->
  <ellipse cx="360" cy="165" rx="55" ry="28" class="assoc"/>
  <text x="360" y="170" class="assoc-text">GÈRE</text>
  <line x1="220" y1="165" x2="305" y2="165" class="link"/>
  <line x1="415" y1="165" x2="500" y2="165" class="link"/>
  <text x="232" y="158" class="card">1,n</text>
  <text x="478" y="158" class="card">1,1</text>

  <!-- Association CULTIVE (Parcelle - Culture) -->
  <ellipse cx="820" cy="165" rx="55" ry="28" class="assoc"/>
  <text x="820" y="170" class="assoc-text">CULTIVE</text>
  <line x1="680" y1="165" x2="765" y2="165" class="link"/>
  <line x1="875" y1="165" x2="960" y2="165" class="link"/>
  <text x="690" y="158" class="card">1,n</text>
  <text x="935" y="158" class="card">1,1</text>

  <!-- Association CONCERNE (Observation - Parcelle) -->
  <ellipse cx="360" cy="380" rx="60" ry="28" class="assoc"/>
  <text x="360" y="385" class="assoc-text">CONCERNE</text>
  <line x1="160" y1="430" x2="350" y2="408" class="link"/>
  <line x1="555" y1="230" x2="395" y2="358" class="link"/>
  <text x="220" y="395" class="card">1,1</text>
  <text x="430" y="320" class="card">1,n</text>

  <!-- Association DECLENCHE (Parcelle - Alerte) -->
  <ellipse cx="445" cy="455" rx="60" ry="28" class="assoc"/>
  <text x="445" y="460" class="assoc-text">DÉCLENCHE</text>
  <line x1="555" y1="230" x2="450" y2="425" class="link"/>
  <line x1="500" y1="600" x2="455" y2="485" class="link"/>
  <text x="535" y="335" class="card">1,n</text>
  <text x="450" y="540" class="card">1,1</text>

  <!-- Association OBSERVE_METEO (Observation - Météo) -->
  <ellipse cx="600" cy="495" rx="55" ry="28" class="assoc"/>
  <text x="600" y="500" class="assoc-text">DATÉE</text>
  <line x1="220" y1="495" x2="545" y2="495" class="link"/>
  <line x1="655" y1="495" x2="960" y2="495" class="link"/>
  <text x="232" y="488" class="card">1,1</text>
  <text x="940" y="488" class="card">0,n</text>

  <!-- Légende -->
  <rect x="40" y="710" width="450" height="80" fill="#FAFAFA" stroke="#9E9E9E" stroke-width="1" rx="4"/>
  <text x="55" y="730" font-size="12" font-weight="bold" fill="#212121">Légende :</text>
  <rect x="55" y="740" width="20" height="14" class="entity"/>
  <text x="80" y="752" font-size="11" fill="#212121">Entité</text>
  <ellipse cx="155" cy="747" rx="20" ry="10" class="assoc"/>
  <text x="180" y="752" font-size="11" fill="#212121">Association</text>
  <text x="260" y="752" font-size="11" fill="#212121">(min,max) = cardinalités</text>
  <text x="55" y="775" font-size="11" fill="#555">PK = clé primaire (souligné)</text>
</svg>
"""

with open(os.path.join(OUTPUT_DIR, "MCD.svg"), "w", encoding="utf-8") as f:
    f.write(MCD)

# ===== MLD (Modèle Logique de Données) =====
MLD = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1300 850" font-family="Arial, sans-serif">
  <style>
    .table { fill: #F1F8E9; stroke: #2E7D32; stroke-width: 2; }
    .table-header { fill: #2E7D32; }
    .table-title { fill: white; font-weight: bold; font-size: 14px; text-anchor: middle; }
    .row { font-size: 11.5px; fill: #1B5E20; }
    .pk { font-weight: bold; }
    .fk { font-style: italic; fill: #BF360C; }
    .link { stroke: #424242; stroke-width: 1.5; fill: none; marker-end: url(#arrow); }
    .title { fill: #1A237E; font-size: 22px; font-weight: bold; text-anchor: middle; }
    .legend { fill: #FAFAFA; stroke: #9E9E9E; stroke-width: 1; }
  </style>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#424242"/>
    </marker>
  </defs>

  <text x="650" y="30" class="title">MLD - Modèle Logique de Données</text>
  <text x="650" y="52" font-size="13" text-anchor="middle" fill="#555">Tables relationnelles, clés primaires (PK) et étrangères (FK)</text>

  <!-- UTILISATEUR -->
  <rect x="40" y="100" width="220" height="170" rx="6" class="table"/>
  <rect x="40" y="100" width="220" height="28" rx="6" class="table-header"/>
  <text x="150" y="120" class="table-title">utilisateur</text>
  <text x="55" y="148" class="row pk">PK  id_utilisateur     INT</text>
  <text x="55" y="168" class="row">       nom                VARCHAR(80)</text>
  <text x="55" y="186" class="row">       email              VARCHAR(120)</text>
  <text x="55" y="204" class="row">       mot_de_passe       VARCHAR(255)</text>
  <text x="55" y="222" class="row">       role               VARCHAR(30)</text>
  <text x="55" y="240" class="row">       date_creation      DATETIME</text>

  <!-- PARCELLE -->
  <rect x="380" y="100" width="240" height="170" rx="6" class="table"/>
  <rect x="380" y="100" width="240" height="28" rx="6" class="table-header"/>
  <text x="500" y="120" class="table-title">parcelle</text>
  <text x="395" y="148" class="row pk">PK  id_parcelle        INT</text>
  <text x="395" y="168" class="row">       nom                VARCHAR(80)</text>
  <text x="395" y="186" class="row">       localisation       VARCHAR(60)</text>
  <text x="395" y="204" class="row">       surface_ha         DECIMAL(6,2)</text>
  <text x="395" y="222" class="row fk">FK  id_utilisateur     INT</text>

  <!-- CULTURE -->
  <rect x="740" y="100" width="240" height="170" rx="6" class="table"/>
  <rect x="740" y="100" width="240" height="28" rx="6" class="table-header"/>
  <text x="860" y="120" class="table-title">culture</text>
  <text x="755" y="148" class="row pk">PK  id_culture         INT</text>
  <text x="755" y="168" class="row">       type               VARCHAR(50)</text>
  <text x="755" y="186" class="row">       date_semis         DATE</text>
  <text x="755" y="204" class="row fk">FK  id_parcelle        INT</text>

  <!-- METEO -->
  <rect x="1060" y="100" width="220" height="170" rx="6" class="table"/>
  <rect x="1060" y="100" width="220" height="28" rx="6" class="table-header"/>
  <text x="1170" y="120" class="table-title">meteo</text>
  <text x="1075" y="148" class="row pk">PK  date              DATE</text>
  <text x="1075" y="168" class="row">       temperature       DECIMAL(4,1)</text>
  <text x="1075" y="186" class="row">       humidite          DECIMAL(5,1)</text>
  <text x="1075" y="204" class="row">       pluie_mm          DECIMAL(5,1)</text>

  <!-- OBSERVATION -->
  <rect x="200" y="500" width="260" height="180" rx="6" class="table"/>
  <rect x="200" y="500" width="260" height="28" rx="6" class="table-header"/>
  <text x="330" y="520" class="table-title">observation</text>
  <text x="215" y="548" class="row pk">PK  id_observation     INT</text>
  <text x="215" y="568" class="row">       date               DATE</text>
  <text x="215" y="586" class="row">       etat               VARCHAR(40)</text>
  <text x="215" y="604" class="row">       commentaire        VARCHAR(255)</text>
  <text x="215" y="622" class="row fk">FK  id_parcelle        INT</text>

  <!-- ALERTE -->
  <rect x="600" y="500" width="260" height="200" rx="6" class="table"/>
  <rect x="600" y="500" width="260" height="28" rx="6" class="table-header"/>
  <text x="730" y="520" class="table-title">alerte</text>
  <text x="615" y="548" class="row pk">PK  id_alerte          INT</text>
  <text x="615" y="568" class="row">       date               DATE</text>
  <text x="615" y="586" class="row">       type               VARCHAR(40)</text>
  <text x="615" y="604" class="row">       niveau             TINYINT (1-3)</text>
  <text x="615" y="622" class="row">       statut             VARCHAR(20)</text>
  <text x="615" y="640" class="row fk">FK  id_parcelle        INT</text>

  <!-- Liens FK avec flèches -->
  <!-- utilisateur -> parcelle -->
  <path d="M 260 200 L 380 200" class="link"/>
  <text x="290" y="194" font-size="10" fill="#424242">1..n</text>

  <!-- parcelle -> culture -->
  <path d="M 620 200 L 740 200" class="link"/>
  <text x="650" y="194" font-size="10" fill="#424242">1..n</text>

  <!-- parcelle -> observation -->
  <path d="M 460 270 Q 400 380 330 500" class="link"/>
  <text x="370" y="380" font-size="10" fill="#424242">1..n</text>

  <!-- parcelle -> alerte -->
  <path d="M 540 270 Q 620 380 700 500" class="link"/>
  <text x="600" y="380" font-size="10" fill="#424242">1..n</text>

  <!-- meteo (date) référencée par observation/alerte (info) -->
  <path d="M 1060 200 Q 1000 380 860 540" stroke="#9E9E9E" stroke-width="1.5" fill="none" stroke-dasharray="5,5"/>
  <text x="970" y="380" font-size="10" fill="#9E9E9E">croisement par date</text>

  <!-- Légende -->
  <rect x="40" y="730" width="500" height="100" rx="4" class="legend"/>
  <text x="55" y="752" font-size="12" font-weight="bold" fill="#212121">Légende :</text>
  <text x="55" y="772" class="row pk">PK : clé primaire (Primary Key)</text>
  <text x="55" y="790" class="row fk">FK : clé étrangère (Foreign Key)</text>
  <line x1="55" y1="805" x2="105" y2="805" class="link"/>
  <text x="115" y="809" font-size="11" fill="#212121">Relation 1..n (intégrité référentielle)</text>
  <line x1="55" y1="822" x2="105" y2="822" stroke="#9E9E9E" stroke-width="1.5" stroke-dasharray="5,5"/>
  <text x="115" y="826" font-size="11" fill="#212121">Jointure logique (par date) sans FK directe</text>
</svg>
"""

with open(os.path.join(OUTPUT_DIR, "MLD.svg"), "w", encoding="utf-8") as f:
    f.write(MLD)

print(f"Schémas générés dans : {OUTPUT_DIR}")
print(" - MCD.svg")
print(" - MLD.svg")
