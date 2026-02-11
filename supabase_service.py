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
    
    def sync_all_to_supabase(self) -> Dict:
        """
        Sincroniza todos os dados (questões e desempenho) para o Supabase
        """
        resultado_questoes = self.sync_questoes_to_supabase()
        resultado_desempenho = self.sync_desempenho_to_supabase()
        
        return {
            'status': 'sucesso' if resultado_questoes['status'] == 'sucesso' and resultado_desempenho['status'] == 'sucesso' else 'parcial',
            'questoes': resultado_questoes,
            'desempenho': resultado_desempenho,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_supabase_stats(self) -> Dict:
        """
        Obtém estatísticas dos dados no Supabase
        """
        try:
            # Contar questões
            questoes_result = self.client.table('questoes').select('count', count='exact').execute()
            total_questoes = questoes_result.count if hasattr(questoes_result, 'count') else 0
            
            # Contar desempenho
            desempenho_result = self.client.table('desempenho').select('count', count='exact').execute()
            total_desempenho = desempenho_result.count if hasattr(desempenho_result, 'count') else 0
            
            # Obter últimas sincronizações
            ultimas_questoes = self.client.table('questoes').select('data_sincronizacao').order('data_sincronizacao', desc=True).limit(1).execute()
            ult_desempenho = self.client.table('desempenho').select('data_sincronizacao').order('data_sincronizacao', desc=True).limit(1).execute()
            
            return {
                'status': 'sucesso',
                'total_questoes': total_questoes,
                'total_desempenho': total_desempenho,
                'ultima_sinc_questoes': ultimas_questoes.data[0]['data_sincronizacao'] if ultimas_questoes.data else None,
                'ultima_sinc_desempenho': ult_desempenho.data[0]['data_sincronizacao'] if ult_desempenho.data else None
            }
            
        except Exception as e:
            return {'status': 'erro', 'message': f'Erro ao obter estatísticas: {str(e)}'}
    
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
                data_resposta TIMESTAMP WITH TIME ZONE,
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
                'questoes_no_supabase': result.count if hasattr(result, 'count') else 0
            }
        except Exception as e:
            return {
                'status': 'erro',
                'message': f'Erro na conexão com Supabase: {str(e)}'
            }

# Instância global do serviço
supabase_service = SupabaseService() if os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_KEY') else None
