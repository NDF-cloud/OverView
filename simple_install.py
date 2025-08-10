import subprocess
import sys
import os

def run_command(command):
    """Exécute une commande et retourne le résultat"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print("🔧 Installation de Flask...")
    
    # Essayer différentes méthodes d'installation
    methods = [
        "python -m pip install flask",
        "py -m pip install flask",
        "pip install flask",
        "pip3 install flask"
    ]
    
    for method in methods:
        print(f"\n🔄 Tentative avec: {method}")
        success, stdout, stderr = run_command(method)
        
        if success:
            print(f"✅ Succès avec: {method}")
            print("🎉 Flask est maintenant installé!")
            
            # Essayer de lancer l'application
            print("\n🚀 Lancement de l'application...")
            launch_success, launch_stdout, launch_stderr = run_command("python app.py")
            
            if launch_success:
                print("✅ Application lancée avec succès!")
            else:
                print("❌ Erreur lors du lancement de l'application")
                print(f"Erreur: {launch_stderr}")
            return
        else:
            print(f"❌ Échec avec: {method}")
            if stderr:
                print(f"Erreur: {stderr}")
    
    print("\n❌ Aucune méthode d'installation n'a fonctionné")
    print("💡 Suggestions:")
    print("1. Vérifiez que Python est installé et dans le PATH")
    print("2. Installez pip: python -m ensurepip --upgrade")
    print("3. Installez Flask manuellement: pip install flask")

if __name__ == "__main__":
    main()

