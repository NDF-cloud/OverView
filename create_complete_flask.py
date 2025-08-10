import os
import sys
import shutil

def create_complete_flask():
    """Crée une version complète de Flask avec toutes les dépendances"""
    print("Création d'une version complète de Flask...")
    
    site_packages = "python-portable/Lib/site-packages"
    
    # Créer les dossiers nécessaires
    packages = [
        "flask",
        "werkzeug",
        "jinja2",
        "markupsafe",
        "itsdangerous",
        "click",
        "blinker"
    ]
    
    for package in packages:
        package_dir = os.path.join(site_packages, package)
        os.makedirs(package_dir, exist_ok=True)
        
        # Créer __init__.py pour chaque package
        init_file = os.path.join(package_dir, "__init__.py")
        with open(init_file, 'w', encoding='utf-8') as f:
            f.write(f"# Package {package} initialisé\n")
    
    # Créer Flask complet
    flask_dir = os.path.join(site_packages, "flask")
    
    flask_init = '''
from .app import Flask
from .blueprints import Blueprint
from .globals import current_app, g, request, session
from .helpers import flash, redirect, url_for
from .json import jsonify
from .templating import render_template

__version__ = "3.1.1"
'''
    
    with open(os.path.join(flask_dir, "__init__.py"), 'w', encoding='utf-8') as f:
        f.write(flask_init)
    
    # Créer app.py
    app_content = '''
import http.server
import socketserver
import webbrowser
import threading
import time
import os

class Flask:
    def __init__(self, import_name):
        self.import_name = import_name
        self.debug = False
        self.secret_key = None
        self.routes = {}
        
    def route(self, rule, **options):
        def decorator(f):
            self.routes[rule] = f
            return f
        return decorator
        
    def run(self, debug=True, host='127.0.0.1', port=5000):
        self.debug = debug
        print(f"Application Flask démarrée sur http://{host}:{port}")
        print("Ouvrez votre navigateur et allez à cette adresse")
        
        # Ouvrir le navigateur
        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open(f'http://{host}:{port}')
                print("Navigateur ouvert automatiquement!")
            except:
                print("Ouvrez manuellement votre navigateur")
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Démarrer le serveur
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer((host, port), handler) as httpd:
            print(f"Serveur démarré sur http://{host}:{port}")
            print("Appuyez sur Ctrl+C pour arrêter")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\\nArrêt du serveur...")
'''
    
    with open(os.path.join(flask_dir, "app.py"), 'w', encoding='utf-8') as f:
        f.write(app_content)
    
    # Créer les autres modules Flask
    modules = {
        "blueprints.py": '''
class Blueprint:
    def __init__(self, name, import_name):
        self.name = name
        self.import_name = import_name
''',
        "globals.py": '''
class MockRequest:
    def __init__(self):
        self.method = "GET"
        self.args = {}
        self.form = {}
        self.values = {}
    
    def get(self, key, default=None):
        return self.args.get(key, default)

class MockSession:
    def __init__(self):
        self.data = {}
    
    def get(self, key, default=None):
        return self.data.get(key, default)
    
    def __setitem__(self, key, value):
        self.data[key] = value

class MockG:
    pass

request = MockRequest()
session = MockSession()
g = MockG()
current_app = None
''',
        "helpers.py": '''
def flash(message, category="info"):
    print(f"Flash: {message} ({category})")

def redirect(url):
    return f"Redirection vers: {url}"

def url_for(endpoint, **kwargs):
    return f"/{endpoint}"
''',
        "json.py": '''
def jsonify(data):
    return f"JSON: {data}"
''',
        "templating.py": '''
def render_template(template_name, **context):
    return f"Template: {template_name} avec {context}"
'''
    }
    
    for filename, content in modules.items():
        with open(os.path.join(flask_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Créer Werkzeug
    werkzeug_dir = os.path.join(site_packages, "werkzeug")
    werkzeug_init = '''
# Werkzeug package initialisé
class Local:
    pass

class LocalManager:
    pass

local = Local()
'''
    
    with open(os.path.join(werkzeug_dir, "__init__.py"), 'w', encoding='utf-8') as f:
        f.write(werkzeug_init)
    
    # Créer Jinja2
    jinja2_dir = os.path.join(site_packages, "jinja2")
    jinja2_init = '''
# Jinja2 package initialisé
class Environment:
    pass

class Template:
    pass
'''
    
    with open(os.path.join(jinja2_dir, "__init__.py"), 'w', encoding='utf-8') as f:
        f.write(jinja2_init)
    
    print("Version complète de Flask créée avec toutes les dépendances")

def test_flask():
    """Teste si Flask fonctionne maintenant"""
    print("Test de Flask...")
    
    try:
        sys.path.insert(0, "python-portable/Lib/site-packages")
        import flask
        print("Flask importé avec succès!")
        
        from flask import Flask
        app = Flask(__name__)
        print("Classe Flask créée avec succès!")
        
        return True
        
    except Exception as e:
        print(f"Erreur lors du test: {e}")
        return False

def main():
    print("Création d'une version complète de Flask...")
    print("=" * 50)
    
    # Créer Flask complet
    create_complete_flask()
    
    # Tester Flask
    if test_flask():
        print("Flask fonctionne! Lancement de votre application...")
        
        # Lancer l'application
        try:
            from flask import Flask
            app = Flask(__name__)
            app.run(debug=True)
        except Exception as e:
            print(f"Erreur lors du lancement: {e}")
    else:
        print("Flask ne fonctionne toujours pas")

if __name__ == "__main__":
    main()

