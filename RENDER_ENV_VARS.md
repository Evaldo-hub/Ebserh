# 🔧 Variáveis de Ambiente no Render

## 📋 Configurar no Painel do Render

Acesse: https://dashboard.render.com/ → Seu Web Service → Environment

### 🔑 Variáveis Essenciais

Copie e cole cada variável individualmente:

```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=sua-chave-secreta-unica-aqui
PORT=5000
HOST=0.0.0.0
```

### 🗄️ Supabase Sync

```
SUPABASE_URL=https://xlqcjfcfbehcgkkpyrde.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRiLmhscWNqZmNmYmVoY2dra3B5cmRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY0NzI5MDAsImV4cCI6MjA1MjA0ODkwMH0.7wYkQhE5L3k8XqJ9X2mF4P6vR7sT1nW2pY3zK4V8c
```

### 🐘 PostgreSQL Supabase (Produção)

```
DB_HOST=aws-1-sa-east-1.pooler.supabase.com
DB_NAME=postgres
DB_USER=postgres.texwhpgiaazpyosctjia
DB_PASSWORD=@Neia171427
```

### 🌐 Opcional: Database URL

```
DATABASE_URL=postgresql://postgres.texwhpgiaazpyosctjia:@Neia171427@aws-1-sa-east-1.pooler.supabase.com:5432/postgres
```

## 🚀 Como Configurar Passo a Passo

### 1. Acessar Painel Render
1. Login em https://dashboard.render.com/
2. Clicar no seu Web Service
3. Ir para aba "Environment"

### 2. Adicionar Variáveis
1. Clicar "Add Environment Variable"
2. Colar cada variável acima
3. Clicar "Save"

### 3. Deploy Automático
1. Após salvar, Render faz deploy automático
2. Aguardar alguns minutos
3. Testar aplicação

## 🔍 Verificação

### Testar Conexão PostgreSQL
```bash
curl https://seu-app.onrender.com/health
```

### Testar Supabase Sync
```bash
curl https://seu-app.onrender.com/supabase/test
```

## ⚠️ Importante

### Segurança
- ✅ Nenhum segredo no código
- ✅ Variáveis criptografadas no Render
- ✅ Sem arquivos .env no repositório

### Funcionamento
- ✅ **Produção**: PostgreSQL Supabase
- ✅ **Desenvolvimento**: SQLite local
- ✅ **Detecção automática** via FLASK_ENV

### Persistência
- ✅ Dados permanentes no Supabase
- ✅ Backup automático via sync
- ✅ Acesso de qualquer lugar

## 🔄 Fluxo de Dados

```
Render (Produção)
    ↓
PostgreSQL Supabase
    ↓
Sync Service
    ↓
Supabase Storage (Backup)
```

## 📱 URLs Após Deploy

- **Aplicação**: https://ebserh-study.onrender.com
- **Health**: https://ebserh-study.onrender.com/health
- **Supabase**: https://ebserh-study.onrender.com/supabase

## 🎯 Pronto!

Após configurar as variáveis:
1. ✅ Deploy automático
2. ✅ Dados no PostgreSQL Supabase
3. ✅ Sync funcional
4. ✅ Aplicação em produção

**Sua aplicação estará 100% funcional em produção!** 🎉
