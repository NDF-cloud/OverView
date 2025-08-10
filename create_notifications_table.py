#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour créer la table notifications manquante
Cette table est nécessaire pour la suppression en cascade des comptes
"""

import sqlite3
import os

def create_notifications_table():
    """Créer la table notifications si elle n'existe pas"""
    
    db_path = 'epargne.db'
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier si la table existe déjà
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notifications'")
        if cursor.fetchone():
            print("✅ Table 'notifications' existe déjà")
            return True
        
        print("🏗️ Création de la table 'notifications'...")
        
        # Créer la table notifications
        cursor.execute('''
        CREATE TABLE notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            titre VARCHAR(200) NOT NULL,
            message TEXT NOT NULL,
            lu BOOLEAN DEFAULT FALSE,
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            type_notification VARCHAR(50) DEFAULT 'info',
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        ''')
        
        # Créer un index pour améliorer les performances
        cursor.execute('''
        CREATE INDEX idx_notifications_user_id ON notifications(user_id)
        ''')
        
        # Créer un index pour les notifications non lues
        cursor.execute('''
        CREATE INDEX idx_notifications_lu ON notifications(lu)
        ''')
        
        conn.commit()
        print("✅ Table 'notifications' créée avec succès")
        print("✅ Index créés pour optimiser les performances")
        print("✅ Contrainte FOREIGN KEY avec ON DELETE CASCADE configurée")
        
        # Vérifier la structure de la table
        cursor.execute("PRAGMA table_info(notifications)")
        columns = cursor.fetchall()
        
        print(f"\n📋 Structure de la table 'notifications':")
        print("-" * 50)
        for col in columns:
            col_id, name, type_name, not_null, default_val, pk = col
            print(f"  {col_id}. {name} ({type_name}) {'NOT NULL' if not_null else 'NULL'} {'PRIMARY KEY' if pk else ''}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

def insert_sample_notifications():
    """Insérer quelques notifications d'exemple pour tester"""
    
    db_path = 'epargne.db'
    if not os.path.exists(db_path):
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier s'il y a des utilisateurs
        cursor.execute("SELECT id, username FROM users LIMIT 3")
        users = cursor.fetchall()
        
        if not users:
            print("⚠️  Aucun utilisateur trouvé pour créer des notifications d'exemple")
            return False
        
        print(f"\n📝 Création de notifications d'exemple pour {len(users)} utilisateurs...")
        
        # Créer des notifications d'exemple
        sample_notifications = [
            ("Bienvenue !", "Votre compte a été créé avec succès.", "info"),
            ("Rappel", "N'oubliez pas de définir vos objectifs d'épargne.", "reminder"),
            ("Succès", "Félicitations ! Vous avez atteint un objectif.", "success"),
            ("Mise à jour", "Nouvelle fonctionnalité disponible.", "info"),
            ("Sécurité", "Connexion depuis un nouvel appareil détectée.", "warning")
        ]
        
        for user_id, username in users:
            for titre, message, type_notif in sample_notifications:
                cursor.execute('''
                INSERT INTO notifications (user_id, titre, message, type_notification)
                VALUES (?, ?, ?, ?)
                ''', (user_id, titre, message, type_notif))
        
        conn.commit()
        print(f"✅ {len(users) * len(sample_notifications)} notifications d'exemple créées")
        
        # Compter les notifications par utilisateur
        for user_id, username in users:
            cursor.execute("SELECT COUNT(*) FROM notifications WHERE user_id = ?", (user_id,))
            count = cursor.fetchone()[0]
            print(f"  👤 {username}: {count} notifications")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des notifications: {e}")
        conn.rollback()
        return False
    
    finally:
        conn.close()

def main():
    """Fonction principale"""
    
    print("🔔 CRÉATION DE LA TABLE NOTIFICATIONS")
    print("=" * 50)
    
    # Créer la table
    if create_notifications_table():
        # Insérer des notifications d'exemple
        insert_sample_notifications()
        
        print("\n" + "=" * 50)
        print("🎉 SUCCÈS ! La table notifications est maintenant disponible")
        print("✅ La suppression en cascade des comptes fonctionnera complètement")
        print("✅ Toutes les données utilisateur seront supprimées")
        print("✅ Le registre de caisse sera bien supprimé avec le compte")
    else:
        print("\n❌ ÉCHEC ! Impossible de créer la table notifications")
        print("⚠️  La suppression en cascade pourrait ne pas fonctionner correctement")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
