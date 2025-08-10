#!/usr/bin/env python3
"""
Script de migration pour le nouveau système de notifications
"""

import sqlite3
import os
from datetime import datetime

def migrate_notifications():
    """Migrer vers le nouveau système de notifications"""
    
    # Chemin vers la base de données
    db_path = 'database.db'
    
    if not os.path.exists(db_path):
        print("❌ Base de données non trouvée")
        return
    
    print("🔄 Migration du système de notifications...")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        
        # Vérifier si la table notifications existe déjà
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notifications'")
        table_exists = cur.fetchone()
        
        if not table_exists:
            print("📋 Création de la table notifications...")
            
            # Créer la nouvelle table notifications
            cur.execute('''
                CREATE TABLE notifications (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    type TEXT NOT NULL,
                    titre TEXT NOT NULL,
                    message TEXT NOT NULL,
                    priorite TEXT DEFAULT 'normal',
                    lue BOOLEAN DEFAULT FALSE,
                    action_url TEXT,
                    action_text TEXT,
                    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    date_lecture TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Créer des index pour améliorer les performances
            cur.execute('CREATE INDEX idx_notifications_user_id ON notifications(user_id)')
            cur.execute('CREATE INDEX idx_notifications_lue ON notifications(lue)')
            cur.execute('CREATE INDEX idx_notifications_type ON notifications(type)')
            cur.execute('CREATE INDEX idx_notifications_date_creation ON notifications(date_creation)')
            
            print("✅ Table notifications créée avec succès")
        else:
            print("ℹ️ Table notifications existe déjà")
        
        # Vérifier si la colonne notif_count existe dans la table users
        cur.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cur.fetchall()]
        
        if 'notif_count' not in columns:
            print("📊 Ajout de la colonne notif_count...")
            cur.execute('ALTER TABLE users ADD COLUMN notif_count INTEGER DEFAULT 0')
            print("✅ Colonne notif_count ajoutée")
        
        # Générer des notifications initiales pour tous les utilisateurs
        print("🔔 Génération des notifications initiales...")
        
        # Récupérer tous les utilisateurs
        cur.execute('SELECT id FROM users')
        users = cur.fetchall()
        
        notification_count = 0
        
        for (user_id,) in users:
            # Générer des notifications pour les objectifs proches de la fin
            cur.execute('''
                SELECT id, nom, montant_cible, montant_actuel 
                FROM objectifs 
                WHERE user_id = ? AND status = 'actif' AND (montant_actuel / montant_cible) >= 0.9
            ''', (user_id,))
            
            objectifs_proches = cur.fetchall()
            for obj in objectifs_proches:
                obj_id, nom, montant_cible, montant_actuel = obj
                progression = (montant_actuel / montant_cible) * 100
                
                # Vérifier si la notification existe déjà
                cur.execute('''
                    SELECT id FROM notifications 
                    WHERE user_id = ? AND type = 'objectif' AND action_url = ?
                ''', (user_id, f'/objectif/{obj_id}'))
                
                if not cur.fetchone():
                    cur.execute('''
                        INSERT INTO notifications (user_id, type, titre, message, priorite, action_url, action_text)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        user_id, 'objectif', 
                        f'🎯 Objectif presque atteint !', 
                        f'Votre objectif "{nom}" est à {progression:.1f}% de sa cible !',
                        'important', f'/objectif/{obj_id}', 'Voir l\'objectif'
                    ))
                    notification_count += 1
            
            # Générer des notifications pour les tâches en retard
            cur.execute('''
                SELECT id, titre 
                FROM taches 
                WHERE user_id = ? AND termine = FALSE AND date_creation < date("now", "-7 days")
            ''', (user_id,))
            
            taches_retard = cur.fetchall()
            for tache in taches_retard:
                tache_id, titre = tache
                
                # Vérifier si la notification existe déjà
                cur.execute('''
                    SELECT id FROM notifications 
                    WHERE user_id = ? AND type = 'tache' AND action_url = ?
                ''', (user_id, f'/tache/{tache_id}/detail'))
                
                if not cur.fetchone():
                    cur.execute('''
                        INSERT INTO notifications (user_id, type, titre, message, priorite, action_url, action_text)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        user_id, 'tache', 
                        f'⚠️ Tâche en retard', 
                        f'La tâche "{titre}" est en retard depuis plus d\'une semaine.',
                        'urgent', f'/tache/{tache_id}/detail', 'Voir la tâche'
                    ))
                    notification_count += 1
            
            # Générer des notifications pour les événements à venir
            cur.execute('''
                SELECT id, titre, date_debut 
                FROM evenements 
                WHERE user_id = ? AND termine = FALSE 
                AND date_debut BETWEEN date("now") AND date("now", "+3 days")
            ''', (user_id,))
            
            evenements_proches = cur.fetchall()
            for event in evenements_proches:
                event_id, titre, date_debut = event
                
                # Vérifier si la notification existe déjà
                cur.execute('''
                    SELECT id FROM notifications 
                    WHERE user_id = ? AND type = 'evenement' AND action_url = ?
                ''', (user_id, f'/evenement/{event_id}'))
                
                if not cur.fetchone():
                    cur.execute('''
                        INSERT INTO notifications (user_id, type, titre, message, priorite, action_url, action_text)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        user_id, 'evenement', 
                        f'📅 Événement à venir', 
                        f'L\'événement "{titre}" a lieu le {date_debut}.',
                        'normal', f'/evenement/{event_id}', 'Voir l\'événement'
                    ))
                    notification_count += 1
        
        # Mettre à jour le compteur de notifications pour chaque utilisateur
        print("📊 Mise à jour des compteurs de notifications...")
        
        for (user_id,) in users:
            cur.execute('''
                SELECT COUNT(*) FROM notifications 
                WHERE user_id = ? AND lue = FALSE
            ''', (user_id,))
            
            unread_count = cur.fetchone()[0]
            cur.execute('UPDATE users SET notif_count = ? WHERE id = ?', (unread_count, user_id))
        
        # Valider les changements
        conn.commit()
        
        print(f"✅ Migration terminée avec succès !")
        print(f"📋 {notification_count} notifications générées")
        print(f"👥 {len(users)} utilisateurs traités")
        
        # Afficher quelques statistiques
        cur.execute('SELECT COUNT(*) FROM notifications')
        total_notifications = cur.fetchone()[0]
        
        cur.execute('SELECT COUNT(*) FROM notifications WHERE lue = FALSE')
        unread_notifications = cur.fetchone()[0]
        
        print(f"📊 Statistiques finales:")
        print(f"   - Total notifications: {total_notifications}")
        print(f"   - Notifications non lues: {unread_notifications}")
        
    except Exception as e:
        print(f"❌ Erreur lors de la migration: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_notifications()
