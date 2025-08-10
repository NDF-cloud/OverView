#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script pour démarrer l'application OverView avec le bon répertoire de travail
"""

import os
import sys

# Changer vers le répertoire de l'application
app_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(app_dir)
print(f"📁 Répertoire de travail: {os.getcwd()}")

# Ajouter le répertoire courant au chemin Python
sys.path.insert(0, app_dir)

# Maintenant importer et lancer l'application
from app import app, init_database

def start_application():
    """Démarrer l'application"""

    print("🚀 Démarrage d'OverView...")
    print("=" * 40)

    # Vérifier si la base de données est initialisée
    print("🔍 Vérification de la base de données...")

    try:
        # Initialiser la base de données si nécessaire
        init_database()

        print("✅ Base de données prête")
        print("✅ Application prête à démarrer")
        print("\n🌐 L'application sera accessible à l'adresse:")
        print("   http://localhost:5000")
        print("\n📱 Pour arrêter l'application, appuyez sur Ctrl+C")
        print("=" * 40)

        # Démarrer l'application
        app.run(debug=True, host='0.0.0.0', port=5000)

    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return False

if __name__ == "__main__":
    start_application()
