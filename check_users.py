#!/usr/bin/env python3
"""
Script pour vérifier les utilisateurs existants dans la base de données
"""

import sqlite3
import os

def check_users():
    """Vérifier les utilisateurs existants"""
    
    print("👥 Vérification des utilisateurs...")
    
    # Connexion à la base de données SQLite
    db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    try:
        # Vérifier si la table users existe
        cur.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='users'
        """)
        
        if not cur.fetchone():
            print("❌ Table users n'existe pas")
            return
        
        # Lister tous les utilisateurs
        cur.execute("SELECT id, username, email FROM users")
        users = cur.fetchall()
        
        print(f"📊 Nombre d'utilisateurs: {len(users)}")
        
        if users:
            print("\n👤 Utilisateurs trouvés:")
            for user in users:
                user_id, username, email = user
                print(f"  - ID: {user_id}, Username: {username}, Email: {email}")
        else:
            print("💡 Aucun utilisateur trouvé")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    finally:
        cur.close()
        conn.close()
    
    print("\n🎯 Vérification terminée !")

if __name__ == "__main__":
    check_users()
