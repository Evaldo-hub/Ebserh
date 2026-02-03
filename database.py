"""
Database utilities para EBSERH TI Study App
Suporte para SQLite (desenvolvimento) e PostgreSQL (produção)
"""

import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from config import get_config

class DatabaseManager:
    """Gerenciador de banco de dados multi-plataforma"""
    
    def __init__(self):
        self.config = get_config()
        self.db_type = self._detect_db_type()
    
    def _detect_db_type(self):
        """Detecta tipo de banco baseado em configuração"""
        if hasattr(self.config, 'DATABASE_URL') and self.config.DATABASE_URL:
            return 'postgresql'
        return 'sqlite'
    
    def get_connection(self):
        """Retorna conexão com banco de dados"""
        if self.db_type == 'postgresql':
            return self._get_postgres_connection()
        else:
            return self._get_sqlite_connection()
    
    def _get_sqlite_connection(self):
        """Conexão SQLite para desenvolvimento"""
        db_path = getattr(self.config, 'DATABASE_PATH', 'ebserh_study.db')
        return sqlite3.connect(db_path, check_same_thread=False)
    
    def _get_postgres_connection(self):
        """Conexão PostgreSQL para produção"""
        database_url = self.config.DATABASE_URL
        
        if not database_url:
            raise ValueError("DATABASE_URL não configurado para PostgreSQL")
        
        return psycopg2.connect(database_url)
    
    @contextmanager
    def get_cursor(self, dict_cursor=False):
        """Context manager para cursor"""
        conn = self.get_connection()
        try:
            if self.db_type == 'postgresql':
                cursor_class = RealDictCursor if dict_cursor else None
                cursor = conn.cursor(cursor_factory=cursor_class)
            else:
                # SQLite usa row_factory para dict-like
                if dict_cursor:
                    conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
            
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()
            conn.close()
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=True):
        """Executa query e retorna resultados"""
        with self.get_cursor(dict_cursor=True) as cursor:
            cursor.execute(query, params or ())
            
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                return None
    
    def execute_update(self, query, params=None):
        """Executa query de atualização"""
        with self.get_cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.rowcount
    
    def init_database(self):
        """Inicializa banco de dados com tabelas"""
        
        # SQL para criar tabelas (compatível com ambos os bancos)
        tables_sql = """
        -- Tabela de questões
        CREATE TABLE IF NOT EXISTS questoes (
            id SERIAL PRIMARY KEY,
            disciplina TEXT NOT NULL,
            semana INTEGER NOT NULL,
            nivel TEXT NOT NULL CHECK (nivel IN ('Básico', 'Alto', 'Pegadinha')),
            banca TEXT NOT NULL,
            enunciado TEXT NOT NULL,
            alternativas TEXT NOT NULL,
            resposta_correta TEXT NOT NULL,
            comentario TEXT NOT NULL,
            tags TEXT,
            dificuldade_num INTEGER DEFAULT 1,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ia_generated BOOLEAN DEFAULT FALSE
        );

        -- Tabela de desempenho
        CREATE TABLE IF NOT EXISTS desempenho (
            id SERIAL PRIMARY KEY,
            questao_id INTEGER NOT NULL,
            resposta_usuario TEXT NOT NULL,
            acerto BOOLEAN NOT NULL,
            data_resposta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            usuario_id TEXT DEFAULT 'anonymous',
            FOREIGN KEY (questao_id) REFERENCES questoes (id)
        );

        -- Tabela do plano de estudos
        CREATE TABLE IF NOT EXISTS plano_estudos (
            id SERIAL PRIMARY KEY,
            semana INTEGER NOT NULL UNIQUE,
            conteudo TEXT NOT NULL,
            disciplinas TEXT NOT NULL,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Tabela de feedback IA
        CREATE TABLE IF NOT EXISTS ia_feedback (
            id SERIAL PRIMARY KEY,
            questao_id INTEGER NOT NULL,
            usuario_id TEXT DEFAULT 'anonymous',
            tipo TEXT NOT NULL,
            conteudo TEXT NOT NULL,
            utilidade INTEGER DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (questao_id) REFERENCES questoes (id)
        );

        -- Tabela de sessões (para PWA/sincronização)
        CREATE TABLE IF NOT EXISTS sessoes (
            id SERIAL PRIMARY KEY,
            usuario_id TEXT NOT NULL,
            device_info TEXT,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Índices para performance
        CREATE INDEX IF NOT EXISTS idx_questoes_disciplina ON questoes(disciplina);
        CREATE INDEX IF NOT EXISTS idx_questoes_nivel ON questoes(nivel);
        CREATE INDEX IF NOT EXISTS idx_desempenho_usuario ON desempenho(usuario_id);
        CREATE INDEX IF NOT EXISTS idx_desempenho_data ON desempenho(data_resposta);
        CREATE INDEX IF NOT EXISTS idx_ia_feedback_questao ON ia_feedback(questao_id);
        """
        
        # Executa criação das tabelas
        statements = [stmt.strip() for stmt in tables_sql.split(';') if stmt.strip()]
        
        for statement in statements:
            try:
                self.execute_update(statement)
            except Exception as e:
                print(f"Aviso ao executar statement: {e}")
                print(f"Statement: {statement[:100]}...")
    
    def get_database_info(self):
        """Retorna informações do banco de dados"""
        info = {
            'type': self.db_type,
            'tables': {},
            'total_records': 0
        }
        
        # Contagem de registros por tabela
        tables = ['questoes', 'desempenho', 'plano_estudos', 'ia_feedback', 'sessoes']
        
        for table in tables:
            try:
                result = self.execute_query(f"SELECT COUNT(*) as count FROM {table}")
                count = result[0]['count'] if result else 0
                info['tables'][table] = count
                info['total_records'] += count
            except Exception as e:
                info['tables'][table] = f"Erro: {e}"
        
        return info

# Instância global do gerenciador
db_manager = DatabaseManager()

# Funções de conveniência
def get_db_connection():
    """Retorna conexão com banco de dados"""
    return db_manager.get_connection()

def init_db():
    """Inicializa banco de dados"""
    db_manager.init_database()

def execute_query(query, params=None, fetch_one=False, fetch_all=True):
    """Executa query com tratamento de erro"""
    try:
        return db_manager.execute_query(query, params, fetch_one, fetch_all)
    except Exception as e:
        print(f"Erro na query: {e}")
        print(f"Query: {query}")
        raise

def execute_update(query, params=None):
    """Executa update com tratamento de erro"""
    try:
        return db_manager.execute_update(query, params)
    except Exception as e:
        print(f"Erro no update: {e}")
        print(f"Query: {query}")
        raise
