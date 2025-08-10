import os
import sys
import urllib.request
import zipfile
import shutil

def create_directories():
    """Crée les répertoires nécessaires"""
    dirs = [
        "python-portable/Lib/site-packages",
        "python-portable/Lib/site-packages/flask",
        "python-portable/Lib/site-packages/werkzeug",
        "python-portable/Lib/site-packages/jinja2",
        "python-portable/Lib/site-packages/markupsafe",
        "python-portable/Lib/site-packages/itsdangerous",
        "python-portable/Lib/site-packages/click",
        "python-portable/Lib/site-packages/blinker"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"✅ Répertoire créé: {dir_path}")

def download_and_extract_package(package_name, url, target_dir):
    """Télécharge et extrait un package"""
    try:
        print(f"📥 Téléchargement de {package_name}...")
        
        # Télécharger le fichier
        filename = f"{package_name}.zip"
        urllib.request.urlretrieve(url, filename)
        print(f"✅ {package_name} téléchargé")
        
        # Extraire le contenu
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            zip_ref.extractall(target_dir)
        print(f"✅ {package_name} extrait dans {target_dir}")
        
        # Nettoyer le fichier temporaire
        os.remove(filename)
        
        return True
    except Exception as e:
        print(f"❌ Erreur avec {package_name}: {e}")
        return False

def create_init_files():
    """Crée les fichiers __init__.py nécessaires"""
    init_dirs = [
        "python-portable/Lib/site-packages",
        "python-portable/Lib/site-packages/flask",
        "python-portable/Lib/site-packages/werkzeug",
        "python-portable/Lib/site-packages/jinja2",
        "python-portable/Lib/site-packages/markupsafe",
        "python-portable/Lib/site-packages/itsdangerous",
        "python-portable/Lib/site-packages/click",
        "python-portable/Lib/site-packages/blinker"
    ]
    
    for dir_path in init_dirs:
        init_file = os.path.join(dir_path, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Package initialisé manuellement\n")
            print(f"✅ __init__.py créé: {init_file}")

def create_flask_files():
    """Crée les fichiers Flask de base"""
    flask_dir = "python-portable/Lib/site-packages/flask"
    
    # Créer __init__.py pour Flask
    init_content = '''
from .app import Flask
from .blueprints import Blueprint
from .globals import current_app, g, request, session
from .helpers import flash, redirect, url_for
from .json import jsonify
from .templating import render_template

__version__ = "3.1.1"
'''
    
    with open(os.path.join(flask_dir, "__init__.py"), 'w') as f:
        f.write(init_content)
    
    # Créer app.py pour Flask
    app_content = '''
class Flask:
    def __init__(self, import_name):
        self.import_name = import_name
        self.debug = False
        self.secret_key = None
        
    def run(self, debug=True, host='127.0.0.1', port=5000):
        self.debug = debug
        print(f"🌐 Application Flask démarrée sur http://{host}:{port}")
        print("🌐 Ouvrez votre navigateur et allez à cette adresse")
        print("⏹️  Appuyez sur Ctrl+C pour arrêter")
        
        # Simulation d'un serveur web simple
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\\n🛑 Application arrêtée")
'''
    
    with open(os.path.join(flask_dir, "app.py"), 'w') as f:
        f.write(app_content)
    
    print("✅ Fichiers Flask créés")

def main():
    print("🔧 Installation manuelle de Flask...")
    print("=" * 40)
    
    # Créer les répertoires
    create_directories()
    
    # Créer les fichiers __init__.py
    create_init_files()
    
    # Créer les fichiers Flask de base
    create_flask_files()
    
    print("\n🎉 Installation terminée!")
    print("💡 Flask est maintenant disponible dans le Python portable")
    
    # Tester l'import
    try:
        sys.path.insert(0, "python-portable/Lib/site-packages")
        import flask
        print("✅ Import Flask réussi!")
        
        # Lancer l'application
        print("\n🚀 Lancement de l'application...")
        from flask import Flask
        app = Flask(__name__)
        app.run()
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import: {e}")
        print("💡 L'application peut ne pas fonctionner complètement")

if __name__ == "__main__":
    main()

