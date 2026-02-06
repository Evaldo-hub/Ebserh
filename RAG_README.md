# RAG - Retrieval-Augmented Generation

Nova funcionalidade do EBSERH Study que permite upload de PDFs, geração automática de questões e chat inteligente com base no conteúdo dos documentos.

## 🏗️ Arquitetura

O fluxo ideal é esse aqui:

1. **Upload do PDF** → Você envia um arquivo PDF
2. **Extração de Texto** → O backend extrai o texto do PDF
3. **Divisão em Chunks** → O texto é dividido em pedaços menores
4. **Embeddings** → Cria representações vetoriais com API da OpenAI
5. **Armazenamento** → Salva embeddings no banco vetorial (FAISS)
6. **Busca & Geração** → Quando você pergunta, busca os trechos mais relevantes e envia para o Chat

## 📋 Funcionalidades

### 1. Upload de Documentos
- Interface drag-and-drop para upload de PDFs
- Processamento automático do conteúdo
- Extração de texto e metadados
- Criação de embeddings

### 2. Chat Inteligente
- Faça perguntas sobre o conteúdo dos documentos
- Busca semântica nos chunks relevantes
- Respostas baseadas APENAS no conteúdo dos documentos
- Citação das fontes (páginas)

### 3. Geração de Questões
- Geração automática de questões de múltipla escolha
- Baseadas no conteúdo real dos documentos
- Configuração de dificuldade e quantidade
- Explicações para cada questão

## 🔧 Configuração

### Variáveis de Ambiente
Configure no arquivo `.env`:

```bash
OPENAI_API_KEY=sua_openai_api_key_aqui
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=text-embedding-3-small
CHAT_MODEL=gpt-4o-mini
```

### Dependências
As seguintes bibliotecas foram adicionadas:

```bash
pip install openai faiss-cpu pypdf2 python-dotenv tiktoken
```

## 📁 Estrutura de Arquivos

### Novos Arquivos
- `rag_service.py` - Serviço principal de RAG
- `.env` - Configurações de ambiente
- `templates/rag_index.html` - Página principal
- `templates/rag_documents.html` - Lista de documentos
- `templates/rag_chat.html` - Interface de chat
- `templates/rag_questions.html` - Questões geradas

### Modificações
- `app.py` - Adicionadas rotas RAG
- `requirements.txt` - Novas dependências

## 🗄️ Banco de Dados

### Novas Tabelas
- `pdf_documents` - Metadados dos PDFs
- `pdf_chunks` - Trechos de texto com embeddings
- `rag_questions` - Questões geradas por RAG

### Armazenamento
- `pdfs/` - Diretório para PDFs temporários
- `embeddings/` - Índices FAISS

## 🚀 Como Usar

### 1. Configurar API Key
Edite o arquivo `.env` e adicione sua API key da OpenAI:
```bash
OPENAI_API_KEY=sk-sua-key-aqui
```

### 2. Iniciar o Aplicativo
```bash
python app.py
```

### 3. Acessar o RAG
Abra `http://localhost:5000/rag` no navegador

## 📱 Fluxo de Uso

### Upload de Documento
1. Acesse `/rag`
2. Arraste um PDF ou clique para selecionar
3. Aguarde o processamento
4. O documento estará disponível em `/rag/documents`

### Chat com Documentos
1. Acesse `/rag/chat`
2. Selecione um documento (opcional)
3. Faça perguntas sobre o conteúdo
4. Receba respostas com fontes

### Gerar Questões
1. Acesse `/rag/documents`
2. Clique em "Gerar Questões"
3. Configure quantidade e dificuldade
4. Aguarde a geração
5. Visualize em `/rag/questions/{document_id}`

## 🔍 Busca Semântica

O sistema usa:
- **Embeddings**: Representações vetoriais do texto
- **FAISS**: Banco vetorial para busca eficiente
- **Similaridade**: Encontra trechos mais relevantes
- **Contexto**: Fornece contexto para a IA

## 🎯 Benefícios

### Para o Usuário
- **Aprendizado Personalizado**: Estude com base em seus materiais
- **Questões Reais**: Baseadas no conteúdo real
- **Chat Inteligente**: Tire dúvidas sobre o material
- **Fontes Confiáveis**: Respostas baseadas nos documentos

### Para o Sistema
- **Escalável**: Processa múltiplos documentos
- **Eficiente**: Busca rápida com embeddings
- **Modular**: Arquitetura bem organizada
- **Extensível**: Fácil adicionar novas funcionalidades

## 🛠️ Detalhes Técnicos

### Chunking
- **Tamanho**: 1000 tokens por chunk
- **Sobreposição**: 200 tokens entre chunks
- **Divisão Inteligente**: Corta em pontos finais

### Embeddings
- **Modelo**: `text-embedding-3-small`
- **Dimensão**: 1536 dimensões
- **Armazenamento**: Índices FAISS

### Models OpenAI
- **Embeddings**: `text-embedding-3-small`
- **Chat**: `gpt-4o-mini`
- **Geração de Questões**: `gpt-4o-mini`

## 🔮 Próximos Passos

### Melhorias Planejadas
- [ ] Suporte para outros formatos (DOCX, TXT)
- [ ] Interface de administração de documentos
- [ ] Exportação de questões em diferentes formatos
- [ ] Sistema de avaliação de qualidade das questões
- [ ] Integração com plano de estudos
- [ ] Análise de desempenho no conteúdo RAG

### Otimizações
- [ ] Cache de embeddings
- [ ] Processamento assíncrono
- [ ] Interface de upload em lote
- [ ] Busca híbrida (semântica + keyword)

## 🐛 Troubleshooting

### Problemas Comuns

**API Key Inválida**
- Verifique se a API key está correta no `.env`
- Confirme se tem créditos disponíveis

**Erro no Upload**
- Verifique se o PDF tem texto extraível
- Confirme se o arquivo não está corrompido

**Respostas Vazias**
- Verifique se o documento foi processado
- Tente fazer perguntas mais específicas

**Lentidão**
- O primeiro processamento pode ser demorado
- Os próximos são mais rápidos (embeddings em cache)

## 📞 Suporte

Caso encontre problemas:
1. Verifique os logs do console
2. Confirme as configurações no `.env`
3. Teste com um PDF simples primeiro
4. Verifique o consumo da API OpenAI

---

**Desenvolvido com ❤️ para a equipe EBSERH Study**
