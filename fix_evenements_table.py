#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import psycopg2

def fix_evenements_table():
    """Ajouter la colonne rappel_minutes à la table evenements"""

    # Vérifier si on utilise PostgreSQL ou SQLite
    DATABASE_URL = os.getenv('DATABASE_URL')

    if DATABASE_URL:
        # PostgreSQL
        print("🔧 Correction de la table evenements (PostgreSQL)...")
        try:
            conn = psycopg2.connect(DATABASE_URL)
            cur = conn.cursor()

            # Vérifier si la colonne rappel_minutes existe
            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'evenements' AND column_name = 'rappel_minutes'
            """)

            if not cur.fetchone():
                print("➕ Ajout de la colonne rappel_minutes...")
                cur.execute("ALTER TABLE evenements ADD COLUMN rappel_minutes INTEGER DEFAULT 30")
                conn.commit()
                print("✅ Colonne rappel_minutes ajoutée avec succès")
            else:
                print("✅ Colonne rappel_minutes existe déjà")

            cur.close()
            conn.close()

        except Exception as e:
            print(f"❌ Erreur lors de la correction PostgreSQL: {e}")
            return False

    else:
        # SQLite
        print("🔧 Correction de la table evenements (SQLite)...")
        try:
            conn = sqlite3.connect('epargne.db')
            cur = conn.cursor()

            # Vérifier si la colonne rappel_minutes existe
            cur.execute("PRAGMA table_info(evenements)")
            columns = [column[1] for column in cur.fetchall()]

            if 'rappel_minutes' not in columns:
                print("➕ Ajout de la colonne rappel_minutes...")
                cur.execute("ALTER TABLE evenements ADD COLUMN rappel_minutes INTEGER DEFAULT 30")
                conn.commit()
                print("✅ Colonne rappel_minutes ajoutée avec succès")
            else:
                print("✅ Colonne rappel_minutes existe déjà")

            cur.close()
            conn.close()

        except Exception as e:
            print(f"❌ Erreur lors de la correction SQLite: {e}")
            return False

    print("🎉 Correction de la table evenements terminée!")
    return True

if __name__ == "__main__":
    fix_evenements_table()