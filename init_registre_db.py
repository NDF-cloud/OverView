#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def init_registre_database():
    """Initialiser la base de données avec la table registre_caisse"""

    print("🏗️ Initialisation de la base de données...")

    try:
        conn = sqlite3.connect('epargne.db')
        cursor = conn.cursor()

        # Créer la table registre_caisse
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS registre_caisse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom_operation TEXT NOT NULL,
            prix_unitaire REAL NOT NULL,
            quantite INTEGER NOT NULL DEFAULT 1,
            prix_total REAL NOT NULL,
            type_operation TEXT NOT NULL CHECK (type_operation IN ('entree', 'sortie')),
            description TEXT,
            date_operation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER
        )
        ''')

        # Créer un index pour améliorer les performances
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_registre_user_date
        ON registre_caisse(user_id, date_operation)
        ''')

        conn.commit()
        print("✅ Table registre_caisse créée avec succès")

        # Vérifier la structure
        cursor.execute("PRAGMA table_info(registre_caisse)")
        columns = cursor.fetchall()

        print("📊 Structure de la table:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        return False

if __name__ == "__main__":
    init_registre_database()