# Usar imagem oficial Python
FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (para cache do Docker)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar arquivos da aplicação
COPY . .

# Criar diretório para o banco de dados
RUN mkdir -p /app/data

# Expor porta
EXPOSE 5000

# Variáveis de ambiente
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
ENV PORT=5000
ENV HOST=0.0.0.0

# Comando para iniciar
CMD ["python", "app.py"]
