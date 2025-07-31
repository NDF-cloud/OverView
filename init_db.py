#!/usr/bin/env python3
# ==============================================================================
# SCRIPT D'INITIALISATION DE BASE DE DONNÉES (SQLite et PostgreSQL)
# ==============================================================================
import os
import sqlite3
import psycopg
import psycopg.errors

def init_sqlite_db():
    """Initialise la base de données SQLite"""
    print("🔧 Initialisation de la base de données SQLite...")
    conn = sqlite3.connect('epargne.db')
    cur = conn.cursor()

    # Création des tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            security_question TEXT,
            security_answer TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS objectifs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            montant_cible REAL NOT NULL,
            montant_actuel REAL NOT NULL,
            date_limite TEXT,
            status TEXT NOT NULL DEFAULT 'actif',
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            objectif_id INTEGER NOT NULL,
            montant REAL NOT NULL,
            type_transaction TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER NOT NULL,
            devise_saisie TEXT DEFAULT 'XAF',
            FOREIGN KEY (objectif_id) REFERENCES objectifs (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS taches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            titre TEXT NOT NULL,
            description TEXT,
            date_limite TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            termine BOOLEAN DEFAULT FALSE,
            ordre INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS etapes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tache_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            terminee BOOLEAN DEFAULT FALSE,
            ordre INTEGER DEFAULT 0,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tache_id) REFERENCES taches (id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS evenements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            titre TEXT NOT NULL,
            description TEXT,
            date_debut TEXT NOT NULL,
            heure_debut TEXT,
            date_fin TEXT,
            heure_fin TEXT,
            lieu TEXT,
            couleur TEXT DEFAULT '#fd7e14',
            rappel_minutes TEXT DEFAULT '0',
            termine BOOLEAN DEFAULT FALSE,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de données SQLite initialisée avec succès!")

def init_postgres_db():
    """Initialise la base de données PostgreSQL"""
    print("🔧 Initialisation de la base de données PostgreSQL...")
    db_url = os.environ.get('DATABASE_URL')

    if not db_url:
        print("❌ ERREUR : Variable d'environnement DATABASE_URL non définie")
        return False

    try:
        conn = psycopg.connect(db_url)
        cur = conn.cursor()

        # Création des tables
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(80) UNIQUE NOT NULL,
                password VARCHAR(120) NOT NULL,
                security_question TEXT,
                security_answer VARCHAR(120)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS objectifs (
                id SERIAL PRIMARY KEY,
                nom VARCHAR(200) NOT NULL,
                montant_cible DECIMAL(10,2) NOT NULL,
                montant_actuel DECIMAL(10,2) DEFAULT 0,
                date_limite DATE,
                status VARCHAR(20) NOT NULL DEFAULT 'actif',
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id SERIAL PRIMARY KEY,
                objectif_id INTEGER NOT NULL REFERENCES objectifs(id) ON DELETE CASCADE,
                montant DECIMAL(10,2) NOT NULL,
                type_transaction VARCHAR(20) NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                devise_saisie VARCHAR(10) DEFAULT 'XAF'
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS taches (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                titre VARCHAR(200) NOT NULL,
                description TEXT,
                date_limite DATE,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                termine BOOLEAN DEFAULT FALSE,
                ordre INTEGER DEFAULT 0
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS etapes (
                id SERIAL PRIMARY KEY,
                tache_id INTEGER NOT NULL REFERENCES taches(id) ON DELETE CASCADE,
                description VARCHAR(500) NOT NULL,
                terminee BOOLEAN DEFAULT FALSE,
                ordre INTEGER NOT NULL,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS evenements (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                titre VARCHAR(200) NOT NULL,
                description TEXT,
                date_debut DATE NOT NULL,
                heure_debut TIME,
                date_fin DATE,
                heure_fin TIME,
                lieu VARCHAR(200),
                couleur VARCHAR(7) DEFAULT '#fd7e14',
                rappel_minutes VARCHAR(10) DEFAULT '0',
                termine BOOLEAN DEFAULT FALSE,
                date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()
        print("✅ Base de données PostgreSQL initialisée avec succès!")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation PostgreSQL : {e}")
        return False

def main():
    """Fonction principale d'initialisation"""
    print("🚀 Démarrage de l'initialisation de la base de données...")

    # Vérifier si on utilise PostgreSQL ou SQLite
    if os.environ.get('DATABASE_URL'):
        print("📊 Mode PostgreSQL détecté")
        success = init_postgres_db()
        if not success:
            print("⚠️ Échec de l'initialisation PostgreSQL, passage en mode SQLite...")
            init_sqlite_db()
    else:
        print("📊 Mode SQLite détecté")
        init_sqlite_db()

    print("✅ Initialisation terminée!")

if __name__ == '__main__':
    main()