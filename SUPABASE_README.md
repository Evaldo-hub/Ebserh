# Integração com Supabase - EBSERH Study App

## 📋 Visão Geral

Esta aplicação agora suporta sincronização de dados com o Supabase, permitindo:
- Backup automático das questões e desempenho
- Acesso aos dados de qualquer dispositivo
- Sincronização bidirecional
- Interface web para gerenciamento

## 🚀 Configuração Rápida

### 1. Criar Projeto Supabase

1. Acesse [https://supabase.com](https://supabase.com)
2. Crie uma conta ou faça login
3. Clique em "New Project"
4. Escolha uma organização e nomeie o projeto (ex: `ebserh-study`)
5. Aguarde a criação do projeto

### 2. Configurar Banco de Dados

1. No painel do Supabase, vá para **SQL Editor**
2. Clique em "New query"
3. Copie e cole o conteúdo do arquivo `supabase_schema.sql`
4. Execute o script para criar as tabelas

### 3. Obter Credenciais

1. No painel do Supabase, vá para **Settings** > **API**
2. Copie a **Project URL** (ex: `https://xxxxxxxx.supabase.co`)
3. Copie a **anon public** API Key
4. Abra o arquivo `.env` na raiz do projeto
5. Adicione as credenciais:

```bash
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-anon-aqui
```

### 4. Instalar Dependências

```bash
pip install supabase python-dotenv
```

### 5. Reiniciar Aplicação

```bash
python app.py
```

## 📁 Estrutura de Arquivos

```
├── supabase_service.py    # Serviço de sincronização
├── supabase_schema.sql    # Schema SQL para o Supabase
├── .env                  # Credenciais (não commitar)
├── requirements.txt        # Dependências atualizadas
└── templates/
    ├── supabase_index.html  # Interface de sincronização
    └── supabase_error.html  # Página de erro
```

## 🔧 Funcionalidades

### Interface Web

Acesse `http://127.0.0.1:5000/supabase` para:

- **Estatísticas**: Visualizar quantidade de dados sincronizados
- **Teste de Conexão**: Verificar comunicação com Supabase
- **Sincronização Manual**: Enviar dados para o Supabase
- **Logs**: Acompanhar operações realizadas

### Tipos de Sincronização

1. **Completa**: Questões + Desempenho
2. **Apenas Questões**: Apenas tabela `questoes`
3. **Apenas Desempenho**: Apenas tabela `desempenho`

### Mapeamento de Tabelas

| SQLite Local | Supabase | Observações |
|-------------|------------|-------------|
| `questoes` | `questoes` | Mantém `id_local` como referência |
| `desempenho` | `desempenho` | Mantém `id_local` e `questao_id_local` |

## 🔄 Como Funciona

### Sincronização Automática

- **Upsert**: Atualiza registros existentes ou insere novos
- **Timestamp**: Cada sincronização registra data/hora
- **Conflitos**: Dados locais prevalecem sobre dados do Supabase

### Fluxo de Dados

```
SQLite Local → Supabase Service → API Supabase → Banco Supabase
```

### Tratamento de Erros

- Erros são registrados nos logs da interface
- Sincronização continua para outros registros
- Falhas de conexão são exibidas claramente

## 🛠️ Comandos Úteis

### Testar Conexão
```bash
curl http://127.0.0.1:5000/supabase/test
```

### Sincronizar Tudo
```bash
curl -X POST http://127.0.0.1:5000/supabase/sync \
  -H "Content-Type: application/json" \
  -d '{"type": "all"}'
```

### Obter Estatísticas
```bash
curl http://127.0.0.1:5000/supabase/stats
```

## 🔒 Segurança

### Boas Práticas

1. **Nunca** commitar o arquivo `.env`
2. Use **Row Level Security (RLS)** para produção
3. Considere criar uma **Service Role Key** para operações de backend
4. Limite o acesso conforme necessário

### Variáveis de Ambiente

```bash
# Desenvolvimento
SUPABASE_URL=https://dev-project.supabase.co
SUPABASE_KEY=dev-anon-key

# Produção
SUPABASE_URL=https://prod-project.supabase.co
SUPABASE_KEY=prod-anon-key
```

## 🐛 Troubleshooting

### Erros Comuns

**"Supabase não configurado"**
- Verifique se as variáveis estão no `.env`
- Reinicie a aplicação após configurar

**"Erro na conexão"**
- Verifique a URL e a chave no `.env`
- Confirme se o projeto está ativo no Supabase

**"Tabela não existe"**
- Execute o `supabase_schema.sql` no painel SQL
- Verifique se não houve erros na execução

**"Permissão negada"**
- Verifique as políticas RLS no Supabase
- Confirme se a API Key tem permissões necessárias

### Logs de Depuração

Ative logs detalhados no `supabase_service.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Monitoramento

### Métricas Disponíveis

- Total de questões sincronizadas
- Total de registros de desempenho
- Data/hora da última sincronização
- Taxa de sucesso/erro

### Alertas

Considere configurar alertas no Supabase para:
- Falhas de conexão
- Uso elevado de API
- Erros de permissão

## 🚀 Próximos Passos

1. **Sincronização Automática**: Agendar sincronizações periódicas
2. **Modo Offline**: Funcionamento sem conexão com sincronização posterior
3. **Multiusuário**: Suporte a múltiplos usuários com autenticação
4. **Dashboard**: Analytics avançados dos dados

## 📞 Suporte

- **Documentação Supabase**: https://supabase.com/docs
- **Issues do Projeto**: Abrir issue no repositório
- **FAQ**: Verificar seção de troubleshooting acima
