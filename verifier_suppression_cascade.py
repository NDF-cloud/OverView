#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de vérification des contraintes de suppression en cascade
Vérifie que toutes les tables ont bien les bonnes contraintes FOREIGN KEY avec ON DELETE CASCADE
"""

import sqlite3
import os
import psycopg2
import psycopg2.extras

def verifier_sqlite_cascade():
    """Vérifier les contraintes de suppression en cascade dans SQLite"""
    
    print("🔍 VÉRIFICATION DES CONTRAINTES CASCADE - SQLite")
    print("=" * 60)
    
    db_path = 'epargne.db'
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Récupérer toutes les contraintes FOREIGN KEY
        cursor.execute("PRAGMA foreign_key_list")
        foreign_keys = cursor.fetchall()
        
        if not foreign_keys:
            print("⚠️  Aucune contrainte FOREIGN KEY trouvée")
            return False
        
        print(f"📋 {len(foreign_keys)} contraintes FOREIGN KEY trouvées:")
        print("-" * 60)
        
        cascade_count = 0
        no_cascade_count = 0
        
        for fk in foreign_keys:
            table_name = fk[2]  # Table qui a la contrainte
            ref_table = fk[3]    # Table référencée
            on_delete = fk[6]    # Action ON DELETE
            
            if on_delete == 'CASCADE':
                status = "✅ CASCADE"
                cascade_count += 1
            else:
                status = f"❌ {on_delete or 'NO ACTION'}"
                no_cascade_count += 1
            
            print(f"📊 {table_name} → {ref_table}: {status}")
        
        print("-" * 60)
        print(f"✅ Contraintes CASCADE: {cascade_count}")
        print(f"❌ Contraintes sans CASCADE: {no_cascade_count}")
        
        if no_cascade_count == 0:
            print("\n🎉 PARFAIT ! Toutes les contraintes sont en CASCADE")
            return True
        else:
            print(f"\n⚠️  ATTENTION ! {no_cascade_count} contraintes ne sont pas en CASCADE")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False
    
    finally:
        conn.close()

def verifier_postgres_cascade():
    """Vérifier les contraintes de suppression en cascade dans PostgreSQL"""
    
    print("\n🔍 VÉRIFICATION DES CONTRAINTES CASCADE - PostgreSQL")
    print("=" * 60)
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("⚠️  Variable DATABASE_URL non définie")
        return False
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Récupérer toutes les contraintes FOREIGN KEY avec leurs actions ON DELETE
        query = """
        SELECT 
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name,
            rc.delete_rule
        FROM 
            information_schema.table_constraints AS tc 
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
              AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
              AND ccu.table_schema = tc.table_schema
            JOIN information_schema.referential_constraints AS rc
              ON tc.constraint_name = rc.constraint_name
        WHERE tc.constraint_type = 'FOREIGN KEY'
        ORDER BY tc.table_name, kcu.column_name;
        """
        
        cursor.execute(query)
        foreign_keys = cursor.fetchall()
        
        if not foreign_keys:
            print("⚠️  Aucune contrainte FOREIGN KEY trouvée")
            return False
        
        print(f"📋 {len(foreign_keys)} contraintes FOREIGN KEY trouvées:")
        print("-" * 60)
        
        cascade_count = 0
        no_cascade_count = 0
        
        for fk in foreign_keys:
            table_name = fk[0]
            column_name = fk[1]
            foreign_table = fk[2]
            foreign_column = fk[3]
            delete_rule = fk[4]
            
            if delete_rule == 'CASCADE':
                status = "✅ CASCADE"
                cascade_count += 1
            else:
                status = f"❌ {delete_rule}"
                no_cascade_count += 1
            
            print(f"📊 {table_name}.{column_name} → {foreign_table}.{foreign_column}: {status}")
        
        print("-" * 60)
        print(f"✅ Contraintes CASCADE: {cascade_count}")
        print(f"❌ Contraintes sans CASCADE: {no_cascade_count}")
        
        if no_cascade_count == 0:
            print("\n🎉 PARFAIT ! Toutes les contraintes sont en CASCADE")
            return True
        else:
            print(f"\n⚠️  ATTENTION ! {no_cascade_count} contraintes ne sont pas en CASCADE")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification PostgreSQL: {e}")
        return False
    
    finally:
        if 'conn' in locals():
            conn.close()

def verifier_structure_tables():
    """Vérifier la structure des tables principales"""
    
    print("\n🏗️  VÉRIFICATION DE LA STRUCTURE DES TABLES")
    print("=" * 60)
    
    # Vérifier SQLite
    db_path = 'epargne.db'
    if os.path.exists(db_path):
        print(f"📱 Vérification SQLite ({db_path}):")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        tables = ['users', 'objectifs', 'transactions', 'taches', 'etapes', 'evenements', 'registre_caisse', 'notifications']
        
        for table in tables:
            try:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                if columns:
                    print(f"  ✅ {table}: {len(columns)} colonnes")
                else:
                    print(f"  ❌ {table}: Table non trouvée")
            except:
                print(f"  ❌ {table}: Erreur d'accès")
        
        conn.close()
    
    # Vérifier PostgreSQL si disponible
    database_url = os.getenv('DATABASE_URL')
    if database_url:
        print(f"\n🐘 Vérification PostgreSQL:")
        try:
            conn = psycopg2.connect(database_url)
            cursor = conn.cursor()
            
            tables = ['users', 'objectifs', 'transactions', 'taches', 'etapes', 'evenements', 'registre_caisse', 'notifications']
            
            for table in tables:
                try:
                    cursor.execute(f"""
                        SELECT COUNT(*) FROM information_schema.columns 
                        WHERE table_name = '{table}'
                    """)
                    count = cursor.fetchone()[0]
                    if count > 0:
                        print(f"  ✅ {table}: {count} colonnes")
                    else:
                        print(f"  ❌ {table}: Table non trouvée")
                except:
                    print(f"  ❌ {table}: Erreur d'accès")
            
            conn.close()
        except Exception as e:
            print(f"  ❌ Erreur de connexion PostgreSQL: {e}")

def main():
    """Fonction principale de vérification"""
    
    print("🔍 VÉRIFICATION COMPLÈTE DE LA SUPPRESSION EN CASCADE")
    print("=" * 70)
    
    # Vérifier SQLite
    sqlite_ok = verifier_sqlite_cascade()
    
    # Vérifier PostgreSQL
    postgres_ok = verifier_postgres_cascade()
    
    # Vérifier la structure des tables
    verifier_structure_tables()
    
    # Résumé final
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DE LA VÉRIFICATION:")
    print("-" * 40)
    
    if sqlite_ok:
        print("✅ SQLite: Contraintes CASCADE correctes")
    else:
        print("❌ SQLite: Problèmes avec les contraintes CASCADE")
    
    if postgres_ok:
        print("✅ PostgreSQL: Contraintes CASCADE correctes")
    else:
        print("❌ PostgreSQL: Problèmes avec les contraintes CASCADE")
    
    if sqlite_ok and postgres_ok:
        print("\n🎉 EXCELLENT ! Toutes les bases sont correctement configurées")
        print("✅ La suppression de compte supprimera TOUTES les données")
        print("✅ Le registre de caisse sera bien supprimé avec le compte")
    else:
        print("\n⚠️  ATTENTION ! Certaines bases ont des problèmes")
        print("❌ La suppression de compte pourrait ne pas fonctionner correctement")
    
    print("=" * 70)

if __name__ == "__main__":
    main()
