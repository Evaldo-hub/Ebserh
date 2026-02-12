"""
Serviço de sincronização com Supabase
Gerencia a conexão e sincronização de dados entre SQLite local e Supabase
"""

import os
import sqlite3
import json
from datetime import datetime
from supabase import create_client, Client

class SupabaseService:
    def __init__(self):
        self.supabase_url = os.getenv('SUPABASE_URL', 'https://xlqcjfcfbehcgkkpyrde.supabase.co')
        self.supabase_key = os.getenv('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRiLmhscWNqZmNmYmVoY2dra3B5cmRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY0NzI5MDAsImV4cCI6MjA1MjA0ODkwMH0.7wYkQhE5L3k8XqJ9X2mF4P6vR7sT1nW2pY3zK4V8c')
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        self.db_name = 'ebserh_study.db'
    
    def get_local_connection(self):
        """Obtém conexão com o banco SQLite local"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def test_connection(self):
        """Testa conexão com Supabase"""
        try:
            response = self.client.table('questoes').select('id').limit(1).execute()
            return {
                'status': 'sucesso',
                'message': 'Conexão com Supabase estabelecida com sucesso!'
            }
        except Exception as e:
            return {
                'status': 'erro',
                'message': f'Erro na conexão: {str(e)}'
            }
    
    def get_supabase_stats(self):
        """Obtém estatísticas das tabelas no Supabase"""
        try:
            stats = {}
            
            # Contar registros em cada tabela
            tables = ['questoes', 'desempenho', 'plano_estudos', 'ia_feedback']
            
            for table in tables:
                try:
                    response = self.client.table(table).select('id').execute()
                    stats[f'total_{table}'] = len(response.data) if response.data else 0
                    
                    # Obter última sincronização
                    if table == 'questoes':
                        response_sync = self.client.table(table).select('data_sincronizacao').order('data_sincronizacao', desc=True).limit(1).execute()
                        if response_sync.data:
                            stats[f'ultima_sinc_{table}'] = response_sync.data[0].get('data_sincronizacao')
                        else:
                            stats[f'ultima_sinc_{table}'] = None
                    elif table == 'desempenho':
                        stats[f'ultima_sinc_{table}'] = None
                    elif table == 'plano_estudos':
                        stats[f'ultima_sinc_plano'] = None
                    elif table == 'ia_feedback':
                        stats[f'ultima_sinc_feedback'] = None
                        
                except Exception as e:
                    stats[f'total_{table}'] = 0
                    stats[f'ultima_sinc_{table}'] = None
            
            return {
                'status': 'sucesso',
                **stats
            }
            
        except Exception as e:
            return {
                'status': 'erro',
                'message': f'Erro ao obter estatísticas: {str(e)}'
            }
    
    def sync_questoes_to_supabase(self):
        """Sincroniza tabela questoes para Supabase"""
        try:
            conn = self.get_local_connection()
            cursor = conn.cursor()
            
            # Obter todas as questões locais
            cursor.execute('SELECT * FROM questoes')
            questoes = cursor.fetchall()
            conn.close()
            
            synced = 0
            errors = 0
            
            for questao in questoes:
                try:
                    # Converter para dicionário e adicionar campos do Supabase
                    data = dict(questao)
                    data['id_local'] = data['id']
                    data['data_sincronizacao'] = datetime.now().isoformat()
                    
                    # Remover id original para usar auto-increment do Supabase
                    del data['id']
                    
                    # Upsert no Supabase
                    response = self.client.table('questoes').upsert(data).execute()
                    
                    if response.data:
                        synced += 1
                    else:
                        errors += 1
                        
                except Exception as e:
                    errors += 1
                    continue
            
            return {
                'status': 'sucesso',
                'message': f'Sincronização concluída: {synced} questões sincronizadas, {errors} erros',
                'synced': synced,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'status': 'erro',
                'message': f'Erro na sincronização: {str(e)}'
            }
    
    def sync_desempenho_to_supabase(self):
        """Sincroniza tabela desempenho para Supabase"""
        try:
            conn = self.get_local_connection()
            cursor = conn.cursor()
            
            # Obter todos os registros de desempenho
            cursor.execute('SELECT * FROM desempenho')
            desempenho = cursor.fetchall()
            conn.close()
            
            synced = 0
            errors = 0
            
            for registro in desempenho:
                try:
                    data = dict(registro)
                    data['id_local'] = data['id']
                    data['data_sincronizacao'] = datetime.now().isoformat()
                    del data['id']
                    
                    response = self.client.table('desempenho').upsert(data).execute()
                    
                    if response.data:
                        synced += 1
                    else:
                        errors += 1
                        
                except Exception as e:
                    errors += 1
                    continue
            
            return {
                'status': 'sucesso',
                'message': f'Sincronização concluída: {synced} registros sincronizados, {errors} erros',
                'synced': synced,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'status': 'erro',
                'message': f'Erro na sincronização: {str(e)}'
            }
    
    def sync_plano_estudos_to_supabase(self):
        """Sincroniza tabela plano_estudos para Supabase"""
        try:
            conn = self.get_local_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM plano_estudos')
            plano = cursor.fetchall()
            conn.close()
            
            synced = 0
            errors = 0
            
            for registro in plano:
                try:
                    data = dict(registro)
                    data['id_local'] = data['id']
                    data['data_sincronizacao'] = datetime.now().isoformat()
                    del data['id']
                    
                    response = self.client.table('plano_estudos').upsert(data).execute()
                    
                    if response.data:
                        synced += 1
                    else:
                        errors += 1
                        
                except Exception as e:
                    errors += 1
                    continue
            
            return {
                'status': 'sucesso',
                'message': f'Sincronização concluída: {synced} registros sincronizados, {errors} erros',
                'synced': synced,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'status': 'erro',
                'message': f'Erro na sincronização: {str(e)}'
            }
    
    def sync_ia_feedback_to_supabase(self):
        """Sincroniza tabela ia_feedback para Supabase"""
        try:
            conn = self.get_local_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM ia_feedback')
            feedback = cursor.fetchall()
            conn.close()
            
            synced = 0
            errors = 0
            
            for registro in feedback:
                try:
                    data = dict(registro)
                    data['id_local'] = data['id']
                    data['data_sincronizacao'] = datetime.now().isoformat()
                    del data['id']
                    
                    response = self.client.table('ia_feedback').upsert(data).execute()
                    
                    if response.data:
                        synced += 1
                    else:
                        errors += 1
                        
                except Exception as e:
                    errors += 1
                    continue
            
            return {
                'status': 'sucesso',
                'message': f'Sincronização concluída: {synced} registros sincronizados, {errors} erros',
                'synced': synced,
                'errors': errors
            }
            
        except Exception as e:
            return {
                'status': 'erro',
                'message': f'Erro na sincronização: {str(e)}'
            }
    
    def sync_all_to_supabase(self):
        """Sincroniza todas as tabelas para Supabase"""
        results = {}
        
        # Sincronizar cada tabela
        results['questoes'] = self.sync_questoes_to_supabase()
        results['desempenho'] = self.sync_desempenho_to_supabase()
        results['plano_estudos'] = self.sync_plano_estudos_to_supabase()
        results['ia_feedback'] = self.sync_ia_feedback_to_supabase()
        
        # Calcular totais
        total_synced = sum(r.get('synced', 0) for r in results.values() if isinstance(r, dict))
        total_errors = sum(r.get('errors', 0) for r in results.values() if isinstance(r, dict))
        
        return {
            'status': 'sucesso',
            'message': f'Sincronização completa: {total_synced} registros sincronizados, {total_errors} erros',
            'details': results,
            'total_synced': total_synced,
            'total_errors': total_errors
        }
    
    def init_supabase_tables(self):
        """Inicializa tabelas no Supabase (gera SQL para execução manual)"""
        sql_statements = {
            'questoes': '''
                CREATE TABLE IF NOT EXISTS questoes (
                    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                    id_local INTEGER UNIQUE,
                    disciplina TEXT NOT NULL,
                    semana INTEGER NOT NULL,
                    nivel TEXT NOT NULL CHECK (nivel IN ('Básico', 'Alto', 'Pegadinha')),
                    banca TEXT NOT NULL,
                    enunciado TEXT NOT NULL,
                    alternativas TEXT NOT NULL,
                    resposta_correta TEXT NOT NULL,
                    comentario TEXT NOT NULL,
                    data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                
                CREATE INDEX IF NOT EXISTS idx_questoes_id_local ON questoes(id_local);
                CREATE INDEX IF NOT EXISTS idx_questoes_disciplina ON questoes(disciplina);
                CREATE INDEX IF NOT EXISTS idx_questoes_semana ON questoes(semana);
            ''',
            
            'desempenho': '''
                CREATE TABLE IF NOT EXISTS desempenho (
                    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                    id_local INTEGER UNIQUE,
                    questao_id INTEGER NOT NULL,
                    resposta_usuario TEXT NOT NULL,
                    acerto BOOLEAN NOT NULL,
                    data_resposta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                
                CREATE INDEX IF NOT EXISTS idx_desempenho_id_local ON desempenho(id_local);
                CREATE INDEX IF NOT EXISTS idx_desempenho_questao_id ON desempenho(questao_id);
                CREATE INDEX IF NOT EXISTS idx_desempenho_acerto ON desempenho(acerto);
            ''',
            
            'plano_estudos': '''
                CREATE TABLE IF NOT EXISTS plano_estudos (
                    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                    id_local INTEGER UNIQUE,
                    semana INTEGER NOT NULL UNIQUE,
                    conteudo TEXT NOT NULL,
                    disciplinas TEXT NOT NULL,
                    data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                
                CREATE INDEX IF NOT EXISTS idx_plano_estudos_id_local ON plano_estudos(id_local);
                CREATE INDEX IF NOT EXISTS idx_plano_estudos_semana ON plano_estudos(semana);
            ''',
            
            'ia_feedback': '''
                CREATE TABLE IF NOT EXISTS ia_feedback (
                    id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                    id_local INTEGER UNIQUE,
                    questao_id_local INTEGER NOT NULL,
                    tipo TEXT NOT NULL,
                    conteudo TEXT NOT NULL,
                    utilidade INTEGER DEFAULT 0,
                    data TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                
                CREATE INDEX IF NOT EXISTS idx_ia_feedback_id_local ON ia_feedback(id_local);
                CREATE INDEX IF NOT EXISTS idx_ia_feedback_questao_id ON ia_feedback(questao_id_local);
                CREATE INDEX IF NOT EXISTS idx_ia_feedback_tipo ON ia_feedback(tipo);
            '''
        }
        
        return {
            'status': 'sucesso',
            'message': 'SQL gerado para criação das tabelas',
            'sql': sql_statements
        }
    
    def fix_supabase_tables(self):
        """Gera SQL para corrigir tabelas existentes no Supabase"""
        fix_sql = '''
            -- Adicionar colunas faltantes na tabela questoes
            ALTER TABLE questoes ADD COLUMN IF NOT EXISTS id_local INTEGER UNIQUE;
            ALTER TABLE questoes ADD COLUMN IF NOT EXISTS data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE questoes ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE questoes ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            
            -- Adicionar colunas faltantes na tabela desempenho
            ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS id_local INTEGER UNIQUE;
            ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            
            -- Adicionar colunas faltantes na tabela plano_estudos
            ALTER TABLE plano_estudos ADD COLUMN IF NOT EXISTS id_local INTEGER UNIQUE;
            ALTER TABLE plano_estudos ADD COLUMN IF NOT EXISTS data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE plano_estudos ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE plano_estudos ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            
            -- Adicionar colunas faltantes na tabela ia_feedback
            ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS id_local INTEGER UNIQUE;
            ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            
            -- Criar índices para melhor performance
            CREATE INDEX IF NOT EXISTS idx_questoes_id_local ON questoes(id_local);
            CREATE INDEX IF NOT EXISTS idx_desempenho_id_local ON desempenho(id_local);
            CREATE INDEX IF NOT EXISTS idx_plano_estudos_id_local ON plano_estudos(id_local);
            CREATE INDEX IF NOT EXISTS idx_ia_feedback_id_local ON ia_feedback(id_local);
        '''
        
        return {
            'status': 'sucesso',
            'message': 'SQL gerado para correção das tabelas',
            'sql': fix_sql
        }

# Instância global do serviço
supabase_service = SupabaseService()
