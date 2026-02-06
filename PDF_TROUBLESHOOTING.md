# 📄 Guia de Solução de Problemas com PDFs

## ❌ Erro: "PDF não contém texto extraível"

Este erro ocorre quando o sistema RAG não consegue extrair texto suficiente do PDF para processamento.

## 🔍 Causas Comuns

### 1. **PDF Scaneado (Baseado em Imagens)**
- **Sintoma**: PDF parece normal mas não tem texto selecionável
- **Causa**: O PDF foi criado escaneando documentos físicos
- **Solução**: Usar OCR (Reconhecimento Óptico de Caracteres)

### 2. **PDF Protegido por Senha**
- **Sintoma**: PDF pede senha para abrir
- **Causa**: Restrições de segurança no documento
- **Solução**: Remover a proteção

### 3. **PDF com Fontes Não Padronizadas**
- **Sintoma**: PDF tem texto mas não é extraível
- **Causa**: Fontes customizadas ou vetoriais
- **Solução**: Converter para PDF padrão

### 4. **PDF Corrompido**
- **Sintoma**: Erro ao abrir o arquivo
- **Causa**: Download incompleto ou danificado
- **Solução**: Baixar novamente o arquivo

## 🛠️ Ferramentas de Diagnóstico

### 1. Usar nossa Ferramenta de Diagnóstico
```bash
python pdf_diagnostic.py caminho/do/seu/pdf.pdf
```

### 2. Verificação Manual
1. Abra o PDF em um visualizador
2. Tente selecionar o texto com o mouse
3. Se não conseguir selecionar → PDF é baseado em imagem
4. Se conseguir mas o sistema não extrair → problema técnico

## 💡 Soluções Práticas

### Opção 1: PDF com Texto Digital (Recomendado)
- ✅ Melhor qualidade
- ✅ Processamento rápido
- ✅ Resultados precisos

**Como conseguir:**
- Procure versões digitais dos documentos
- Use "Salvar como texto" do PDF original
- Exporte de editores de texto para PDF

### Opção 2: OCR para PDFs Scaneados
- ⚠️ Qualidade depende da imagem
- ⚠️ Pode ter erros de reconhecimento
- ⚠️ Processamento mais lento

**Ferramentas de OCR:**
- **Online**: OCR.space, OnlineOCR, i2OCR
- **Desktop**: Adobe Acrobat Pro, ABBYY FineReader
- **Gratuito**: Tesseract (com interface)

### Opção 3: Conversão Online
Use serviços como:
- Smallpdf.com
- ILovePDF.com
- PDF2Go.com

## 📋 Checklist Antes de Fazer Upload

### ✅ Verificação Rápida
- [ ] PDF abre sem erros
- [ ] Texto é selecionável
- [ ] PDF não pede senha
- [ ] Tamanho do arquivo < 50MB
- [ ] Nome do arquivo sem caracteres especiais

### 🧪 Teste de Extração
1. Copie um parágrafo do PDF
2. Cole em um editor de texto
3. Se o texto colar corretamente → PDF está OK

## 🚀 Como Usar o Sistema RAG

### Passo 1: Diagnóstico
```bash
# Verificar o PDF antes de fazer upload
python pdf_diagnostic.py meu_documento.pdf
```

### Passo 2: Upload Correto
1. Use apenas PDFs com texto digital
2. Evite PDFs scaneados
3. Verifique o tamanho do arquivo

### Passo 3: Processamento
1. Faça upload pela interface web
2. Aguarde o processamento
3. Verifique se apareceu em "Meus Documentos"

## 🔧 Configurações Avançadas

### Ajustar Sensibilidade
Edite `rag_service.py`:
```python
# Reduzir exigência mínima de texto
if len(clean_text) > 20:  # Era 50
```

### Adicionar Timeout
```python
# Para PDFs grandes
import signal
def timeout_handler(signum, frame):
    raise TimeoutError("Processamento demorou demais")
```

## 📞 Se o Problema Persistir

### 1. Informações para Suporte
- Tipo do PDF (digital/scaneado)
- Tamanho do arquivo
- Mensagem de erro completa
- Resultado do diagnóstico

### 2. Teste com PDF Simples
Crie um PDF de teste:
```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

c = canvas.Canvas("teste.pdf")
c.drawString(100, 750, "Este é um PDF de teste com texto extraível.")
c.save()
```

## 🎯 Dicas Profissionais

### Qualidade do PDF
- Use fontes padronizadas (Arial, Times New Roman)
- Evite imagens com texto
- Comprima imagens sem perder qualidade
- Teste em diferentes visualizadores

### OCR de Alta Qualidade
- Use resolução mínima de 300 DPI
- Ajuste contraste e brilho
- Limpe a imagem antes do OCR
- Revise o resultado manualmente

---

**Lembre-se**: O sistema RAG funciona melhor com PDFs de texto digital de alta qualidade! 📚✨
