import os
import sys
import subprocess
import urllib.request
import zipfile
import shutil

def download_flask_wheel():
    """Telecharge le wheel Flask depuis PyPI"""
    print("Telechargement de Flask...")
    
    # URL du wheel Flask pour Python 3.11
    flask_url = "https://files.pythonhosted.org/packages/2e/80/6e51de196e441d4a1d1f75c5e80b7355c40cfaac2f74d4d4d8b5f8f5b5b5/Flask-3.1.1-py3-none-any.whl"
    
    try:
        # Telecharger le fichier
        filename = "Flask-3.1.1-py3-none-any.whl"
        urllib.request.urlretrieve(flask_url, filename)
        print(f"Flask telecharge: {filename}")
        return filename
    except Exception as e:
        print(f"Erreur lors du telechargement: {e}")
        return None

def install_from_wheel(wheel_file):
    """Installe Flask depuis le wheel"""
    print("Installation de Flask depuis le wheel...")
    
    try:
        # Extraire le wheel
        with zipfile.ZipFile(wheel_file, 'r') as zip_ref:
            # Lister le contenu
            file_list = zip_ref.namelist()
            print(f"Contenu du wheel: {len(file_list)} fichiers")
            
            # Extraire dans le dossier site-packages
            site_packages = "python-portable/Lib/site-packages"
            zip_ref.extractall(site_packages)
            
        print("Flask extrait avec succes!")
        return True
        
    except Exception as e:
        print(f"Erreur lors de l'extraction: {e}")
        return False

def test_flask():
    """Teste si Flask fonctionne"""
    print("Test de Flask...")
    
    try:
        # Ajouter le chemin des packages
        sys.path.insert(0, "python-portable/Lib/site-packages")
        
        # Importer Flask
        import flask
        print("Flask importe avec succes!")
        
        # Tester la classe Flask
        from flask import Flask
        app = Flask(__name__)
        print("Classe Flask creee avec succes!")
        
        return True
        
    except Exception as e:
        print(f"Erreur lors du test: {e}")
        return False

def main():
    print("Installation finale de Flask...")
    print("=" * 40)
    
    # Telecharger Flask
    wheel_file = download_flask_wheel()
    if not wheel_file:
        print("Impossible de telecharger Flask")
        return
    
    # Installer Flask
    if install_from_wheel(wheel_file):
        print("Flask installe!")
        
        # Tester Flask
        if test_flask():
            print("Flask fonctionne! Lancement de l'application...")
            
            # Lancer l'application
            try:
                from flask import Flask
                app = Flask(__name__)
                app.run(debug=True)
            except Exception as e:
                print(f"Erreur lors du lancement: {e}")
        else:
            print("Flask ne fonctionne pas correctement")
    else:
        print("Echec de l'installation de Flask")
    
    # Nettoyer le fichier temporaire
    if os.path.exists(wheel_file):
        os.remove(wheel_file)

if __name__ == "__main__":
    main()

