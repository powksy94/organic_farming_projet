-- =====================================================================
--  Projet B2 Sup de Vinci - Agriculture
--  Requêtes SQL pour le tableau de bord (dashboard)
--  SGBD : MySQL 8 / MariaDB 10
--
--  Chaque section contient une requête à brancher sur le frontend.
--  Les requêtes sont commentées et numérotées pour être réutilisées
--  côté backend (Flask / PHP / Java).
-- =====================================================================

USE agri_db;

-- =====================================================================
-- [Q1] Indicateurs synthétiques (cartes du haut du dashboard)
--      Nombre de parcelles, surface totale, nombre de cultures actives,
--      nombre d'alertes actives.
-- =====================================================================
SELECT
    (SELECT COUNT(*) FROM parcelle)                                  AS nb_parcelles,
    (SELECT ROUND(SUM(surface_ha), 2) FROM parcelle)                 AS surface_totale_ha,
    (SELECT COUNT(*) FROM culture)                                   AS nb_cultures,
    (SELECT COUNT(*) FROM alerte WHERE statut = 'active')            AS nb_alertes_actives,
    (SELECT COUNT(*) FROM alerte WHERE statut = 'active' AND niveau = 3)
                                                                     AS nb_alertes_critiques;

-- =====================================================================
-- [Q2] Météo des 7 derniers jours
--      Pour le graphique en courbe sur le dashboard.
-- =====================================================================
SELECT
    date,
    temperature,
    humidite,
    pluie_mm
FROM meteo
ORDER BY date DESC
LIMIT 7;

-- =====================================================================
-- [Q3] Moyenne météo des 30 derniers jours
--      Indicateur synthétique en haut du tableau de bord.
-- =====================================================================
SELECT
    ROUND(AVG(temperature), 1) AS temp_moyenne,
    ROUND(AVG(humidite), 1)    AS humidite_moyenne,
    ROUND(SUM(pluie_mm), 1)    AS pluie_totale_mm,
    COUNT(*)                   AS jours
FROM meteo
WHERE date >= (SELECT MAX(date) FROM meteo) - INTERVAL 30 DAY;

-- =====================================================================
-- [Q4] État courant de chaque parcelle (dernière observation connue)
--      Utile pour la liste des parcelles avec un badge de statut.
--      MAX(id_observation) garantit qu'on prend une seule ligne par
--      parcelle même si plusieurs observations ont la même date.
-- =====================================================================
SELECT
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
           SELECT o2.id_observation
           FROM observation o2
           WHERE o2.id_parcelle = p.id_parcelle
           ORDER BY o2.date DESC, o2.id_observation DESC
           LIMIT 1
       )
ORDER BY p.id_parcelle;

-- =====================================================================
-- [Q5] Liste des alertes actives, triées par gravité puis date
--      Affichée en page "Alertes" et en widget rouge du dashboard.
-- =====================================================================
SELECT
    a.id_alerte,
    a.date,
    a.type,
    a.niveau,
    CASE a.niveau
        WHEN 1 THEN 'Faible'
        WHEN 2 THEN 'Modéré'
        WHEN 3 THEN 'Élevé'
    END AS niveau_libelle,
    p.nom            AS parcelle,
    p.localisation
FROM alerte a
JOIN parcelle p ON p.id_parcelle = a.id_parcelle
WHERE a.statut = 'active'
ORDER BY a.niveau DESC, a.date DESC
LIMIT 50;

-- =====================================================================
-- [Q6] Répartition des cultures (camembert)
-- =====================================================================
SELECT
    c.type                    AS culture,
    COUNT(*)                  AS nb_parcelles,
    ROUND(SUM(p.surface_ha),2) AS surface_ha
FROM culture c
JOIN parcelle p ON p.id_parcelle = c.id_parcelle
GROUP BY c.type
ORDER BY surface_ha DESC;

-- =====================================================================
-- [Q7] Répartition des observations par état (barres)
-- =====================================================================
SELECT
    etat,
    COUNT(*) AS nb_observations
FROM observation
GROUP BY etat
ORDER BY nb_observations DESC;

-- =====================================================================
-- [Q8] Historique des observations d'une parcelle (param :id_parcelle)
--      Utilisé sur la page "détail parcelle".
-- =====================================================================
SELECT
    o.date,
    o.etat,
    o.commentaire,
    m.temperature,
    m.humidite,
    m.pluie_mm
FROM observation o
LEFT JOIN meteo m ON m.date = o.date
WHERE o.id_parcelle = :id_parcelle      -- paramètre à binder côté backend
ORDER BY o.date DESC;

-- =====================================================================
-- [Q9] DÉTECTION AUTOMATIQUE DE RISQUES (règles métier)
--      Cette requête est le cœur de la logique d'analyse.
--      Elle croise météo + observations pour identifier les parcelles
--      en situation à risque sur les 7 derniers jours.
--
--      Règles métier (seuils ajustables par culture en V2) :
--        R1) Stress hydrique : pluie totale 14j < 10 mm ET temp moyenne > 20°C
--        R2) Risque maladie  : humidité moyenne 14j > 70% ET temp moyenne > 15°C
--        R3) Coup de chaleur : au moins 1 jour à temp >= 30°C sur la période
--        R4) Excès d'eau     : pluie totale 14j > 60 mm
-- =====================================================================
WITH meteo_recente AS (
    SELECT
        AVG(temperature) AS temp_moy,
        AVG(humidite)    AS hum_moy,
        SUM(pluie_mm)    AS pluie_14j,
        MAX(temperature) AS temp_max
    FROM meteo
    WHERE date >= (SELECT MAX(date) FROM meteo) - INTERVAL 14 DAY
)
SELECT
    p.id_parcelle,
    p.nom,
    p.localisation,
    c.type AS culture,
    CASE
        WHEN (mr.pluie_14j < 10 AND mr.temp_moy > 20)
            THEN 'Stress hydrique probable'
        WHEN (mr.hum_moy > 70 AND mr.temp_moy > 15)
            THEN 'Risque maladie cryptogamique'
        WHEN (mr.temp_max >= 30)
            THEN 'Coup de chaleur'
        WHEN (mr.pluie_14j > 60)
            THEN 'Excès d''eau'
        ELSE 'RAS'
    END AS risque_detecte,
    ROUND(mr.temp_moy, 1)  AS temp_moy_14j,
    ROUND(mr.hum_moy, 1)   AS hum_moy_14j,
    ROUND(mr.pluie_14j, 1) AS pluie_14j,
    ROUND(mr.temp_max, 1)  AS temp_max_14j
FROM parcelle p
LEFT JOIN culture c ON c.id_parcelle = p.id_parcelle
CROSS JOIN meteo_recente mr
HAVING risque_detecte <> 'RAS'
ORDER BY p.id_parcelle;

-- =====================================================================
-- [Q10] Top 5 des parcelles les plus alertées (sur toute la période)
-- =====================================================================
SELECT
    p.nom,
    p.localisation,
    COUNT(a.id_alerte)            AS nb_alertes,
    SUM(a.niveau)                 AS gravite_cumulee
FROM parcelle p
LEFT JOIN alerte a ON a.id_parcelle = p.id_parcelle
GROUP BY p.id_parcelle, p.nom, p.localisation
ORDER BY nb_alertes DESC, gravite_cumulee DESC
LIMIT 5;

-- =====================================================================
-- [Q11] Évolution journalière du nombre d'alertes (graphique temporel)
-- =====================================================================
SELECT
    a.date,
    COUNT(*)                       AS nb_alertes,
    SUM(CASE WHEN a.niveau = 3 THEN 1 ELSE 0 END) AS nb_critiques
FROM alerte a
GROUP BY a.date
ORDER BY a.date;

-- =====================================================================
-- [Q12] Insertion automatique d'une alerte quand une observation
--       remonte un état "Risque maladie" ou "Stress hydrique"
--       (à exécuter côté backend après chaque INSERT observation,
--        ou via un trigger SQL — exemple ci-dessous).
-- =====================================================================
DELIMITER //

CREATE TRIGGER trg_observation_to_alerte
AFTER INSERT ON observation
FOR EACH ROW
BEGIN
    IF NEW.etat IN ('Risque maladie', 'Stress hydrique', 'Maladie détectée') THEN
        INSERT INTO alerte (date, type, niveau, statut, id_parcelle)
        VALUES (
            NEW.date,
            NEW.etat,
            CASE NEW.etat
                WHEN 'Maladie détectée' THEN 3
                WHEN 'Risque maladie'   THEN 2
                ELSE                          2
            END,
            'active',
            NEW.id_parcelle
        );
    END IF;
END;
//

DELIMITER ;
