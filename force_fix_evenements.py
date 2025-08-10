import sqlite3
import os

def force_fix_evenements():
    """Forcer la correction de la table evenements"""

    print("🔧 Correction forcée de la table evenements...")

    try:
        conn = sqlite3.connect('epargne.db')
        cur = conn.cursor()

        # Vérifier si la table existe
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='evenements'")
        table_exists = cur.fetchone()

        if table_exists:
            print("📋 Table evenements existe, vérification de la structure...")

            # Obtenir la structure actuelle
            cur.execute("PRAGMA table_info(evenements)")
            columns = cur.fetchall()
            column_names = [col[1] for col in columns]

            print(f"Colonnes actuelles: {column_names}")

            # Vérifier si rappel_minutes existe
            if 'rappel_minutes' not in column_names:
                print("➕ Ajout de la colonne rappel_minutes...")
                try:
                    cur.execute("ALTER TABLE evenements ADD COLUMN rappel_minutes INTEGER DEFAULT 30")
                    conn.commit()
                    print("✅ Colonne rappel_minutes ajoutée")
                except Exception as e:
                    print(f"❌ Erreur lors de l'ajout: {e}")
                    # Si l'ajout échoue, recréer la table
                    print("🔄 Recréation de la table evenements...")

                    # Sauvegarder les données existantes
                    cur.execute("SELECT * FROM evenements")
                    existing_data = cur.fetchall()
                    print(f"📊 {len(existing_data)} événements à sauvegarder")

                    # Supprimer l'ancienne table
                    cur.execute("DROP TABLE evenements")

                    # Recréer la table avec la bonne structure
                    cur.execute('''
                        CREATE TABLE evenements (
                            id INTEGER PRIMARY KEY,
                            user_id INTEGER NOT NULL,
                            titre TEXT NOT NULL,
                            description TEXT,
                            date_debut TEXT NOT NULL,
                            date_fin TEXT,
                            heure_debut TEXT,
                            heure_fin TEXT,
                            lieu TEXT,
                            couleur TEXT DEFAULT '#fd7e14',
                            rappel_minutes INTEGER DEFAULT 30,
                            termine BOOLEAN DEFAULT FALSE,
                            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            rappel TEXT,
                            FOREIGN KEY (user_id) REFERENCES users (id)
                        )
                    ''')

                    # Réinsérer les données si possible
                    if existing_data:
                        print("📥 Réinsertion des données...")
                        for row in existing_data:
                            # Adapter les données à la nouvelle structure
                            if len(row) >= 14:  # Ancienne structure
                                cur.execute('''
                                    INSERT INTO evenements
                                    (id, user_id, titre, description, date_debut, date_fin, heure_debut, heure_fin, lieu, couleur, rappel_minutes, termine, date_creation, rappel)
                                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                ''', row)
                            else:
                                print(f"⚠️  Données incompatibles ignorées: {row}")

                    conn.commit()
                    print("✅ Table evenements recréée avec succès")
            else:
                print("✅ Colonne rappel_minutes existe déjà")
        else:
            print("➕ Création de la table evenements...")
            cur.execute('''
                CREATE TABLE evenements (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    titre TEXT NOT NULL,
                    description TEXT,
                    date_debut TEXT NOT NULL,
                    date_fin TEXT,
                    heure_debut TEXT,
                    heure_fin TEXT,
                    lieu TEXT,
                    couleur TEXT DEFAULT '#fd7e14',
                    rappel_minutes INTEGER DEFAULT 30,
                    termine BOOLEAN DEFAULT FALSE,
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    rappel TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.commit()
            print("✅ Table evenements créée")

        # Vérification finale
        cur.execute("PRAGMA table_info(evenements)")
        final_columns = cur.fetchall()
        print("📋 Structure finale:")
        for col in final_columns:
            print(f"  - {col[1]} ({col[2]}) - Default: {col[4]}")

        cur.close()
        conn.close()
        print("🎉 Correction terminée!")

    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")

if __name__ == "__main__":
    force_fix_evenements()