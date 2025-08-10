import subprocess
import sys
import os

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} installé avec succès!")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Erreur lors de l'installation de {package}")
        return False

def main():
    print("🔧 Installation des dépendances...")
    
    packages = ["flask", "psycopg2-binary", "werkzeug"]
    
    for package in packages:
        if install_package(package):
            print(f"✅ {package} installé")
        else:
            print(f"❌ Échec de l'installation de {package}")
    
    print("🎉 Installation terminée!")

if __name__ == "__main__":
    main()

