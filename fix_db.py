#!/usr/bin/env python3
"""
Script de migration pour corriger le nom de colonne dans les bases de données SQLite existantes.
Change 'date' en 'date_transaction' dans la table transactions.
"""

import sqlite3
import os

def migrate_sqlite_database():
    """Migre la base de données SQLite pour corriger le nom de colonne"""

    db_path = 'epargne.db'

    if not os.path.exists(db_path):
        print("✅ Base de données SQLite non trouvée, aucune migration nécessaire.")
        return

    print("🔧 Migration de la base de données SQLite...")

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Vérifier si la colonne 'date' existe
        cur.execute("PRAGMA table_info(transactions)")
        columns = cur.fetchall()
        column_names = [col[1] for col in columns]

        if 'date' in column_names and 'date_transaction' not in column_names:
            print("📝 Colonne 'date' trouvée, migration en cours...")

            # Créer une nouvelle table avec la bonne structure
            cur.execute("""
                CREATE TABLE transactions_new (
                    id INTEGER PRIMARY KEY,
                    objectif_id INTEGER NOT NULL,
                    montant REAL NOT NULL,
                    type_transaction TEXT NOT NULL,
                    devise_saisie TEXT DEFAULT 'XAF',
                    date_transaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    user_id INTEGER NOT NULL,
                    FOREIGN KEY (objectif_id) REFERENCES objectifs (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)

            # Copier les données de l'ancienne table vers la nouvelle
            cur.execute("""
                INSERT INTO transactions_new (id, objectif_id, montant, type_transaction, devise_saisie, date_transaction, user_id)
                SELECT id, objectif_id, montant, type_transaction, devise_saisie, date, user_id
                FROM transactions
            """)

            # Supprimer l'ancienne table
            cur.execute("DROP TABLE transactions")

            # Renommer la nouvelle table
            cur.execute("ALTER TABLE transactions_new RENAME TO transactions")

            conn.commit()
            print("✅ Migration terminée avec succès!")

        elif 'date_transaction' in column_names:
            print("✅ Colonne 'date_transaction' déjà présente, aucune migration nécessaire.")

        else:
            print("⚠️  Structure de table inattendue, vérifiez manuellement.")

    except Exception as e:
        print(f"❌ Erreur lors de la migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_sqlite_database()