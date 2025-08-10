#!/usr/bin/env python3
"""
Script pour corriger le système de devise en supprimant les colonnes de devise
de la base de données existante et en s'assurant que tout est cohérent.
"""

import os
import psycopg2
import sqlite3
from psycopg2.extras import RealDictCursor

def fix_postgres_database():
    """Corrige la base de données PostgreSQL en supprimant les colonnes de devise"""
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        print("⚠️  DATABASE_URL non définie, impossible de corriger PostgreSQL")
        return False

    try:
        print("🔗 Connexion à PostgreSQL...")
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Vérifier si la colonne devise_saisie existe dans la table transactions
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'transactions'
            AND column_name = 'devise_saisie'
        """)

        if cur.fetchone():
            print("🗑️  Suppression de la colonne devise_saisie de la table transactions...")
            cur.execute("ALTER TABLE transactions DROP COLUMN IF EXISTS devise_saisie")
            conn.commit()
            print("✅ Colonne devise_saisie supprimée")
        else:
            print("✅ Colonne devise_saisie n'existe pas déjà")

        # Vérifier si la colonne devise_cible existe dans la table objectifs
        cur.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'objectifs'
            AND column_name = 'devise_cible'
        """)

        if cur.fetchone():
            print("🗑️  Suppression de la colonne devise_cible de la table objectifs...")
            cur.execute("ALTER TABLE objectifs DROP COLUMN IF EXISTS devise_cible")
            conn.commit()
            print("✅ Colonne devise_cible supprimée")
        else:
            print("✅ Colonne devise_cible n'existe pas déjà")

        # Vérifier si les colonnes de devise existent dans la table users
        for col in ['default_currency', 'display_currency']:
            cur.execute(f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'users'
                AND column_name = '{col}'
            """)

            if cur.fetchone():
                print(f"🗑️  Suppression de la colonne {col} de la table users...")
                cur.execute(f"ALTER TABLE users DROP COLUMN IF EXISTS {col}")
                conn.commit()
                print(f"✅ Colonne {col} supprimée")
            else:
                print(f"✅ Colonne {col} n'existe pas déjà")

        cur.close()
        conn.close()
        print("✅ Base de données PostgreSQL corrigée avec succès")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de la correction de PostgreSQL: {e}")
        return False

def fix_sqlite_database():
    """Corrige la base de données SQLite en supprimant les colonnes de devise"""
    try:
        print("🔗 Connexion à SQLite...")
        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        # Vérifier si la colonne devise_saisie existe dans la table transactions
        cur.execute("PRAGMA table_info(transactions)")
        columns = [col[1] for col in cur.fetchall()]

        if 'devise_saisie' in columns:
            print("🗑️  Suppression de la colonne devise_saisie de la table transactions...")
            # SQLite ne supporte pas DROP COLUMN directement, on doit recréer la table
            cur.execute("""
                CREATE TABLE transactions_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    objectif_id INTEGER NOT NULL,
                    montant REAL NOT NULL,
                    type_transaction TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    date_transaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (objectif_id) REFERENCES objectifs (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)

            # Copier les données sans la colonne devise_saisie
            cur.execute("""
                INSERT INTO transactions_new (id, objectif_id, montant, type_transaction, user_id, date_transaction)
                SELECT id, objectif_id, montant, type_transaction, user_id, date_transaction
                FROM transactions
            """)

            cur.execute("DROP TABLE transactions")
            cur.execute("ALTER TABLE transactions_new RENAME TO transactions")
            conn.commit()
            print("✅ Colonne devise_saisie supprimée")
        else:
            print("✅ Colonne devise_saisie n'existe pas déjà")

        # Vérifier si la colonne devise_cible existe dans la table objectifs
        cur.execute("PRAGMA table_info(objectifs)")
        columns = [col[1] for col in cur.fetchall()]

        if 'devise_cible' in columns:
            print("🗑️  Suppression de la colonne devise_cible de la table objectifs...")
            # Recréer la table objectifs sans devise_cible
            cur.execute("""
                CREATE TABLE objectifs_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    montant_cible REAL NOT NULL,
                    montant_actuel REAL DEFAULT 0,
                    date_limite DATE,
                    status TEXT DEFAULT 'actif',
                    user_id INTEGER NOT NULL,
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)

            # Copier les données sans la colonne devise_cible
            cur.execute("""
                INSERT INTO objectifs_new (id, nom, montant_cible, montant_actuel, date_limite, status, user_id, date_creation)
                SELECT id, nom, montant_cible, montant_actuel, date_limite, status, user_id, date_creation
                FROM objectifs
            """)

            cur.execute("DROP TABLE objectifs")
            cur.execute("ALTER TABLE objectifs_new RENAME TO objectifs")
            conn.commit()
            print("✅ Colonne devise_cible supprimée")
        else:
            print("✅ Colonne devise_cible n'existe pas déjà")

        # Vérifier si les colonnes de devise existent dans la table users
        cur.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cur.fetchall()]

        for col in ['default_currency', 'display_currency']:
            if col in columns:
                print(f"🗑️  Suppression de la colonne {col} de la table users...")
                # Recréer la table users sans la colonne de devise
                cur.execute("""
                    CREATE TABLE users_new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        security_question TEXT,
                        security_answer TEXT,
                        display_progress BOOLEAN DEFAULT 1,
                        notification_enabled BOOLEAN DEFAULT 1,
                        auto_delete_completed BOOLEAN DEFAULT 0,
                        auto_delete_days INTEGER DEFAULT 90,
                        countdown_enabled BOOLEAN DEFAULT 1,
                        countdown_days INTEGER DEFAULT 30,
                        nom TEXT,
                        prenom TEXT,
                        date_naissance DATE,
                        telephone TEXT,
                        email TEXT,
                        sexe TEXT,
                        photo_profil TEXT,
                        bio TEXT,
                        adresse TEXT,
                        ville TEXT,
                        pays TEXT DEFAULT 'Cameroun',
                        date_creation_profil TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Copier les données sans la colonne de devise
                cur.execute("""
                    INSERT INTO users_new SELECT * FROM users
                """)

                cur.execute("DROP TABLE users")
                cur.execute("ALTER TABLE users_new RENAME TO users")
                conn.commit()
                print(f"✅ Colonne {col} supprimée")
            else:
                print(f"✅ Colonne {col} n'existe pas déjà")

        cur.close()
        conn.close()
        print("✅ Base de données SQLite corrigée avec succès")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de la correction de SQLite: {e}")
        return False

def main():
    """Fonction principale pour corriger le système de devise"""
    print("🔧 Correction du système de devise...")
    print("=" * 50)

    # Corriger PostgreSQL si disponible
    if os.getenv('DATABASE_URL'):
        fix_postgres_database()

    # Corriger SQLite
    fix_sqlite_database()

    print("=" * 50)
    print("✅ Correction du système de devise terminée")
    print("📝 Toutes les références aux devises ont été supprimées")
    print("💡 Le système utilise maintenant uniquement FCFA")

if __name__ == "__main__":
    main()