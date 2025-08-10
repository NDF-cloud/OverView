#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script simple pour vérifier les tables existantes dans la base de données
"""

import sqlite3

def check_tables():
    """Vérifier les tables existantes"""
    
    try:
        conn = sqlite3.connect('epargne.db')
        cursor = conn.cursor()
        
        # Lister toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print("📋 Tables existantes dans la base de données:")
        print("-" * 40)
        
        for table in tables:
            table_name = table[0]
            print(f"  📊 {table_name}")
            
            # Compter les lignes dans chaque table
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"    → {count} lignes")
            except Exception as e:
                print(f"    → Erreur: {e}")
        
        print("-" * 40)
        print(f"Total: {len(tables)} tables")
        
        # Vérifier si la table notifications existe
        if any('notifications' in table[0] for table in tables):
            print("\n✅ Table 'notifications' trouvée")
        else:
            print("\n❌ Table 'notifications' manquante")
            print("   Cette table est nécessaire pour la suppression en cascade")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    check_tables()
