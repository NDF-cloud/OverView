#!/usr/bin/env python3
"""
Script pour mettre à jour la base de données et ajouter les champs de notifications
"""

import sqlite3
import os
import sys

def get_db_connection():
    """Créer une connexion à la base de données"""
    if os.environ.get('DATABASE_URL'):
        # PostgreSQL
        import psycopg2
        return psycopg2.connect(os.environ.get('DATABASE_URL'))
    else:
        # SQLite
        return sqlite3.connect('epargne.db')

def update_database():
    """Mettre à jour la base de données"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Vérifier si la colonne balance_privacy existe déjà
        if os.environ.get('DATABASE_URL'):
            # PostgreSQL
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'users' AND column_name = 'balance_privacy'
            """)
        else:
            # SQLite
            cur.execute("PRAGMA table_info(users)")
            columns = [column[1] for column in cur.fetchall()]
        
        column_exists = False
        if os.environ.get('DATABASE_URL'):
            column_exists = cur.fetchone() is not None
        else:
            column_exists = 'balance_privacy' in columns
        
        if not column_exists:
            print("Ajout de la colonne balance_privacy à la table users...")
            
            if os.environ.get('DATABASE_URL'):
                # PostgreSQL
                cur.execute("ALTER TABLE users ADD COLUMN balance_privacy BOOLEAN DEFAULT FALSE")
            else:
                # SQLite
                cur.execute("ALTER TABLE users ADD COLUMN balance_privacy BOOLEAN DEFAULT 0")
            
            conn.commit()
            print("✅ Colonne balance_privacy ajoutée avec succès!")
        else:
            print("✅ La colonne balance_privacy existe déjà")

        # Ajouter les nouvelles colonnes de préférences de notifications
        notification_columns = ['notif_objectifs', 'notif_taches', 'notif_evenements', 'notif_rapports']
        
        for column in notification_columns:
            if os.environ.get('DATABASE_URL'):
                # PostgreSQL
                cur.execute(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = '{column}'
                """)
                exists = cur.fetchone() is not None
            else:
                # SQLite
                cur.execute("PRAGMA table_info(users)")
                columns = [col[1] for col in cur.fetchall()]
                exists = column in columns
            
            if not exists:
                print(f"Ajout de la colonne {column} à la table users...")
                
                if os.environ.get('DATABASE_URL'):
                    # PostgreSQL
                    cur.execute(f"ALTER TABLE users ADD COLUMN {column} BOOLEAN DEFAULT TRUE")
                else:
                    # SQLite
                    cur.execute(f"ALTER TABLE users ADD COLUMN {column} BOOLEAN DEFAULT 1")
                
                conn.commit()
                print(f"✅ Colonne {column} ajoutée avec succès!")
            else:
                print(f"✅ La colonne {column} existe déjà")
        
        # Vérifier la structure de la table
        print("\nStructure actuelle de la table users:")
        if os.environ.get('DATABASE_URL'):
            # PostgreSQL
            cur.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = 'users'
                ORDER BY ordinal_position
            """)
        else:
            # SQLite
            cur.execute("PRAGMA table_info(users)")
        
        columns_info = cur.fetchall()
        for col in columns_info:
            if os.environ.get('DATABASE_URL'):
                print(f"  - {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")
            else:
                print(f"  - {col[1]}: {col[2]} (nullable: {col[3]}, default: {col[4]})")
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()
    
    return True

if __name__ == "__main__":
    print("🔄 Mise à jour de la base de données...")
    
    if update_database():
        print("\n✅ Mise à jour terminée avec succès!")
        print("La fonctionnalité de confidentialité des soldes et les préférences de notifications sont maintenant disponibles.")
    else:
        print("\n❌ Échec de la mise à jour")
        sys.exit(1)