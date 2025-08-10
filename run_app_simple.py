import os
import sys
import subprocess
import webbrowser
import time

def main():
    print("Lancement de l'application web...")
    print("=" * 40)
    
    # Verifier que app.py existe
    if not os.path.exists("app.py"):
        print("Erreur: app.py non trouve!")
        return
    
    # Essayer de lancer avec Python portable
    python_path = "python-portable/python.exe"
    
    if os.path.exists(python_path):
        print(f"Utilisation de: {python_path}")
        
        try:
            # Lancer l'application
            print("Lancement de l'application...")
            print("URL: http://localhost:5000")
            print("Appuyez sur Ctrl+C pour arreter")
            
            # Ouvrir le navigateur apres un delai
            def open_browser():
                time.sleep(3)
                try:
                    webbrowser.open('http://localhost:5000')
                    print("Navigateur ouvert automatiquement!")
                except:
                    print("Ouvrez manuellement: http://localhost:5000")
            
            # Lancer l'ouverture du navigateur dans un thread
            import threading
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            # Lancer l'application
            process = subprocess.Popen([python_path, "app.py"], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            print("Application lancee! PID:", process.pid)
            
            # Attendre que l'application se termine
            stdout, stderr = process.communicate()
            
            if stdout:
                print("Sortie:", stdout.decode())
            if stderr:
                print("Erreurs:", stderr.decode())
                
        except KeyboardInterrupt:
            print("\nArret de l'application...")
            if 'process' in locals():
                process.terminate()
        except Exception as e:
            print(f"Erreur lors du lancement: {e}")
            
            # Essayer de lancer avec le serveur simple
            print("\nTentative avec le serveur simple...")
            try:
                subprocess.run([python_path, "simple_server.py"])
            except Exception as e2:
                print(f"Erreur avec le serveur simple: {e2}")
    else:
        print("Python portable non trouve!")
        print("Veuillez installer Python ou utiliser le Python systeme")

if __name__ == "__main__":
    main()

