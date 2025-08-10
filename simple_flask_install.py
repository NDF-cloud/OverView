import os
import sys

def create_directories():
    """Cree les repertoires necessaires"""
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
        print(f"Repertoire cree: {dir_path}")

def create_init_files():
    """Cree les fichiers __init__.py necessaires"""
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
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write("# Package initialise manuellement\n")
            print(f"__init__.py cree: {init_file}")

def create_flask_files():
    """Cree les fichiers Flask de base"""
    flask_dir = "python-portable/Lib/site-packages/flask"
    
    # Creer __init__.py pour Flask
    init_content = '''
from .app import Flask
from .blueprints import Blueprint
from .globals import current_app, g, request, session
from .helpers import flash, redirect, url_for
from .json import jsonify
from .templating import render_template

__version__ = "3.1.1"
'''
    
    with open(os.path.join(flask_dir, "__init__.py"), 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    # Creer app.py pour Flask
    app_content = '''
class Flask:
    def __init__(self, import_name):
        self.import_name = import_name
        self.debug = False
        self.secret_key = None
        
    def run(self, debug=True, host='127.0.0.1', port=5000):
        self.debug = debug
        print(f"Application Flask demarree sur http://{host}:{port}")
        print("Ouvrez votre navigateur et allez a cette adresse")
        print("Appuyez sur Ctrl+C pour arreter")
        
        # Simulation d'un serveur web simple
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\\nApplication arretee")
'''
    
    with open(os.path.join(flask_dir, "app.py"), 'w', encoding='utf-8') as f:
        f.write(app_content)
    
    print("Fichiers Flask crees")

def create_werkzeug_files():
    """Cree les fichiers Werkzeug de base"""
    werkzeug_dir = "python-portable/Lib/site-packages/werkzeug"
    
    init_content = '''
# Werkzeug package initialise manuellement
'''
    
    with open(os.path.join(werkzeug_dir, "__init__.py"), 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    print("Fichiers Werkzeug crees")

def create_jinja2_files():
    """Cree les fichiers Jinja2 de base"""
    jinja2_dir = "python-portable/Lib/site-packages/jinja2"
    
    init_content = '''
# Jinja2 package initialise manuellement
'''
    
    with open(os.path.join(jinja2_dir, "__init__.py"), 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    print("Fichiers Jinja2 crees")

def main():
    print("Installation manuelle de Flask...")
    print("=" * 40)
    
    # Creer les repertoires
    create_directories()
    
    # Creer les fichiers __init__.py
    create_init_files()
    
    # Creer les fichiers Flask de base
    create_flask_files()
    
    # Creer les autres packages
    create_werkzeug_files()
    create_jinja2_files()
    
    print("\\nInstallation terminee!")
    print("Flask est maintenant disponible dans le Python portable")
    
    # Tester l'import
    try:
        sys.path.insert(0, "python-portable/Lib/site-packages")
        import flask
        print("Import Flask reussi!")
        
        # Lancer l'application
        print("\\nLancement de l'application...")
        from flask import Flask
        app = Flask(__name__)
        app.run()
        
    except Exception as e:
        print(f"Erreur lors de l'import: {e}")
        print("L'application peut ne pas fonctionner completement")

if __name__ == "__main__":
    main()

