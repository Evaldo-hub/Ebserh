# App de Estudos EBSERH TI

Sistema completo de estudos para concurso da EBSERH na área de Tecnologia da Informação.

## 🎯 Objetivo

Ajudar candidatos a se prepararem efetivamente para o concurso da EBSERH - TI através de um sistema organizado de questões comentadas e acompanhamento de desempenho.

## 🚀 Funcionalidades

### 📚 Plano de Estudos (12 Semanas)
- **Semana 1-4**: Fase inicial - Conceitos básicos
- **Semana 5-8**: Fase intermediária - Profundização  
- **Semana 9-12**: Fase final - Revisão e pegadinhas

### 📝 Sistema de Questões
- **🟢 Nível Básico**: Fixação de conceitos
- **🟡 Nível Alto**: Questões analíticas
- **🔴 Nível Pegadinha**: Armadilhas da banca

### 📊 Acompanhamento de Desempenho
- Estatísticas gerais e por disciplina
- Identificação de erros recorrentes
- Metas e recomendações personalizadas

### 🎯 Simulados Personalizados
- Configuração por disciplina e nível
- Feedback detalhado com comentários
- Análise de desempenho

## 🛠️ Tecnologias

- **Backend**: Flask (Python)
- **Banco de Dados**: SQLite
- **Frontend**: Bootstrap 5 + Jinja2
- **Interface**: Responsiva e moderna

## 📦 Instalação

1. Clone o repositório:
```bash
git clone <repositório>
cd APPEbserh
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Inicialize o banco de dados:
```bash
python populate_db.py
```

4. Execute a aplicação:
```bash
python app.py
```

5. Acesse no navegador: `http://localhost:5000`

## 📁 Estrutura do Projeto

```
APPEbserh/
├── app.py                 # Aplicação principal Flask
├── populate_db.py         # Script para popular o banco
├── requirements.txt       # Dependências Python
├── ebserh_study.db       # Banco de dados SQLite
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página inicial
│   ├── plano.html        # Plano de estudos
│   ├── questoes.html     # Lista de questões
│   ├── questao.html      # Detalhe da questão
│   ├── desempenho.html   # Desempenho do usuário
│   ├── simulado.html     # Configuração de simulado
│   ├── simulado_questao.html # Questão do simulado
│   └── resultado_simulado.html # Resultado do simulado
└── README.md             # Este arquivo
```

## 🎮 Como Usar

### 1. Página Inicial
- Acesse todas as funcionalidades principais
- Veja o guia de como começar

### 2. Plano de Estudos
- Siga as 12 semanas organizadas
- Clique em cada semana para ver as questões

### 3. Questões
- Filtre por disciplina, semana e nível
- Responda e veja comentários detalhados

### 4. Simulados
- Configure simulados personalizados
- Teste seu conhecimento em condições de prova

### 5. Desempenho
- Acompanhe sua evolução
- Identifique pontos a melhorar

## 💡 Dicas de Estudo

### Para Iniciantes
- Comece pelas questões básicas
- Siga o plano semanal
- Foque em entender os comentários

### Para Intermediários  
- Balance os níveis de dificuldade
- Faça simulados regulares
- Revise erros recorrentes

### Para Avançados
- Foque em pegadinhas
- Faça simulados completos
- Mantenha taxa de acerto ≥ 70%

## 📈 Metas de Desempenho

- **Questões Básicas**: ≥ 80% de acerto
- **Questões Altas**: ≥ 65% de acerto  
- **Pegadinhas**: ≥ 50% de acerto
- **Geral**: ≥ 70% de acerto

## 🔧 Personalização

### Adicionar Novas Questões

1. Edite `populate_db.py`
2. Adicione novas questões no formato:
```python
{
    'disciplina': 'Nome da Disciplina',
    'semana': 1,
    'nivel': 'Básico',  # ou 'Alto', 'Pegadinha'
    'banca': 'IBFC',    # ou 'CESPE', 'FGV'
    'enunciado': 'Texto da questão...',
    'alternativas': '{"A": "Alternativa A", "B": "Alternativa B", ...}',
    'resposta_correta': 'B',
    'comentario': 'Comentário detalhado...'
}
```

3. Execute `python populate_db.py`

### Modificar Plano de Estudos

1. Edite a lista `plano_estudos` em `populate_db.py`
2. Atualize o conteúdo das semanas
3. Execute `python populate_db.py`

## 🐛 Troubleshooting

### Problemas Comuns

**Banco de dados não encontrado**:
- Execute `python populate_db.py` para criar o banco

**Erro de importação**:
- Instale as dependências: `pip install -r requirements.txt`

**Porta já em uso**:
- Feche outras aplicações na porta 5000
- Ou modifique a porta no `app.py`

## 📞 Suporte

Para dúvidas ou sugestões:
- Abra uma issue no repositório
- Envie um e-mail para [seu-email]

## 📄 Licença

Este projeto está licenciado sob a MIT License.

---

**Foco na sua aprovação! 💪**
