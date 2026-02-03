#!/bin/bash

# Build script para Render.com
echo "🚀 Iniciando build do EBSERH TI Study App"

# Verificar Python version
echo "📋 Python version:"
python --version

# Verificar pip version
echo "📋 Pip version:"
pip --version

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Instalar dependências
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Verificar instalações críticas
echo "🔍 Verificando instalações:"
python -c "import flask; print('✅ Flask:', flask.__version__)"
python -c "import jinja2; print('✅ Jinja2:', jinja2.__version__)"
python -c "import psycopg2; print('✅ psycopg2: OK')"
python -c "import PIL; print('✅ Pillow: OK')"
python -c "import gunicorn; print('✅ Gunicorn: OK')"

# Inicializar banco de dados
echo "🗄️ Inicializando banco de dados..."
python -c "from database import init_db; init_db(); print('✅ Banco inicializado')"

# Verificar arquivos importantes
echo "📁 Verificando arquivos:"
ls -la templates/
ls -la static/
ls -la *.py *.json *.xml *.yaml 2>/dev/null || echo "Arquivos de configuração encontrados"

# Testar import do app
echo "🧪 Testando import do app:"
python -c "from app_production import app; print('✅ App importado com sucesso')"

echo "🎉 Build concluído com sucesso!"
