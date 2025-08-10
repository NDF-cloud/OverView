#!/usr/bin/env python3
"""
Script pour créer un utilisateur de test
"""

import sqlite3
import os
import hashlib
from datetime import datetime

def create_test_user():
    """Créer un utilisateur de test"""
    
    print("👤 Création d'un utilisateur de test...")
    
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
        
        # Vérifier si l'utilisateur de test existe déjà
        cur.execute("SELECT id FROM users WHERE username = ?", ('test_user',))
        if cur.fetchone():
            print("✅ Utilisateur de test existe déjà")
            return
        
        # Créer l'utilisateur de test
        username = 'test_user'
        password = 'test123'
        email = 'test@example.com'
        
        # Hasher le mot de passe
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        # Insérer l'utilisateur
        cur.execute('''
            INSERT INTO users (username, password, nom, prenom)
            VALUES (?, ?, ?, ?)
        ''', (username, password_hash, 'Test', 'User'))
        
        user_id = cur.lastrowid
        
        # Créer quelques données de test
        # 1. Un objectif
        cur.execute('''
            INSERT INTO objectifs (user_id, nom, montant_cible, montant_actuel, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 'Objectif Test', 1000.0, 950.0, 'actif'))
        
        objectif_id = cur.lastrowid
        
        # 2. Une tâche
        cur.execute('''
            INSERT INTO taches (user_id, titre, description, priorite, termine)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 'Tâche Test', 'Tâche pour tester les notifications', 'haute', False))
        
        # 3. Un événement
        cur.execute('''
            INSERT INTO evenements (user_id, titre, description, date_debut, date_fin, termine)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, 'Événement Test', 'Événement pour tester les notifications', datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%Y-%m-%d'), False))
        
        conn.commit()
        
        print(f"✅ Utilisateur de test créé avec succès!")
        print(f"  - Username: {username}")
        print(f"  - Password: {password}")
        print(f"  - Email: {email}")
        print(f"  - ID: {user_id}")
        print(f"  - Objectif créé: ID {objectif_id}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
    
    finally:
        cur.close()
        conn.close()
    
    print("\n🎯 Création terminée !")

if __name__ == "__main__":
    create_test_user()
