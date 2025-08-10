#!/usr/bin/env python3
"""
Script de lancement de l'application web
"""

import os
import sys
import subprocess
import webbrowser
import time

def main():
    print("=" * 50)
    print("  LANCEMENT DE L'APPLICATION WEB")
    print("=" * 50)
    print()
    
    # Verifier que Python portable existe
    python_path = "python-portable/python.exe"
    if not os.path.exists(python_path):
        print("Erreur: Python portable non trouve!")
        print("Veuillez verifier que le dossier python-portable existe")
        return
    
    # Verifier que le script de lancement existe
    launch_script = "launch_web.py"
    if not os.path.exists(launch_script):
        print("Erreur: Script de lancement non trouve!")
        return
    
    print("Python portable trouve:", python_path)
    print("Script de lancement trouve:", launch_script)
    print()
    
    # Lancer l'application
    print("Demarrage du serveur web...")
    print("URL: http://localhost:5000")
    print()
    print("Le navigateur s'ouvrira automatiquement")
    print("Appuyez sur Ctrl+C pour arreter")
    print()
    
    try:
        # Lancer le serveur web
        subprocess.run([python_path, launch_script])
    except KeyboardInterrupt:
        print("\nArret de l'application...")
    except Exception as e:
        print(f"Erreur lors du lancement: {e}")

if __name__ == "__main__":
    main()