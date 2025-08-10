#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de débogage pour comprendre pourquoi Flask ne trouve pas les templates
"""

import os
import sys

# Changer vers le répertoire de l'application
app_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(app_dir)
print(f"📁 Répertoire de travail: {os.getcwd()}")

# Ajouter le répertoire courant au chemin Python
sys.path.insert(0, app_dir)

# Maintenant importer Flask et créer une application de test
from flask import Flask, render_template

# Créer une application Flask simple
app = Flask(__name__)

print(f"🔍 Configuration Flask:")
print(f"   - __name__: {__name__}")
print(f"   - template_folder: {app.template_folder}")
print(f"   - static_folder: {app.static_folder}")
print(f"   - instance_path: {app.instance_path}")

# Vérifier si le fichier template existe
template_path = os.path.join(app.template_folder, 'login.html')
print(f"📄 Template login.html:")
print(f"   - Chemin complet: {template_path}")
print(f"   - Existe: {os.path.exists(template_path)}")
print(f"   - Est un fichier: {os.path.isfile(template_path) if os.path.exists(template_path) else False}")

# Vérifier le répertoire templates
templates_dir = app.template_folder
print(f"📁 Répertoire templates:")
print(f"   - Chemin: {templates_dir}")
print(f"   - Existe: {os.path.exists(templates_dir)}")
print(f"   - Est un répertoire: {os.path.isdir(templates_dir) if os.path.exists(templates_dir) else False}")

if os.path.exists(templates_dir):
    print(f"   - Contenu: {os.listdir(templates_dir)}")

# Test de rendu de template
@app.route('/')
def test():
    try:
        return render_template('login.html')
    except Exception as e:
        return f"Erreur template: {str(e)}"

if __name__ == "__main__":
    print("\n🚀 Lancement de l'application de test...")
    app.run(debug=True, host='0.0.0.0', port=5001)
