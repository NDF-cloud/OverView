#!/usr/bin/env python3
"""
Fonctions de gestion des notifications pour l'application Flask
"""

import sqlite3
import psycopg2
import psycopg2.extras
import os
from datetime import datetime

def get_db_connection():
    """Obtenir une connexion à la base de données"""
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    if DATABASE_URL:
        return psycopg2.connect(DATABASE_URL)
    else:
        return sqlite3.connect('database.db')

def get_cursor(conn):
    """Obtenir un curseur approprié pour la base de données"""
    if isinstance(conn, psycopg2.extensions.connection):
        return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    else:
        return conn.cursor()

def sql_placeholder(query):
    """Convertir les placeholders SQL selon le type de base de données"""
    if os.getenv('DATABASE_URL'):
        return query.replace('?', '%s')
    else:
        return query

def create_notification(user_id, type_notif, titre, message, priorite='normal', action_url=None, action_text=None):
    """Créer une nouvelle notification pour un utilisateur"""
    conn = get_db_connection()
    cur = get_cursor(conn)
    
    try:
        # Vérifier si la table notifications existe
        if isinstance(conn, psycopg2.extensions.connection):
            # PostgreSQL
            sql = '''
                INSERT INTO notifications (user_id, type_notification, titre, message, priorite, action_url, action_text, lue, date_creation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, FALSE, CURRENT_TIMESTAMP)
            '''
        else:
            # SQLite
            sql = '''
                INSERT INTO notifications (user_id, type_notification, titre, message, priorite, action_url, action_text, lue, date_creation)
                VALUES (?, ?, ?, ?, ?, ?, ?, 0, datetime('now'))
            '''
        
        cur.execute(sql, (user_id, type_notif, titre, message, priorite, action_url, action_text))
        conn.commit()
        
        if isinstance(conn, psycopg2.extensions.connection):
            return cur.fetchone()['id'] if cur.fetchone() else None
        else:
            return cur.lastrowid
    finally:
        cur.close()
        conn.close()

def get_user_notifications(user_id, limit=50, unread_only=False):
    """Récupérer les notifications d'un utilisateur"""
    conn = get_db_connection()
    cur = get_cursor(conn)
    
    try:
        if unread_only:
            sql = sql_placeholder('''
                SELECT * FROM notifications 
                WHERE user_id = ? AND lue = FALSE 
                ORDER BY date_creation DESC 
                LIMIT ?
            ''')
        else:
            sql = sql_placeholder('''
                SELECT * FROM notifications 
                WHERE user_id = ? 
                ORDER BY date_creation DESC 
                LIMIT ?
            ''')
        
        cur.execute(sql, (user_id, limit))
        notifications_raw = cur.fetchall()
        
        notifications = []
        for row in notifications_raw:
            if isinstance(conn, psycopg2.extensions.connection):
                notif_dict = dict(row)
            else:
                notif_dict = {
                    'id': row[0],
                    'user_id': row[1],
                    'type_notification': row[2],
                    'titre': row[3],
                    'message': row[4],
                    'priorite': row[5],
                    'action_url': row[6],
                    'action_text': row[7],
                    'lue': bool(row[8]),
                    'date_creation': row[9],
                    'date_lecture': row[10] if len(row) > 10 else None
                }
            notifications.append(notif_dict)
        
        return notifications
    finally:
        cur.close()
        conn.close()

def mark_notification_read(notification_id, user_id):
    """Marquer une notification comme lue"""
    conn = get_db_connection()
    cur = get_cursor(conn)
    
    try:
        if isinstance(conn, psycopg2.extensions.connection):
            sql = '''
                UPDATE notifications 
                SET lue = TRUE, date_lecture = CURRENT_TIMESTAMP 
                WHERE id = %s AND user_id = %s
            '''
        else:
            sql = '''
                UPDATE notifications 
                SET lue = 1, date_lecture = datetime('now') 
                WHERE id = ? AND user_id = ?
            '''
        
        cur.execute(sql, (notification_id, user_id))
        conn.commit()
        return cur.rowcount > 0
    finally:
        cur.close()
        conn.close()

def mark_all_notifications_read_for_user(user_id):
    """Marquer toutes les notifications d'un utilisateur comme lues"""
    conn = get_db_connection()
    cur = get_cursor(conn)
    
    try:
        if isinstance(conn, psycopg2.extensions.connection):
            sql = '''
                UPDATE notifications 
                SET lue = TRUE, date_lecture = CURRENT_TIMESTAMP 
                WHERE user_id = %s AND lue = FALSE
            '''
        else:
            sql = '''
                UPDATE notifications 
                SET lue = 1, date_lecture = datetime('now') 
                WHERE user_id = ? AND lue = 0
            '''
        
        cur.execute(sql, (user_id,))
        conn.commit()
        return cur.rowcount
    finally:
        cur.close()
        conn.close()

def delete_old_notifications(user_id, days_old=30):
    """Supprimer les anciennes notifications d'un utilisateur"""
    conn = get_db_connection()
    cur = get_cursor(conn)
    
    try:
        if isinstance(conn, psycopg2.extensions.connection):
            sql = '''
                DELETE FROM notifications 
                WHERE user_id = %s AND date_creation < CURRENT_TIMESTAMP - INTERVAL '%s days'
            '''
        else:
            sql = '''
                DELETE FROM notifications 
                WHERE user_id = ? AND date_creation < datetime('now', '-{} days')
            '''.format(days_old)
        
        cur.execute(sql, (user_id,))
        deleted_count = cur.rowcount
        conn.commit()
        return deleted_count
    finally:
        cur.close()
        conn.close()

def generate_system_notifications(user_id):
    """Générer des notifications système automatiques"""
    conn = get_db_connection()
    cur = get_cursor(conn)
    
    try:
        # Vérifier les objectifs proches de la fin
        sql_objectifs = sql_placeholder('''
            SELECT id, nom, montant_cible, montant_actuel, date_limite
            FROM objectifs
            WHERE user_id = ? AND status = 'actif' AND (montant_actuel / montant_cible) >= 0.9
        ''')
        cur.execute(sql_objectifs, (user_id,))
        objectifs_proches = cur.fetchall()
        
        for obj in objectifs_proches:
            # Vérifier si la notification existe déjà
            sql_check = sql_placeholder('''
                SELECT id FROM notifications 
                WHERE user_id = ? AND type_notification = 'objectif' AND action_url = ? AND lue = FALSE
            ''')
            cur.execute(sql_check, (user_id, f'/objectif/{obj[0]}'))
            
            if not cur.fetchone():
                progression = (obj[3] / obj[2]) * 100
                create_notification(
                    user_id=user_id,
                    type_notif='objectif',
                    titre='🎯 Objectif presque atteint !',
                    message=f'Votre objectif "{obj[1]}" est à {progression:.1f}% de sa cible !',
                    priorite='important',
                    action_url=f'/objectif/{obj[0]}',
                    action_text='Voir l\'objectif'
                )
        
        # Vérifier les tâches en retard
        sql_taches = sql_placeholder('''
            SELECT id, titre 
            FROM taches 
            WHERE user_id = ? AND termine = FALSE AND date_creation < date("now", "-7 days")
        ''')
        cur.execute(sql_taches, (user_id,))
        taches_retard = cur.fetchall()
        
        for tache in taches_retard:
            # Vérifier si la notification existe déjà
            sql_check = sql_placeholder('''
                SELECT id FROM notifications 
                WHERE user_id = ? AND type_notification = 'tache' AND action_url = ? AND lue = FALSE
            ''')
            cur.execute(sql_check, (user_id, f'/tache/{tache[0]}/detail'))
            
            if not cur.fetchone():
                create_notification(
                    user_id=user_id,
                    type_notif='tache',
                    titre='⚠️ Tâche en retard',
                    message=f'La tâche "{tache[1]}" est en retard depuis plus d\'une semaine.',
                    priorite='urgent',
                    action_url=f'/tache/{tache[0]}/detail',
                    action_text='Voir la tâche'
                )
        
        # Vérifier les événements à venir
        sql_evenements = sql_placeholder('''
            SELECT id, titre, date_debut 
            FROM evenements 
            WHERE user_id = ? AND termine = FALSE 
            AND date_debut BETWEEN date("now") AND date("now", "+3 days")
        ''')
        cur.execute(sql_evenements, (user_id,))
        evenements_proches = cur.fetchall()
        
        for event in evenements_proches:
            # Vérifier si la notification existe déjà
            sql_check = sql_placeholder('''
                SELECT id FROM notifications 
                WHERE user_id = ? AND type_notification = 'evenement' AND action_url = ? AND lue = FALSE
            ''')
            cur.execute(sql_check, (user_id, f'/evenement/{event[0]}'))
            
            if not cur.fetchone():
                create_notification(
                    user_id=user_id,
                    type_notif='evenement',
                    titre='📅 Événement à venir',
                    message=f'L\'événement "{event[1]}" a lieu le {event[2]}.',
                    priorite='normal',
                    action_url=f'/evenement/{event[0]}',
                    action_text='Voir l\'événement'
                )
    
    finally:
        cur.close()
        conn.close()

def get_notification_count_new(user_id):
    """Nouveau système de comptage des notifications non lues"""
    conn = get_db_connection()
    cur = get_cursor(conn)
    
    try:
        sql = sql_placeholder('''
            SELECT COUNT(*) FROM notifications 
            WHERE user_id = ? AND lue = FALSE
        ''')
        cur.execute(sql, (user_id,))
        result = cur.fetchone()
        if isinstance(conn, psycopg2.extensions.connection):
            return result['count'] if result else 0
        else:
            return result[0] if result else 0
    finally:
        cur.close()
        conn.close()
