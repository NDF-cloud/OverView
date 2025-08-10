# 🚀 Configuration Render pour Mon App Web

## 📋 Étapes de Configuration

### 1. Créer une Base de Données PostgreSQL sur Render

1. **Connectez-vous à votre dashboard Render**
2. **Cliquez sur "New +" → "PostgreSQL"**
3. **Configurez la base de données :**
   - **Name** : `mon-app-db` (ou le nom de votre choix)
   - **Database** : `mon_app_web`
   - **User** : `mon_app_user`
   - **Region** : Choisissez la région la plus proche
   - **PostgreSQL Version** : `15` (recommandé)

### 2. Configurer la Variable d'Environnement

1. **Dans votre service web Render, allez dans "Environment"**
2. **Ajoutez la variable :**
   - **Key** : `DATABASE_URL`
   - **Value** : Copiez l'URL depuis votre base de données PostgreSQL
   
   L'URL ressemble à :
   ```
   postgresql://mon_app_user:password@host:port/mon_app_web
   ```

### 3. Initialiser la Base de Données

**Option A : Via le Dashboard Render (Recommandé)**

1. **Allez dans votre service web**
2. **Cliquez sur "Shell"**
3. **Exécutez :**
   ```bash
   python init_render_db.py
   ```

**Option B : Via les Logs Render**

1. **Redémarrez votre service web**
2. **Vérifiez les logs pour voir les erreurs de base de données**
3. **L'application devrait maintenant fonctionner**

### 4. Vérifier la Configuration

Après l'initialisation, vous devriez voir :
- ✅ **Build successful** dans les logs
- ✅ **Application accessible** à l'URL fournie
- ✅ **Page de connexion** qui s'affiche correctement

## 🔑 Identifiants de Test

Une fois la base de données initialisée, vous pouvez vous connecter avec :
- **Username** : `admin`
- **Password** : `admin123`

## 🚨 Dépannage

### Erreur "TemplateNotFound"
- ✅ **Résolu** : Les templates ont été ajoutés au dépôt Git

### Erreur de Base de Données
- 🔧 **Solution** : Exécuter `python init_render_db.py` dans le shell Render

### Erreur de Connexion PostgreSQL
- 🔧 **Vérifiez** : La variable `DATABASE_URL` est correctement configurée
- 🔧 **Vérifiez** : La base de données PostgreSQL est active et accessible

## 📞 Support

Si vous rencontrez des problèmes :
1. **Vérifiez les logs Render** dans la section "Logs"
2. **Vérifiez la configuration** des variables d'environnement
3. **Redémarrez le service** après modification des variables

---

**Note** : Ce guide suppose que vous avez déjà créé et configuré votre service web sur Render avec le fichier `render.yaml` fourni.
