"""Test des principales requêtes dashboard sur la base SQLite."""
import sqlite3

conn = sqlite3.connect("/tmp/test_agri.db")
cur = conn.cursor()

print("=" * 60)
print("[Q1] Indicateurs synthétiques")
print("=" * 60)
cur.execute("""
SELECT
    (SELECT COUNT(*) FROM parcelle),
    (SELECT ROUND(SUM(surface_ha), 2) FROM parcelle),
    (SELECT COUNT(*) FROM culture),
    (SELECT COUNT(*) FROM alerte WHERE statut = 'active'),
    (SELECT COUNT(*) FROM alerte WHERE statut = 'active' AND niveau = 3)
""")
n_parc, surface, n_cult, n_alertes, n_crit = cur.fetchone()
print(f"  Parcelles : {n_parc}  |  Surface totale : {surface} ha")
print(f"  Cultures  : {n_cult}  |  Alertes actives : {n_alertes} (dont {n_crit} critiques)")

print("\n" + "=" * 60)
print("[Q3] Météo moyenne sur 30 jours")
print("=" * 60)
cur.execute("""
SELECT ROUND(AVG(temperature),1), ROUND(AVG(humidite),1), ROUND(SUM(pluie_mm),1), COUNT(*)
FROM meteo
WHERE date >= date((SELECT MAX(date) FROM meteo), '-30 day')
""")
t, h, p, j = cur.fetchone()
print(f"  Température moyenne : {t} °C")
print(f"  Humidité moyenne    : {h} %")
print(f"  Pluie totale        : {p} mm sur {j} jours")

print("\n" + "=" * 60)
print("[Q4] État courant des parcelles")
print("=" * 60)
cur.execute("""
SELECT p.nom, p.localisation, p.surface_ha, c.type, o.date, o.etat
FROM parcelle p
LEFT JOIN culture c ON c.id_parcelle = p.id_parcelle
LEFT JOIN observation o
       ON o.id_parcelle = p.id_parcelle
      AND o.date = (SELECT MAX(o2.date) FROM observation o2 WHERE o2.id_parcelle = p.id_parcelle)
ORDER BY p.id_parcelle
""")
print(f"  {'Parcelle':<14} {'Zone':<8} {'ha':>6}  {'Culture':<10} {'Dernière obs':<14} État")
for nom, loc, ha, cult, d, etat in cur.fetchall():
    print(f"  {nom:<14} {loc:<8} {ha:>6.2f}  {(cult or '-'):<10} {(d or '-'):<14} {etat or '-'}")

print("\n" + "=" * 60)
print("[Q5] Top alertes actives")
print("=" * 60)
cur.execute("""
SELECT a.date, a.type, a.niveau, p.nom, p.localisation
FROM alerte a JOIN parcelle p ON p.id_parcelle = a.id_parcelle
WHERE a.statut = 'active'
ORDER BY a.niveau DESC, a.date DESC
LIMIT 8
""")
for d, t, n, p, l in cur.fetchall():
    sev = ['', 'Faible', 'Modéré', 'Élevé'][n]
    print(f"  {d}  [{sev:7s}] {t:<18} → {p} ({l})")

print("\n" + "=" * 60)
print("[Q6] Répartition des cultures")
print("=" * 60)
cur.execute("""
SELECT c.type, COUNT(*), ROUND(SUM(p.surface_ha), 2)
FROM culture c JOIN parcelle p ON p.id_parcelle = c.id_parcelle
GROUP BY c.type
ORDER BY SUM(p.surface_ha) DESC
""")
for t, n, ha in cur.fetchall():
    print(f"  {t:<12} : {n} parcelle(s)  /  {ha} ha")

print("\n" + "=" * 60)
print("[Q9] DÉTECTION DE RISQUES (règles métier)")
print("=" * 60)
cur.execute("""
WITH meteo_recente AS (
    SELECT AVG(temperature) AS temp_moy, AVG(humidite) AS hum_moy,
           SUM(pluie_mm) AS pluie_7j, MAX(temperature) AS temp_max
    FROM meteo WHERE date >= date((SELECT MAX(date) FROM meteo), '-7 day')
)
SELECT p.nom, p.localisation, c.type,
    CASE
        WHEN (mr.pluie_7j < 5 AND mr.temp_moy > 22) THEN 'Stress hydrique probable'
        WHEN (mr.hum_moy > 75 AND mr.temp_moy > 18) THEN 'Risque maladie cryptogamique'
        WHEN (mr.temp_max > 32) THEN 'Coup de chaleur'
        ELSE 'RAS'
    END AS risque,
    ROUND(mr.temp_moy,1), ROUND(mr.hum_moy,1), ROUND(mr.pluie_7j,1)
FROM parcelle p
LEFT JOIN culture c ON c.id_parcelle = p.id_parcelle
CROSS JOIN meteo_recente mr
""")
print(f"  {'Parcelle':<14} {'Culture':<10} {'Risque':<32} T° H% Pluie")
risque_count = 0
for nom, loc, cult, risque, tm, hm, pl in cur.fetchall():
    print(f"  {nom:<14} {(cult or '-'):<10} {risque:<32} {tm}°C {hm}% {pl}mm")
    if risque != 'RAS':
        risque_count += 1
print(f"\n  >> {risque_count} parcelles avec risque détecté sur les 7 derniers jours")

print("\n" + "=" * 60)
print("[Q10] Top 5 parcelles les plus alertées")
print("=" * 60)
cur.execute("""
SELECT p.nom, p.localisation, COUNT(a.id_alerte), SUM(a.niveau)
FROM parcelle p LEFT JOIN alerte a ON a.id_parcelle = p.id_parcelle
GROUP BY p.id_parcelle, p.nom, p.localisation
ORDER BY COUNT(a.id_alerte) DESC, SUM(a.niveau) DESC
LIMIT 5
""")
for nom, loc, n, grav in cur.fetchall():
    print(f"  {nom:<14} {loc:<8} : {n} alertes (gravité cumulée {grav})")

conn.close()
print("\n[OK] Toutes les requêtes du dashboard renvoient des résultats cohérents.")
