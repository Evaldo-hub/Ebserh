#!/usr/bin/env python3
"""
Migração de dados do SQLite para PostgreSQL
Script para transferir dados do desenvolvimento para produção
"""

import os
import sys
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import json

def get_sqlite_connection():
    """Conexão com SQLite (desenvolvimento)"""
    return sqlite3.connect('ebserh_study.db')

def get_postgres_connection():
    """Conexão com PostgreSQL (produção)"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL não encontrada!")
        print("Configure a variável de ambiente com a string de conexão PostgreSQL")
        sys.exit(1)
    
    return psycopg2.connect(database_url)

def migrate_table(pg_conn, table_name, data, columns):
    """Migra dados para tabela específica"""
    try:
        cursor = pg_conn.cursor()
        
        # Limpar tabela existente
        cursor.execute(f"DELETE FROM {table_name}")
        print(f"🗑️  Limpei tabela {table_name}")
        
        # Inserir dados
        if data:
            # Preparar placeholders
            placeholders = ', '.join(['%s'] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            # Converter dados para formato PostgreSQL
            for row in data:
                converted_row = []
                for value in row:
                    if isinstance(value, str):
                        # Converter strings vazias para None
                        converted_row.append(value if value.strip() else None)
                    else:
                        converted_row.append(value)
                
                cursor.execute(query, converted_row)
            
            print(f"✅ Inseridos {len(data)} registros em {table_name}")
        else:
            print(f"⚠️  Nenhum dado para migrar em {table_name}")
        
        pg_conn.commit()
        cursor.close()
        
    except Exception as e:
        print(f"❌ Erro ao migrar {table_name}: {e}")
        pg_conn.rollback()
        raise

def migrate_questoes(pg_conn):
    """Migra tabela de questões"""
    print("\n📚 Migrando questões...")
    
    sqlite_conn = get_sqlite_connection()
    sqlite_conn.row_factory = sqlite3.Row
    
    try:
        cursor = sqlite_conn.cursor()
        cursor.execute("""
            SELECT id, disciplina, semana, nivel, banca, enunciado, 
                   alternativas, resposta_correta, comentario
            FROM questoes
            ORDER BY id
        """)
        
        rows = cursor.fetchall()
        
        # Converter para lista de tuplas
        data = []
        for row in rows:
            # Adicionar campos novos com valores padrão
            data.append((
                row['id'],
                row['disciplina'],
                row['semana'],
                row['nivel'],
                row['banca'],
                row['enunciado'],
                row['alternativas'],
                row['resposta_correta'],
                row['comentario'],
                None,  # tags
                1,     # dificuldade_num
                False, # ia_generated
                datetime.now()  # data_criacao
            ))
        
        columns = [
            'id', 'disciplina', 'semana', 'nivel', 'banca', 'enunciado',
            'alternativas', 'resposta_correta', 'comentario', 'tags',
            'dificuldade_num', 'ia_generated', 'data_criacao'
        ]
        
        migrate_table(pg_conn, 'questoes', data, columns)
        
    finally:
        sqlite_conn.close()

def migrate_desempenho(pg_conn):
    """Migra tabela de desempenho"""
    print("\n📊 Migrando desempenho...")
    
    sqlite_conn = get_sqlite_connection()
    sqlite_conn.row_factory = sqlite3.Row
    
    try:
        cursor = sqlite_conn.cursor()
        cursor.execute("""
            SELECT id, questao_id, resposta_usuario, acerto, data_resposta
            FROM desempenho
            ORDER BY id
        """)
        
        rows = cursor.fetchall()
        
        # Converter para lista de tuplas
        data = []
        for row in rows:
            data.append((
                row['id'],
                row['questao_id'],
                row['resposta_usuario'],
                bool(row['acerto']),
                row['data_resposta'],
                'anonymous'  # usuario_id padrão
            ))
        
        columns = [
            'id', 'questao_id', 'resposta_usuario', 'acerto', 
            'data_resposta', 'usuario_id'
        ]
        
        migrate_table(pg_conn, 'desempenho', data, columns)
        
    finally:
        sqlite_conn.close()

def migrate_plano_estudos(pg_conn):
    """Migra tabela do plano de estudos"""
    print("\n📅 Migrando plano de estudos...")
    
    sqlite_conn = get_sqlite_connection()
    sqlite_conn.row_factory = sqlite3.Row
    
    try:
        cursor = sqlite_conn.cursor()
        cursor.execute("""
            SELECT id, semana, conteudo, disciplinas
            FROM plano_estudos
            ORDER BY semana
        """)
        
        rows = cursor.fetchall()
        
        # Converter para lista de tuplas
        data = []
        for row in rows:
            data.append((
                row['id'],
                row['semana'],
                row['conteudo'],
                row['disciplinas'],
                datetime.now()  # data_criacao
            ))
        
        columns = ['id', 'semana', 'conteudo', 'disciplinas', 'data_criacao']
        
        migrate_table(pg_conn, 'plano_estudos', data, columns)
        
    finally:
        sqlite_conn.close()

def verify_migration(pg_conn):
    """Verifica se migração foi bem-sucedida"""
    print("\n🔍 Verificando migração...")
    
    cursor = pg_conn.cursor()
    
    tables = ['questoes', 'desempenho', 'plano_estudos', 'ia_feedback', 'sessoes']
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"📋 {table}: {count} registros")
        except Exception as e:
            print(f"❌ Erro ao verificar {table}: {e}")
    
    cursor.close()

def main():
    """Função principal de migração"""
    print("🚀 Iniciando migração SQLite → PostgreSQL")
    print("=" * 50)
    
    try:
        # Conectar ao PostgreSQL
        pg_conn = get_postgres_connection()
        print("✅ Conectado ao PostgreSQL")
        
        # Verificar se tabelas existem
        cursor = pg_conn.cursor()
        cursor.execute("""
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        
        expected_tables = ['questoes', 'desempenho', 'plano_estudos', 'ia_feedback', 'sessoes']
        
        if not all(table in tables for table in expected_tables):
            print("❌ Tabelas não encontradas no PostgreSQL!")
            print("Execute o app_production.py primeiro para criar as tabelas.")
            return
        
        # Migrar dados
        migrate_questoes(pg_conn)
        migrate_desempenho(pg_conn)
        migrate_plano_estudos(pg_conn)
        
        # Verificar migração
        verify_migration(pg_conn)
        
        pg_conn.close()
        
        print("\n" + "=" * 50)
        print("🎉 Migração concluída com sucesso!")
        print("📱 Seu app está pronto para produção!")
        
    except Exception as e:
        print(f"\n❌ Erro durante migração: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
