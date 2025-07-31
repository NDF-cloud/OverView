# ==============================================================================
# FICHIER FINAL, ULTIME ET 100% COMPLET : app.py
# (Multi-Utilisateurs + PostgreSQL + Toutes les fonctionnalités)
# ==============================================================================
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session, send_file
import sqlite3
from datetime import datetime
import os
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import psycopg
import psycopg.errors
import csv
import io
REPORTLAB_AVAILABLE = False
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = 'une-cle-vraiment-secrete-pour-les-sessions-utilisateurs'

# ==============================================================================
# FONCTIONS DE TRADUCTION
# ==============================================================================

def get_translations():
    """Retourne les traductions disponibles"""
    return {
        'fr': {
            # Navigation
            'dashboard': 'Tableau de Bord',
            'notifications': 'Notifications',
            'agenda': 'Agenda',
            'reports': 'Rapports',
            'settings': 'Paramètres',
            'savings': 'Épargne',
            'tasks': 'Tâches',
            'back': 'Retour',

            # Actions
            'create': 'Créer',
            'edit': 'Modifier',
            'delete': 'Supprimer',
            'save': 'Sauvegarder',
            'cancel': 'Annuler',
            'confirm': 'Confirmer',
            'update': 'Mettre à jour',
            'archive': 'Archiver',
            'complete': 'Terminer',

            # Messages
            'success': 'Succès',
            'error': 'Erreur',
            'warning': 'Avertissement',
            'info': 'Information',
            'loading': 'Chargement...',
            'no_data': 'Aucune donnée',

            # Formulaires
            'name': 'Nom',
            'description': 'Description',
            'amount': 'Montant',
            'target_amount': 'Montant cible',
            'current_amount': 'Montant actuel',
            'currency': 'Devise',
            'deadline': 'Date limite',
            'start_date': 'Date de début',
            'end_date': 'Date de fin',
            'location': 'Lieu',
            'color': 'Couleur',
            'reminder': 'Rappel',
            'type': 'Type',
            'status': 'Statut',
            'progress': 'Progression',
            'remaining': 'Restant',
            'completed': 'Terminé',
            'active': 'Actif',
            'archived': 'Archivé',

            # Pages principales
            'total_savings': 'Total Épargne',
            'new_objective': 'Nouvel Objectif',
            'new_task': 'Nouvelle Tâche',
            'new_event': 'Nouvel Événement',
            'objectives': 'Objectifs',
            'tasks': 'Tâches',
            'events': 'Événements',
            'transactions': 'Transactions',
            'archives': 'Archives',

            # Paramètres
            'settings': 'Paramètres',
            'manage_preferences': 'Gérez vos préférences OverView',
            'account_deletion': 'Suppression de Compte',
            'danger_zone': 'Zone Dangereuse',
            'account_deletion_warning': '⚠️ ATTENTION : Cette action est irréversible !',
            'account_deletion_description': 'Toutes vos données (objectifs, tâches, événements, épargne) seront définitivement supprimées.',
            'delete_my_account': 'Supprimer Mon Compte',
            'confirm_account_deletion': 'Confirmer la Suppression',
            'account_deletion_modal_warning': 'Êtes-vous sûr de vouloir supprimer définitivement votre compte ?',
            'this_action_cannot_be_undone': 'Cette action ne peut pas être annulée.',
            'delete_account_confirm': 'Oui, Supprimer Mon Compte',
            'account_deleted_successfully': 'Votre compte a été supprimé avec succès.',
            'error_deleting_account': 'Erreur lors de la suppression du compte.',
            'user_not_found': 'Utilisateur non trouvé.',
            'enter_password_to_confirm': 'Entrez votre mot de passe pour confirmer',
            'enter_your_password': 'Entrez votre mot de passe',
            'password_required_for_deletion': 'Votre mot de passe est requis pour supprimer le compte',
            'password_required': 'Le mot de passe est requis',
            'incorrect_password': 'Mot de passe incorrect',
            'error_verifying_password': 'Erreur lors de la vérification du mot de passe',
            'language': 'Langue',
            'application_language': 'Langue de l\'application',
            'language_used_throughout_app': 'Langue utilisée dans toute l\'application',
            'theme': 'Thème',
            'display_mode': 'Mode d\'affichage',
            'enable_dark_mode': 'Activer le Mode Nuit',
            'disable_dark_mode': 'Désactiver le Mode Nuit',
            'change_interface_theme': 'Changer le thème de l\'interface',
            'dark_mode': 'Mode Nuit',
            'light_mode': 'Mode Jour',
            'default_currency': 'Devise par défaut',
            'currency_used_for_amounts': 'Devise utilisée pour l\'affichage des montants dans toute l\'application',
            'countdown_settings': 'Paramètres de compte à rebours',
            'notification_settings': 'Paramètres de notifications',
            'data_management': 'Gestion des données',
            'account_settings': 'Paramètres du compte',
            'security': 'Sécurité',
            'personalization': 'Personnalisation',

            # Messages de confirmation
            'objective_created': 'Objectif créé avec succès',
            'objective_updated': 'Objectif mis à jour avec succès',
            'objective_deleted': 'Objectif supprimé avec succès',
            'task_created': 'Tâche créée avec succès',
            'task_updated': 'Tâche mise à jour avec succès',
            'task_deleted': 'Tâche supprimée avec succès',
            'event_created': 'Événement créé avec succès',
            'event_updated': 'Événement mis à jour avec succès',
            'event_deleted': 'Événement supprimé avec succès',
            'transaction_added': 'Transaction ajoutée avec succès',
            'settings_saved': 'Paramètres sauvegardés avec succès',

            # Authentification
            'create_account': 'Créer un Compte',
            'username': 'Nom d\'utilisateur',
            'password': 'Mot de passe',
            'register': 'S\'inscrire',
            'login': 'Se connecter',
            'logout': 'Se déconnecter',
            'already_have_account': 'Déjà un compte ?',
            'login_here': 'Connectez-vous ici',
            'choose_security_question': 'Choisissez votre question de sécurité',
            'security_answer': 'Votre réponse secrète',
            'please_choose_question': 'Veuillez choisir une question',
            'access_your_overview_space': 'Accédez à votre espace OverView',
            'no_account_yet': 'Pas encore de compte ?',
            'register_here': 'Inscrivez-vous ici',
            'join_overview_community': 'Rejoignez la communauté OverView',
            'continue': 'Continuer',
            'back_to_login': 'Retour à la connexion',
            'forgot_password_step2': 'Question de Sécurité',
            'answer_security_question': 'Répondez à votre question de sécurité',
            'security_question': 'Question de sécurité',
            'verify_answer': 'Vérifier la réponse',
            'forgot_password_step3': 'Nouveau Mot de Passe',
            'enter_new_password': 'Entrez votre nouveau mot de passe',
            'new_password': 'Nouveau mot de passe',
            'confirm_password': 'Confirmer le mot de passe',
            'reset_password': 'Réinitialiser le mot de passe',
            'settings': 'Paramètres',
            'dark_mode': 'Mode sombre',
            'language': 'Langue',
            'on': 'Activé',
            'off': 'Désactivé',
            'language_changed_to': 'Langue changée vers',

            # Erreurs
            'access_denied': 'Accès refusé',
            'invalid_password': 'Mot de passe incorrect',
            'required_field': 'Ce champ est requis',
            'invalid_amount': 'Montant invalide',
            'invalid_date': 'Date invalide',
            'invalid_language': 'Langue non valide',
            'connection_error': 'Erreur de connexion',

            # Compteurs à rebours
            'days_remaining': 'jours restants',
            'hours_remaining': 'heures restantes',
            'minutes_remaining': 'minutes restantes',
            'overdue': 'En retard',
            'due_today': 'Échéance aujourd\'hui',
            'due_tomorrow': 'Échéance demain',

            # Graphiques et statistiques
            'progress_chart': 'Graphique de progression',
            'savings_evolution': 'Évolution de l\'épargne',
            'task_completion': 'Taux de completion des tâches',
            'monthly_summary': 'Résumé mensuel',
            'total_objectives': 'Total objectifs',
            'total_tasks': 'Total tâches',
            'total_events': 'Total événements',
            'completion_rate': 'Taux de completion',

            # Authentification
            'login': 'Connexion',
            'register': 'Inscription',
            'logout': 'Déconnexion',
            'username': 'Nom d\'utilisateur',
            'password': 'Mot de passe',
            'old_password': 'Ancien Mot de Passe',
            'new_password': 'Nouveau Mot de Passe',
            'confirm_password': 'Confirmer le mot de passe',
            'email': 'Email',
            'forgot_password': 'Mot de passe oublié',
            'reset_password': 'Réinitialiser le mot de passe',
            'security_question': 'Question de sécurité',
            'security_answer': 'Réponse de sécurité',

            # Devises
            'xaf': 'Franc CFA (FCFA)',
            'eur': 'Euro (€)',
            'usd': 'Dollar US ($)',

            # Types de transactions
            'income': 'Entrée',
            'expense': 'Sortie',

            # Pages principales
            'my_savings_goals': 'Mes Objectifs d\'Épargne',
            'my_tasks': 'Mes Tâches',
            'tasks_overview': 'Tâches OverView',
            'manage_your_tasks_and_projects': 'Gérez vos tâches et projets',
            'my_active_tasks': 'Mes Tâches Actives',
            'completed_tasks': 'Tâches Terminées',
            'dashboard_overview': 'Dashboard OverView',
            'overview_of_your_activities': 'Vue d\'ensemble de vos activités',
            'savings_objectives': 'Objectifs d\'Épargne',
            'active_objectives': 'Objectifs actifs',
            'notifications_overview': 'Notifications OverView',
            'stay_informed_about_important_activities': 'Restez informé de vos activités importantes',
            'all_your_savings_objectives_are_on_track': 'Tous vos objectifs d\'épargne sont en bonne voie !',
            'agenda_overview': 'Agenda OverView',
            'view_and_manage_your_events': 'Visualisez et gérez vos événements',
            'reports_overview': 'Rapports OverView',
            'detailed_analysis_of_your_performance': 'Analyses détaillées de vos performances',
            'savings_overview': 'Épargne OverView',
            'manage_your_savings_goals': 'Gérez vos objectifs d\'épargne',
            'new_objective': '+ Nouvel Objectif',
            'savings': 'Épargne',
            'agenda': 'Agenda',
            'total_active_savings': 'Épargne Totale Active',
            'show_hide_balance': 'Afficher/Cacher le solde',
            'view_completed_objectives_archives': 'Voir mes objectifs terminés (Archives)',
            'no_active_objectives_click_plus_to_start': 'Aucun objectif actif. Cliquez sur le \'+\' pour commencer !',

            # Types d'événements
            'meeting': 'Réunion',
            'appointment': 'Rendez-vous',
            'reminder': 'Rappel',
            'deadline': 'Échéance',
            'other': 'Autre',

            # Messages JavaScript et confirmations
            'calculating': 'Calcul en cours...',
            'overdue': 'En retard !',
            'enter_password_to_show_balance': 'Veuillez entrer votre mot de passe pour afficher le solde :',
            'incorrect_password': 'Mot de passe incorrect !',
            'confirm_delete_objective': 'Êtes-vous sûr de vouloir supprimer DÉFINITIVEMENT cet objectif ?',
            'enter_password_to_confirm_deletion': 'Pour confirmer la suppression, veuillez entrer votre mot de passe :',
            'confirm_delete_task': 'Êtes-vous sûr de vouloir supprimer cette tâche ?',
            'confirm_delete_event': 'Êtes-vous sûr de vouloir supprimer cet événement ?',
            'enter_current_password': 'Entrez votre mot de passe actuel',
            'enter_new_password': 'Entrez votre nouveau mot de passe',
            'confirm_new_password': 'Confirmez votre nouveau mot de passe',
            'password_changed_successfully': 'Mot de passe modifié avec succès',
            'old_password_incorrect': 'L\'ancien mot de passe est incorrect',
            'both_fields_required': 'Les deux champs sont requis',
            'please_fill_all_fields': 'Veuillez remplir tous les champs',
            'user_already_exists': 'L\'utilisateur existe déjà',
            'invalid_credentials': 'Identifiants incorrects. Veuillez réessayer.',
            'successfully_logged_out': 'Vous avez été déconnecté avec succès.',
            'user_not_found': 'Utilisateur non trouvé',
            'no_security_question': 'Aucune question de sécurité définie',
            'session_error': 'Erreur de session. Veuillez recommencer.',
            'incorrect_secret_answer': 'La réponse secrète est incorrecte',
            'password_reset_success': 'Mot de passe réinitialisé ! Vous pouvez vous connecter.',
            'please_choose_question': '-- Veuillez choisir une question --',
            'forgot_password_step1': 'Mot de Passe Oublié (Étape 1/3)',
            'enter_username_to_start_recovery': 'Veuillez entrer votre nom d\'utilisateur pour commencer le processus de récupération.',
            'forgot_password_step2': 'Mot de Passe Oublié (Étape 2/3)',
            'enter_secret_answer': 'Veuillez entrer votre réponse secrète.',
            'forgot_password_step3': 'Mot de Passe Oublié (Étape 3/3)',
            'verification_successful': 'Vérification réussie ! Veuillez entrer votre nouveau mot de passe.',
            'new_password_label': 'Nouveau mot de passe',
            'reset_password_button': 'Réinitialiser le mot de passe',
            'tasks_overdue': 'Tâches en Retard',
            'no_overdue_tasks': 'Aucune tâche en retard',
            'overdue_warning': '⚠️ En retard',
            'please_confirm_with_password': 'Confirmez avec votre mot de passe',
            'overdue_tasks_notifications': 'Notifications pour les tâches en retard',
            'change_password_button': '🔐 Changer le mot de passe',
            'current_password_label': 'Mot de passe actuel',
            'new_password_label': 'Nouveau mot de passe',
            'confirm_new_password_label': 'Confirmer le nouveau mot de passe',

            # Mois de l'année
            'january': 'Janvier',
            'february': 'Février',
            'march': 'Mars',
            'april': 'Avril',
            'may': 'Mai',
            'june': 'Juin',
            'july': 'Juillet',
            'august': 'Août',
            'september': 'Septembre',
            'october': 'Octobre',
            'november': 'Novembre',
            'december': 'Décembre',

            # Abréviations des mois
            'jan': 'Jan',
            'feb': 'Fév',
            'mar': 'Mar',
            'apr': 'Avr',
            'may_short': 'Mai',
            'jun': 'Juin',

            # Messages du calendrier
            'calendar_tip': 'Astuce : Maintenez le clic 1.8 secondes sur une date pour créer un événement',
            'december_2024': 'Décembre 2024',

            # Messages des paramètres avancés
            'next_auto_backup': 'Prochaine sauvegarde automatique : Demain à 02:00',
            'backup_now': 'Sauvegarder maintenant',
            'email_notifications': 'Notifications par email',
            'email_notifications_desc': 'Recevoir des notifications par email',
            'email_address': 'Adresse email',
            'email_placeholder': 'votre@email.com',
            'enabled': 'Activées',
            'disabled': 'Désactivées',
            'email_notifications_desc_small': 'Recevoir des notifications par email pour les échéances',

            # Archives
            'my_successes': 'Mes Succès',
            'your_completed_savings_goals': 'Vos objectifs d\'épargne accomplis',
            'completed_objectives': 'Objectifs accomplis',
            'final_amount': 'Montant final',
            'no_archived_objectives': 'Aucun objectif archivé',
            'no_completed_objectives_yet': 'Vous n\'avez pas encore d\'objectifs accomplis. Continuez à épargner pour voir vos succès ici !',

            # Détails d'objectif
            'objective_detail': 'Détail de l\'Objectif',

            # Détails de tâche
            'task_detail': 'Détail de la Tâche',

            # Paramètres avancés
            'advanced_settings': 'Paramètres Avancés'
        },
        'en': {
            # Navigation
            'dashboard': 'Dashboard',
            'notifications': 'Notifications',
            'agenda': 'Agenda',
            'reports': 'Reports',
            'settings': 'Settings',
            'savings': 'Savings',
            'tasks': 'Tasks',
            'back': 'Back',

            # Actions
            'create': 'Create',
            'edit': 'Edit',
            'delete': 'Delete',
            'save': 'Save',
            'cancel': 'Cancel',
            'confirm': 'Confirm',
            'update': 'Update',
            'archive': 'Archive',
            'complete': 'Complete',

            # Messages
            'success': 'Success',
            'error': 'Error',
            'warning': 'Warning',
            'info': 'Information',
            'loading': 'Loading...',
            'no_data': 'No data',

            # Formulaires
            'name': 'Name',
            'description': 'Description',
            'amount': 'Amount',
            'target_amount': 'Target amount',
            'current_amount': 'Current amount',
            'currency': 'Currency',
            'deadline': 'Deadline',
            'start_date': 'Start date',
            'end_date': 'End date',
            'location': 'Location',
            'color': 'Color',
            'reminder': 'Reminder',
            'type': 'Type',
            'status': 'Status',
            'progress': 'Progress',
            'remaining': 'Remaining',
            'completed': 'Completed',
            'active': 'Active',
            'archived': 'Archived',

            # Pages principales
            'my_savings_goals': 'My Savings Goals',
            'my_tasks': 'My Tasks',
            'tasks_overview': 'Tasks OverView',
            'manage_your_tasks_and_projects': 'Manage your tasks and projects',
            'my_active_tasks': 'My Active Tasks',
            'completed_tasks': 'Completed Tasks',
            'dashboard_overview': 'Dashboard OverView',
            'overview_of_your_activities': 'Overview of your activities',
            'savings_objectives': 'Savings Objectives',
            'active_objectives': 'Active objectives',
            'notifications_overview': 'Notifications OverView',
            'stay_informed_about_important_activities': 'Stay informed about important activities',
            'all_your_savings_objectives_are_on_track': 'All your savings objectives are on track!',
            'agenda_overview': 'Agenda OverView',
            'view_and_manage_your_events': 'View and manage your events',
            'reports_overview': 'Reports OverView',
            'detailed_analysis_of_your_performance': 'Detailed analysis of your performance',
            'savings_overview': 'Savings OverView',
            'manage_your_savings_goals': 'Manage your savings goals',
            'new_objective': '+ New Objective',
            'savings': 'Savings',
            'agenda': 'Agenda',
            'total_active_savings': 'Total Active Savings',
            'show_hide_balance': 'Show/Hide balance',
            'view_completed_objectives_archives': 'View my completed objectives (Archives)',
            'no_active_objectives_click_plus_to_start': 'No active objectives. Click the \'+\' to start!',
            'total_savings': 'Total Savings',
            'new_task': 'New Task',
            'new_event': 'New Event',
            'objectives': 'Objectives',
            'tasks': 'Tasks',
            'events': 'Events',
            'transactions': 'Transactions',
            'archives': 'Archives',

            # Paramètres
            'settings': 'Settings',
            'manage_preferences': 'Manage your OverView preferences',
            'account_deletion': 'Account Deletion',
            'danger_zone': 'Danger Zone',
            'account_deletion_warning': '⚠️ WARNING: This action is irreversible!',
            'account_deletion_description': 'All your data (objectives, tasks, events, savings) will be permanently deleted.',
            'delete_my_account': 'Delete My Account',
            'confirm_account_deletion': 'Confirm Deletion',
            'account_deletion_modal_warning': 'Are you sure you want to permanently delete your account?',
            'this_action_cannot_be_undone': 'This action cannot be undone.',
            'delete_account_confirm': 'Yes, Delete My Account',
            'account_deleted_successfully': 'Your account has been successfully deleted.',
            'error_deleting_account': 'Error deleting account.',
            'user_not_found': 'User not found.',
            'enter_password_to_confirm': 'Enter your password to confirm',
            'enter_your_password': 'Enter your password',
            'password_required_for_deletion': 'Your password is required to delete the account',
            'password_required': 'Password is required',
            'incorrect_password': 'Incorrect password',
            'error_verifying_password': 'Error verifying password',
            'language': 'Language',
            'application_language': 'Application Language',
            'language_used_throughout_app': 'Language used throughout the application',
            'theme': 'Theme',
            'display_mode': 'Display Mode',
            'enable_dark_mode': 'Enable Dark Mode',
            'disable_dark_mode': 'Disable Dark Mode',
            'change_interface_theme': 'Change the interface theme',
            'dark_mode': 'Dark Mode',
            'light_mode': 'Light Mode',
            'default_currency': 'Default currency',
            'currency_used_for_amounts': 'Currency used for displaying amounts throughout the application',
            'countdown_settings': 'Countdown settings',
            'notification_settings': 'Notification settings',
            'data_management': 'Data management',
            'account_settings': 'Account settings',
            'security': 'Security',
            'personalization': 'Personalization',

            # Messages de confirmation
            'objective_created': 'Objective created successfully',
            'objective_updated': 'Objective updated successfully',
            'objective_deleted': 'Objective deleted successfully',
            'task_created': 'Task created successfully',
            'task_updated': 'Task updated successfully',
            'task_deleted': 'Task deleted successfully',
            'event_created': 'Event created successfully',
            'event_updated': 'Event updated successfully',
            'event_deleted': 'Event deleted successfully',
            'transaction_added': 'Transaction added successfully',
            'settings_saved': 'Settings saved successfully',
            'language_changed_to': 'Language changed to',

            # Erreurs
            'access_denied': 'Access denied',
            'invalid_password': 'Invalid password',
            'required_field': 'This field is required',
            'invalid_amount': 'Invalid amount',
            'invalid_date': 'Invalid date',
            'invalid_language': 'Invalid language',
            'connection_error': 'Connection error',

            # Compteurs à rebours
            'days_remaining': 'days remaining',
            'hours_remaining': 'hours remaining',
            'minutes_remaining': 'minutes remaining',
            'overdue': 'Overdue',
            'due_today': 'Due today',
            'due_tomorrow': 'Due tomorrow',

            # Graphiques et statistiques
            'progress_chart': 'Progress chart',
            'savings_evolution': 'Savings evolution',
            'task_completion': 'Task completion rate',
            'monthly_summary': 'Monthly summary',
            'total_objectives': 'Total objectives',
            'total_tasks': 'Total tasks',
            'total_events': 'Total events',
            'completion_rate': 'Completion rate',

            # Authentification
            'login': 'Login',
            'register': 'Register',
            'logout': 'Logout',
            'username': 'Username',
            'password': 'Password',
            'old_password': 'Old Password',
            'new_password': 'New Password',
            'confirm_password': 'Confirm password',
            'email': 'Email',
            'forgot_password': 'Forgot password',
            'reset_password': 'Reset password',
            'security_question': 'Security question',
            'security_answer': 'Security answer',
            'create_account': 'Create Account',
            'already_have_account': 'Already have an account?',
            'login_here': 'Login here',
            'choose_security_question': 'Choose your security question',
            'please_choose_question': 'Please choose a question',
            'access_your_overview_space': 'Access your OverView space',
            'no_account_yet': 'No account yet?',
            'register_here': 'Register here',
            'join_overview_community': 'Join the OverView community',
            'continue': 'Continue',
            'back_to_login': 'Back to login',
            'forgot_password_step2': 'Security Question',
            'answer_security_question': 'Answer your security question',
            'security_question': 'Security question',
            'verify_answer': 'Verify answer',
            'forgot_password_step3': 'New Password',
            'enter_new_password': 'Enter your new password',
            'new_password': 'New password',
            'confirm_password': 'Confirm password',
            'reset_password': 'Reset password',
            'settings': 'Settings',
            'dark_mode': 'Dark mode',
            'language': 'Language',
            'on': 'On',
            'off': 'Off',

            # Devises
            'xaf': 'CFA Franc (FCFA)',
            'eur': 'Euro (€)',
            'usd': 'US Dollar ($)',

            # Types de transactions
            'income': 'Income',
            'expense': 'Expense',

            # Types d'événements
            'meeting': 'Meeting',
            'appointment': 'Appointment',
            'reminder': 'Reminder',
            'deadline': 'Deadline',
            'other': 'Other',

            # Messages JavaScript et confirmations
            'calculating': 'Calculating...',
            'overdue': 'Overdue!',
            'enter_password_to_show_balance': 'Please enter your password to show the balance:',
            'incorrect_password': 'Incorrect password!',
            'confirm_delete_objective': 'Are you sure you want to PERMANENTLY delete this objective?',
            'enter_password_to_confirm_deletion': 'To confirm deletion, please enter your password:',
            'confirm_delete_task': 'Are you sure you want to delete this task?',
            'confirm_delete_event': 'Are you sure you want to delete this event?',
            'enter_current_password': 'Enter your current password',
            'enter_new_password': 'Enter your new password',
            'confirm_new_password': 'Confirm your new password',
            'password_changed_successfully': 'Password changed successfully',
            'old_password_incorrect': 'Old password is incorrect',
            'both_fields_required': 'Both fields are required',
            'please_fill_all_fields': 'Please fill all fields',
            'user_already_exists': 'User already exists',
            'invalid_credentials': 'Invalid credentials. Please try again.',
            'successfully_logged_out': 'You have been successfully logged out.',
            'user_not_found': 'User not found',
            'no_security_question': 'No security question defined',
            'session_error': 'Session error. Please try again.',
            'incorrect_secret_answer': 'Incorrect secret answer',
            'password_reset_success': 'Password reset! You can now log in.',
            'please_choose_question': '-- Please choose a question --',
            'forgot_password_step1': 'Forgot Password (Step 1/3)',
            'enter_username_to_start_recovery': 'Please enter your username to start the recovery process.',
            'forgot_password_step2': 'Forgot Password (Step 2/3)',
            'enter_secret_answer': 'Please enter your secret answer.',
            'forgot_password_step3': 'Forgot Password (Step 3/3)',
            'verification_successful': 'Verification successful! Please enter your new password.',
            'new_password_label': 'New password',
            'reset_password_button': 'Reset password',
            'tasks_overdue': 'Overdue Tasks',
            'no_overdue_tasks': 'No overdue tasks',
            'overdue_warning': '⚠️ Overdue',
            'please_confirm_with_password': 'Please confirm with your password',
            'overdue_tasks_notifications': 'Notifications for overdue tasks',
            'change_password_button': '🔐 Change password',
            'current_password_label': 'Current password',
            'new_password_label': 'New password',
            'confirm_new_password_label': 'Confirm new password',

            # Months of the year
            'january': 'January',
            'february': 'February',
            'march': 'March',
            'april': 'April',
            'may': 'May',
            'june': 'June',
            'july': 'July',
            'august': 'August',
            'september': 'September',
            'october': 'October',
            'november': 'November',
            'december': 'December',

            # Month abbreviations
            'jan': 'Jan',
            'feb': 'Feb',
            'mar': 'Mar',
            'apr': 'Apr',
            'may_short': 'May',
            'jun': 'Jun',

            # Calendar messages
            'calendar_tip': 'Tip: Hold click for 1.8 seconds on a date to create an event',
            'december_2024': 'December 2024',

            # Advanced settings messages
            'next_auto_backup': 'Next automatic backup: Tomorrow at 02:00',
            'backup_now': 'Backup now',
            'email_notifications': 'Email notifications',
            'email_notifications_desc': 'Receive notifications by email',
            'email_address': 'Email address',
            'email_placeholder': 'your@email.com',
            'enabled': 'Enabled',
            'disabled': 'Disabled',
            'email_notifications_desc_small': 'Receive email notifications for deadlines',

            # Archives
            'my_successes': 'My Successes',
            'your_completed_savings_goals': 'Your completed savings goals',
            'completed_objectives': 'Completed objectives',
            'final_amount': 'Final amount',
            'no_archived_objectives': 'No archived objectives',
            'no_completed_objectives_yet': 'You don\'t have any completed objectives yet. Keep saving to see your successes here!',

            # Objective detail
            'objective_detail': 'Objective Detail',

            # Task detail
            'task_detail': 'Task Detail',

            # Advanced settings
            'advanced_settings': 'Advanced Settings'
        }
    }

def get_current_language():
    """Retourne la langue actuelle de l'utilisateur"""
    return session.get('language', 'fr')

def t(key, language=None):
    """Fonction de traduction"""
    if language is None:
        language = get_current_language()

    translations = get_translations()
    if language in translations and key in translations[language]:
        return translations[language][key]
    else:
        # Fallback vers le français si la traduction n'existe pas
        fr_translations = translations.get('fr', {})
        return fr_translations.get(key, key)

def get_db_connection():
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        try:
            return psycopg.connect(db_url)
        except Exception as e:
            print(f"!!! ERREUR DE CONNEXION POSTGRESQL : {e}")
            return None
    else:
        # Mode local pour les tests
        conn = sqlite3.connect('epargne.db')
        conn.row_factory = sqlite3.Row
        return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Veuillez vous connecter pour accéder à cette page.", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_security_questions():
    return ["Quel est le nom de votre premier animal de compagnie ?", "Quelle est votre ville de naissance ?", "Quel était le nom de votre école primaire ?"]

# --- Adaptateur SQL pour la syntaxe des paramètres ---
def sql_placeholder(query):
    return query.replace('?', '%s') if os.environ.get('DATABASE_URL') else query

# --- Helper pour créer un curseur compatible ---
class SQLiteCursorWrapper:
    def __init__(self, cursor):
        self.cursor = cursor

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __getattr__(self, name):
        return getattr(self.cursor, name)

def get_cursor(conn):
    if os.environ.get('DATABASE_URL'):
        return conn.cursor(row_factory=psycopg.rows.dict_row)
    else:
        # Pour SQLite, on retourne un wrapper qui supporte le protocole de gestionnaire de contexte
        return SQLiteCursorWrapper(conn.cursor())

# --- Helper pour convertir les résultats en dictionnaires ---
def convert_to_dict(row, is_postgres=False):
    if is_postgres:
        return dict(row)
    else:
        # Pour SQLite, structure réelle: id, nom, montant_cible, montant_actuel, date_limite, status, user_id
        return {
            'id': row[0], 'nom': row[1], 'montant_cible': row[2], 'montant_actuel': row[3],
            'date_limite': row[4], 'status': row[5], 'user_id': row[6], 'date_creation': None
        }

def convert_tache_to_dict(row, is_postgres=False):
    if is_postgres:
        return dict(row)
    else:
        # Pour SQLite, structure de la table taches: id, user_id, titre, description, date_creation, date_modification, termine, ordre, date_limite
        return {
            'id': row[0], 'user_id': row[1], 'titre': row[2], 'description': row[3],
            'date_creation': row[4], 'date_modification': row[5], 'termine': row[6], 'ordre': row[7], 'date_limite': row[8] if len(row) > 8 else None
        }

def convert_etape_to_dict(row, is_postgres=False):
    if is_postgres:
        return dict(row)
    else:
        # Pour SQLite, structure de la table etapes: id, tache_id, description, terminee, ordre, date_creation, date_modification
        return {
            'id': row[0], 'tache_id': row[1], 'description': row[2], 'terminee': row[3],
            'ordre': row[4], 'date_creation': row[5], 'date_modification': row[6]
        }

def format_currency(amount, currency=None):
    """Formate un montant selon la devise sélectionnée"""
    if amount is None:
        return "0 FCFA"

    if currency is None:
        currency = session.get('default_currency', 'XAF')

    currency_symbols = {
        'XAF': 'FCFA',
        'EUR': '€',
        'USD': '$'
    }

    symbol = currency_symbols.get(currency, 'FCFA')

    # Arrondir le montant selon la devise
    if currency == 'XAF':
        # Pour XAF, arrondir à l'unité (pas de décimales)
        rounded_amount = round(amount)
        formatted_amount = "{:,}".format(int(rounded_amount)).replace(',', ' ')
    else:
        # Pour EUR et USD, arrondir à 2 décimales et supprimer les .00 si nécessaire
        rounded_amount = round(amount, 2)
        if rounded_amount == int(rounded_amount):
            # Si c'est un nombre entier, pas de décimales
            formatted_amount = "{:,}".format(int(rounded_amount)).replace(',', ' ')
        else:
            # Sinon, afficher avec 2 décimales
            formatted_amount = "{:,.2f}".format(rounded_amount).replace(',', ' ').replace('.', ',')

    return f"{formatted_amount} {symbol}"

def get_currency_symbol():
    """Retourne le symbole de la devise actuelle"""
    currency = session.get('default_currency', 'XAF')
    currency_symbols = {
        'XAF': 'FCFA',
        'EUR': '€',
        'USD': '$'
    }
    return currency_symbols.get(currency, 'FCFA')

def get_exchange_rates():
    """Retourne les taux de change (simulés pour l'instant)"""
    return {
        'XAF': {
            'EUR': 0.00152,  # 1 XAF = 0.00152 EUR
            'USD': 0.00165,  # 1 XAF = 0.00165 USD
            'XAF': 1.0
        },
        'EUR': {
            'XAF': 657.89,   # 1 EUR = 657.89 XAF (1/0.00152)
            'USD': 1.09,     # 1 EUR = 1.09 USD
            'EUR': 1.0
        },
        'USD': {
            'XAF': 606.06,   # 1 USD = 606.06 XAF (1/0.00165)
            'EUR': 0.917431, # 1 USD = 0.917431 EUR (1/1.09)
            'USD': 1.0
        }
    }

def convert_currency(amount, from_currency, to_currency):
    """Convertit un montant d'une devise vers une autre"""
    if from_currency == to_currency:
        return amount

    rates = get_exchange_rates()
    if from_currency in rates and to_currency in rates[from_currency]:
        converted_amount = amount * rates[from_currency][to_currency]

        # Arrondir selon la devise de destination
        if to_currency == 'XAF':
            return round(converted_amount)  # Pas de décimales pour XAF
        else:
            return round(converted_amount, 2)  # 2 décimales pour EUR et USD

    return amount

def get_all_currencies():
    """Retourne toutes les devises disponibles"""
    return {
        'XAF': 'Franc CFA (FCFA)',
        'EUR': 'Euro (€)',
        'USD': 'Dollar US ($)'
    }

def convert_amount_to_system_currency(amount, from_currency='XAF'):
    """Convertit un montant vers la devise système"""
    devise_systeme = session.get('default_currency', 'XAF')
    return convert_currency(amount, from_currency, devise_systeme)

# --- AUTHENTIFICATION ---
@app.route('/register', methods=('GET', 'POST'))
def register():
    if 'user_id' in session: return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            question = request.form['security_question']
            answer = request.form['security_answer']

            if not all([username, password, question, answer]):
                flash("Veuillez remplir tous les champs.", "error")
                return render_template('register.html', questions=get_security_questions(), t=t, get_current_language=get_current_language)

            conn = get_db_connection()
            if conn is None:
                flash("Erreur de connexion à la base de données. Veuillez réessayer.", "error")
                return render_template('register.html', questions=get_security_questions(), t=t, get_current_language=get_current_language)

            cur = get_cursor(conn)
            try:
                # Vérifier si la table users existe, sinon la créer
                if os.environ.get('DATABASE_URL'):
                    # Syntaxe PostgreSQL
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(80) UNIQUE NOT NULL,
                            password VARCHAR(120) NOT NULL,
                            security_question TEXT,
                            security_answer VARCHAR(120)
                        )
                    """)
                else:
                    # Syntaxe SQLite
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            password TEXT NOT NULL,
                            security_question TEXT,
                            security_answer TEXT
                        )
                    """)
                conn.commit()

                hashed_password = generate_password_hash(password)
                hashed_answer = generate_password_hash(answer)
                sql = sql_placeholder('INSERT INTO users (username, password, security_question, security_answer) VALUES (?, ?, ?, ?)')
                cur.execute(sql, (username, hashed_password, question, hashed_answer))
                conn.commit()
                flash('Inscription réussie ! Vous pouvez maintenant vous connecter.', 'success')
                return redirect(url_for('login'))
            except (sqlite3.IntegrityError, psycopg.errors.IntegrityError):
                flash(f"L'utilisateur '{username}' existe déjà.", 'error')
            except Exception as e:
                print(f"Erreur lors de l'inscription: {e}")
                flash("Erreur lors de l'inscription. Veuillez réessayer.", "error")
            finally:
                cur.close()
                conn.close()
        except Exception as e:
            print(f"Erreur générale lors de l'inscription: {e}")
            flash("Erreur lors de l'inscription. Veuillez réessayer.", "error")

    return render_template('register.html', questions=get_security_questions(), t=t, get_current_language=get_current_language)

@app.route('/login', methods=('GET', 'POST'))
def login():
    if 'user_id' in session: return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cur = get_cursor(conn)
        try:
            sql = sql_placeholder('SELECT * FROM users WHERE username = ?')
            cur.execute(sql, (username,))
            user = cur.fetchone()
        finally:
            cur.close()
            conn.close()

        if user is None or not check_password_hash(user['password'], password):
            flash('Identifiants incorrects. Veuillez réessayer.', 'error')
        else:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))
    return render_template('login.html', t=t, get_current_language=get_current_language)

@app.route('/logout')
def logout():
    session.clear()
    flash('Vous avez été déconnecté avec succès.', 'success')
    return redirect(url_for('login'))

# --- FLUX DE RÉINITIALISATION DE MOT DE PASSE OUBLIÉ ---
@app.route('/forgot_password', methods=('GET', 'POST'))
def forgot_password_request():
    if 'user_id' in session: return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        conn = get_db_connection()
        cur = get_cursor(conn)
        try:
            sql = sql_placeholder('SELECT id, security_question FROM users WHERE username = ?')
            cur.execute(sql, (username,))
            user = cur.fetchone()
        finally:
            cur.close()
            conn.close()
        if user and user['security_question']:
            session['reset_user'] = username
            return redirect(url_for('forgot_password_answer'))
        else:
            flash("Utilisateur non trouvé ou aucune question de sécurité définie.", "error")
    return render_template('forgot_password_request.html', t=t, get_current_language=get_current_language)

@app.route('/forgot_password/answer', methods=('GET', 'POST'))
def forgot_password_answer():
    username = session.get('reset_user')
    if not username: return redirect(url_for('login'))
    conn = get_db_connection()
    cur = get_cursor(conn)
    try:
        sql = sql_placeholder('SELECT security_question, security_answer FROM users WHERE username = ?')
        cur.execute(sql, (username,))
        user = cur.fetchone()
    finally:
        cur.close()
        conn.close()
    if user is None:
        flash("Erreur de session. Veuillez recommencer.", "error")
        return redirect(url_for('forgot_password_request'))
    if request.method == 'POST':
        answer = request.form['security_answer']
        if check_password_hash(user['security_answer'], answer):
            session['reset_authorized'] = True
            return redirect(url_for('reset_password_final'))
        else:
            flash("La réponse secrète est incorrecte.", "error")
    return render_template('forgot_password_answer.html', question=user['security_question'], t=t, get_current_language=get_current_language)

@app.route('/reset_password_final', methods=('GET', 'POST'))
def reset_password_final():
    username = session.get('reset_user')
    if not session.get('reset_authorized') or not username: return redirect(url_for('login'))
    if request.method == 'POST':
        new_password = request.form['new_password']
        hashed_password = generate_password_hash(new_password)
        conn = get_db_connection()
        cur = get_cursor(conn)
        try:
            sql = sql_placeholder('UPDATE users SET password = ? WHERE username = ?')
            cur.execute(sql, (hashed_password, username))
            conn.commit()
        finally:
            cur.close()
            conn.close()
        session.pop('reset_user', None)
        session.pop('reset_authorized', None)
        flash("Mot de passe réinitialisé ! Vous pouvez vous connecter.", "success")
        return redirect(url_for('login'))
    return render_template('reset_password_final.html', t=t, get_current_language=get_current_language)

# --- ROUTES DE L'APPLICATION ---
@app.route('/')
@login_required
def index():
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))

    try:
        sql = sql_placeholder("SELECT * FROM objectifs WHERE status = 'actif' AND user_id = ? ORDER BY id DESC")
        cur.execute(sql, (user_id,))
        objectifs_db = cur.fetchall()
        sql = sql_placeholder("SELECT SUM(montant_actuel) as total FROM objectifs WHERE status = 'actif' AND user_id = ?")
        cur.execute(sql, (user_id,))
        total_epargne_result = cur.fetchone()
    finally:
        cur.close()
        conn.close()

    if is_postgres:
        total_epargne = total_epargne_result['total'] if total_epargne_result and total_epargne_result['total'] is not None else 0
        objectifs = [dict(obj) for obj in objectifs_db]
    else:
        total_epargne = total_epargne_result[0] if total_epargne_result and total_epargne_result[0] is not None else 0
        objectifs = [convert_to_dict(obj, is_postgres=False) for obj in objectifs_db]

    # Convertir le total vers la devise système
    total_epargne_converti = convert_amount_to_system_currency(total_epargne, 'XAF')

    for obj in objectifs:
        progression = (obj['montant_actuel'] / obj['montant_cible']) * 100 if obj['montant_cible'] > 0 else 0
        obj['progression'] = progression
    return render_template('index.html', objectifs=objectifs, total_epargne=total_epargne_converti, format_currency=format_currency, get_currency_symbol=get_currency_symbol, t=t, get_current_language=get_current_language)

@app.route('/archives')
@login_required
def archives():
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))

    try:
        sql = sql_placeholder("SELECT * FROM objectifs WHERE status = 'archivé' AND user_id = ? ORDER BY id DESC")
        cur.execute(sql, (user_id,))
        objectifs_archives = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    if is_postgres:
        objectifs = [dict(obj) for obj in objectifs_archives]
    else:
        objectifs = [convert_to_dict(obj, is_postgres=False) for obj in objectifs_archives]

    # Convertir les montants vers la devise système
    for obj in objectifs:
        obj['montant_cible'] = convert_amount_to_system_currency(obj['montant_cible'], 'XAF')
        obj['montant_actuel'] = convert_amount_to_system_currency(obj['montant_actuel'], 'XAF')

    return render_template('archives.html', objectifs=objectifs, format_currency=format_currency, get_currency_symbol=get_currency_symbol, get_current_language=get_current_language, t=t)

@app.route('/objectif/<int:objectif_id>')
@login_required
def objectif_detail(objectif_id):
    user_id = session['user_id']
    conn = get_db_connection()
    with get_cursor(conn) as cur:
        sql = sql_placeholder('SELECT * FROM objectifs WHERE id = ? AND user_id = ?')
        cur.execute(sql, (objectif_id, user_id))
        objectif = cur.fetchone()
        if objectif is None:
            flash("Cet objectif n'existe pas ou ne vous appartient pas.", "error")
            return redirect(url_for('index'))
        sql = sql_placeholder('SELECT * FROM transactions WHERE objectif_id = ? AND user_id = ? ORDER BY date DESC')
        cur.execute(sql, (objectif_id, user_id))
        transactions = cur.fetchall()
    conn.close()
    # Convertir les montants vers la devise système
    montant_cible_converti = convert_amount_to_system_currency(objectif['montant_cible'], 'XAF')
    montant_actuel_converti = convert_amount_to_system_currency(objectif['montant_actuel'], 'XAF')

    progression = (montant_actuel_converti / montant_cible_converti) * 100 if montant_cible_converti > 0 else 0
    montant_restant = montant_cible_converti - montant_actuel_converti
    rythme_quotidien = 0
    if objectif['date_limite'] and montant_restant > 0:
        try:
            date_limite = datetime.strptime(objectif['date_limite'], '%Y-%m-%d')
            jours_restants = (date_limite - datetime.now()).days
            if jours_restants > 0: rythme_quotidien = montant_restant / jours_restants
        except (ValueError, TypeError): pass
    # Créer un objectif avec les montants convertis
    objectif_converti = dict(objectif)
    objectif_converti['montant_cible'] = montant_cible_converti
    objectif_converti['montant_actuel'] = montant_actuel_converti

    return render_template('objectif_detail.html', objectif=objectif_converti, transactions=transactions, progression=progression, montant_restant=montant_restant, rythme_quotidien=rythme_quotidien, format_currency=format_currency, get_currency_symbol=get_currency_symbol, get_all_currencies=get_all_currencies, convert_currency=convert_currency, t=t, get_current_language=get_current_language)

@app.route('/formulaire_objectif/', defaults={'objectif_id': None}, methods=['GET'])
@app.route('/formulaire_objectif/<int:objectif_id>', methods=['GET'])
@login_required
def formulaire_objectif(objectif_id):
    objectif = None
    if objectif_id:
        user_id = session['user_id']
        conn = get_db_connection()
        with get_cursor(conn) as cur:
            sql = sql_placeholder('SELECT * FROM objectifs WHERE id = ? AND user_id = ?')
            cur.execute(sql, (objectif_id, user_id))
            objectif = cur.fetchone()
        conn.close()
        if objectif is None:
            flash("Cet objectif n'existe pas ou ne vous appartient pas.", "error")
            return redirect(url_for('index'))
    return render_template('formulaire_objectif.html', objectif=objectif, get_currency_symbol=get_currency_symbol, get_all_currencies=get_all_currencies, t=t, get_current_language=get_current_language)

@app.route('/sauvegarder_objectif/', defaults={'objectif_id': None}, methods=['POST'])
@app.route('/sauvegarder_objectif/<int:objectif_id>', methods=['POST'])
@login_required
def sauvegarder_objectif(objectif_id):
    user_id = session['user_id']
    password = request.form.get('password')
    conn = get_db_connection()
    with get_cursor(conn) as cur:
        sql = sql_placeholder('SELECT password FROM users WHERE id = ?')
        cur.execute(sql, (user_id,))
        user = cur.fetchone()
        if not password or not check_password_hash(user['password'], password):
            flash("Mot de passe incorrect !", "error")
            conn.close()
            return redirect(url_for('formulaire_objectif', objectif_id=objectif_id))

        nom = request.form['nom']
        montant_cible = float(request.form['montant_cible'])
        devise_cible = request.form.get('devise_cible', session.get('default_currency', 'XAF'))
        devise_systeme = session.get('default_currency', 'XAF')

        # Convertir le montant cible vers la devise du système
        montant_cible_converti = convert_currency(montant_cible, devise_cible, devise_systeme)
        date_limite = request.form['date_limite'] if request.form['date_limite'] else None

        if objectif_id:
            sql = sql_placeholder('UPDATE objectifs SET nom = ?, montant_cible = ?, date_limite = ? WHERE id = ? AND user_id = ?')
            cur.execute(sql, (nom, montant_cible_converti, date_limite, objectif_id, user_id))
            flash(f"L'objectif '{nom}' a été mis à jour.", 'success')
        else:
            sql = sql_placeholder('INSERT INTO objectifs (nom, montant_cible, montant_actuel, date_limite, status, user_id) VALUES (?, ?, ?, ?, ?, ?)')
            cur.execute(sql, (nom, montant_cible_converti, 0, date_limite, 'actif', user_id))
            if devise_cible != devise_systeme:
                flash(f"L'objectif '{nom}' a été créé avec un montant cible de {format_currency(montant_cible, devise_cible)} converti en {format_currency(montant_cible_converti, devise_systeme)}.", 'success')
            else:
                flash(f"L'objectif '{nom}' a été créé.", 'success')
        conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/supprimer_objectif/<int:objectif_id>', methods=['POST'])
@login_required
def supprimer_objectif(objectif_id):
    user_id = session['user_id']
    password = request.form.get('password')
    conn = get_db_connection()
    with get_cursor(conn) as cur:
        sql = sql_placeholder('SELECT password FROM users WHERE id = ?')
        cur.execute(sql, (user_id,))
        user = cur.fetchone()
        if not password or not check_password_hash(user['password'], password):
            flash("Mot de passe incorrect ! Suppression annulée.", "error")
            conn.close()
            return redirect(request.referrer or url_for('index'))

        sql = sql_placeholder('SELECT id FROM objectifs WHERE id = ? AND user_id = ?')
        cur.execute(sql, (objectif_id, user_id))
        objectif = cur.fetchone()
        if objectif:
            sql_trans = sql_placeholder('DELETE FROM transactions WHERE objectif_id = ?')
            cur.execute(sql_trans, (objectif_id,))
            sql_obj = sql_placeholder('DELETE FROM objectifs WHERE id = ?')
            cur.execute(sql_obj, (objectif_id,))
            flash("L'objectif a été supprimé définitivement.", 'success')
        else:
            flash("Action non autorisée.", "error")
        conn.commit()
    conn.close()
    return redirect(request.referrer or url_for('index'))

@app.route('/objectif/<int:objectif_id>/archiver', methods=['POST'])
@login_required
def archiver_objectif(objectif_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    try:
        sql = sql_placeholder("UPDATE objectifs SET status = 'archivé' WHERE id = ? AND user_id = ?")
        cur.execute(sql, (objectif_id, user_id))
        conn.commit()
        flash("Objectif archivé avec succès !", "success")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('index'))

@app.route('/objectif/<int:objectif_id>/add_transaction', methods=['POST'])
@login_required
def add_transaction(objectif_id):
    user_id = session['user_id']
    montant = float(request.form['montant'])
    type_transaction = request.form['type_transaction']
    devise_saisie = request.form.get('devise', session.get('default_currency', 'XAF'))
    devise_systeme = session.get('default_currency', 'XAF')

    # Convertir le montant vers la devise du système
    montant_converti = convert_currency(montant, devise_saisie, devise_systeme)

    conn = get_db_connection()
    with get_cursor(conn) as cur:
        sql = sql_placeholder('SELECT * FROM objectifs WHERE id = ? AND user_id = ?')
        cur.execute(sql, (objectif_id, user_id))
        objectif = cur.fetchone()
        if objectif is None:
            flash("Action non autorisée.", "error")
            return redirect(url_for('index'))

        montant_actuel = objectif['montant_actuel']
        nouveau_montant = montant_actuel + montant_converti if type_transaction == 'entree' else montant_actuel - montant_converti

        sql_update = sql_placeholder('UPDATE objectifs SET montant_actuel = ? WHERE id = ?')
        cur.execute(sql_update, (nouveau_montant, objectif_id))

        # Ajouter la transaction avec la devise de saisie
        sql_insert = sql_placeholder('INSERT INTO transactions (objectif_id, montant, type_transaction, user_id, devise_saisie) VALUES (?, ?, ?, ?, ?)')
        cur.execute(sql_insert, (objectif_id, montant, type_transaction, user_id, devise_saisie))

        conn.commit()

        # Message de confirmation avec conversion
        if devise_saisie != devise_systeme:
            flash(f"Transaction {type_transaction} de {format_currency(montant, devise_saisie)} convertie en {format_currency(montant_converti, devise_systeme)} ajoutée avec succès !", "success")
        else:
            flash(f"Transaction {type_transaction} de {format_currency(montant, devise_saisie)} ajoutée avec succès !", "success")

    conn.close()
    return redirect(url_for('objectif_detail', objectif_id=objectif_id))

@app.route('/parametres')
@login_required
def parametres():
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))
    try:
        sql = sql_placeholder('SELECT username, security_question FROM users WHERE id = ?')
        cur.execute(sql, (user_id,))
        user_raw = cur.fetchone()
        if is_postgres:
            user = dict(user_raw)
        else:
            user = {'username': user_raw[0], 'security_question': user_raw[1]}
    finally:
        cur.close()
        conn.close()
    return render_template('parametres.html', username=user['username'], security_question=user['security_question'], t=t, get_current_language=get_current_language)

@app.route('/update_password', methods=['POST'])
@login_required
def update_password():
    user_id = session['user_id']
    ancien_mdp = request.form.get('ancien_mdp')
    nouveau_mdp = request.form.get('nouveau_mdp')
    if not ancien_mdp or not nouveau_mdp:
        flash("Les deux champs sont requis.", "error")
        return redirect(url_for('parametres'))
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))
    try:
        sql = sql_placeholder('SELECT password FROM users WHERE id = ?')
        cur.execute(sql, (user_id,))
        user_raw = cur.fetchone()
        if is_postgres:
            user = dict(user_raw)
        else:
            user = {'password': user_raw[0]}
        if not check_password_hash(user['password'], ancien_mdp):
            flash("L'ancien mot de passe est incorrect.", "error")
        else:
            hashed_password = generate_password_hash(nouveau_mdp)
            sql_update = sql_placeholder('UPDATE users SET password = ? WHERE id = ?')
            cur.execute(sql_update, (hashed_password, user_id))
            conn.commit()
            flash("Mot de passe mis à jour.", "success")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('parametres'))

@app.route('/update_countdown_settings', methods=['POST'])
@login_required
def update_countdown_settings():
    user_id = session['user_id']
    countdown_update_interval = request.form.get('countdown_update_interval', 60)
    countdown_warning_days = request.form.get('countdown_warning_days', 3)

    # Sauvegarder dans la session pour l'instant (pourrait être stocké en base)
    session['countdown_update_interval'] = int(countdown_update_interval)
    session['countdown_warning_days'] = int(countdown_warning_days)

    flash('Paramètres de compte à rebours mis à jour !', 'success')
    return redirect(url_for('parametres'))

@app.route('/update_display_settings', methods=['POST'])
@login_required
def update_display_settings():
    user_id = session['user_id']
    show_countdown_on_list = request.form.get('show_countdown_on_list', 'true') == 'true'
    show_urgency_charts = request.form.get('show_urgency_charts', 'true') == 'true'
    default_currency = request.form.get('default_currency', 'XAF')

    # Sauvegarder dans la session pour l'instant
    session['show_countdown_on_list'] = show_countdown_on_list
    session['show_urgency_charts'] = show_urgency_charts
    session['default_currency'] = default_currency

    flash('Paramètres d\'affichage mis à jour !', 'success')
    return redirect(url_for('parametres'))

@app.route('/update_notification_settings', methods=['POST'])
@login_required
def update_notification_settings():
    user_id = session['user_id']
    email_notifications = request.form.get('email_notifications', 'true') == 'true'
    notification_advance_days = request.form.get('notification_advance_days', 1)

    # Sauvegarder dans la session pour l'instant
    session['email_notifications'] = email_notifications
    session['notification_advance_days'] = int(notification_advance_days)

    flash('Paramètres de notifications mis à jour !', 'success')
    return redirect(url_for('parametres'))

@app.route('/update_deletion_settings', methods=['POST'])
@login_required
def update_deletion_settings():
    user_id = session['user_id']
    auto_archive_completed = request.form.get('auto_archive_completed', 'true') == 'true'
    confirm_deletions = request.form.get('confirm_deletions', 'true') == 'true'

    # Sauvegarder dans la session pour l'instant
    session['auto_archive_completed'] = auto_archive_completed
    session['confirm_deletions'] = confirm_deletions

    flash('Paramètres de suppression mis à jour !', 'success')
    return redirect(url_for('parametres'))

@app.route('/update_language_settings', methods=['GET', 'POST'])
def update_language_settings():
    if request.method == 'POST':
        language = request.form.get('language', 'fr')
    else:
        language = request.args.get('language', 'fr')

    if language in ['fr', 'en']:
        session['language'] = language
        flash(f"{t('language_changed_to', language)} {t('language', language)}.", "success")
    else:
        flash(t("invalid_language"), "error")

    # Rediriger vers la page précédente ou la page de connexion
    referrer = request.referrer
    if referrer and any(page in referrer for page in ['login', 'register', 'forgot_password']):
        return redirect(referrer)
    else:
        return redirect(url_for('login'))

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    """Supprime définitivement le compte utilisateur et toutes ses données"""
    try:
        user_id = session.get('user_id')
        print(f"Tentative de suppression du compte pour l'utilisateur ID: {user_id}")  # Debug

        if not user_id:
            flash(t('user_not_found'), 'error')
            return redirect(url_for('login'))

        conn = get_db_connection()
        cursor = get_cursor(conn)

        # Supprimer toutes les données de l'utilisateur
        print("Début de la suppression des données...")  # Debug

        # 1. Supprimer les transactions
        sql_transactions = sql_placeholder("DELETE FROM transactions WHERE user_id = ?")
        cursor.execute(sql_transactions, (user_id,))
        print("Transactions supprimées")  # Debug

        # 2. Supprimer les objectifs
        sql_objectifs = sql_placeholder("DELETE FROM objectifs WHERE user_id = ?")
        cursor.execute(sql_objectifs, (user_id,))
        print("Objectifs supprimés")  # Debug

        # 3. Supprimer les étapes des tâches
        sql_etapes = sql_placeholder("""
            DELETE FROM etapes
            WHERE tache_id IN (SELECT id FROM taches WHERE user_id = ?)
        """)
        cursor.execute(sql_etapes, (user_id,))
        print("Étapes des tâches supprimées")  # Debug

        # 4. Supprimer les tâches
        sql_taches = sql_placeholder("DELETE FROM taches WHERE user_id = ?")
        cursor.execute(sql_taches, (user_id,))
        print("Tâches supprimées")  # Debug

        # 5. Supprimer les événements
        sql_evenements = sql_placeholder("DELETE FROM evenements WHERE user_id = ?")
        cursor.execute(sql_evenements, (user_id,))
        print("Événements supprimés")  # Debug

        # 6. Supprimer les questions de sécurité (si la table existe)
        try:
            sql_security = sql_placeholder("DELETE FROM security_questions WHERE user_id = ?")
            cursor.execute(sql_security, (user_id,))
            print("Questions de sécurité supprimées")  # Debug
        except Exception as e:
            print(f"Table security_questions non trouvée ou erreur: {e}")  # Debug

        # 7. Enfin, supprimer l'utilisateur
        sql_users = sql_placeholder("DELETE FROM users WHERE id = ?")
        cursor.execute(sql_users, (user_id,))
        print("Utilisateur supprimé")  # Debug

        conn.commit()
        conn.close()
        print("Base de données fermée")  # Debug

        # Nettoyer complètement la session
        session.clear()
        print("Session nettoyée")  # Debug

        # Forcer la déconnexion en supprimant toutes les données de session
        session.pop('user_id', None)
        session.pop('username', None)
        session.pop('logged_in', None)
        print("Données de session supprimées")  # Debug

        flash(t('account_deleted_successfully'), 'success')
        print("Redirection vers la page de connexion...")  # Debug
        return redirect(url_for('login'))

    except Exception as e:
        print(f"Erreur lors de la suppression du compte: {e}")  # Debug

        # Même en cas d'erreur, on essaie de supprimer l'utilisateur et de nettoyer la session
        try:
            # Supprimer l'utilisateur même si les autres suppressions ont échoué
            sql_users = sql_placeholder("DELETE FROM users WHERE id = ?")
            cursor.execute(sql_users, (user_id,))
            conn.commit()
            print("Utilisateur supprimé malgré l'erreur")  # Debug

            # Nettoyer la session
            session.clear()
            session.pop('user_id', None)
            session.pop('username', None)
            session.pop('logged_in', None)

            flash(t('account_deleted_successfully'), 'success')
            return redirect(url_for('login'))

        except Exception as final_error:
            print(f"Erreur finale lors de la suppression: {final_error}")  # Debug
            flash(t('error_deleting_account'), 'error')
            return redirect(url_for('parametres'))

# --- API Routes ---
@app.route('/api/check_user_password', methods=['POST'])
@login_required
def check_user_password():
    user_id = session['user_id']
    password = request.json.get('password')
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))
    try:
        sql = sql_placeholder('SELECT password FROM users WHERE id = ?')
        cur.execute(sql, (user_id,))
        user_raw = cur.fetchone()
        if is_postgres:
            user = dict(user_raw)
        else:
            user = {'password': user_raw[0]}
    finally:
        cur.close()
        conn.close()
    if user and check_password_hash(user['password'], password):
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/api/chart_data/<int:objectif_id>')
@login_required
def chart_data(objectif_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))
    try:
        sql_obj = sql_placeholder('SELECT id FROM objectifs WHERE id = ? AND user_id = ?')
        cur.execute(sql_obj, (objectif_id, user_id))
        objectif = cur.fetchone()
        if objectif is None: return jsonify({'error': 'Not authorized'}), 403
        sql_trans = sql_placeholder('SELECT montant, type_transaction, date FROM transactions WHERE objectif_id = ? AND user_id = ? ORDER BY date ASC')
        cur.execute(sql_trans, (objectif_id, user_id))
        transactions_raw = cur.fetchall()
        if is_postgres:
            transactions = [dict(trans) for trans in transactions_raw]
        else:
            transactions = [{'montant': trans[0], 'type_transaction': trans[1], 'date': trans[2]} for trans in transactions_raw]
    finally:
        cur.close()
        conn.close()
    labels, data_entrees, data_sorties = ["Départ"], [0], [0]
    montant_cumulatif_entrees, montant_cumulatif_sorties = 0, 0
    for trans in transactions:
        if trans['type_transaction'] == 'entree': montant_cumulatif_entrees += trans['montant']
        else: montant_cumulatif_sorties += trans['montant']
        date_obj = trans['date']
        # La date est stockée comme une chaîne, on l'utilise directement
        formatted_date = date_obj if date_obj else 'N/A'
        labels.append(formatted_date)
        data_entrees.append(montant_cumulatif_entrees)
        data_sorties.append(montant_cumulatif_sorties)
    return jsonify({'labels': labels, 'data_entrees': data_entrees, 'data_sorties': data_sorties})

# --- ROUTES POUR LA GESTION DES TÂCHES ---
@app.route('/taches')
@login_required
def taches():
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))

    try:
        # Récupérer les tâches actives
        sql_actives = sql_placeholder('SELECT * FROM taches WHERE user_id = ? AND termine = FALSE ORDER BY ordre ASC, date_creation ASC')
        cur.execute(sql_actives, (user_id,))
        taches_actives_raw = cur.fetchall()
        taches_actives = [convert_tache_to_dict(tache, is_postgres) for tache in taches_actives_raw]

        # Récupérer les tâches terminées
        sql_terminees = sql_placeholder('SELECT * FROM taches WHERE user_id = ? AND termine = TRUE ORDER BY date_modification DESC')
        cur.execute(sql_terminees, (user_id,))
        taches_terminees_raw = cur.fetchall()
        taches_terminees = [convert_tache_to_dict(tache, is_postgres) for tache in taches_terminees_raw]

        # Calculer le pourcentage de progression pour chaque tâche active
        total_etapes_global = 0
        total_etapes_terminees_global = 0

        for tache in taches_actives:
            sql_etapes = sql_placeholder('SELECT COUNT(*) as total, SUM(CASE WHEN terminee = TRUE THEN 1 ELSE 0 END) as terminees FROM etapes WHERE tache_id = ?')
            cur.execute(sql_etapes, (tache['id'],))
            result = cur.fetchone()
            if is_postgres:
                total_etapes = result['total'] or 0
                etapes_terminees = result['terminees'] or 0
            else:
                total_etapes = result[0] or 0
                etapes_terminees = result[1] or 0
            tache['progression'] = (etapes_terminees / total_etapes * 100) if total_etapes > 0 else 0
            tache['total_etapes'] = total_etapes
            tache['etapes_terminees'] = etapes_terminees

            # Ajouter au total global
            total_etapes_global += total_etapes
            total_etapes_terminees_global += etapes_terminees

        # Calculer le taux d'achèvement global
        taux_achevement_global = (total_etapes_terminees_global / total_etapes_global * 100) if total_etapes_global > 0 else 0
    finally:
        cur.close()
        conn.close()

    return render_template('taches.html', taches_actives=taches_actives, taches_terminees=taches_terminees, taux_achevement_global=taux_achevement_global, format_currency=format_currency, get_currency_symbol=get_currency_symbol, t=t, get_current_language=get_current_language)

@app.route('/formulaire_tache/', defaults={'tache_id': None}, methods=['GET'])
@app.route('/formulaire_tache/<int:tache_id>', methods=['GET'])
@login_required
def formulaire_tache(tache_id):
    tache = None
    etapes = []
    if tache_id:
        user_id = session['user_id']
        conn = get_db_connection()
        cur = get_cursor(conn)
        is_postgres = bool(os.environ.get('DATABASE_URL'))
        try:
            sql = sql_placeholder('SELECT * FROM taches WHERE id = ? AND user_id = ?')
            cur.execute(sql, (tache_id, user_id))
            tache_raw = cur.fetchone()
            if tache_raw:
                tache = convert_tache_to_dict(tache_raw, is_postgres)
                sql_etapes = sql_placeholder('SELECT * FROM etapes WHERE tache_id = ? ORDER BY ordre ASC')
                cur.execute(sql_etapes, (tache_id,))
                etapes_raw = cur.fetchall()
                etapes = [convert_etape_to_dict(etape, is_postgres) for etape in etapes_raw]
        finally:
            cur.close()
            conn.close()
    return render_template('formulaire_tache.html', tache=tache, etapes=etapes, get_currency_symbol=get_currency_symbol, t=t, get_current_language=get_current_language)

@app.route('/sauvegarder_tache/', defaults={'tache_id': None}, methods=['POST'])
@app.route('/sauvegarder_tache/<int:tache_id>', methods=['POST'])
@login_required
def sauvegarder_tache(tache_id):
    user_id = session['user_id']
    titre = request.form.get('titre')
    description = request.form.get('description', '')
    date_limite = request.form.get('date_limite')
    etapes_text = request.form.get('etapes', '')

    if not titre:
        flash("Le titre de la tâche est requis.", "error")
        return redirect(url_for('formulaire_tache', tache_id=tache_id))

    conn = get_db_connection()
    cur = get_cursor(conn)
    try:
        if tache_id:
            # Modification d'une tâche existante
            sql_update = sql_placeholder('UPDATE taches SET titre = ?, description = ?, date_limite = ?, date_modification = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?')
            cur.execute(sql_update, (titre, description, date_limite, tache_id, user_id))

            # Supprimer les anciennes étapes
            sql_delete_etapes = sql_placeholder('DELETE FROM etapes WHERE tache_id = ?')
            cur.execute(sql_delete_etapes, (tache_id,))
        else:
            # Création d'une nouvelle tâche
            sql_insert = sql_placeholder('INSERT INTO taches (user_id, titre, description, date_limite) VALUES (?, ?, ?, ?) RETURNING id')
            cur.execute(sql_insert, (user_id, titre, description, date_limite))
            tache_id = cur.fetchone()[0]

        # Ajouter les nouvelles étapes
        if etapes_text.strip():
            etapes_list = [etape.strip() for etape in etapes_text.split('\n') if etape.strip()]
            for i, etape in enumerate(etapes_list):
                sql_etape = sql_placeholder('INSERT INTO etapes (tache_id, description, ordre) VALUES (?, ?, ?)')
                cur.execute(sql_etape, (tache_id, etape, i + 1))

        conn.commit()
        flash("Tâche sauvegardée avec succès !", "success")
        return redirect(url_for('taches'))

    except Exception as e:
        conn.rollback()
        flash(f"Erreur lors de la sauvegarde : {str(e)}", "error")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('formulaire_tache', tache_id=tache_id))

@app.route('/tache/<int:tache_id>/toggle_etape/<int:etape_id>', methods=['POST'])
@login_required
def toggle_etape(tache_id, etape_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))

    try:
        # Vérifier que la tâche appartient à l'utilisateur
        sql_tache = sql_placeholder('SELECT id FROM taches WHERE id = ? AND user_id = ?')
        cur.execute(sql_tache, (tache_id, user_id))
        if not cur.fetchone():
            return jsonify({'success': False, 'error': 'Tâche non trouvée'})

        # Basculer le statut de l'étape
        sql_toggle = sql_placeholder('UPDATE etapes SET terminee = NOT terminee, date_modification = CURRENT_TIMESTAMP WHERE id = ? AND tache_id = ?')
        cur.execute(sql_toggle, (etape_id, tache_id))

        # Vérifier si toutes les étapes sont terminées
        sql_check = sql_placeholder('SELECT COUNT(*) as total, SUM(CASE WHEN terminee = TRUE THEN 1 ELSE 0 END) as terminees FROM etapes WHERE tache_id = ?')
        cur.execute(sql_check, (tache_id,))
        result = cur.fetchone()
        if is_postgres:
            total_etapes = result['total'] or 0
            etapes_terminees = result['terminees'] or 0
        else:
            total_etapes = result[0] or 0
            etapes_terminees = result[1] or 0

        # Si toutes les étapes sont terminées, marquer la tâche comme terminée
        if total_etapes > 0 and etapes_terminees == total_etapes:
            sql_termine = sql_placeholder('UPDATE taches SET termine = TRUE, date_modification = CURRENT_TIMESTAMP WHERE id = ?')
            cur.execute(sql_termine, (tache_id,))

        conn.commit()
        progression = (etapes_terminees / total_etapes * 100) if total_etapes > 0 else 0
        return jsonify({
            'success': True,
            'progression': round(progression, 1),
            'etapes_terminees': etapes_terminees,
            'total_etapes': total_etapes,
            'terminee': etapes_terminees == total_etapes if total_etapes > 0 else False
        })

    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        cur.close()
        conn.close()

@app.route('/supprimer_tache/<int:tache_id>', methods=['POST'])
@login_required
def supprimer_tache(tache_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    try:
        sql = sql_placeholder('DELETE FROM taches WHERE id = ? AND user_id = ?')
        cur.execute(sql, (tache_id, user_id))
        if cur.rowcount > 0:
            conn.commit()
            flash("Tâche supprimée avec succès.", "success")
        else:
            flash("Tâche non trouvée.", "error")
    except Exception as e:
        conn.rollback()
        flash(f"Erreur lors de la suppression : {str(e)}", "error")
    finally:
        cur.close()
        conn.close()
    return redirect(url_for('taches'))

@app.route('/tache/<int:tache_id>/detail')
@login_required
def tache_detail(tache_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))

    try:
        sql_tache = sql_placeholder('SELECT * FROM taches WHERE id = ? AND user_id = ?')
        cur.execute(sql_tache, (tache_id, user_id))
        tache_raw = cur.fetchone()

        if not tache_raw:
            flash("Tâche non trouvée.", "error")
            return redirect(url_for('taches'))

        tache = convert_tache_to_dict(tache_raw, is_postgres)

        sql_etapes = sql_placeholder('SELECT * FROM etapes WHERE tache_id = ? ORDER BY ordre ASC')
        cur.execute(sql_etapes, (tache_id,))
        etapes_raw = cur.fetchall()
        etapes = [convert_etape_to_dict(etape, is_postgres) for etape in etapes_raw]

        # Calculer la progression
        total_etapes = len(etapes)
        etapes_terminees = sum(1 for etape in etapes if etape['terminee'])
        progression = (etapes_terminees / total_etapes * 100) if total_etapes > 0 else 0
        tache['progression'] = progression
        tache['total_etapes'] = total_etapes
        tache['etapes_terminees'] = etapes_terminees

    finally:
        cur.close()
        conn.close()

    return render_template('tache_detail.html', tache=tache, etapes=etapes, progression=progression, format_currency=format_currency, get_currency_symbol=get_currency_symbol, t=t, get_current_language=get_current_language)

# --- AGENDA ROUTES ---
@app.route('/agenda')
@login_required
def agenda():
    # Rediriger vers le calendrier qui fait maintenant office d'agenda
    return redirect(url_for('calendrier'))

@app.route('/formulaire_evenement/', defaults={'evenement_id': None}, methods=['GET'])
@app.route('/formulaire_evenement/<int:evenement_id>', methods=['GET'])
@login_required
def formulaire_evenement(evenement_id):
    evenement = None
    if evenement_id:
        user_id = session['user_id']
        conn = get_db_connection()
        cur = get_cursor(conn)
        is_postgres = bool(os.environ.get('DATABASE_URL'))

        try:
            sql = sql_placeholder('SELECT * FROM evenements WHERE id = ? AND user_id = ?')
            cur.execute(sql, (evenement_id, user_id))
            evenement_raw = cur.fetchone()
            if evenement_raw:
                evenement = convert_evenement_to_dict(evenement_raw, is_postgres)
        finally:
            cur.close()
            conn.close()

    return render_template('formulaire_evenement.html', evenement=evenement, t=t, get_current_language=get_current_language)

@app.route('/sauvegarder_evenement/', defaults={'evenement_id': None}, methods=['POST'])
@app.route('/sauvegarder_evenement/<int:evenement_id>', methods=['POST'])
@login_required
def sauvegarder_evenement(evenement_id):
    user_id = session['user_id']
    titre = request.form['titre']
    description = request.form.get('description', '')
    date_debut = request.form['date_debut']
    heure_debut = request.form.get('heure_debut', '')
    date_fin = request.form.get('date_fin', '')
    heure_fin = request.form.get('heure_fin', '')
    lieu = request.form.get('lieu', '')
    couleur = request.form.get('couleur', '#fd7e14')
    rappel_minutes = request.form.get('rappel', '0')

    conn = get_db_connection()
    cur = get_cursor(conn)

    try:
        if evenement_id:
            sql = sql_placeholder('UPDATE evenements SET titre = ?, description = ?, date_debut = ?, heure_debut = ?, date_fin = ?, heure_fin = ?, lieu = ?, couleur = ?, rappel_minutes = ?, date_modification = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?')
            cur.execute(sql, (titre, description, date_debut, heure_debut, date_fin, heure_fin, lieu, couleur, rappel_minutes, evenement_id, user_id))
            flash("Événement modifié avec succès.", "success")
        else:
            sql = sql_placeholder('INSERT INTO evenements (user_id, titre, description, date_debut, heure_debut, date_fin, heure_fin, lieu, couleur, rappel_minutes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)')
            cur.execute(sql, (user_id, titre, description, date_debut, heure_debut, date_fin, heure_fin, lieu, couleur, rappel_minutes))
            flash("Événement créé avec succès.", "success")

        conn.commit()
    except Exception as e:
        conn.rollback()
        flash(f"Erreur lors de la sauvegarde : {str(e)}", "error")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('calendrier'))

@app.route('/evenement/<int:evenement_id>/toggle', methods=['POST'])
@login_required
def toggle_evenement(evenement_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)

    try:
        sql = sql_placeholder('UPDATE evenements SET termine = NOT termine WHERE id = ? AND user_id = ?')
        cur.execute(sql, (evenement_id, user_id))
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'error': str(e)})
    finally:
        cur.close()
        conn.close()

@app.route('/supprimer_evenement/<int:evenement_id>', methods=['POST'])
@login_required
def supprimer_evenement(evenement_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)

    try:
        sql = sql_placeholder('DELETE FROM evenements WHERE id = ? AND user_id = ?')
        cur.execute(sql, (evenement_id, user_id))
        if cur.rowcount > 0:
            conn.commit()
            flash("Événement supprimé avec succès.", "success")
        else:
            flash("Événement non trouvé.", "error")
    except Exception as e:
        conn.rollback()
        flash(f"Erreur lors de la suppression : {str(e)}", "error")
    finally:
        cur.close()
        conn.close()

    return redirect(url_for('agenda'))

def convert_evenement_to_dict(row, is_postgres=False):
    if is_postgres:
        return dict(row)
    else:
        return {
            'id': row[0], 'user_id': row[1], 'titre': row[2], 'description': row[3],
            'date_debut': row[4], 'date_fin': row[5], 'heure_debut': row[6], 'heure_fin': row[7],
            'lieu': row[8], 'couleur': row[9], 'rappel_minutes': row[10], 'termine': row[11],
            'date_creation': row[12]
        }

# --- DASHBOARD ROUTES ---
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))

    try:
        # Statistiques des objectifs
        sql_objectifs = sql_placeholder('SELECT COUNT(*) FROM objectifs WHERE user_id = ? AND status = "actif"')
        cur.execute(sql_objectifs, (user_id,))
        total_objectifs = cur.fetchone()[0]

        sql_epargne = sql_placeholder('SELECT SUM(montant_actuel) FROM objectifs WHERE user_id = ? AND status = "actif"')
        cur.execute(sql_epargne, (user_id,))
        total_epargne = cur.fetchone()[0] or 0
        # Convertir le total vers la devise système
        total_epargne_converti = convert_amount_to_system_currency(total_epargne, 'XAF')

        # Statistiques des tâches
        sql_taches = sql_placeholder('SELECT COUNT(*) FROM taches WHERE user_id = ?')
        cur.execute(sql_taches, (user_id,))
        total_taches = cur.fetchone()[0]

        sql_taches_terminees = sql_placeholder('SELECT COUNT(*) FROM taches WHERE user_id = ? AND termine = TRUE')
        cur.execute(sql_taches_terminees, (user_id,))
        taches_terminees = cur.fetchone()[0]

        # Statistiques des événements
        sql_evenements = sql_placeholder('SELECT COUNT(*) FROM evenements WHERE user_id = ? AND termine = FALSE')
        cur.execute(sql_evenements, (user_id,))
        evenements_a_venir = cur.fetchone()[0]

        # Objectifs proches de la fin
        sql_objectifs_proches = sql_placeholder('''
            SELECT id, nom, montant_cible, montant_actuel, date_limite, status, user_id
            FROM objectifs
            WHERE user_id = ? AND status = "actif"
            ORDER BY (montant_cible - montant_actuel) ASC
            LIMIT 3
        ''')
        cur.execute(sql_objectifs_proches, (user_id,))
        objectifs_proches_raw = cur.fetchall()
        objectifs_proches = [convert_to_dict(obj, is_postgres) for obj in objectifs_proches_raw]

        # Convertir les montants des objectifs vers la devise système
        for obj in objectifs_proches:
            obj['montant_cible'] = convert_amount_to_system_currency(obj['montant_cible'], 'XAF')
            obj['montant_actuel'] = convert_amount_to_system_currency(obj['montant_actuel'], 'XAF')

        # Tâches prioritaires (non terminées)
        sql_taches_prioritaires = sql_placeholder('''
            SELECT id, user_id, titre, description, date_creation, date_modification, termine, ordre
            FROM taches
            WHERE user_id = ? AND termine = FALSE
            ORDER BY date_creation ASC
            LIMIT 5
        ''')
        cur.execute(sql_taches_prioritaires, (user_id,))
        taches_prioritaires_raw = cur.fetchall()
        taches_prioritaires = [convert_tache_to_dict(tache, is_postgres) for tache in taches_prioritaires_raw]

    finally:
        cur.close()
        conn.close()

    stats = {
        'total_objectifs': total_objectifs,
        'total_epargne': total_epargne_converti,
        'total_taches': total_taches,
        'taches_terminees': taches_terminees,
        'evenements_a_venir': evenements_a_venir,
        'objectifs_proches': objectifs_proches,
        'taches_prioritaires': taches_prioritaires
    }

    return render_template('dashboard.html', stats=stats, format_currency=format_currency, get_currency_symbol=get_currency_symbol, t=t, get_current_language=get_current_language)

# --- NOTIFICATIONS ROUTES ---
@app.route('/notifications')
@login_required
def notifications():
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))

    try:
        # Objectifs proches de la fin (90% ou plus)
        sql_objectifs_proches = sql_placeholder('''
            SELECT id, nom, montant_cible, montant_actuel, date_limite, status, user_id
            FROM objectifs
            WHERE user_id = ? AND status = "actif" AND (montant_actuel / montant_cible) >= 0.9
        ''')
        cur.execute(sql_objectifs_proches, (user_id,))
        objectifs_proches_raw = cur.fetchall()
        objectifs_proches = [convert_to_dict(obj, is_postgres) for obj in objectifs_proches_raw]

        # Convertir les montants des objectifs vers la devise système
        for obj in objectifs_proches:
            obj['montant_cible'] = convert_amount_to_system_currency(obj['montant_cible'], 'XAF')
            obj['montant_actuel'] = convert_amount_to_system_currency(obj['montant_actuel'], 'XAF')

        # Tâches en retard (créées il y a plus de 7 jours)
        sql_taches_retard = sql_placeholder('''
            SELECT id, user_id, titre, description, date_creation, date_modification, termine, ordre
            FROM taches
            WHERE user_id = ? AND termine = FALSE AND date_creation < date("now", "-7 days")
        ''')
        cur.execute(sql_taches_retard, (user_id,))
        taches_retard_raw = cur.fetchall()
        taches_retard = [convert_tache_to_dict(tache, is_postgres) for tache in taches_retard_raw]

        # Événements à venir (dans les 7 prochains jours)
        sql_evenements_proches = sql_placeholder('''
            SELECT id, user_id, titre, description, date_debut, date_fin, heure_debut, heure_fin, lieu, couleur, rappel_minutes, termine, date_creation
            FROM evenements
            WHERE user_id = ? AND termine = FALSE
            AND date_debut BETWEEN date("now") AND date("now", "+7 days")
            ORDER BY date_debut ASC, heure_debut ASC
        ''')
        cur.execute(sql_evenements_proches, (user_id,))
        evenements_proches_raw = cur.fetchall()
        evenements_proches = [convert_evenement_to_dict(evenement, is_postgres) for evenement in evenements_proches_raw]

    finally:
        cur.close()
        conn.close()

    notifications = {
        'objectifs_proches': objectifs_proches,
        'taches_retard': taches_retard,
        'evenements_proches': evenements_proches
    }

    return render_template('notifications.html', notifications=notifications, format_currency=format_currency, get_currency_symbol=get_currency_symbol, t=t, get_current_language=get_current_language)

# --- CALENDRIER ROUTES ---
@app.route('/calendrier')
@login_required
def calendrier():
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))

    try:
        sql = sql_placeholder('SELECT * FROM evenements WHERE user_id = ? ORDER BY date_debut ASC, heure_debut ASC')
        cur.execute(sql, (user_id,))
        evenements_raw = cur.fetchall()
        evenements = [convert_evenement_to_dict(evenement, is_postgres) for evenement in evenements_raw]
    finally:
        cur.close()
        conn.close()

    return render_template('calendrier.html', evenements=evenements, format_currency=format_currency, get_currency_symbol=get_currency_symbol, t=t, get_current_language=get_current_language)

# --- RAPPORTS ROUTES ---
@app.route('/rapports')
@login_required
def rapports():
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))

    try:
        # Statistiques générales
        sql_total_objectifs = sql_placeholder('SELECT COUNT(*) FROM objectifs WHERE user_id = ?')
        cur.execute(sql_total_objectifs, (user_id,))
        total_objectifs = cur.fetchone()[0]

        sql_epargne_actuelle = sql_placeholder('SELECT SUM(montant_actuel) FROM objectifs WHERE user_id = ? AND status = "actif"')
        cur.execute(sql_epargne_actuelle, (user_id,))
        epargne_actuelle = cur.fetchone()[0] or 0
        # Convertir l'épargne vers la devise système
        epargne_actuelle_convertie = convert_amount_to_system_currency(epargne_actuelle, 'XAF')

        sql_total_taches = sql_placeholder('SELECT COUNT(*) FROM taches WHERE user_id = ?')
        cur.execute(sql_total_taches, (user_id,))
        total_taches = cur.fetchone()[0]

        sql_taux_reussite = sql_placeholder('''
            SELECT
                CASE
                    WHEN COUNT(*) > 0 THEN (COUNT(CASE WHEN termine = TRUE THEN 1 END) * 100.0 / COUNT(*))
                    ELSE 0
                END
            FROM taches WHERE user_id = ?
        ''')
        cur.execute(sql_taux_reussite, (user_id,))
        taux_reussite = cur.fetchone()[0] or 0

        # Évolution mensuelle des épargnes
        sql_evolution_mensuelle = sql_placeholder('''
            SELECT
                '2024-12' as mois,
                SUM(montant_actuel) as total
            FROM objectifs
            WHERE user_id = ?
        ''')
        cur.execute(sql_evolution_mensuelle, (user_id,))
        evolution_mensuelle_raw = cur.fetchall()
        evolution_mensuelle = [{'mois': row[0], 'total': convert_amount_to_system_currency(row[1], 'XAF')} for row in evolution_mensuelle_raw]

        # Performance des tâches par mois
        sql_performance_taches = sql_placeholder('''
            SELECT
                '2024-12' as mois,
                COUNT(*) as total_taches,
                COUNT(CASE WHEN termine = TRUE THEN 1 END) as taches_terminees
            FROM taches
            WHERE user_id = ?
        ''')
        cur.execute(sql_performance_taches, (user_id,))
        performance_taches_raw = cur.fetchall()
        performance_taches = [{'mois': row[0], 'total': row[1], 'terminees': row[2]} for row in performance_taches_raw]

    finally:
        cur.close()
        conn.close()

    stats = {
        'total_objectifs': total_objectifs,
        'epargne_actuelle': epargne_actuelle_convertie,
        'total_taches': total_taches,
        'taux_reussite': round(taux_reussite, 1),
        'evolution_mensuelle': evolution_mensuelle,
        'performance_taches': performance_taches
    }

    return render_template('rapports.html', stats=stats, format_currency=format_currency, get_currency_symbol=get_currency_symbol, t=t, get_current_language=get_current_language)

# --- PARAMÈTRES AVANCÉS ROUTES ---
@app.route('/parametres_avances')
@login_required
def parametres_avances():
    return render_template('parametres_avances.html')

# --- ROUTES D'EXPORT ---
@app.route('/export/pdf')
@login_required
def export_pdf():
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))

    try:
        # Récupérer les données pour le rapport
        # Statistiques générales
        sql_total_objectifs = sql_placeholder('SELECT COUNT(*) FROM objectifs WHERE user_id = ?')
        cur.execute(sql_total_objectifs, (user_id,))
        total_objectifs = cur.fetchone()[0]

        sql_epargne_actuelle = sql_placeholder('SELECT SUM(montant_actuel) FROM objectifs WHERE user_id = ? AND status = "actif"')
        cur.execute(sql_epargne_actuelle, (user_id,))
        epargne_actuelle = cur.fetchone()[0] or 0
        epargne_actuelle_convertie = convert_amount_to_system_currency(epargne_actuelle, 'XAF')

        sql_total_taches = sql_placeholder('SELECT COUNT(*) FROM taches WHERE user_id = ?')
        cur.execute(sql_total_taches, (user_id,))
        total_taches = cur.fetchone()[0]

        sql_taux_reussite = sql_placeholder('''
            SELECT
                CASE
                    WHEN COUNT(*) > 0 THEN (COUNT(CASE WHEN termine = TRUE THEN 1 END) * 100.0 / COUNT(*))
                    ELSE 0
                END
            FROM taches WHERE user_id = ?
        ''')
        cur.execute(sql_taux_reussite, (user_id,))
        taux_reussite = cur.fetchone()[0] or 0

        # Récupérer les objectifs
        sql_objectifs = sql_placeholder('SELECT nom, montant_cible, montant_actuel, date_limite, status FROM objectifs WHERE user_id = ? ORDER BY date_limite')
        cur.execute(sql_objectifs, (user_id,))
        objectifs = cur.fetchall()

        # Récupérer les tâches
        sql_taches = sql_placeholder('SELECT titre, description, date_limite, termine FROM taches WHERE user_id = ? ORDER BY date_creation')
        cur.execute(sql_taches, (user_id,))
        taches = cur.fetchall()

    finally:
        cur.close()
        conn.close()

        if REPORTLAB_AVAILABLE:
            # Créer le PDF avec reportlab
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            story = []
            styles = getSampleStyleSheet()

            # Titre
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                spaceAfter=30,
                alignment=1  # Centré
            )
            story.append(Paragraph("Rapport OverView", title_style))
            story.append(Spacer(1, 20))

            # Informations utilisateur
            story.append(Paragraph(f"Utilisateur: {session['username']}", styles['Normal']))
            story.append(Paragraph(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
            story.append(Spacer(1, 20))

            # Statistiques générales
            story.append(Paragraph("Statistiques Générales", styles['Heading2']))
            story.append(Spacer(1, 12))

            stats_data = [
                ['Métrique', 'Valeur'],
                ['Objectifs d\'épargne totaux', str(total_objectifs)],
                ['Épargne actuelle', f"{format_currency(epargne_actuelle_convertie)}"],
                ['Tâches créées', str(total_taches)],
                ['Taux de réussite moyen', f"{round(taux_reussite, 1)}%"]
            ]

            stats_table = Table(stats_data)
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(stats_table)
            story.append(Spacer(1, 20))

            # Objectifs
            story.append(Paragraph("Objectifs d'Épargne", styles['Heading2']))
            story.append(Spacer(1, 12))

            if objectifs:
                objectifs_data = [['Nom', 'Montant Cible', 'Montant Actuel', 'Date Limite', 'Statut']]
                for obj in objectifs:
                    objectifs_data.append([
                        obj[0],
                        f"{format_currency(convert_amount_to_system_currency(obj[1], 'XAF'))}",
                        f"{format_currency(convert_amount_to_system_currency(obj[2], 'XAF'))}",
                        obj[3] or 'Non définie',
                        obj[4]
                    ])

                objectifs_table = Table(objectifs_data)
                objectifs_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 10)
                ]))
                story.append(objectifs_table)
            else:
                story.append(Paragraph("Aucun objectif trouvé.", styles['Normal']))

            story.append(Spacer(1, 20))

            # Tâches
            story.append(Paragraph("Tâches", styles['Heading2']))
            story.append(Spacer(1, 12))

            if taches:
                taches_data = [['Titre', 'Description', 'Date Limite', 'Statut']]
                for tache in taches:
                    taches_data.append([
                        tache[0],
                        tache[1] or 'Aucune description',
                        tache[2] or 'Non définie',
                        'Terminée' if tache[3] else 'En cours'
                    ])

                taches_table = Table(taches_data)
                taches_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 10)
                ]))
                story.append(taches_table)
            else:
                story.append(Paragraph("Aucune tâche trouvée.", styles['Normal']))

            # Générer le PDF
            doc.build(story)
            buffer.seek(0)

            return send_file(
                buffer,
                as_attachment=True,
                download_name=f"rapport_overview_{session['username']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mimetype='application/pdf'
            )
        else:
            # Créer le rapport texte formaté (fallback)
            buffer = io.StringIO()

            # En-tête du rapport
            buffer.write("=" * 60 + "\n")
            buffer.write("RAPPORT OVERVIEW\n")
            buffer.write("=" * 60 + "\n\n")
            buffer.write(f"Utilisateur: {session['username']}\n")
            buffer.write(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")

            # Statistiques générales
            buffer.write("STATISTIQUES GÉNÉRALES\n")
            buffer.write("-" * 30 + "\n")
            buffer.write(f"Objectifs d'épargne totaux: {total_objectifs}\n")
            buffer.write(f"Épargne actuelle: {format_currency(epargne_actuelle_convertie)}\n")
            buffer.write(f"Tâches créées: {total_taches}\n")
            buffer.write(f"Taux de réussite moyen: {round(taux_reussite, 1)}%\n\n")

            # Objectifs
            buffer.write("OBJECTIFS D'ÉPARGNE\n")
            buffer.write("-" * 25 + "\n")
            if objectifs:
                buffer.write(f"{'Nom':<20} {'Montant Cible':<15} {'Montant Actuel':<15} {'Date Limite':<12} {'Statut':<10}\n")
                buffer.write("-" * 80 + "\n")
                for obj in objectifs:
                    buffer.write(f"{obj[0]:<20} {format_currency(convert_amount_to_system_currency(obj[1], 'XAF')):<15} {format_currency(convert_amount_to_system_currency(obj[2], 'XAF')):<15} {(obj[3] or 'Non définie'):<12} {obj[4]:<10}\n")
            else:
                buffer.write("Aucun objectif trouvé.\n")
            buffer.write("\n")

            # Tâches
            buffer.write("TÂCHES\n")
            buffer.write("-" * 8 + "\n")
            if taches:
                buffer.write(f"{'Titre':<25} {'Description':<30} {'Date Limite':<12} {'Statut':<10}\n")
                buffer.write("-" * 80 + "\n")
                for tache in taches:
                    description = tache[1] or 'Aucune description'
                    if len(description) > 28:
                        description = description[:25] + "..."
                    buffer.write(f"{tache[0]:<25} {description:<30} {(tache[2] or 'Non définie'):<12} {'Terminée' if tache[3] else 'En cours':<10}\n")
            else:
                buffer.write("Aucune tâche trouvée.\n")

            buffer.seek(0)

            return send_file(
                io.BytesIO(buffer.getvalue().encode('utf-8')),
                as_attachment=True,
                download_name=f"rapport_overview_{session['username']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mimetype='text/plain'
            )

@app.route('/export/excel')
@login_required
def export_excel():
    user_id = session['user_id']
    conn = get_db_connection()
    cur = get_cursor(conn)
    is_postgres = bool(os.environ.get('DATABASE_URL'))

    try:
        # Récupérer les données
        # Statistiques générales
        sql_total_objectifs = sql_placeholder('SELECT COUNT(*) FROM objectifs WHERE user_id = ?')
        cur.execute(sql_total_objectifs, (user_id,))
        total_objectifs = cur.fetchone()[0]

        sql_epargne_actuelle = sql_placeholder('SELECT SUM(montant_actuel) FROM objectifs WHERE user_id = ? AND status = "actif"')
        cur.execute(sql_epargne_actuelle, (user_id,))
        epargne_actuelle = cur.fetchone()[0] or 0
        epargne_actuelle_convertie = convert_amount_to_system_currency(epargne_actuelle, 'XAF')

        sql_total_taches = sql_placeholder('SELECT COUNT(*) FROM taches WHERE user_id = ?')
        cur.execute(sql_total_taches, (user_id,))
        total_taches = cur.fetchone()[0]

        sql_taux_reussite = sql_placeholder('''
            SELECT
                CASE
                    WHEN COUNT(*) > 0 THEN (COUNT(CASE WHEN termine = TRUE THEN 1 END) * 100.0 / COUNT(*))
                    ELSE 0
                END
            FROM taches WHERE user_id = ?
        ''')
        cur.execute(sql_taux_reussite, (user_id,))
        taux_reussite = cur.fetchone()[0] or 0

        # Récupérer les objectifs
        sql_objectifs = sql_placeholder('SELECT nom, montant_cible, montant_actuel, date_limite, status FROM objectifs WHERE user_id = ? ORDER BY date_limite')
        cur.execute(sql_objectifs, (user_id,))
        objectifs = cur.fetchall()

        # Récupérer les tâches
        sql_taches = sql_placeholder('SELECT titre, description, date_limite, termine FROM taches WHERE user_id = ? ORDER BY date_creation')
        cur.execute(sql_taches, (user_id,))
        taches = cur.fetchall()

    finally:
        cur.close()
        conn.close()

    # Créer le fichier Excel (CSV)
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    # En-tête du rapport
    writer.writerow(['Rapport OverView'])
    writer.writerow([f'Utilisateur: {session["username"]}'])
    writer.writerow([f'Date: {datetime.now().strftime("%d/%m/%Y %H:%M")}'])
    writer.writerow([])

    # Statistiques générales
    writer.writerow(['Statistiques Générales'])
    writer.writerow(['Métrique', 'Valeur'])
    writer.writerow(['Objectifs d\'épargne totaux', total_objectifs])
    writer.writerow(['Épargne actuelle', format_currency(epargne_actuelle_convertie)])
    writer.writerow(['Tâches créées', total_taches])
    writer.writerow(['Taux de réussite moyen', f"{round(taux_reussite, 1)}%"])
    writer.writerow([])

    # Objectifs
    writer.writerow(['Objectifs d\'Épargne'])
    writer.writerow(['Nom', 'Montant Cible', 'Montant Actuel', 'Date Limite', 'Statut'])
    for obj in objectifs:
        writer.writerow([
            obj[0],
            format_currency(convert_amount_to_system_currency(obj[1], 'XAF')),
            format_currency(convert_amount_to_system_currency(obj[2], 'XAF')),
            obj[3] or 'Non définie',
            obj[4]
        ])
    writer.writerow([])

    # Tâches
    writer.writerow(['Tâches'])
    writer.writerow(['Titre', 'Description', 'Date Limite', 'Statut'])
    for tache in taches:
        writer.writerow([
            tache[0],
            tache[1] or 'Aucune description',
            tache[2] or 'Non définie',
            'Terminée' if tache[3] else 'En cours'
        ])

    buffer.seek(0)

    return send_file(
        io.BytesIO(buffer.getvalue().encode('utf-8')),
        as_attachment=True,
        download_name=f"rapport_overview_{session['username']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mimetype='text/csv'
    )

# --- ROUTE DE DIAGNOSTIC ---
@app.route('/debug')
def debug_info():
    """Route de diagnostic pour vérifier l'état de l'application"""
    info = {
        'database_url': bool(os.environ.get('DATABASE_URL')),
        'database_connection': None,
        'tables_exist': False,
        'psycopg_available': False,
        'sqlite3_available': False
    }

    # Vérifier les imports
    try:
        import psycopg
        info['psycopg_available'] = True
    except ImportError:
        pass

    try:
        import sqlite3
        info['sqlite3_available'] = True
    except ImportError:
        pass

    # Vérifier la connexion à la base de données
    try:
        conn = get_db_connection()
        if conn:
            info['database_connection'] = True
            cur = conn.cursor()

            # Vérifier si la table users existe
            try:
                cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
                result = cur.fetchone()
                info['tables_exist'] = result is not None
            except:
                # Pour PostgreSQL
                try:
                    cur.execute("SELECT tablename FROM pg_tables WHERE tablename = 'users'")
                    result = cur.fetchone()
                    info['tables_exist'] = result is not None
                except:
                    pass

            cur.close()
            conn.close()
    except Exception as e:
        info['database_connection'] = str(e)

    return jsonify(info)

@app.route('/init-db')
def init_database():
    """Route pour initialiser manuellement la base de données"""
    try:
        conn = get_db_connection()
        if conn:
            cur = get_cursor(conn)

            # Créer toutes les tables nécessaires
            if os.environ.get('DATABASE_URL'):
                # PostgreSQL - Créer toutes les tables
                tables_sql = [
                    """CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(80) UNIQUE NOT NULL,
                        password VARCHAR(120) NOT NULL,
                        security_question TEXT,
                        security_answer VARCHAR(120)
                    )""",
                    """CREATE TABLE IF NOT EXISTS objectifs (
                        id SERIAL PRIMARY KEY,
                        nom VARCHAR(200) NOT NULL,
                        montant_cible DECIMAL(10,2) NOT NULL,
                        montant_actuel DECIMAL(10,2) NOT NULL,
                        date_limite DATE,
                        status VARCHAR(20) NOT NULL DEFAULT 'actif',
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )""",
                    """CREATE TABLE IF NOT EXISTS transactions (
                        id SERIAL PRIMARY KEY,
                        objectif_id INTEGER NOT NULL,
                        montant DECIMAL(10,2) NOT NULL,
                        type_transaction VARCHAR(20) NOT NULL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_id INTEGER NOT NULL,
                        devise_saisie VARCHAR(10) DEFAULT 'XAF',
                        FOREIGN KEY (objectif_id) REFERENCES objectifs (id),
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )""",
                    """CREATE TABLE IF NOT EXISTS evenements (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        titre VARCHAR(200) NOT NULL,
                        description TEXT,
                        date_debut DATE NOT NULL,
                        heure_debut TIME,
                        date_fin DATE,
                        heure_fin TIME,
                        lieu VARCHAR(200),
                        couleur VARCHAR(7) DEFAULT '#fd7e14',
                        rappel_minutes VARCHAR(10) DEFAULT '0',
                        termine BOOLEAN DEFAULT FALSE,
                        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )"""
                ]
            else:
                # SQLite - Créer toutes les tables
                tables_sql = [
                    """CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        security_question TEXT,
                        security_answer TEXT
                    )""",
                    """CREATE TABLE IF NOT EXISTS objectifs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT NOT NULL,
                        montant_cible REAL NOT NULL,
                        montant_actuel REAL NOT NULL,
                        date_limite TEXT,
                        status TEXT NOT NULL DEFAULT 'actif',
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )""",
                    """CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        objectif_id INTEGER NOT NULL,
                        montant REAL NOT NULL,
                        type_transaction TEXT NOT NULL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_id INTEGER NOT NULL,
                        devise_saisie TEXT DEFAULT 'XAF',
                        FOREIGN KEY (objectif_id) REFERENCES objectifs (id),
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )""",
                    """CREATE TABLE IF NOT EXISTS evenements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        titre TEXT NOT NULL,
                        description TEXT,
                        date_debut TEXT NOT NULL,
                        heure_debut TEXT,
                        date_fin TEXT,
                        heure_fin TEXT,
                        lieu TEXT,
                        couleur TEXT DEFAULT '#fd7e14',
                        rappel_minutes TEXT DEFAULT '0',
                        termine BOOLEAN DEFAULT FALSE,
                        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )"""
                ]

            # Exécuter toutes les créations de tables
            for sql in tables_sql:
                cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()

            return jsonify({
                'status': 'success',
                'message': 'Database tables created successfully'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Database connection failed'
            })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

def init_database_tables():
    """Initialise les tables de la base de données"""
    print("🔧 Initialisation de la base de données...")
    try:
        conn = get_db_connection()
        if conn:
            cur = get_cursor(conn)
            
            # Créer toutes les tables nécessaires
            if os.environ.get('DATABASE_URL'):
                # PostgreSQL - Créer toutes les tables
                tables_sql = [
                    """CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(80) UNIQUE NOT NULL,
                        password VARCHAR(120) NOT NULL,
                        security_question TEXT,
                        security_answer VARCHAR(120)
                    )""",
                    """CREATE TABLE IF NOT EXISTS objectifs (
                        id SERIAL PRIMARY KEY,
                        nom VARCHAR(200) NOT NULL,
                        montant_cible DECIMAL(10,2) NOT NULL,
                        montant_actuel DECIMAL(10,2) NOT NULL,
                        date_limite DATE,
                        status VARCHAR(20) NOT NULL DEFAULT 'actif',
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )""",
                    """CREATE TABLE IF NOT EXISTS transactions (
                        id SERIAL PRIMARY KEY,
                        objectif_id INTEGER NOT NULL,
                        montant DECIMAL(10,2) NOT NULL,
                        type_transaction VARCHAR(20) NOT NULL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_id INTEGER NOT NULL,
                        devise_saisie VARCHAR(10) DEFAULT 'XAF',
                        FOREIGN KEY (objectif_id) REFERENCES objectifs (id),
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )""",
                    """CREATE TABLE IF NOT EXISTS evenements (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        titre VARCHAR(200) NOT NULL,
                        description TEXT,
                        date_debut DATE NOT NULL,
                        heure_debut TIME,
                        date_fin DATE,
                        heure_fin TIME,
                        lieu VARCHAR(200),
                        couleur VARCHAR(7) DEFAULT '#fd7e14',
                        rappel_minutes VARCHAR(10) DEFAULT '0',
                        termine BOOLEAN DEFAULT FALSE,
                        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )"""
                ]
            else:
                # SQLite - Créer toutes les tables
                tables_sql = [
                    """CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        security_question TEXT,
                        security_answer TEXT
                    )""",
                    """CREATE TABLE IF NOT EXISTS objectifs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nom TEXT NOT NULL,
                        montant_cible REAL NOT NULL,
                        montant_actuel REAL NOT NULL,
                        date_limite TEXT,
                        status TEXT NOT NULL DEFAULT 'actif',
                        user_id INTEGER NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )""",
                    """CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        objectif_id INTEGER NOT NULL,
                        montant REAL NOT NULL,
                        type_transaction TEXT NOT NULL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        user_id INTEGER NOT NULL,
                        devise_saisie TEXT DEFAULT 'XAF',
                        FOREIGN KEY (objectif_id) REFERENCES objectifs (id),
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )""",
                    """CREATE TABLE IF NOT EXISTS evenements (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        titre TEXT NOT NULL,
                        description TEXT,
                        date_debut TEXT NOT NULL,
                        heure_debut TEXT,
                        date_fin TEXT,
                        heure_fin TEXT,
                        lieu TEXT,
                        couleur TEXT DEFAULT '#fd7e14',
                        rappel_minutes TEXT DEFAULT '0',
                        termine BOOLEAN DEFAULT FALSE,
                        date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )"""
                ]
            
            # Exécuter toutes les créations de tables
            for sql in tables_sql:
                cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            print("✅ Toutes les tables ont été créées avec succès")
        else:
            print("⚠️ Impossible de se connecter à la base de données")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'initialisation de la base de données: {e}")

# Initialiser les tables au démarrage de l'application
init_database_tables()

# --- Point de démarrage ---
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))