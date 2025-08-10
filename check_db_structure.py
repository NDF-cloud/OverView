#!/usr/bin/env python3
"""
Script pour examiner la structure complète de la base de données
"""

import sqlite3
import os

def check_db_structure():
    """Examiner la structure de la base de données"""
    
    print("🔍 Vérification de la structure de la base de données...")
    
    # Connexion à la base de données SQLite
    db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    try:
        # Lister toutes les tables
        cur.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table'
            ORDER BY name
        """)
        
        tables = cur.fetchall()
        print(f"📊 Nombre de tables: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            print(f"\n📋 Table: {table_name}")
            
            # Vérifier la structure de chaque table
            cur.execute(f"PRAGMA table_info({table_name})")
            columns = cur.fetchall()
            
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                pk_mark = " 🔑" if pk else ""
                not_null_mark = " NOT NULL" if not_null else ""
                default_mark = f" DEFAULT {default_val}" if default_val else ""
                print(f"  - {col_name} ({col_type}){not_null_mark}{default_mark}{pk_mark}")
            
            # Compter les lignes
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cur.fetchone()[0]
            print(f"  📊 Lignes: {count}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    finally:
        cur.close()
        conn.close()
    
    print("\n🎯 Vérification terminée !")

if __name__ == "__main__":
    check_db_structure()
