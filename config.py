import os
from datetime import timedelta

class Config:
    """Configurações base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ebserh-ti-study-production-key-2024'
    
    # Configurações de sessão
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # Configurações PWA
    PWA_ENABLED = True
    
    # Configurações de cache
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300

class DevelopmentConfig(Config):
    """Configurações de desenvolvimento"""
    DEBUG = True
    TESTING = False
    
    # SQLite para desenvolvimento
    DATABASE_PATH = 'ebserh_study.db'
    
    # Logging detalhado
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configurações de produção"""
    DEBUG = False
    TESTING = False
    
    # PostgreSQL para produção
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Segurança
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Logging de produção
    LOG_LEVEL = 'INFO'
    
    # Performance
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 ano cache estático

class RenderConfig(ProductionConfig):
    """Configurações específicas para Render.com"""
    
    # Render já fornece SSL
    PREFERRED_URL_SCHEME = 'https'
    
    # Configurações de banco PostgreSQL do Render
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    # Configurações de performance para Render
    WEB_CONCURRENCY = int(os.environ.get('WEB_CONCURRENCY', '1'))
    
    # Timeout para Render
    TIMEOUT = int(os.environ.get('TIMEOUT', '30'))

# Configuração baseada em variável de ambiente
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'render': RenderConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Retorna configuração baseada em ambiente"""
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Detecta automaticamente se está no Render
    if os.environ.get('RENDER_SERVICE_ID'):
        env = 'render'
    
    return config.get(env, config['default'])
