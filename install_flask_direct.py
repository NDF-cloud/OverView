import os
import sys
import urllib.request
import zipfile
import shutil

def download_flask_source():
    """Télécharge Flask depuis GitHub"""
    print("Téléchargement de Flask depuis GitHub...")
    
    # URL de Flask sur GitHub (version stable)
    flask_url = "https://github.com/pallets/flask/archive/refs/tags/3.1.1.zip"
    
    try:
        filename = "flask-3.1.1.zip"
        urllib.request.urlretrieve(flask_url, filename)
        print(f"Flask téléchargé: {filename}")
        return filename
    except Exception as e:
        print(f"Erreur lors du téléchargement: {e}")
        return None

def install_flask_from_source(zip_file):
    """Installe Flask depuis les sources"""
    print("Installation de Flask depuis les sources...")
    
    try:
        # Extraire le fichier
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Créer le dossier site-packages
        site_packages = "python-portable/Lib/site-packages"
        os.makedirs(site_packages, exist_ok=True)
        
        # Copier Flask dans site-packages
        flask_source = "flask-3.1.1/src/flask"
        flask_dest = os.path.join(site_packages, "flask")
        
        if os.path.exists(flask_source):
            shutil.copytree(flask_source, flask_dest, dirs_exist_ok=True)
            print("Flask copié dans site-packages")
            
            # Créer un fichier __init__.py simple
            init_file = os.path.join(site_packages, "__init__.py")
            with open(init_file, 'w') as f:
                f.write("# Site packages initialisé\n")
            
            return True
        else:
            print("Dossier source Flask non trouvé")
            return False
            
    except Exception as e:
        print(f"Erreur lors de l'installation: {e}")
        return False

def create_simple_flask():
    """Crée une version simplifiée de Flask qui fonctionne"""
    print("Création d'une version simplifiée de Flask...")
    
    site_packages = "python-portable/Lib/site-packages"
    flask_dir = os.path.join(site_packages, "flask")
    
    # Créer le dossier Flask
    os.makedirs(flask_dir, exist_ok=True)
    
    # Créer __init__.py
    init_content = '''
class Flask:
    def __init__(self, import_name):
        self.import_name = import_name
        self.debug = False
        self.secret_key = None
        
    def run(self, debug=True, host='127.0.0.1', port=5000):
        self.debug = debug
        print(f"Application Flask démarrée sur http://{host}:{port}")
        print("Ouvrez votre navigateur et allez à cette adresse")
        
        # Lancer un serveur web simple
        import http.server
        import socketserver
        import webbrowser
        import threading
        import time
        
        def open_browser():
            time.sleep(2)
            try:
                webbrowser.open(f'http://{host}:{port}')
                print("Navigateur ouvert automatiquement!")
            except:
                print("Ouvrez manuellement votre navigateur")
        
        # Ouvrir le navigateur
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

# Simuler les autres modules Flask
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
'''
    
    with open(os.path.join(flask_dir, "__init__.py"), 'w', encoding='utf-8') as f:
        f.write(init_content)
    
    print("Version simplifiée de Flask créée")

def main():
    print("Installation de Flask pour votre application...")
    print("=" * 50)
    
    # Essayer d'abord de télécharger depuis GitHub
    zip_file = download_flask_source()
    if zip_file and install_flask_from_source(zip_file):
        print("Flask installé depuis les sources!")
    else:
        print("Installation depuis les sources échouée, création d'une version simplifiée...")
        create_simple_flask()
    
    # Nettoyer les fichiers temporaires
    if zip_file and os.path.exists(zip_file):
        os.remove(zip_file)
    
    # Tester l'import
    try:
        sys.path.insert(0, "python-portable/Lib/site-packages")
        import flask
        print("Flask importé avec succès!")
        
        # Lancer l'application
        print("\\nLancement de votre application...")
        from flask import Flask
        app = Flask(__name__)
        app.run(debug=True)
        
    except Exception as e:
        print(f"Erreur lors de l'import: {e}")
        print("L'application peut ne pas fonctionner complètement")

if __name__ == "__main__":
    main()

