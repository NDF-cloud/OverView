#!/usr/bin/env python3
"""
Script d'initialisation de la base de données PostgreSQL pour Render
Ce script doit être exécuté une seule fois après la création de la base de données
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def init_render_database():
    """Initialise la base de données PostgreSQL sur Render"""
    
    # Récupérer l'URL de la base de données depuis les variables d'environnement
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if not DATABASE_URL:
        print("❌ ERREUR: DATABASE_URL non définie")
        print("Veuillez configurer la variable d'environnement DATABASE_URL sur Render")
        return False
    
    try:
        print("🔗 Connexion à la base de données PostgreSQL sur Render...")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Vérifier si les tables existent déjà
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name = 'users'
            );
        """)
        
        tables_exist = cur.fetchone()[0]
        
        if tables_exist:
            print("✅ Tables déjà existantes, base de données déjà initialisée")
            cur.close()
            conn.close()
            return True
        
        print("🗑️  Suppression des anciennes tables (si elles existent)...")
        cur.execute("DROP TABLE IF EXISTS transactions CASCADE;")
        cur.execute("DROP TABLE IF EXISTS taches CASCADE;")
        cur.execute("DROP TABLE IF EXISTS etapes CASCADE;")
        cur.execute("DROP TABLE IF EXISTS evenements CASCADE;")
        cur.execute("DROP TABLE IF EXISTS objectifs CASCADE;")
        cur.execute("DROP TABLE IF EXISTS users CASCADE;")
        cur.execute("DROP TABLE IF EXISTS registre_caisse CASCADE;")
        cur.execute("DROP TABLE IF EXISTS notifications CASCADE;")
        
        print("🏗️  Création de la structure des tables...")
        
        # Table users
        cur.execute('''
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(80) UNIQUE NOT NULL,
            password VARCHAR(120) NOT NULL,
            security_question VARCHAR(200),
            security_answer VARCHAR(120),
            display_progress BOOLEAN DEFAULT TRUE,
            notification_enabled BOOLEAN DEFAULT TRUE,
            auto_delete_completed BOOLEAN DEFAULT FALSE,
            auto_delete_days INTEGER DEFAULT 90,
            countdown_enabled BOOLEAN DEFAULT TRUE,
            countdown_days INTEGER DEFAULT 30,
            balance_privacy BOOLEAN DEFAULT FALSE,
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
        );
        ''')
        
        # Table objectifs
        cur.execute('''
        CREATE TABLE objectifs (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(200) NOT NULL,
            montant_cible DECIMAL(15,2) NOT NULL,
            montant_actuel DECIMAL(15,2) DEFAULT 0,
            date_limite DATE,
            status VARCHAR(20) DEFAULT 'actif',
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        
        # Table transactions
        cur.execute('''
        CREATE TABLE transactions (
            id SERIAL PRIMARY KEY,
            objectif_id INTEGER REFERENCES objectifs(id) ON DELETE CASCADE,
            montant DECIMAL(15,2) NOT NULL,
            type_transaction VARCHAR(20) NOT NULL,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            date_transaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        
        # Table taches
        cur.execute('''
        CREATE TABLE taches (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            titre VARCHAR(200) NOT NULL,
            description TEXT,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            termine BOOLEAN DEFAULT FALSE,
            ordre INTEGER DEFAULT 0,
            date_limite DATE
        );
        ''')
        
        # Table etapes
        cur.execute('''
        CREATE TABLE etapes (
            id SERIAL PRIMARY KEY,
            tache_id INTEGER REFERENCES taches(id) ON DELETE CASCADE,
            description VARCHAR(500) NOT NULL,
            terminee BOOLEAN DEFAULT FALSE,
            ordre INTEGER DEFAULT 0,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        
        # Table evenements
        cur.execute('''
        CREATE TABLE evenements (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            titre VARCHAR(200) NOT NULL,
            description TEXT,
            date_debut TIMESTAMP NOT NULL,
            date_fin TIMESTAMP,
            lieu VARCHAR(200),
            termine BOOLEAN DEFAULT FALSE,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        
        # Table registre_caisse
        cur.execute('''
        CREATE TABLE registre_caisse (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            type_operation VARCHAR(20) NOT NULL,
            montant DECIMAL(15,2) NOT NULL,
            description TEXT,
            date_operation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            categorie VARCHAR(100),
            methode_paiement VARCHAR(50)
        );
        ''')
        
        # Table notifications
        cur.execute('''
        CREATE TABLE notifications (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            type_notif VARCHAR(50) NOT NULL,
            titre VARCHAR(200) NOT NULL,
            message TEXT NOT NULL,
            lu BOOLEAN DEFAULT FALSE,
            priorite VARCHAR(20) DEFAULT 'normal',
            action_url VARCHAR(500),
            action_text VARCHAR(100),
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        
        # Créer un utilisateur de test par défaut
        print("👤 Création d'un utilisateur de test...")
        cur.execute('''
        INSERT INTO users (username, password, security_question, security_answer, nom, prenom)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', ('admin', 'pbkdf2:sha256:600000$test123$test_hash', 
              'Quel est le nom de votre premier animal de compagnie ?', 
              'pbkdf2:sha256:600000$test123$test_hash', 'Admin', 'Test'))
        
        # Valider les changements
        conn.commit()
        
        print("✅ Base de données initialisée avec succès sur Render !")
        print("📝 Utilisateur de test créé :")
        print("   - Username: admin")
        print("   - Password: admin123")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ ERREUR lors de l'initialisation de la base de données : {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == '__main__':
    print("🚀 Initialisation de la base de données PostgreSQL sur Render...")
    success = init_render_database()
    if success:
        print("🎉 Base de données prête ! Vous pouvez maintenant redémarrer l'application.")
    else:
        print("💥 Échec de l'initialisation de la base de données.")
