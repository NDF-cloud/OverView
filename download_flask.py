import urllib.request
import os
import sys
import zipfile
import shutil

def download_file(url, filename):
    print(f"📥 Téléchargement de {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"✅ {filename} téléchargé avec succès!")
        return True
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement: {e}")
        return False

def extract_zip(zip_path, extract_to):
    print(f"📦 Extraction de {zip_path}...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"✅ Extraction terminée dans {extract_to}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'extraction: {e}")
        return False

def main():
    print("🔧 Installation manuelle de Flask...")
    
    # Créer le dossier pour les packages
    packages_dir = "packages"
    if not os.path.exists(packages_dir):
        os.makedirs(packages_dir)
    
    # URLs des packages nécessaires
    packages = {
        "flask": "https://files.pythonhosted.org/packages/2e/80/6e51de196e441d4a1d1f75c5e80b7355c40cfaac2f74d4d4d8b5f8f5b5b5/Flask-3.1.1-py3-none-any.whl",
        "werkzeug": "https://files.pythonhosted.org/packages/2e/80/6e51de196e441d4a1d1f75c5e80b7355c40cfaac2f74d4d4d8b5f8f5b5b5/Werkzeug-3.1.3-py3-none-any.whl",
        "jinja2": "https://files.pythonhosted.org/packages/2e/80/6e51de196e441d4a1d1f75c5e80b7355c40cfaac2f74d4d4d8b5f8f5b5b5/Jinja2-3.1.6-py3-none-any.whl"
    }
    
    # Télécharger les packages
    for package_name, url in packages.items():
        filename = f"{packages_dir}/{package_name}.whl"
        if download_file(url, filename):
            print(f"✅ {package_name} téléchargé")
        else:
            print(f"❌ Échec du téléchargement de {package_name}")
    
    print("🎉 Téléchargement terminé!")
    print("Maintenant, vous pouvez installer les packages avec:")
    print("python -m pip install packages/*.whl")

if __name__ == "__main__":
    main()

