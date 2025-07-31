#!/usr/bin/env python3
# ==============================================================================
# SCRIPT DE TEST POUR VÉRIFIER LE DÉPLOIEMENT
# ==============================================================================
import os
import sys

def test_imports():
    """Teste que tous les imports nécessaires fonctionnent"""
    print("🔍 Test des imports...")

    try:
        from flask import Flask
        print("✅ Flask importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import Flask: {e}")
        return False

    try:
        import psycopg
        print("✅ psycopg importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import psycopg: {e}")
        return False

    try:
        import psycopg.errors
        print("✅ psycopg.errors importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import psycopg.errors: {e}")
        return False

    try:
        import sqlite3
        print("✅ sqlite3 importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur import sqlite3: {e}")
        return False

    return True

def test_app_creation():
    """Teste que l'application Flask peut être créée"""
    print("🔍 Test de création de l'application...")

    try:
        # Simuler l'environnement de production
        os.environ['DATABASE_URL'] = 'postgresql://test:test@localhost/test'

        # Importer l'application
        from app import app

        print("✅ Application Flask créée avec succès")
        return True

    except Exception as e:
        print(f"❌ Erreur lors de la création de l'application: {e}")
        return False

def test_database_connection():
    """Teste la connexion à la base de données"""
    print("🔍 Test de connexion à la base de données...")

    try:
        from app import get_db_connection

        # Test avec SQLite (mode local)
        os.environ.pop('DATABASE_URL', None)
        conn = get_db_connection()

        if conn:
            print("✅ Connexion SQLite réussie")
            conn.close()
            return True
        else:
            print("❌ Échec de la connexion SQLite")
            return False

    except Exception as e:
        print(f"❌ Erreur lors du test de connexion: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Démarrage des tests de déploiement...")

    tests = [
        ("Imports", test_imports),
        ("Création de l'application", test_app_creation),
        ("Connexion à la base de données", test_database_connection)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Test: {test_name}")
        if test_func():
            passed += 1
        else:
            print(f"❌ Test '{test_name}' a échoué")

    print(f"\n📊 Résultats: {passed}/{total} tests réussis")

    if passed == total:
        print("✅ Tous les tests sont passés! L'application est prête pour le déploiement.")
        return 0
    else:
        print("❌ Certains tests ont échoué. Veuillez corriger les problèmes avant le déploiement.")
        return 1

if __name__ == '__main__':
    sys.exit(main())