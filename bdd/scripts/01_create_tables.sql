-- =====================================================================
--  Projet B2 Sup de Vinci - Agriculture
--  Script de création de la base de données
--  SGBD : MySQL 8.0 / MariaDB 10.x
--  Auteur : Équipe projet (P3 - Base de données)
-- =====================================================================

-- Création de la base
DROP DATABASE IF EXISTS agri_db;
CREATE DATABASE agri_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE agri_db;

-- =====================================================================
--  Table : utilisateur
--  Gestion des comptes (agriculteurs, technicien Chambre d'Agriculture)
-- =====================================================================
CREATE TABLE utilisateur (
    id_utilisateur   INT AUTO_INCREMENT PRIMARY KEY,
    nom              VARCHAR(80)  NOT NULL,
    email            VARCHAR(120) NOT NULL UNIQUE,
    mot_de_passe     VARCHAR(255) NOT NULL,            -- hash bcrypt
    role             ENUM('agriculteur','technicien','admin') NOT NULL DEFAULT 'agriculteur',
    date_creation    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- =====================================================================
--  Table : parcelle
--  Une parcelle agricole, rattachée à un utilisateur
-- =====================================================================
CREATE TABLE parcelle (
    id_parcelle      INT AUTO_INCREMENT PRIMARY KEY,
    nom              VARCHAR(80)  NOT NULL,
    localisation     VARCHAR(60)  NOT NULL,             -- ex : "Zone A"
    surface_ha       DECIMAL(6,2) NOT NULL CHECK (surface_ha > 0),
    id_utilisateur   INT NULL,
    CONSTRAINT fk_parcelle_utilisateur
        FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur)
        ON DELETE SET NULL
) ENGINE=InnoDB;

-- =====================================================================
--  Table : culture
--  Une culture (Blé, Orge, Maïs...) plantée sur une parcelle
-- =====================================================================
CREATE TABLE culture (
    id_culture       INT AUTO_INCREMENT PRIMARY KEY,
    type             VARCHAR(50) NOT NULL,
    date_semis       DATE        NOT NULL,
    id_parcelle      INT         NOT NULL,
    CONSTRAINT fk_culture_parcelle
        FOREIGN KEY (id_parcelle) REFERENCES parcelle(id_parcelle)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- =====================================================================
--  Table : meteo
--  Conditions météo journalières (clé = date)
-- =====================================================================
CREATE TABLE meteo (
    date             DATE         PRIMARY KEY,
    temperature      DECIMAL(4,1) NOT NULL,             -- en °C
    humidite         DECIMAL(5,1) NOT NULL,             -- en %
    pluie_mm         DECIMAL(5,1) NOT NULL DEFAULT 0    -- en mm
) ENGINE=InnoDB;

-- =====================================================================
--  Table : observation
--  Observation terrain saisie sur une parcelle
-- =====================================================================
CREATE TABLE observation (
    id_observation   INT AUTO_INCREMENT PRIMARY KEY,
    date             DATE         NOT NULL,
    etat             VARCHAR(40)  NOT NULL,             -- OK / Risque maladie / Stress hydrique / Maladie détectée
    commentaire      VARCHAR(255) NULL,
    id_parcelle      INT          NOT NULL,
    CONSTRAINT fk_observation_parcelle
        FOREIGN KEY (id_parcelle) REFERENCES parcelle(id_parcelle)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- =====================================================================
--  Table : alerte
--  Alerte générée automatiquement (règles métier) ou manuellement
-- =====================================================================
CREATE TABLE alerte (
    id_alerte        INT AUTO_INCREMENT PRIMARY KEY,
    date             DATE         NOT NULL,
    type             VARCHAR(40)  NOT NULL,             -- Stress hydrique / Risque maladie / ...
    niveau           TINYINT      NOT NULL CHECK (niveau BETWEEN 1 AND 3),
    statut           VARCHAR(20)  NOT NULL DEFAULT 'active',  -- active / résolue / ignorée
    id_parcelle      INT          NOT NULL,
    CONSTRAINT fk_alerte_parcelle
        FOREIGN KEY (id_parcelle) REFERENCES parcelle(id_parcelle)
        ON DELETE CASCADE
) ENGINE=InnoDB;

-- =====================================================================
--  Index pour optimiser les requêtes du dashboard
-- =====================================================================
CREATE INDEX idx_observation_parcelle_date ON observation(id_parcelle, date);
CREATE INDEX idx_alerte_parcelle_date      ON alerte(id_parcelle, date);
CREATE INDEX idx_alerte_statut             ON alerte(statut);
CREATE INDEX idx_meteo_date                ON meteo(date);

-- =====================================================================
--  Données de démonstration (utilisateur)
-- =====================================================================
INSERT INTO utilisateur (nom, email, mot_de_passe, role) VALUES
('Admin Démo',     'admin@chambre-agri.fr',     '$2b$12$DEMOHASHADMIN',   'admin'),
('Jean Dupont',    'jean.dupont@ferme.fr',      '$2b$12$DEMOHASHJEAN',    'agriculteur'),
('Marie Martin',   'marie.martin@ferme.fr',     '$2b$12$DEMOHASHMARIE',   'agriculteur'),
('Tech Conseil',   'conseil@chambre-agri.fr',   '$2b$12$DEMOHASHTECH',    'technicien');
