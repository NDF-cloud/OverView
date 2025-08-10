#!/usr/bin/env python3
"""
Script de vérification finale pour s'assurer que la correction des graphes est complète
"""

import os
import re

def check_files():
    """Vérifier que tous les fichiers nécessaires sont présents"""

    print("🔍 Vérification des fichiers...")

    required_files = [
        'app.py',
        'static/dashboard_charts.js',
        'templates/tab_content/dashboard.html',
        'templates/base_with_tabs.html'
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")

    if missing_files:
        print(f"❌ Fichiers manquants: {missing_files}")
        return False

    print("✅ Tous les fichiers requis sont présents")
    return True

def check_app_py():
    """Vérifier que app.py contient les bonnes modifications"""

    print("\n🔍 Vérification de app.py...")

    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # Vérifier les nouvelles données
    checks = [
        ('objectifs_inactifs', 'Calcul des objectifs inactifs'),
        ('taches_en_cours', 'Calcul des tâches en cours'),
        ("'objectifs_inactifs': objectifs_inactifs", 'Passage des objectifs inactifs aux stats'),
        ("'taches_en_cours': taches_en_cours", 'Passage des tâches en cours aux stats')
    ]

    for pattern, description in checks:
        if re.search(pattern, content):
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - MANQUANT")
            return False

    return True

def check_dashboard_template():
    """Vérifier que le template dashboard contient les bonnes modifications"""

    print("\n🔍 Vérification du template dashboard...")

    with open('templates/tab_content/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Vérifier les attributs data-*
    checks = [
        ('data-objectifs-actifs', 'Attribut data-objectifs-actifs'),
        ('data-objectifs-inactifs', 'Attribut data-objectifs-inactifs'),
        ('data-taches-terminees', 'Attribut data-taches-terminees'),
        ('data-taches-en-cours', 'Attribut data-taches-en-cours'),
        ('dashboard_charts.js', 'Inclusion du fichier dashboard_charts.js')
    ]

    for pattern, description in checks:
        if re.search(pattern, content):
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - MANQUANT")
            return False

    return True

def check_base_template():
    """Vérifier que le template principal inclut le fichier JavaScript"""

    print("\n🔍 Vérification du template principal...")

    with open('templates/base_with_tabs.html', 'r', encoding='utf-8') as f:
        content = f.read()

    if 'dashboard_charts.js' in content:
        print("✅ Inclusion de dashboard_charts.js")
        return True
    else:
        print("❌ Inclusion de dashboard_charts.js - MANQUANT")
        return False

def check_js_file():
    """Vérifier que le fichier JavaScript contient les bonnes fonctions"""

    print("\n🔍 Vérification du fichier JavaScript...")

    with open('static/dashboard_charts.js', 'r', encoding='utf-8') as f:
        content = f.read()

    # Vérifier les fonctions essentielles
    checks = [
        ('waitForChartJs', 'Fonction waitForChartJs'),
        ('createObjectifsChart', 'Fonction createObjectifsChart'),
        ('createTachesChart', 'Fonction createTachesChart'),
        ('initDashboardCharts', 'Fonction initDashboardCharts'),
        ('dataset.objectifsActifs', 'Lecture des données objectifs'),
        ('dataset.tachesTerminees', 'Lecture des données tâches')
    ]

    for pattern, description in checks:
        if re.search(pattern, content):
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - MANQUANT")
            return False

    return True

def main():
    """Fonction principale de vérification"""

    print("🚀 VÉRIFICATION FINALE DE LA CORRECTION DES GRAPHES")
    print("=" * 60)

    # Vérifier les fichiers
    if not check_files():
        print("\n❌ Vérification échouée - Fichiers manquants")
        return False

    # Vérifier app.py
    if not check_app_py():
        print("\n❌ Vérification échouée - Modifications app.py manquantes")
        return False

    # Vérifier le template dashboard
    if not check_dashboard_template():
        print("\n❌ Vérification échouée - Modifications template dashboard manquantes")
        return False

    # Vérifier le template principal
    if not check_base_template():
        print("\n❌ Vérification échouée - Inclusion JavaScript manquante")
        return False

    # Vérifier le fichier JavaScript
    if not check_js_file():
        print("\n❌ Vérification échouée - Fonctions JavaScript manquantes")
        return False

    print("\n" + "=" * 60)
    print("✅ VÉRIFICATION TERMINÉE AVEC SUCCÈS!")
    print("🎉 Tous les composants de la correction sont présents")
    print("\n📋 PROCHAINES ÉTAPES:")
    print("1. Démarrer l'application: python app.py")
    print("2. Ouvrir http://localhost:5000")
    print("3. Se connecter et vérifier le dashboard")
    print("4. Vérifier que les graphes s'affichent correctement")
    print("5. Consulter la console du navigateur pour les logs")

    return True

if __name__ == "__main__":
    main()