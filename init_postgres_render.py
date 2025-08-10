#!/usr/bin/env python3
"""
Script pour initialiser la base de données PostgreSQL sur Render
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def init_postgres_render():
    """Initialise la base de données PostgreSQL sur Render"""

    print("🚀 Initialisation de la base de données PostgreSQL sur Render...")

    # Récupérer l'URL de la base de données depuis les variables d'environnement
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        print("❌ DATABASE_URL non définie")
        return

    try:
        # Se connecter à la base de données
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        print("✅ Connexion à PostgreSQL établie")

        # Créer la table users avec toutes les colonnes nécessaires
        print("📋 Création de la table users...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                password VARCHAR(120) NOT NULL,
                security_question VARCHAR(200),
                security_answer VARCHAR(120),
                display_currency BOOLEAN DEFAULT TRUE,
                display_progress BOOLEAN DEFAULT TRUE,
                notification_enabled BOOLEAN DEFAULT TRUE,
                auto_delete_completed BOOLEAN DEFAULT FALSE,
                auto_delete_days INTEGER DEFAULT 90,
                countdown_enabled BOOLEAN DEFAULT TRUE,
                countdown_days INTEGER DEFAULT 30,

                nom VARCHAR(100),
                prenom VARCHAR(100),
                date_naissance DATE,
                telephone VARCHAR(20),
                email VARCHAR(120),
                sexe VARCHAR(10),
                photo_profil VARCHAR(200),
                bio TEXT,
                adresse TEXT,
                ville VARCHAR(100),
                pays VARCHAR(100) DEFAULT 'Cameroun',
                date_creation_profil TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Créer la table objectifs
        print("📋 Création de la table objectifs...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS objectifs (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(200) NOT NULL,
                montant_cible DECIMAL(15,2) NOT NULL,
                montant_actuel DECIMAL(15,2) DEFAULT 0,
                date_limite DATE,
                status VARCHAR(20) DEFAULT 'actif',
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Créer la table transactions
        print("📋 Création de la table transactions...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                objectif_id INTEGER REFERENCES objectifs(id) ON DELETE CASCADE,
                montant DECIMAL(15,2) NOT NULL,
                type_transaction VARCHAR(20) NOT NULL,

                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                date_transaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Créer la table taches
        print("📋 Création de la table taches...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS taches (
                id SERIAL PRIMARY KEY,
                titre VARCHAR(200) NOT NULL,
                description TEXT,
                priorite VARCHAR(20) DEFAULT 'moyenne',
                status VARCHAR(20) DEFAULT 'en_cours',
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_limite DATE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        # Créer la table etapes
        print("📋 Création de la table etapes...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS etapes (
                id SERIAL PRIMARY KEY,
                tache_id INTEGER REFERENCES taches(id) ON DELETE CASCADE,
                description VARCHAR(200) NOT NULL,
                terminee BOOLEAN DEFAULT FALSE,
                ordre INTEGER DEFAULT 0
            )
        """)

        # Créer la table evenements
        print("📋 Création de la table evenements...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS evenements (
                id SERIAL PRIMARY KEY,
                titre VARCHAR(200) NOT NULL,
                description TEXT,
                date_debut TIMESTAMP NOT NULL,
                date_fin TIMESTAMP,
                lieu VARCHAR(200),
                type_evenement VARCHAR(50) DEFAULT 'general',
                rappel_minutes INTEGER DEFAULT 30,
                termine BOOLEAN DEFAULT FALSE,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Créer la table notifications
        print("📋 Création de la table notifications...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                titre VARCHAR(200) NOT NULL,
                message TEXT NOT NULL,
                type_notification VARCHAR(50) DEFAULT 'info',
                lue BOOLEAN DEFAULT FALSE,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Valider les changements
        conn.commit()
        print("✅ Toutes les tables ont été créées avec succès !")

        # Vérifier les tables créées
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)

        tables = cur.fetchall()
        print("\n📊 Tables créées :")
        for table in tables:
            print(f"   - {table[0]}")

        # Créer un utilisateur de test si aucun utilisateur n'existe
        cur.execute("SELECT COUNT(*) FROM users")
        user_count = cur.fetchone()[0]

        if user_count == 0:
            print("\n👤 Création d'un utilisateur de test...")
            cur.execute("""
                INSERT INTO users (username, password, nom, prenom)
                VALUES ('test', 'pbkdf2:sha256:600000$test$test', 'Test', 'User')
            """)
            conn.commit()
            print("✅ Utilisateur de test créé : username='test', password='test'")

        cur.close()
        conn.close()

        print("\n🎉 Initialisation de la base de données terminée avec succès !")

    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    init_postgres_render()