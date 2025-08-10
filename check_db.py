#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os

def check_database():
    """Vérifier la structure de la base de données"""

    print("🔍 Vérification de la base de données...")

    # Vérifier si le fichier existe
    if not os.path.exists('epargne.db'):
        print("❌ Fichier epargne.db n'existe pas")
        return False

    try:
        conn = sqlite3.connect('epargne.db')
        cursor = conn.cursor()

        # Lister toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print("📋 Tables existantes:")
        for table in tables:
            print(f"  - {table[0]}")

        # Vérifier si la table registre_caisse existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='registre_caisse'")
        registre_exists = cursor.fetchone() is not None

        if registre_exists:
            print("✅ Table registre_caisse existe")

            # Vérifier la structure de la table
            cursor.execute("PRAGMA table_info(registre_caisse)")
            columns = cursor.fetchall()

            print("📊 Structure de la table registre_caisse:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
        else:
            print("❌ Table registre_caisse n'existe pas")

        conn.close()
        return registre_exists

    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

if __name__ == "__main__":
    check_database()