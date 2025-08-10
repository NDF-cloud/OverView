import os
import sys
import subprocess
import shutil

def check_python_installation():
    """Vérifie l'installation Python et propose des solutions"""
    print("🔍 Vérification de l'installation Python...")
    
    # Vérifier Python portable
    portable_python = "python-portable/python.exe"
    if os.path.exists(portable_python):
        print(f"✅ Python portable trouvé: {portable_python}")
        
        # Vérifier si pip fonctionne
        try:
            result = subprocess.run([portable_python, "-m", "pip", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ pip fonctionne avec Python portable")
                return portable_python, True
            else:
                print("❌ pip ne fonctionne pas avec Python portable")
                print(f"Erreur: {result.stderr}")
        except Exception as e:
            print(f"❌ Erreur lors de la vérification de pip: {e}")
    
    # Vérifier Python système
    system_python_paths = [
        r"C:\Users\CA\AppData\Local\Programs\Python\Python313\python.exe",
        r"C:\Python313\python.exe",
        r"C:\Python\python.exe"
    ]
    
    for path in system_python_paths:
        if os.path.exists(path):
            print(f"✅ Python système trouvé: {path}")
            return path, False
    
    print("❌ Aucune installation Python valide trouvée")
    return None, False

def install_flask(python_path, is_portable):
    """Installe Flask avec le Python spécifié"""
    print(f"\n🔧 Installation de Flask avec: {python_path}")
    
    try:
        # Essayer d'installer Flask
        cmd = [python_path, "-m", "pip", "install", "flask"]
        print(f"Commande: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Flask installé avec succès!")
            return True
        else:
            print(f"❌ Échec de l'installation: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False

def launch_app(python_path):
    """Lance l'application Flask"""
    print(f"\n🚀 Lancement de l'application avec: {python_path}")
    
    try:
        # Lancer l'application
        cmd = [python_path, "app.py"]
        print(f"Commande: {' '.join(cmd)}")
        
        # Lancer en arrière-plan pour permettre l'ouverture du navigateur
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("✅ Application lancée!")
        print("🌐 Ouvrez votre navigateur et allez à: http://localhost:5000")
        print("⏹️  Appuyez sur Ctrl+C pour arrêter l'application")
        
        # Attendre un peu pour que l'application démarre
        import time
        time.sleep(3)
        
        # Ouvrir le navigateur
        try:
            import webbrowser
            webbrowser.open('http://localhost:5000')
            print("🌐 Navigateur ouvert automatiquement!")
        except:
            print("💡 Ouvrez manuellement: http://localhost:5000")
        
        # Attendre que l'utilisateur arrête l'application
        process.wait()
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

def main():
    print("🔧 Diagnostic et résolution des problèmes Python/Flask")
    print("=" * 50)
    
    # Vérifier l'installation Python
    python_path, is_portable = check_python_installation()
    
    if not python_path:
        print("\n❌ Impossible de trouver Python")
        print("💡 Solutions:")
        print("1. Réinstallez Python depuis python.org")
        print("2. Ajoutez Python au PATH système")
        return
    
    # Installer Flask
    if install_flask(python_path, is_portable):
        # Lancer l'application
        launch_app(python_path)
    else:
        print("\n❌ Impossible d'installer Flask")
        print("💡 Solutions alternatives:")
        print("1. Installez Flask manuellement: pip install flask")
        print("2. Utilisez un environnement virtuel")
        print("3. Vérifiez votre connexion internet")

if __name__ == "__main__":
    main()

