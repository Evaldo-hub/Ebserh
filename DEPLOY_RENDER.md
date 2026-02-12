# 🚀 Deploy no Render com GitHub + Supabase

## 📋 Pré-requisitos

1. **Conta no Render**: https://render.com/
2. **Conta no GitHub**: https://github.com/
3. **Projeto no Supabase**: Já configurado
4. **Repositório Git**: Projeto versionado

## 🔧 Configuração

### 1. Variáveis de Ambiente no Render

No painel do Render → Environment → Add Environment Variables:

```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=sua-chave-secreta-unica-aqui
SUPABASE_URL=https://db.xlqcjfcfbehcgkkpyrde.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRiLmhscWNqZmNmYmVoY2dra3B5cmRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY0NzI5MDAsImV4cCI6MjA1MjA0ODkwMH0.7wYkQhE5L3k8XqJ9X2mF4P6vR7sT1nW2pY3zK4V8c
PORT=5000
```

### 2. Deploy Automático

#### Opção A: Via GitHub (Recomendado)

1. **Fazer push do código**:
   ```bash
   git add .
   git commit -m "Deploy para produção"
   git push origin main
   ```

2. **Conectar no Render**:
   - New → Web Service → Connect GitHub
   - Selecionar repositório
   - Branch: `main`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`

3. **Configurar Health Check**:
   - Health Check Path: `/health`

#### Opção B: Via Render.yaml

1. **Copiar render.yaml** para raiz do projeto
2. **Fazer push** com o arquivo
3. **Render detecta automaticamente** a configuração

### 3. Banco de Dados

#### Opção 1: SQLite (Padrão)
- Arquivo `ebserh_study.db` fica no servidor
- Persistência limitada no plano free
- Ideal para testes

#### Opção 2: PostgreSQL Supabase
- Descomentar linha no `.env`:
  ```
  DATABASE_URL=postgresql://postgres:F2KEWjp8edVUL9ML@db.xlqcjfcfbehcgkkpyrde.supabase.co:5432/postgres
  ```
- Modificar `app.py` para usar PostgreSQL

## 🌐 Acesso Após Deploy

Após deploy, sua aplicação estará em:
```
https://ebserh-study.onrender.com
```

## 🔍 Verificação

### Health Check
```bash
curl https://ebserh-study.onrender.com/health
```

### Supabase Connection
```bash
curl https://ebserh-study.onrender.com/supabase/test
```

## 📁 Estrutura de Arquivos para Deploy

```
APPEbserh/
├── app.py                 # Aplicação principal
├── requirements.txt        # Dependências Python
├── .env.production       # Variáveis produção (não commitar)
├── render.yaml          # Configuração Render
├── Dockerfile           # Container Docker
├── templates/          # Templates HTML
├── static/            # Arquivos estáticos
├── ebserh_study.db    # Banco SQLite (será criado)
└── supabase_service.py # Serviço Supabase
```

## ⚠️ Importante

### Segurança
- **NUNCA** commitar chaves secretas
- Usar variáveis de ambiente sempre
- `.env.production` no `.gitignore`

### Performance
- Plano free do Render tem limites
- Aplicação dorme após 15min inatividade
- Primeiro acesso pode ser lento

### Persistência
- SQLite no plano free **não é persistente**
- Para dados permanentes, usar PostgreSQL
- Supabase já garante persistência

## 🔄 Deploy Contínuo

### Atualizações Automáticas
1. Fazer mudanças no código
2. Commit e push para GitHub
3. Render detecta e faz deploy automático

### Rollback
1. No Render → Deployments
2. Selecionar deploy anterior
3. Click "Redeploy"

## 📊 Monitoramento

### Logs
- Render → Logs → Web Service
- Ver erros de conexão Supabase
- Monitorar performance

### Métricas
- Render → Metrics
- Acessos, response time
- Uso de recursos

## 🆘 Suporte

### Problemas Comuns

**Erro 502: Service Unavailable**
- Verificar health check
- Logs de erro no Render
- Variáveis de ambiente

**Conexão Supabase Falha**
- Verificar SUPABASE_URL e SUPABASE_KEY
- Testar com `/supabase/test`
- Logs de autenticação

**Deploy Falha**
- Verificar requirements.txt
- Build command correto
- Start command válido

### Contato
- Render Dashboard: https://dashboard.render.com/
- Supabase Dashboard: https://app.supabase.com/
- GitHub Repository: https://github.com/usuario/repo
