import os
import sys
import subprocess
import shutil

def ensure_pip():
    """Installe pip en utilisant ensurepip"""
    print("Installation de pip...")
    
    try:
        # Utiliser ensurepip pour installer pip
        result = subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("pip installe avec succes!")
            return True
        else:
            print(f"Erreur lors de l'installation de pip: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def install_flask():
    """Installe Flask avec pip"""
    print("Installation de Flask...")
    
    try:
        # Installer Flask
        result = subprocess.run([sys.executable, "-m", "pip", "install", "flask"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Flask installe avec succes!")
            return True
        else:
            print(f"Erreur lors de l'installation de Flask: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"Erreur: {e}")
        return False

def test_flask():
    """Teste si Flask fonctionne"""
    print("Test de Flask...")
    
    try:
        import flask
        print("Flask importe avec succes!")
        
        from flask import Flask
        app = Flask(__name__)
        print("Classe Flask creee avec succes!")
        
        return True
        
    except Exception as e:
        print(f"Erreur lors du test: {e}")
        return False

def launch_app():
    """Lance l'application Flask"""
    print("Lancement de l'application...")
    
    try:
        # Lancer l'application
        result = subprocess.run([sys.executable, "app.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Application lancee avec succes!")
        else:
            print(f"Erreur lors du lancement: {result.stderr}")
            
    except Exception as e:
        print(f"Erreur: {e}")

def main():
    print("Installation de pip et Flask...")
    print("=" * 40)
    
    # Installer pip
    if ensure_pip():
        # Installer Flask
        if install_flask():
            # Tester Flask
            if test_flask():
                print("Flask fonctionne! Lancement de l'application...")
                launch_app()
            else:
                print("Flask ne fonctionne pas")
        else:
            print("Impossible d'installer Flask")
    else:
        print("Impossible d'installer pip")

if __name__ == "__main__":
    main()

