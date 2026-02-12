#!/usr/bin/env python3
"""
Script para verificar configuração de deploy
Verifica se todas as variáveis e conexões estão funcionando
"""

import os
import sys

def check_environment():
    """Verifica variáveis de ambiente"""
    print("🔍 Verificando ambiente...")
    
    required_vars = [
        'FLASK_ENV',
        'SUPABASE_URL', 
        'SUPABASE_KEY'
    ]
    
    if os.getenv('FLASK_ENV') == 'production':
        required_vars.extend([
            'DB_HOST',
            'DB_NAME', 
            'DB_USER',
            'DB_PASSWORD'
        ])
    
    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)
    
    if missing:
        print(f"❌ Variáveis faltando: {', '.join(missing)}")
        return False
    else:
        print("✅ Todas as variáveis de ambiente presentes")
        return True

def check_database_connection():
    """Verifica conexão com banco de dados"""
    print("\n🗄️ Verificando conexão com banco...")
    
    try:
        if os.getenv('FLASK_ENV') == 'production':
            import psycopg2
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=5432
            )
            print("✅ PostgreSQL conectado com sucesso!")
            print(f"📍 Host: {os.getenv('DB_HOST')}")
            print(f"👤 User: {os.getenv('DB_USER')}")
            conn.close()
            return True
        else:
            import sqlite3
            conn = sqlite3.connect('ebserh_study.db')
            print("✅ SQLite conectado com sucesso!")
            conn.close()
            return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def check_supabase_connection():
    """Verifica conexão com Supabase"""
    print("\n☁️ Verificando conexão com Supabase...")
    
    try:
        from supabase_service import SupabaseService
        service = SupabaseService()
        result = service.test_connection()
        
        if result['status'] == 'sucesso':
            print("✅ Supabase conectado com sucesso!")
            return True
        else:
            print(f"❌ Erro Supabase: {result['message']}")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar Supabase: {e}")
        return False

def check_tables():
    """Verifica se tabelas existem"""
    print("\n📊 Verificando tabelas...")
    
    try:
        if os.getenv('FLASK_ENV') == 'production':
            import psycopg2
            conn = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=5432
            )
            cursor = conn.cursor()
        else:
            import sqlite3
            conn = sqlite3.connect('ebserh_study.db')
            cursor = conn.cursor()
        
        # Verificar tabelas
        tables = ['questoes', 'desempenho', 'plano_estudos', 'ia_feedback']
        existing_tables = []
        
        if os.getenv('FLASK_ENV') == 'production':
            cursor.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY tablename
            """)
            result = cursor.fetchall()
            existing_tables = [row[0] for row in result]
        else:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            result = cursor.fetchall()
            existing_tables = [row[0] for row in result]
        
        missing_tables = [t for t in tables if t not in existing_tables]
        
        if missing_tables:
            print(f"❌ Tabelas faltando: {', '.join(missing_tables)}")
            return False
        else:
            print("✅ Todas as tabelas existem!")
            print(f"📋 Tabelas encontradas: {', '.join(existing_tables)}")
            return True
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao verificar tabelas: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 Verificação de Deploy - EBserh Study")
    print("=" * 50)
    
    # Verificar ambiente
    env_ok = check_environment()
    
    # Verificar banco de dados
    db_ok = check_database_connection()
    
    # Verificar Supabase
    supabase_ok = check_supabase_connection()
    
    # Verificar tabelas
    tables_ok = check_tables()
    
    # Resumo
    print("\n" + "=" * 50)
    print("📋 RESUMO:")
    print(f"🔧 Ambiente: {'✅' if env_ok else '❌'}")
    print(f"🗄️ Banco: {'✅' if db_ok else '❌'}")
    print(f"☁️ Supabase: {'✅' if supabase_ok else '❌'}")
    print(f"📊 Tabelas: {'✅' if tables_ok else '❌'}")
    
    if all([env_ok, db_ok, supabase_ok, tables_ok]):
        print("\n🎉 TUDO OK PARA DEPLOY!")
        print("🌐 Sua aplicação está pronta para produção!")
        return 0
    else:
        print("\n⚠️ CORRIJA OS PROBLEMAS ANTES DE DEPLOY")
        return 1

if __name__ == "__main__":
    sys.exit(main())
