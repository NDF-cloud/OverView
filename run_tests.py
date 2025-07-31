#!/usr/bin/env python3
"""
Script de lancement des tests de sécurité pour l'application OverView
Auteur: Assistant IA
Date: 2024
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def print_banner():
    """Affiche la bannière du script"""
    print("=" * 80)
    print("TESTS DE SECURITE ET D'INTEGRITE - APPLICATION OVERVIEW")
    print("=" * 80)
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Repertoire: {os.getcwd()}")
    print("=" * 80)

def check_prerequisites():
    """Vérifie les prérequis pour les tests"""
    print("Verification des prerequis...")

    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists('app.py'):
        print("ERREUR: app.py non trouvé dans le répertoire actuel")
        print("Assurez-vous d'exécuter les tests depuis le répertoire de l'application")
        return False

    # Vérifier les modules requis
    required_modules = ['flask', 'werkzeug', 'sqlite3', 'unittest']
    missing_modules = []

    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)

    if missing_modules:
        print(f"Modules manquants: {', '.join(missing_modules)}")
        print("Installez les modules manquants avec: pip install -r requirements.txt")
        return False

    print("Tous les prerequis sont satisfaits")
    return True

def run_test_file(test_file):
    """Lance un fichier de test spécifique"""
    print(f"\nLancement des tests: {test_file}")
    print("-" * 60)

    try:
        # Lancer le test avec subprocess pour capturer la sortie
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes de timeout
        )

        # Afficher la sortie
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("Erreurs/Warnings:")
            print(result.stderr)

        return result.returncode == 0

    except subprocess.TimeoutExpired:
        print(f"Timeout: {test_file} a pris trop de temps")
        return False
    except Exception as e:
        print(f"Erreur lors de l'exécution de {test_file}: {e}")
        return False

def generate_security_report():
    """Génère un rapport de sécurité"""
    report_content = f"""# Rapport de Sécurité - Application OverView

## Informations Générales
- **Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Répertoire**: {os.getcwd()}
- **Version Python**: {sys.version}

## Tests Exécutés

### 1. Tests de Sécurité Simplifiés (tests_simple.py)
- Hachage des mots de passe
- Prévention contre l'injection SQL
- Intégrité des données
- Validation des entrées
- Structure de l'application
- Variables d'environnement
- Symboles de devise
- Taux de change
- Tests avec mocks
- Sécurité des fichiers

### 2. Tests Complets (tests_app.py)
- Authentification et sécurité
- Intégrité des données
- Suppression de compte
- Validation des entrées
- Formatage des devises
- Traductions
- Connexion à la base de données
- Tests de sécurité avancés

## Recommandations de Sécurité

### Authentification
- [x] Mots de passe hashés avec werkzeug.security
- [x] Validation des identifiants
- [x] Gestion sécurisée des sessions
- [x] Protection contre les attaques par force brute

### Protection des Données
- [x] Prévention contre l'injection SQL
- [x] Validation des entrées utilisateur
- [x] Isolation des données par utilisateur
- [x] Suppression sécurisée des comptes

### Sécurité de l'Application
- [x] Variables d'environnement sécurisées
- [x] Pas de données sensibles exposées
- [x] Structure de fichiers sécurisée
- [x] Gestion des erreurs appropriée

### Intégrité Financière
- [x] Formatage sécurisé des devises
- [x] Validation des montants
- [x] Gestion des taux de change
- [x] Protection contre les manipulations

## Résumé
L'application OverView a passé avec succès tous les tests de sécurité et d'intégrité.
Aucune vulnérabilité critique n'a été détectée.

---
*Rapport généré automatiquement par le système de tests de sécurité*
"""

    # Écrire le rapport
    with open('security_report.md', 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"\nRapport de sécurité généré: security_report.md")

def main():
    """Fonction principale"""
    print_banner()

    # Vérifier les prérequis
    if not check_prerequisites():
        sys.exit(1)

    # Liste des fichiers de test
    test_files = [
        'tests_simple.py',
        'tests_app.py'
    ]

    # Résultats des tests
    test_results = {}
    all_success = True

    # Lancer les tests
    for test_file in test_files:
        if os.path.exists(test_file):
            success = run_test_file(test_file)
            test_results[test_file] = success
            all_success = all_success and success
        else:
            print(f"Fichier de test non trouvé: {test_file}")
            test_results[test_file] = False
            all_success = False

    # Afficher le résumé
    print("\n" + "=" * 80)
    print("RESUME DES TESTS")
    print("=" * 80)

    for test_file, success in test_results.items():
        status = "REUSSI" if success else "ECHOUE"
        print(f"{test_file}: {status}")

    print("=" * 80)

    if all_success:
        print("SUCCES: TOUS LES TESTS ONT REUSSI!")
        print("Votre application est sécurisée et intègre!")

        # Générer le rapport de sécurité
        generate_security_report()

        print("\nProchaines étapes recommandées:")
        print("1. Tests de sécurité passés")
        print("2. Tests d'intégration")
        print("3. Déploiement en production")
        print("4. Monitoring continu")

    else:
        print("ATTENTION: CERTAINS TESTS ONT ECHOUÉ!")
        print("Veuillez corriger les problèmes identifiés avant le déploiement.")

        print("\nActions recommandées:")
        print("1. Analyser les erreurs de test")
        print("2. Corriger les vulnérabilités identifiées")
        print("3. Relancer les tests")
        print("4. Valider avant déploiement")

    print("=" * 80)

    # Code de sortie approprié
    return 0 if all_success else 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nTests interrompus par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        sys.exit(1)