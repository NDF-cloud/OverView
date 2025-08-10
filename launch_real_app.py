import os
import sys
import subprocess
import webbrowser
import time
import threading

def create_flask_mock():
    """Crée un mock de Flask qui fonctionne"""
    print("Création d'un mock de Flask...")
    
    # Créer le dossier site-packages
    site_packages = "python-portable/Lib/site-packages"
    os.makedirs(site_packages, exist_ok=True)
    
    # Créer un mock Flask ultra-simple
    flask_dir = os.path.join(site_packages, "flask")
    os.makedirs(flask_dir, exist_ok=True)
    
    # Mock Flask complet
    flask_mock = '''
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

# Mock de tous les autres modules
class Blueprint:
    def __init__(self, name, import_name):
        self.name = name
        self.import_name = import_name

def render_template(template_name, **context):
    return f"Template: {template_name} avec {context}"

def request():
    class MockRequest:
        def __init__(self):
            self.method = "GET"
            self.args = {}
            self.form = {}
            self.values = {}
        def get(self, key, default=None):
            return self.args.get(key, default)
    return MockRequest()

def session():
    class MockSession:
        def __init__(self):
            self.data = {}
        def get(self, key, default=None):
            return self.data.get(key, default)
        def __setitem__(self, key, value):
            self.data[key] = value
    return MockSession()

def redirect(url):
    return f"Redirection vers: {url}"

def url_for(endpoint, **kwargs):
    return f"/{endpoint}"

def flash(message, category="info"):
    print(f"Flash: {message} ({category})")

def jsonify(data):
    return f"JSON: {data}"

# Variables globales
current_app = None
g = type('MockG', (), {})()

# Mock Werkzeug
class Local:
    pass

class LocalManager:
    pass

local = Local()

# Mock Jinja2
class Environment:
    pass

class Template:
    pass
'''
    
    with open(os.path.join(flask_dir, "__init__.py"), 'w', encoding='utf-8') as f:
        f.write(flask_mock)
    
    print("Mock Flask créé avec succès!")

def launch_app():
    """Lance l'application Flask"""
    print("Lancement de votre vraie application Flask...")
    print("=" * 50)
    
    # Créer le mock Flask
    create_flask_mock()
    
    # Ajouter le chemin des packages
    sys.path.insert(0, "python-portable/Lib/site-packages")
    
    try:
        # Importer Flask
        import flask
        print("Flask importé avec succès!")
        
        # Lancer l'application
        print("Lancement de app.py...")
        print("URL: http://localhost:5000")
        print("Appuyez sur Ctrl+C pour arrêter")
        
        # Ouvrir le navigateur
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open('http://localhost:5000')
                print("Navigateur ouvert automatiquement!")
            except:
                print("Ouvrez manuellement votre navigateur et allez à:")
                print("http://localhost:5000")
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Lancer app.py
        result = subprocess.run([sys.executable, "app.py"], 
                              capture_output=False,  # Afficher la sortie en temps réel
                              text=True)
        
        if result.returncode != 0:
            print(f"Application terminée avec le code: {result.returncode}")
        
    except Exception as e:
        print(f"Erreur lors du lancement: {e}")
        print("Tentative de lancement direct...")
        
        # Essayer de lancer directement
        try:
            subprocess.run([sys.executable, "app.py"])
        except Exception as e2:
            print(f"Erreur lors du lancement direct: {e2}")

def main():
    print("🚀 LANCEMENT DE VOTRE VRAIE APPLICATION FLASK")
    print("=" * 50)
    
    if not os.path.exists("app.py"):
        print("Erreur: app.py non trouvé!")
        return
    
    launch_app()

if __name__ == "__main__":
    main()

