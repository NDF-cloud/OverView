#!/usr/bin/env python3
# ==============================================================================
# SCRIPT DE DIAGNOSTIC POUR LE PROBLÈME D'INSCRIPTION
# ==============================================================================
import os
import sys
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash

def test_database_connection():
    """Teste la connexion à la base de données"""
    print("🔍 Test de connexion à la base de données...")
    
    try:
        from app import get_db_connection
        conn = get_db_connection()
        
        if conn is None:
            print("❌ Échec de connexion à la base de données")
            return False
            
        print("✅ Connexion à la base de données réussie")
        
        # Test de création de table
        cur = conn.cursor()
        try:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    security_question TEXT,
                    security_answer TEXT
                )
            """)
            conn.commit()
            print("✅ Table users créée/vérifiée avec succès")
            
            # Test d'insertion
            test_username = "test_user_debug"
            test_password = "test123"
            test_question = "Test question"
            test_answer = "Test answer"
            
            hashed_password = generate_password_hash(test_password)
            hashed_answer = generate_password_hash(test_answer)
            
            cur.execute("""
                INSERT INTO users (username, password, security_question, security_answer) 
                VALUES (?, ?, ?, ?)
            """, (test_username, hashed_password, test_question, hashed_answer))
            conn.commit()
            print("✅ Test d'insertion réussi")
            
            # Nettoyer le test
            cur.execute("DELETE FROM users WHERE username = ?", (test_username,))
            conn.commit()
            print("✅ Nettoyage du test réussi")
            
        except Exception as e:
            print(f"❌ Erreur lors du test de base de données: {e}")
            return False
        finally:
            cur.close()
            conn.close()
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de connexion: {e}")
        return False

def test_registration_process():
    """Teste le processus d'inscription complet"""
    print("🔍 Test du processus d'inscription...")
    
    try:
        from app import app, get_db_connection
        
        with app.test_client() as client:
            # Test de la page d'inscription
            response = client.get('/register')
            if response.status_code == 200:
                print("✅ Page d'inscription accessible")
            else:
                print(f"❌ Erreur page d'inscription: {response.status_code}")
                return False
            
            # Test d'inscription
            test_data = {
                'username': 'test_user_registration',
                'password': 'test123',
                'security_question': 'Quel est le nom de votre premier animal de compagnie ?',
                'security_answer': 'Rex'
            }
            
            response = client.post('/register', data=test_data, follow_redirects=True)
            
            if response.status_code == 200:
                print("✅ Processus d'inscription réussi")
                
                # Nettoyer le test
                conn = get_db_connection()
                if conn:
                    cur = conn.cursor()
                    cur.execute("DELETE FROM users WHERE username = ?", (test_data['username'],))
                    conn.commit()
                    cur.close()
                    conn.close()
                    print("✅ Nettoyage du test d'inscription réussi")
                
                return True
            else:
                print(f"❌ Erreur lors de l'inscription: {response.status_code}")
                print(f"Contenu de la réponse: {response.data.decode()}")
                return False
                
    except Exception as e:
        print(f"❌ Erreur lors du test d'inscription: {e}")
        return False

def check_environment():
    """Vérifie l'environnement de déploiement"""
    print("🔍 Vérification de l'environnement...")
    
    # Vérifier les variables d'environnement
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        print(f"✅ DATABASE_URL trouvé: {db_url[:20]}...")
    else:
        print("⚠️ DATABASE_URL non défini (mode SQLite)")
    
    # Vérifier les imports
    try:
        import psycopg
        print("✅ psycopg disponible")
    except ImportError:
        print("❌ psycopg non disponible")
    
    try:
        import sqlite3
        print("✅ sqlite3 disponible")
    except ImportError:
        print("❌ sqlite3 non disponible")
    
    try:
        from flask import Flask
        print("✅ Flask disponible")
    except ImportError:
        print("❌ Flask non disponible")

def main():
    """Fonction principale de diagnostic"""
    print("🚀 Démarrage du diagnostic d'inscription...")
    
    # Vérifier l'environnement
    check_environment()
    print()
    
    # Tests
    tests = [
        ("Connexion à la base de données", test_database_connection),
        ("Processus d'inscription", test_registration_process)
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
        print("✅ Tous les tests sont passés! L'inscription devrait fonctionner.")
        return 0
    else:
        print("❌ Certains tests ont échoué. Vérifiez les logs pour plus de détails.")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 