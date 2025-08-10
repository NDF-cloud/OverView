#!/usr/bin/env python3
"""
Script pour vérifier et créer la table notifications si nécessaire
"""

import sqlite3
import os

def check_and_create_notifications_table():
    """Vérifier et créer la table notifications si nécessaire"""
    
    print("🔍 Vérification de la table notifications...")
    
    # Connexion à la base de données SQLite
    db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée. Création...")
        conn = sqlite3.connect(db_path)
    else:
        conn = sqlite3.connect(db_path)
    
    cur = conn.cursor()
    
    try:
        # Vérifier si la table notifications existe
        cur.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='notifications'
        """)
        
        if cur.fetchone():
            print("✅ Table notifications existe déjà")
            
            # Vérifier la structure
            cur.execute("PRAGMA table_info(notifications)")
            columns = cur.fetchall()
            print(f"📋 Structure actuelle: {len(columns)} colonnes")
            
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
        else:
            print("❌ Table notifications n'existe pas. Création...")
            
            # Créer la table notifications
            cur.execute('''
                CREATE TABLE notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    type_notification VARCHAR(50) NOT NULL,
                    titre VARCHAR(200) NOT NULL,
                    message TEXT NOT NULL,
                    priorite VARCHAR(20) DEFAULT 'normal',
                    action_url VARCHAR(200),
                    action_text VARCHAR(100),
                    lue BOOLEAN DEFAULT FALSE,
                    date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date_lecture DATETIME,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Créer des index pour améliorer les performances
            cur.execute('''
                CREATE INDEX idx_notifications_user_id ON notifications(user_id)
            ''')
            
            cur.execute('''
                CREATE INDEX idx_notifications_lue ON notifications(lue)
            ''')
            
            cur.execute('''
                CREATE INDEX idx_notifications_date_creation ON notifications(date_creation)
            ''')
            
            conn.commit()
            print("✅ Table notifications créée avec succès")
            
            # Vérifier la structure créée
            cur.execute("PRAGMA table_info(notifications)")
            columns = cur.fetchall()
            print(f"📋 Structure créée: {len(columns)} colonnes")
            
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        
        # Vérifier s'il y a des données
        cur.execute("SELECT COUNT(*) FROM notifications")
        count = cur.fetchone()[0]
        print(f"📊 Nombre de notifications: {count}")
        
        if count == 0:
            print("💡 Aucune notification trouvée. C'est normal pour une nouvelle installation.")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        conn.rollback()
    
    finally:
        cur.close()
        conn.close()
    
    print("\n🎯 Vérification terminée !")

if __name__ == "__main__":
    check_and_create_notifications_table()
