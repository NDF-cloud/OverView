import http.server
import socketserver
import webbrowser
import threading
import time
import os

def main():
    print("Lancement du serveur web...")
    print("=" * 30)
    
    # Port du serveur
    PORT = 5000
    
    # Changer le repertoire de travail
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Creer le serveur
    handler = http.server.SimpleHTTPRequestHandler
    server = socketserver.TCPServer(("", PORT), handler)
    
    print(f"Serveur demarre sur le port {PORT}")
    print(f"URL: http://localhost:{PORT}")
    print("Appuyez sur Ctrl+C pour arreter")
    
    # Ouvrir le navigateur automatiquement
    def open_browser():
        time.sleep(2)
        try:
            webbrowser.open(f'http://localhost:{PORT}')
            print("Navigateur ouvert automatiquement!")
        except:
            print("Ouvrez manuellement votre navigateur et allez a:")
            print(f"http://localhost:{PORT}")
    
    # Lancer l'ouverture du navigateur
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Demarrer le serveur
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArret du serveur...")
        server.shutdown()
        server.server_close()
        print("Serveur arrete.")

if __name__ == "__main__":
    main()

