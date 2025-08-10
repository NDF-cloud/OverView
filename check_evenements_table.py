#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def check_evenements_table():
    """Vérifier la structure de la table evenements"""

    print("🔍 Vérification de la structure de la table evenements...")

    try:
        conn = sqlite3.connect('epargne.db')
        cur = conn.cursor()

        # Vérifier si la table existe
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='evenements'")
        if not cur.fetchone():
            print("❌ La table evenements n'existe pas!")
            return

        # Obtenir la structure de la table
        cur.execute("PRAGMA table_info(evenements)")
        columns = cur.fetchall()

        print("📋 Structure de la table evenements:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]}) - Default: {col[4]}")

        # Vérifier spécifiquement la colonne rappel_minutes
        column_names = [col[1] for col in columns]
        if 'rappel_minutes' in column_names:
            print("✅ Colonne rappel_minutes trouvée")
        else:
            print("❌ Colonne rappel_minutes manquante")

        # Vérifier les autres colonnes importantes
        required_columns = ['id', 'user_id', 'titre', 'description', 'date_debut', 'date_fin', 'heure_debut', 'heure_fin', 'lieu', 'couleur', 'termine', 'date_creation']
        missing_columns = []

        for col in required_columns:
            if col not in column_names:
                missing_columns.append(col)

        if missing_columns:
            print(f"⚠️  Colonnes manquantes: {missing_columns}")
        else:
            print("✅ Toutes les colonnes requises sont présentes")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    check_evenements_table()