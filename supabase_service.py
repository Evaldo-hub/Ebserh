"""
Supabase Service - Sincronização de dados com Supabase
Gerencia a sincronização de questões e desempenho entre SQLite local e Supabase
"""

import os
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
from supabase import create_client, Client

# Carregar variáveis de ambiente
load_dotenv()

class SupabaseService:
    def __init__(self):
        """Inicializa o cliente Supabase"""
        self.supabase_url = os.getenv('SUPABASE_URL')
        self.supabase_key = os.getenv('SUPABASE_KEY')
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem ser configurados no .env")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
        self.db_name = 'ebserh_study.db'
    
    def get_local_connection(self):
        """Obtém conexão com o banco SQLite local"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def sync_questoes_to_supabase(self) -> Dict:
        """
        Sincroniza todas as questões do SQLite local para o Supabase
        """
        try:
            conn = self.get_local_connection()
            
            # Buscar todas as questões locais
            cursor = conn.execute('SELECT * FROM questoes')
            questoes_locais = cursor.fetchall()
            conn.close()
            
            if not questoes_locais:
                return {'status': 'info', 'message': 'Nenhuma questão encontrada para sincronizar'}
            
            sincronizadas = 0
            erros = []
            
            for questao in questoes_locais:
                try:
                    # Converter para formato Supabase
                    questao_data = {
                        'id_local': questao['id'],
                        'disciplina': questao['disciplina'],
                        'semana': questao['semana'],
                        'nivel': questao['nivel'],
                        'banca': questao['banca'],
                        'enunciado': questao['enunciado'],
                        'alternativas': questao['alternativas'],
                        'resposta_correta': questao['resposta_correta'],
                        'comentario': questao['comentario'],
                        'data_sincronizacao': datetime.now().isoformat()
                    }
                    
                    # Verificar se já existe
                    existing = self.client.table('questoes').select('id').eq('id_local', questao['id']).execute()
                    
                    if existing.data:
                        # Atualizar
                        result = self.client.table('questoes').update(questao_data).eq('id_local', questao['id']).execute()
                    else:
                        # Inserir
                        result = self.client.table('questoes').insert(questao_data).execute()
                    
                    if result.data:
                        sincronizadas += 1
                    
                except Exception as e:
                    erros.append(f"Questão {questao['id']}: {str(e)}")
            
            return {
                'status': 'sucesso',
                'sincronizadas': sincronizadas,
                'total': len(questoes_locais),
                'erros': erros
            }
            
        except Exception as e:
            return {'status': 'erro', 'message': f'Erro na sincronização: {str(e)}'}
    
    def sync_desempenho_to_supabase(self) -> Dict:
        """
        Sincroniza todos os registros de desempenho para o Supabase
        """
        try:
            conn = self.get_local_connection()
            
            # Buscar todos os registros de desempenho
            cursor = conn.execute('SELECT * FROM desempenho')
            desempenho_local = cursor.fetchall()
            conn.close()
            
            if not desempenho_local:
                return {'status': 'info', 'message': 'Nenhum registro de desempenho encontrado'}
            
            sincronizados = 0
            erros = []
            
            for registro in desempenho_local:
                try:
                    # Converter para formato Supabase
                    desempenho_data = {
                        'id_local': registro['id'],
                        'questao_id_local': registro['questao_id'],
                        'resposta_usuario': registro['resposta_usuario'],
                        'acerto': bool(registro['acerto']),
                        'data_resposta': registro['data_resposta'],
                        'data_sincronizacao': datetime.now().isoformat()
                    }
                    
                    # Verificar se já existe
                    existing = self.client.table('desempenho').select('id').eq('id_local', registro['id']).execute()
                    
                    if existing.data:
                        # Atualizar
                        result = self.client.table('desempenho').update(desempenho_data).eq('id_local', registro['id']).execute()
                    else:
                        # Inserir
                        result = self.client.table('desempenho').insert(desempenho_data).execute()
                    
                    if result.data:
                        sincronizados += 1
                    
                except Exception as e:
                    erros.append(f"Registro {registro['id']}: {str(e)}")
            
            return {
                'status': 'sucesso',
                'sincronizados': sincronizados,
                'total': len(desempenho_local),
                'erros': erros
            }
            
        except Exception as e:
            return {'status': 'erro', 'message': f'Erro na sincronização: {str(e)}'}
    
    def sync_plano_estudos_to_supabase(self) -> Dict:
        """
        Sincroniza todos os registros de plano de estudos para o Supabase
        """
        try:
            conn = self.get_local_connection()
            
            # Buscar todos os registros de plano de estudos
            cursor = conn.execute('SELECT * FROM plano_estudos')
            plano_local = cursor.fetchall()
            conn.close()
            
            if not plano_local:
                return {'status': 'info', 'message': 'Nenhum registro de plano de estudos encontrado'}
            
            sincronizados = 0
            erros = []
            
            for registro in plano_local:
                try:
                    # Converter para formato Supabase
                    plano_data = {
                        'id_local': registro['id'],
                        'semana': registro['semana'],
                        'conteudo': registro['conteudo'],
                        'disciplinas': registro['disciplinas'],
                        'data_sincronizacao': datetime.now().isoformat()
                    }
                    
                    # Verificar se já existe
                    existing = self.client.table('plano_estudos').select('id').eq('id_local', registro['id']).execute()
                    
                    if existing.data:
                        # Atualizar
                        result = self.client.table('plano_estudos').update(plano_data).eq('id_local', registro['id']).execute()
                    else:
                        # Inserir
                        result = self.client.table('plano_estudos').insert(plano_data).execute()
                    
                    if result.data:
                        sincronizados += 1
                    
                except Exception as e:
                    erros.append(f"Registro {registro['id']}: {str(e)}")
            
            return {
                'status': 'sucesso',
                'sincronizados': sincronizados,
                'total': len(plano_local),
                'erros': erros
            }
            
        except Exception as e:
            return {'status': 'erro', 'message': f'Erro na sincronização: {str(e)}'}
    
    def sync_ia_feedback_to_supabase(self) -> Dict:
        """
        Sincroniza todos os registros de ia_feedback para o Supabase
        """
        try:
            conn = self.get_local_connection()
            
            # Buscar todos os registros de ia_feedback
            cursor = conn.execute('SELECT * FROM ia_feedback')
            feedback_local = cursor.fetchall()
            conn.close()
            
            if not feedback_local:
                return {'status': 'info', 'message': 'Nenhum registro de ia_feedback encontrado'}
            
            sincronizados = 0
            erros = []
            
            for registro in feedback_local:
                try:
                    # Converter para formato Supabase
                    feedback_data = {
                        'id_local': registro['id'],
                        'questao_id_local': registro['questao_id'],
                        'tipo': registro['tipo'],
                        'conteudo': registro['conteudo'],
                        'utilidade': registro['utilidade'],
                        'data': registro['data'],
                        'data_sincronizacao': datetime.now().isoformat()
                    }
                    
                    # Verificar se já existe
                    existing = self.client.table('ia_feedback').select('id').eq('id_local', registro['id']).execute()
                    
                    if existing.data:
                        # Atualizar
                        result = self.client.table('ia_feedback').update(feedback_data).eq('id_local', registro['id']).execute()
                    else:
                        # Inserir
                        result = self.client.table('ia_feedback').insert(feedback_data).execute()
                    
                    if result.data:
                        sincronizados += 1
                    
                except Exception as e:
                    erros.append(f"Registro {registro['id']}: {str(e)}")
            
            return {
                'status': 'sucesso',
                'sincronizados': sincronizados,
                'total': len(feedback_local),
                'erros': erros
            }
            
        except Exception as e:
            return {'status': 'erro', 'message': f'Erro na sincronização: {str(e)}'}
    
    def sync_all_to_supabase(self) -> Dict:
        """
        Sincroniza todos os dados para o Supabase
        """
        resultado_questoes = self.sync_questoes_to_supabase()
        resultado_desempenho = self.sync_desempenho_to_supabase()
        resultado_plano = self.sync_plano_estudos_to_supabase()
        resultado_feedback = self.sync_ia_feedback_to_supabase()
        
        # Verificar se todos foram sucesso
        todos_sucesso = all([
            resultado_questoes['status'] == 'sucesso',
            resultado_desempenho['status'] == 'sucesso',
            resultado_plano['status'] == 'sucesso',
            resultado_feedback['status'] == 'sucesso'
        ])
        
        return {
            'status': 'sucesso' if todos_sucesso else 'parcial',
            'questoes': resultado_questoes,
            'desempenho': resultado_desempenho,
            'plano_estudos': resultado_plano,
            'ia_feedback': resultado_feedback,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_supabase_stats(self) -> Dict:
        """
        Obtém estatísticas dos dados no Supabase
        """
        try:
            # Contar questões
            questoes_result = self.client.table('questoes').select('count', count='exact').execute()
            total_questoes = questoes_result.count or 0
            
            # Contar desempenho
            desempenho_result = self.client.table('desempenho').select('count', count='exact').execute()
            total_desempenho = desempenho_result.count or 0
            
            # Contar plano de estudos
            plano_result = self.client.table('plano_estudos').select('count', count='exact').execute()
            total_plano = plano_result.count or 0
            
            # Contar ia_feedback
            feedback_result = self.client.table('ia_feedback').select('count', count='exact').execute()
            total_feedback = feedback_result.count or 0
            
            # Obter última sincronização
            ultimas_questoes = self.client.table('questoes').select('data_sincronizacao').order('data_sincronizacao', desc=True).limit(1).execute()
            ult_desempenho = self.client.table('desempenho').select('data_sincronizacao').order('data_sincronizacao', desc=True).limit(1).execute()
            ult_plano = self.client.table('plano_estudos').select('data_sincronizacao').order('data_sincronizacao', desc=True).limit(1).execute()
            ult_feedback = self.client.table('ia_feedback').select('data_sincronizacao').order('data_sincronizacao', desc=True).limit(1).execute()
            
            return {
                'status': 'sucesso',
                'total_questoes': total_questoes,
                'total_desempenho': total_desempenho,
                'total_plano_estudos': total_plano,
                'total_ia_feedback': total_feedback,
                'ultima_sinc_questoes': ultimas_questoes.data[0]['data_sincronizacao'] if ultimas_questoes.data else None,
                'ultima_sinc_desempenho': ult_desempenho.data[0]['data_sincronizacao'] if ult_desempenho.data else None,
                'ultima_sinc_plano': ult_plano.data[0]['data_sincronizacao'] if ult_plano.data else None,
                'ultima_sinc_feedback': ult_feedback.data[0]['data_sincronizacao'] if ult_feedback.data else None
            }
            
        except Exception as e:
            return {'status': 'erro', 'message': f'Erro ao obter estatísticas: {str(e)}'}
    
    def fix_supabase_tables(self) -> Dict:
        """
        Corrige as tabelas existentes adicionando colunas faltantes
        """
        try:
            # SQL para corrigir as tabelas
            fix_tables_sql = """
            -- Adicionar colunas faltantes na tabela questoes
            ALTER TABLE questoes ADD COLUMN IF NOT EXISTS id_local INTEGER;
            CREATE UNIQUE INDEX IF NOT EXISTS idx_questoes_id_local ON questoes(id_local);
            
            -- Adicionar colunas faltantes na tabela desempenho
            ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS id_local INTEGER;
            ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS questao_id_local INTEGER;
            CREATE UNIQUE INDEX IF NOT EXISTS idx_desempenho_id_local ON desempenho(id_local);
            CREATE INDEX IF NOT EXISTS idx_desempenho_questao_id_local ON desempenho(questao_id_local);
            
            -- Adicionar colunas faltantes na tabela plano_estudos
            ALTER TABLE plano_estudos ADD COLUMN IF NOT EXISTS id_local INTEGER;
            CREATE UNIQUE INDEX IF NOT EXISTS idx_plano_estudos_id_local ON plano_estudos(id_local);
            
            -- Adicionar colunas faltantes na tabela ia_feedback
            ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS id_local INTEGER;
            ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS questao_id_local INTEGER;
            CREATE UNIQUE INDEX IF NOT EXISTS idx_ia_feedback_id_local ON ia_feedback(id_local);
            CREATE INDEX IF NOT EXISTS idx_ia_feedback_questao_id_local ON ia_feedback(questao_id_local);
            
            -- Adicionar colunas de sincronizacao
            ALTER TABLE questoes ADD COLUMN IF NOT EXISTS data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE plano_estudos ADD COLUMN IF NOT EXISTS data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            
            -- Adicionar timestamps created_at e updated_at
            ALTER TABLE questoes ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE questoes ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE desempenho ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE plano_estudos ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE plano_estudos ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            ALTER TABLE ia_feedback ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW();
            """
            
            return {
                'status': 'info',
                'message': 'Tabelas precisam ser corrigidas manualmente',
                'sql': fix_tables_sql
            }
            
        except Exception as e:
            return {'status': 'erro', 'message': f'Erro ao gerar SQL de correção: {str(e)}'}
    
    def init_supabase_tables(self) -> Dict:
        """
        Cria as tabelas no Supabase se não existirem
        """
        try:
            # SQL para criar as tabelas
            create_tables_sql = """
            -- Criar tabela de questões se não existir
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
            
            -- Criar tabela de desempenho se não existir
            CREATE TABLE IF NOT EXISTS desempenho (
                id BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
                id_local INTEGER UNIQUE,
                questao_id_local INTEGER NOT NULL,
                resposta_usuario TEXT NOT NULL,
                acerto BOOLEAN NOT NULL,
                data_resposta TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                data_sincronizacao TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            
            -- Criar tabela de plano de estudos se não existir
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
            
            -- Criar tabela de ia_feedback se não existir
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
            """
            
            # Executar SQL via RPC (se disponível) ou retornar instruções
            return {
                'status': 'info',
                'message': 'Tabelas precisam ser criadas manualmente',
                'sql': create_tables_sql
            }
            
        except Exception as e:
            return {'status': 'erro', 'message': f'Erro ao criar tabelas: {str(e)}'}
    
    def test_connection(self) -> Dict:
        """
        Testa a conexão com o Supabase
        """
        try:
            # Tentar uma consulta simples
            result = self.client.table('questoes').select('count', count='exact').execute()
            return {
                'status': 'sucesso',
                'message': 'Conexão com Supabase estabelecida com sucesso',
                'count': result.count
            }
        except Exception as e:
            return {'status': 'erro', 'message': f'Erro na conexão com Supabase: {str(e)}'}

# Inicialização do serviço
try:
    supabase_service = SupabaseService()
except Exception as e:
    supabase_service = None
    print(f"Erro ao inicializar Supabase: {e}")
