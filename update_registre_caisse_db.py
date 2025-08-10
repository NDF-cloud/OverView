#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour mettre à jour la table registre_caisse avec les nouvelles colonnes
pour la gestion des paiements partiels
"""

import sqlite3
import os

def update_registre_caisse_table():
    """Mettre à jour la table registre_caisse avec les nouvelles colonnes"""

    print("🔧 Mise à jour de la table registre_caisse...")

    try:
        conn = sqlite3.connect('epargne.db')
        cursor = conn.cursor()

        # Vérifier si la table existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='registre_caisse'")
        table_exists = cursor.fetchone() is not None

        if not table_exists:
            print("❌ Table registre_caisse n'existe pas. Création...")
            cursor.execute('''
                CREATE TABLE registre_caisse (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_operation TEXT NOT NULL,
                    prix_unitaire REAL NOT NULL,
                    quantite INTEGER NOT NULL DEFAULT 1,
                    prix_total REAL NOT NULL,
                    type_operation TEXT NOT NULL CHECK (type_operation IN ('entree', 'sortie')),
                    description TEXT,
                    montant_verse REAL DEFAULT 0,
                    montant_reste REAL DEFAULT 0,
                    statut_paiement TEXT DEFAULT 'complet',
                    date_echeance DATE,
                    date_operation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER
                )
            ''')
            print("✅ Table registre_caisse créée avec toutes les colonnes")
        else:
            print("✅ Table registre_caisse existe déjà")

            # Vérifier les colonnes existantes
            cursor.execute("PRAGMA table_info(registre_caisse)")
            columns = [col[1] for col in cursor.fetchall()]

            print(f"📋 Colonnes existantes: {columns}")

            # Ajouter les nouvelles colonnes si elles n'existent pas
            new_columns = [
                ('montant_verse', 'REAL DEFAULT 0'),
                ('montant_reste', 'REAL DEFAULT 0'),
                ('statut_paiement', 'TEXT DEFAULT \'complet\''),
                ('date_echeance', 'DATE')
            ]

            for col_name, col_type in new_columns:
                if col_name not in columns:
                    print(f"➕ Ajout de la colonne {col_name}...")
                    cursor.execute(f'ALTER TABLE registre_caisse ADD COLUMN {col_name} {col_type}')
                    print(f"✅ Colonne {col_name} ajoutée")
                else:
                    print(f"✅ Colonne {col_name} existe déjà")

        # Créer un index pour améliorer les performances
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_registre_user_date_paiement
            ON registre_caisse(user_id, date_operation, statut_paiement)
        ''')

        conn.commit()
        print("✅ Index créé pour les performances")

        # Vérifier la structure finale
        cursor.execute("PRAGMA table_info(registre_caisse)")
        final_columns = cursor.fetchall()

        print("\n📊 Structure finale de la table registre_caisse:")
        for col in final_columns:
            print(f"  - {col[1]} ({col[2]})")

        conn.close()
        print("\n🎯 Mise à jour terminée avec succès!")

    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {e}")
        return False

    return True

if __name__ == "__main__":
    update_registre_caisse_table()