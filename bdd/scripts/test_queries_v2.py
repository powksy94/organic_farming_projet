"""Test rapide des requêtes corrigées."""
import sqlite3
conn = sqlite3.connect("/tmp/test_agri.db")
cur = conn.cursor()

print("=== Q4 corrigée (1 ligne par parcelle) ===")
cur.execute("""
SELECT p.nom, p.localisation, c.type, o.date, o.etat
FROM parcelle p
LEFT JOIN culture c ON c.id_parcelle = p.id_parcelle
LEFT JOIN observation o
       ON o.id_observation = (
           SELECT o2.id_observation FROM observation o2
           WHERE o2.id_parcelle = p.id_parcelle
           ORDER BY o2.date DESC, o2.id_observation DESC
           LIMIT 1
       )
ORDER BY p.id_parcelle
""")
rows = cur.fetchall()
print(f"  {len(rows)} lignes (attendu : 10)")
for r in rows:
    print(f"  - {r[0]:<14} {r[1]:<8} {r[2] or '-':<10} {r[3] or '-':<14} {r[4] or '-'}")

print("\n=== Q9 ajustée (sur 14 jours, seuils plus larges) ===")
cur.execute("""
WITH meteo_recente AS (
    SELECT AVG(temperature) AS temp_moy, AVG(humidite) AS hum_moy,
           SUM(pluie_mm) AS pluie_14j, MAX(temperature) AS temp_max
    FROM meteo WHERE date >= date((SELECT MAX(date) FROM meteo), '-14 day')
)
SELECT p.nom, p.localisation, c.type,
    CASE
        WHEN (mr.pluie_14j < 10 AND mr.temp_moy > 20) THEN 'Stress hydrique probable'
        WHEN (mr.hum_moy > 70 AND mr.temp_moy > 15) THEN 'Risque maladie cryptogamique'
        WHEN (mr.temp_max >= 30) THEN 'Coup de chaleur'
        WHEN (mr.pluie_14j > 60) THEN 'Excès d''eau'
        ELSE 'RAS'
    END AS risque,
    ROUND(mr.temp_moy,1), ROUND(mr.hum_moy,1), ROUND(mr.pluie_14j,1), ROUND(mr.temp_max,1)
FROM parcelle p
LEFT JOIN culture c ON c.id_parcelle = p.id_parcelle
CROSS JOIN meteo_recente mr
""")
risque_count = 0
for nom, loc, cult, risque, tm, hm, pl, tx in cur.fetchall():
    print(f"  {nom:<14} {(cult or '-'):<10} → {risque:<32}  T°moy={tm} Hum={hm}% Pluie14j={pl}mm Tmax={tx}")
    if risque != 'RAS':
        risque_count += 1
print(f"  >> {risque_count} parcelles à risque détectées")
conn.close()
