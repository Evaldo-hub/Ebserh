# 🚀 Deploy do EBSERH TI Study App em Produção

## 📋 Visão Geral

Este guia explica como fazer o deploy do aplicativo EBSERH TI Study em produção usando Render.com com PostgreSQL.

## 🏗️ Arquitetura

- **Frontend**: HTML5, Bootstrap 5, JavaScript (PWA)
- **Backend**: Flask 3.0 com Python 3.11
- **Banco**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **Deploy**: Render.com
- **Cache**: Service Worker (PWA)

## 📁 Estrutura de Arquivos

```
APPEbserh/
├── app_production.py      # App Flask para produção
├── config.py              # Configurações de ambiente
├── database.py            # Gerenciamento de banco de dados
├── ia_service.py          # Serviço de IA
├── render.yaml            # Configuração do Render
├── requirements.txt       # Dependências Python
├── manifest.json          # PWA manifest
├── browserconfig.xml      # Configuração Windows
├── static/
│   ├── sw.js            # Service Worker
│   └── icons/           # Ícones PWA
├── templates/           # Templates Jinja2
└── .env.example         # Variáveis de ambiente
```

## 🔧 Configurações

### 1. Variáveis de Ambiente

Crie um arquivo `.env` baseado em `.env.example`:

```bash
cp .env.example .env
```

### 2. Banco de Dados

**Desenvolvimento (SQLite):**
```bash
DATABASE_PATH=ebserh_study.db
```

**Produção (PostgreSQL):**
```bash
DATABASE_URL=postgresql://usuario:senha@host:porta/database
```

## 🚀 Deploy no Render.com

### 1. Preparar o Repositório

```bash
# Adicionar arquivos ao Git
git add .
git commit -m "Preparar para deploy em produção"
git push origin main
```

### 2. Configurar no Render

1. **Conectar GitHub**: Conecte seu repositório ao Render
2. **Criar Web Service**: Use o arquivo `render.yaml`
3. **Criar PostgreSQL**: Banco de dados será criado automaticamente
4. **Configurar Variáveis**: Render preencherá automaticamente

### 3. Variáveis do Render

O Render criará automaticamente:
- `DATABASE_URL`: String de conexão PostgreSQL
- `RENDER_SERVICE_ID`: ID do serviço
- `RENDER_EXTERNAL_URL`: URL pública
- `PORT`: Porta do serviço (10000)

## 🔍 Verificação do Deploy

### 1. Health Check

Acesse: `https://seu-app.onrender.com/health`

Resposta esperada:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "version": "1.0.0"
}
```

### 2. Funcionalidades

Teste as funcionalidades:
- ✅ Página inicial carrega
- ✅ Questões funcionam
- ✅ Admin IA funciona
- ✅ PWA instalável
- ✅ Service Worker ativo

## 📊 Monitoramento

### Logs no Render

1. Acesse o dashboard do Render
2. Clique no serviço "ebserh-ti-study"
3. Vá para "Logs"
4. Monitore erros e performance

### Métricas Importantes

- **Response Time**: < 500ms
- **Uptime**: > 99%
- **Memory**: < 512MB (plano free)
- **Database**: < 90% CPU

## 🔄 Atualizações

### Deploy Automático

Com `autoDeploy: true` no `render.yaml`:

1. Faça push para GitHub
2. Render detecta mudanças
3. Build automático
4. Deploy sem downtime

### Deploy Manual

1. Vá para dashboard do Render
2. Clique "Manual Deploy"
3. Escolha branch/commit
4. Aguarde deploy

## 🛠️ Troubleshooting

### Erros Comuns

**1. Database Connection Error**
```bash
# Verificar DATABASE_URL
echo $DATABASE_URL
```

**2. Module Not Found**
```bash
# Verificar requirements.txt
pip install -r requirements.txt
```

**3. Permission Denied**
```bash
# Verificar permissões do arquivo
chmod +x app_production.py
```

**4. Service Worker Error**
- Limpar cache do navegador
- Verificar caminho do sw.js
- Testar em aba anônima

### Debug Mode

Para debug em produção:
```python
# No render.yaml, temporariamente:
envVars:
  - key: FLASK_ENV
    value: development
  - key: DEBUG
    value: "true"
```

## 📈 Performance

### Otimizações Implementadas

1. **Cache Estático**: 1 ano para assets
2. **Service Worker**: Cache inteligente
3. **Database**: Índices otimizados
4. **Compression**: Gzip no Render
5. **CDN**: Assets via CDN do Render

### Métricas de Performance

- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

## 🔐 Segurança

### Implementações

1. **HTTPS**: Automático no Render
2. **Headers**: Security headers configurados
3. **Session**: Cookies seguros
4. **SQL Injection**: Parâmetros protegidos
5. **XSS**: Templates escapados

### Variáveis Sensíveis

- ✅ `SECRET_KEY`: Gerada automaticamente
- ✅ `DATABASE_URL`: Apenas no Render
- ✅ Senhas: Nunca no código

## 📱 PWA em Produção

### Funcionalidades

- ✅ Instalação via banner
- ✅ Funciona offline parcialmente
- ✅ Ícone na tela inicial
- ✅ Sem barra de endereço
- ✅ Notificações push (pronto)

### Teste PWA

1. Acesse o app
2. Aguarde banner de instalação
3. Instale como app nativo
4. Teste funcionalidade offline

## 🎯 Escalabilidade

### Plano Free (Render)

- **Web Service**: 750 horas/mês
- **PostgreSQL**: 90% CPU, 256MB RAM
- **Bandwidth**: 100GB/mês
- **Builds**: 400/mês

### Upgrade para Plano Pago

Se necessário:
1. Vá para dashboard do Render
2. Clique no serviço
3. "Settings" → "Change Plan"
4. Escolha plano adequado

## 📞 Suporte

### Render Support

- **Email**: support@render.com
- **Docs**: render.com/docs
- **Status**: status.render.com

### Problemas Específicos

1. **Database**: Verificar logs do PostgreSQL
2. **Build**: Verificar logs de build
3. **Runtime**: Verificar logs do serviço
4. **PWA**: Testar em diferentes dispositivos

## 🔄 Backup

### Database Backup

Render faz backup automático do PostgreSQL:
- **Frequência**: Diário
- **Retenção**: 7 dias
- **Export**: Via dashboard

### Backup Manual

```sql
-- Exportar dados
pg_dump $DATABASE_URL > backup.sql

-- Importar dados
psql $DATABASE_URL < backup.sql
```

---

**Pronto! Seu app EBSERH TI Study está em produção! 🎉**

Para dúvidas, consulte os logs no dashboard do Render ou verifique a documentação oficial.
