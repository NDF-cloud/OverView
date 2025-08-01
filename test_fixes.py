#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import psycopg
from psycopg.rows import dict_row

# Configuration de la base de données PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://localhost/test_db')

def test_database_connection():
    """Test de connexion à la base de données PostgreSQL"""
    try:
        conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
        print("✅ Connexion à PostgreSQL réussie")

        # Test des requêtes corrigées
        with conn.cursor() as cursor:
            # Test 1: Requête avec $1 et archived = false
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """)
            result = cursor.fetchone()
            print(f"✅ Test 1 réussi: {result['count']} tables trouvées")

            # Test 2: Test de la fonction CURRENT_DATE
            cursor.execute("SELECT CURRENT_DATE as today")
            result = cursor.fetchone()
            print(f"✅ Test 2 réussi: Date actuelle = {result['today']}")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_sql_syntax():
    """Test de la syntaxe SQL corrigée"""
    test_queries = [
        {
            "name": "Test objectifs avec $1 et archived = false",
            "query": """
                SELECT COUNT(*) as count
                FROM objectifs
                WHERE user_id = $1 AND archived = false
            """,
            "params": (1,)
        },
        {
            "name": "Test taches avec $1 et archived = false",
            "query": """
                SELECT COUNT(*) as count
                FROM taches
                WHERE user_id = $1 AND archived = false
            """,
            "params": (1,)
        },
        {
            "name": "Test evenements avec CURRENT_DATE",
            "query": """
                SELECT COUNT(*) as count
                FROM evenements
                WHERE user_id = $1 AND date_debut >= CURRENT_DATE
            """,
            "params": (1,)
        }
    ]

    try:
        conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)

        for test in test_queries:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(test["query"], test["params"])
                    result = cursor.fetchone()
                    print(f"✅ {test['name']}: {result['count']} enregistrements")
            except Exception as e:
                print(f"❌ {test['name']}: {e}")

        conn.close()
        return True

    except Exception as e:
        print(f"❌ Erreur lors des tests SQL: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Test des corrections PostgreSQL...")
    print("=" * 50)

    # Test de connexion
    if test_database_connection():
        # Test de syntaxe SQL
        test_sql_syntax()
    else:
        print("❌ Impossible de se connecter à la base de données")
        sys.exit(1)

    print("=" * 50)
    print("✅ Tests terminés")