"""
Serviço de IA para o EBSERH Study App
Regra de ouro: IA apoia o estudo, nunca responde prova ao vivo
"""

import json
import random
import re

class IAService:
    def __init__(self):
        self.version = "1.0.0"
        
        # Banco de conhecimento por disciplina e nível
        self.banco_conhecimento = {
            'Lei 12.550/2011': {
                'Básico': [
                    {
                        'enunciado': 'A EBSERH foi criada como empresa pública vinculada ao:',
                        'alternativas': {'A': 'Ministério da Saúde', 'B': 'Ministério da Educação', 'C': 'Ministério da Economia', 'D': 'Presidência da República'},
                        'resposta': 'A',
                        'comentario': 'Gabarito: A. A EBSERH é empresa pública vinculada ao Ministério da Saúde.'
                    },
                    {
                        'enunciado': 'Como deve ser composto o capital social da EBSERH segundo o Art. 2º da referida Lei?',
                        'alternativas': {
                            'A': 'Composto por 51% de capital público e 49% de capital privado.',
                            'B': 'Dividido entre a União, Estados e Municípios proporcionalmente ao atendimento.',
                            'C': 'Integralmente sob a propriedade da União.',
                            'D': 'Exclusivamente por meio de doações e legados de instituições de ensino.'
                        },
                        'resposta': 'C',
                        'comentario': 'Gabarito: C. A lei determina que a totalidade do capital social pertença à União, permitindo a integralização via orçamento ou bens avaliáveis em dinheiro.'
                    },
                    {
                        'enunciado': 'O objetivo principal da EBSERH é:',
                        'alternativas': {'A': 'Lucro', 'B': 'Prestar serviços de saúde', 'C': 'Educação', 'D': 'Pesquisa'},
                        'resposta': 'B',
                        'comentario': 'Gabarito: B. O objetivo é prestar serviços de saúde.'
                    }
                ],
                'Alto': [
                    {
                        'enunciado': 'A EBSERH pode contratar com entidades privadas sem licitação?',
                        'alternativas': {'A': 'Sim, sempre', 'B': 'Não, nunca', 'C': 'Apenas em casos específicos', 'D': 'Depende do valor'},
                        'resposta': 'C',
                        'comentario': 'Gabarito: C. Apenas em casos específicos previstos em lei.'
                    }
                ],
                'Pegadinha': [
                    {
                        'enunciado': 'Por ser empresa pública, a EBSERH segue integralmente o regime jurídico de direito público.',
                        'alternativas': {'A': 'Certo', 'B': 'Errado'},
                        'resposta': 'B',
                        'comentario': 'Gabarito: Errado. EBSERH tem personalidade jurídica de direito privado.'
                    }
                ]
            },
            'LGPD': {
                'Básico': [
                    {
                        'enunciado': 'LGPD significa:',
                        'alternativas': {'A': 'Lei Geral de Proteção de Dados', 'B': 'Lei de Gestão de Dados Pessoais', 'C': 'Lei de Garantia de Privacidade', 'D': 'Lei de Governança de Dados'},
                        'resposta': 'A',
                        'comentario': 'Gabarito: A. LGPD = Lei Geral de Proteção de Dados.'
                    }
                ],
                'Alto': [
                    {
                        'enunciado': 'O tratamento de dados na área da saúde:',
                        'alternativas': {'A': 'É sempre proibido', 'B': 'Pode ser feito sem base legal', 'C': 'Exige base legal específica', 'D': 'Não se aplica à LGPD'},
                        'resposta': 'C',
                        'comentario': 'Gabarito: C. Exige base legal específica mesmo na saúde.'
                    }
                ],
                'Pegadinha': [
                    {
                        'enunciado': 'Dados anonimizados não estão sujeitos à LGPD.',
                        'alternativas': {'A': 'Certo', 'B': 'Errado'},
                        'resposta': 'A',
                        'comentario': 'Gabarito: Certo. Dados anonimizados saem do escopo da LGPD.'
                    }
                ]
            },
            'Segurança da Informação': {
                'Básico': [
                    {
                        'enunciado': 'Os três pilares da segurança são:',
                        'alternativas': {'A': 'CIA', 'B': 'ABC', 'C': 'XYZ', 'D': '123'},
                        'resposta': 'A',
                        'comentario': 'Gabarito: A. CIA = Confidencialidade, Integridade, Disponibilidade.'
                    }
                ],
                'Alto': [
                    {
                        'enunciado': 'Criptografia protege principalmente qual pilar?',
                        'alternativas': {'A': 'Confidencialidade', 'B': 'Integridade', 'C': 'Disponibilidade', 'D': 'Todos'},
                        'resposta': 'A',
                        'comentario': 'Gabarito: A. Criptografia protege principalmente a confidencialidade.'
                    }
                ],
                'Pegadinha': [
                    {
                        'enunciado': 'Backup garante a confidencialidade dos dados.',
                        'alternativas': {'A': 'Certo', 'B': 'Errado'},
                        'resposta': 'B',
                        'comentario': 'Gabarito: Errado. Backup garante disponibilidade, não confidencialidade.'
                    }
                ]
            },
            'Scrum': {
                'Básico': [
                    {
                        'enunciado': 'Scrum é um framework para:',
                        'alternativas': {'A': 'Desenvolvimento de software', 'B': 'Gestão financeira', 'C': 'Marketing', 'D': 'Recursos humanos'},
                        'resposta': 'A',
                        'comentario': 'Gabarito: A. Scrum é para desenvolvimento de software.'
                    }
                ],
                'Alto': [
                    {
                        'enunciado': 'Qual evento do Scrum revisa o produto?',
                        'alternativas': {'A': 'Sprint Review', 'B': 'Daily Scrum', 'C': 'Sprint Retrospective', 'D': 'Sprint Planning'},
                        'resposta': 'A',
                        'comentario': 'Gabarito: A. Sprint Review revisa o produto.'
                    }
                ],
                'Pegadinha': [
                    {
                        'enunciado': 'No Scrum, o Product Owner pode alterar a Sprint durante sua execução.',
                        'alternativas': {'A': 'Certo', 'B': 'Errado'},
                        'resposta': 'B',
                        'comentario': 'Gabarito: Errado. Sprint não pode ser alterada após iniciada.'
                    }
                ]
            }
        }
        
    def explicar_erro(self, questao, resposta_usuario):
        """
        Gera explicação personalizada para erro do aluno
        Args:
            questao: dict com dados da questão
            resposta_usuario: resposta marcada pelo aluno
        Returns:
            str: explicação gerada pela IA
        """
        # Parse do comentário padrão (seguir estrutura)
        comentario = questao.get('comentario', '')
        
        prompt = f"""
        Questão:
        {questao.get('enunciado', '')}
        
        Alternativa marcada: {resposta_usuario}
        Gabarito: {questao.get('resposta_correta', '')}
        
        Comentário original:
        {comentario}
        
        Explique o erro de forma simples e objetiva, focando na dificuldade específica do aluno.
        Máximo 3 frases.
        """
        
        # Simulação - futura integração com API de IA
        explicacao = self._gerar_explicacao_simulada(prompt, questao, resposta_usuario)
        
        return explicacao
    
    def gerar_dica_memoria(self, questao):
        """
        Gera dica de memória personalizada
        Args:
            questao: dict com dados da questão
        Returns:
            str: dica gerada pela IA
        """
        # Gerar prompt para dica
        prompt = f"""
        Questão:
        {questao.get('enunciado', '')}
        
        Gabarito: {questao.get('resposta_correta', '')}
        
        Gere uma dica curta e memorável para ajudar o aluno a lembrar desta resposta.
        Máximo 1 frase. Use emojis se ajudar.
        """
        
        # Simulação - futura integração com API de IA
        dica = self._gerar_dica_simulada(prompt, questao.get('disciplina', ''))
        
        return dica
    
    def sugerir_revisao(self, erros_recentes):
        """
        Sugere plano de revisão baseado em erros
        Args:
            erros_recentes: list de questões erradas
        Returns:
            str: sugestão de revisão
        """
        if not erros_recentes:
            return "Continue estudando! Você está no caminho certo."
        
        # Contar erros por disciplina
        disciplinas_erradas = {}
        for erro in erros_recentes:
            disc = erro.get('disciplina', 'Geral')
            disciplinas_erradas[disc] = disciplinas_erradas.get(disc, 0) + 1
        
        # Encontrar disciplina crítica
        disciplina_critica = max(disciplinas_erradas, key=disciplinas_erradas.get)
        
        sugestao = f"""
        📊 ANÁLISE DE ERROS RECENTES:
        
        🎯 Disciplina com mais erros: {disciplina_critica} ({disciplinas_erradas[disciplina_critica]} erros)
        
        📚 PLANO DE REVISÃO SUGERIDO:
        1. Focar em {disciplina_critica} - revisar conceitos fundamentais
        2. Praticar questões específicas desta disciplina
        3. Revisar comentários das questões erradas
        
        📈 Próximo passo: Dominar {disciplina_critica} antes de avançar!
        """
    
    def gerar_questao_inedita(self, disciplina, nivel, quantidade=1):
        """
        Gera questões inéditas (função admin)
        Args:
            disciplina: str - disciplina da questão
            nivel: str - nível de dificuldade
            quantidade: int - quantidade de questões
        Returns:
            list: questões geradas
        """
        # Usar banco de conhecimento da instância
        if disciplina not in self.banco_conhecimento:
            return []
        
        if nivel not in self.banco_conhecimento[disciplina]:
            return []
        
        questoes_disponiveis = self.banco_conhecimento[disciplina][nivel]
        
        # Embaralhar e pegar quantidade solicitada
        random.shuffle(questoes_disponiveis)
        return questoes_disponiveis[:quantidade]
    
    def importar_questao_texto(self, texto_questao, disciplina='Lei 12.550/2011', nivel='Básico'):
        """
        Importa questão automaticamente a partir de texto colado
        Suporta múltiplos formatos de bancas:
        - CESPE: Certo/Errado
        - FCC/IBFC: A) B) C) D)
        - FGV: A. B. C. D.
        - Personalizados: vários formatos
        Args:
            texto_questao: str - texto completo da questão
            disciplina: str - disciplina da questão
            nivel: str - nível da questão
        Returns:
            dict: questão formatada ou None se erro
        """
        try:
            
            linhas = texto_questao.strip().split('\n')
            
            questao = {
                'enunciado': '',
                'alternativas': {},
                'resposta': '',
                'comentario': '',
                'tipo': 'multipla_escolha'  # padrão
            }
            
            # Detectar tipo de questão (Certo/Errado vs Múltipla Escolha)
            tem_certo_errado = any('certo' in linha.lower() or 'errado' in linha.lower() for linha in linhas)
            
            if tem_certo_errado:
                questao['tipo'] = 'certo_errado'
                return self._importar_certo_errado(linhas, questao, disciplina)
            
            # Parse múltipla escolha
            return self._importar_multipla_escolha(linhas, questao, disciplina)
            
        except Exception as e:
            return None
    
    def _importar_certo_errado(self, linhas, questao, disciplina):
        """Importa questões Certo/Errado (CESPE)"""
        # Encontrar enunciado
        for i, linha in enumerate(linhas):
            if '?' in linha or '.' in linha:
                questao['enunciado'] = linha.strip()
                # Procurar por Certo/Errado nas linhas seguintes
                for j in range(i+1, len(linhas)):
                    linha_atual = linhas[j].strip().lower()
                    if 'certo' in linha_atual and 'errado' in linha_atual:
                        # Formato: ( ) Certo ( ) Errado
                        questao['alternativas'] = {'A': 'Certo', 'B': 'Errado'}
                        # Detectar gabarito
                        if '( x )' in linhas[j] or '[x]' in linhas[j]:
                            questao['resposta'] = 'A' if 'certo' in linha_atual else 'B'
                        else:
                            # Procurar gabarito separado
                            for k in range(j+1, len(linhas)):
                                if 'gabarito' in linhas[k].lower():
                                    questao['resposta'] = 'A' if 'certo' in linhas[k].lower() else 'B'
                                    break
                        break
                break
        
        if not questao['enunciado'] or not questao['resposta']:
            return None
        
        questao['comentario'] = f"Gabarito: {questao['resposta']}. Questão CESPE sobre {disciplina}."
        return questao
    
    def _importar_multipla_escolha(self, linhas, questao, disciplina):
        """Importa questões de múltipla escolha (vários formatos)"""
        
        # Capturar enunciado completo (pode ter várias linhas)
        enunciado_linhas = []
        alternativa_inicio = None
        
        for i, linha in enumerate(linhas):
            linha_strip = linha.strip()
            
            if not linha_strip:
                continue
                
            # Verificar se é alternativa - se for, paramos de capturar o enunciado
            if (linha_strip.startswith(('A)', 'B)', 'C)', 'D)', 'A.', 'B.', 'C.', 'D.', '(A)', '(B)', '(C)', '(D)')) or
                'gabarito' in linha_strip.lower()):
                alternativa_inicio = i
                break
                
            # Se não for alternativa, é parte do enunciado
            enunciado_linhas.append(linha_strip)
        
        # Juntar todas as linhas do enunciado
        questao['enunciado'] = ' '.join(enunciado_linhas)
        
        # Processar as linhas a partir da primeira alternativa
        if alternativa_inicio is not None:
            for j in range(alternativa_inicio, len(linhas)):
                linha_atual = linhas[j].strip()
                if not linha_atual:
                    continue
                
                # Verificar se é alternativa
                alternativa_encontrada = False
                padroes = [
                    r'^([ABCD])\.\s*(.+)',      # A. texto
                    r'^([ABCD])\)\s*(.+)',      # A) texto
                    r'^([ABCD])\s+(.+)',        # A  texto
                    r'^\(([ABCD])\)\s*(.+)',    # (A) texto
                    r'^([ABCD])-\s*(.+)',       # A- texto
                ]
                
                for padrao in padroes:
                    match = re.match(padrao, linha_atual)
                    if match:
                        letra = match.group(1)
                        texto = match.group(2).strip()
                        questao['alternativas'][letra] = texto
                        alternativa_encontrada = True
                        break
                
                if alternativa_encontrada:
                    continue
                
                # Verificar gabarito
                if 'gabarito' in linha_atual.lower() or 'resposta' in linha_atual.lower():
                    for letra in 'ABCD':
                        if letra in linha_atual:
                            questao['resposta'] = letra
                            break
                
                # Verificar comentário
                elif 'coment' in linha_atual.lower() or 'justif' in linha_atual.lower():
                    questao['comentario'] = linha_atual
        
        # Validação
        if not questao['enunciado'] or len(questao['alternativas']) != 4 or not questao['resposta']:
            return None
        
        # Gerar comentário padrão
        if not questao['comentario']:
            questao['comentario'] = f"Gabarito: {questao['resposta']}. Questão sobre {disciplina}."
        
        return questao
    
    def detectar_formato_banca(self, texto):
        """
        Detecta o formato da banca com base no texto
        Returns:
            str: 'CESPE', 'FCC', 'IBFC', 'FGV', 'Desconhecido'
        """
        texto_lower = texto.lower()
        
        if 'certo' in texto_lower and 'errado' in texto_lower:
            return 'CESPE'
        elif any(padrao in texto for padrao in ['A)', 'B)', 'C)', 'D)']):
            return 'IBFC'
        elif any(padrao in texto for padrao in ['A.', 'B.', 'C.', 'D.']):
            return 'FGV'
        elif any(padrao in texto for padrao in ['(A)', '(B)', '(C)', '(D)']):
            return 'FCC'
        else:
            return 'Desconhecido'
    
    def adicionar_questao_banco(self, questao, disciplina, nivel):
        """
        Adiciona questão ao banco de conhecimento dinamicamente E no banco de dados SQLite
        Args:
            questao: dict - questão formatada
            disciplina: str - disciplina
            nivel: str - nível
        """
        # Adicionar ao banco de conhecimento em memória
        if disciplina not in self.banco_conhecimento:
            self.banco_conhecimento[disciplina] = {}
        
        if nivel not in self.banco_conhecimento[disciplina]:
            self.banco_conhecimento[disciplina][nivel] = []
        
        # Converter formato para o banco
        questao_formatada = {
            'enunciado': questao['enunciado'],
            'alternativas': questao['alternativas'],
            'resposta': questao['resposta'],
            'comentario': questao['comentario']
        }
        
        self.banco_conhecimento[disciplina][nivel].append(questao_formatada)
        
        # Salvar no banco de dados SQLite
        try:
            import sqlite3
            conn = sqlite3.connect('ebserh_study.db')
            cursor = conn.cursor()
            
            # Determinar a semana (última semana ou padrão)
            cursor.execute('SELECT MAX(semana) FROM questoes')
            max_semana = cursor.fetchone()[0] or 12
            
            # Inserir no banco de dados
            cursor.execute('''
                INSERT INTO questoes (
                    disciplina, semana, nivel, banca, enunciado, 
                    alternativas, resposta_correta, comentario
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                disciplina,
                max_semana,
                nivel,
                'Importada-IA',
                questao['enunciado'],
                json.dumps(questao['alternativas']),
                questao['resposta'],
                questao['comentario']
            ))
            
            conn.commit()
            conn.close()
            
            return True
            
        except Exception as e:
            return False

    def analisar_padroes_erro(self, historico_respostas):
        """
        Analisa padrões de erro para fornecer insights
        Args:
            historico_respostas: lista de respostas do usuário
        Returns:
            dict: análise dos padrões
        """
        if not historico_respostas:
            return {"status": "sem_dados"}
        
        # Implementação básica
        return {
            "total_erros": len(historico_respostas),
            "disciplinas_criticas": ["Lei 12.550/2011"],
            "sugestao": "Focar nos conceitos fundamentais"
        }

    def _gerar_explicacao_simulada(self, prompt, questao, resposta_usuario):
        """
        Simulação de geração de explicação (substituído por API real no futuro)
        """
        explicacoes = {
            'Lei 12.550/2011': f"Você confundiu administração direta com indireta. Lembre-se: empresas públicas sempre fazem parte da administração indireta, mesmo tendo personalidade de direito privado.",
            'LGPD': f"Dados sensíveis na saúde precisam de base legal específica. A exceção de saúde facilita, mas não elimina a necessidade de base legal conforme LGPD.",
            'Segurança da Informação': f"Você misturou os pilares da segurança. Disponibilidade = acesso quando necessário. Integridade = proteção contra alteração. São conceitos diferentes!",
            'Banco de Dados': f"Chave primária identifica registros na própria tabela. Chave estrangeira cria relacionamento com outra tabela. São funções distintas!",
            'Cloud Computing': f"No IaaS, o provedor só dá infraestrutura. Aplicações e sistema operacional são responsabilidade do cliente. Quanto mais 'S', menos você gerencia.",
            'ITIL': f"ITIL v4 não eliminou processos, apenas ampliou com práticas. Cuidado com termos absolutos como 'totalmente' em provas.",
            'Scrum': f"No Scrum, tempo da Sprint é fixo (time-box). O que varia é o escopo, nunca a duração. Tempo fixo, escopo flexível!"
        }
        
        disciplina = questao.get('disciplina', 'Geral')
        return explicacoes.get(disciplina, "Revise os conceitos fundamentais desta disciplina e preste atenção nos detalhes que a banca costuma explorar.")
    
    def _gerar_dica_simulada(self, prompt, disciplina):
        """
        Simulação de geração de dica (substituído por API real no futuro)
        """
        dicas = {
            'Lei 12.550/2011': "🏢 EBSERH = Empresa Pública = Administração Indireta",
            'LGPD': "🏥 Dados de saúde = sensíveis = SEMPRE precisam de base legal",
            'Segurança da Informação': "🔐 CIA: Confidencialidade (acesso), Integridade (alteração), Disponibilidade (tempo)",
            'Banco de Dados': "🔑 PK = identidade própria | FK = relacionamento externo",
            'Cloud Computing': "☁️ IaaS < PaaS < SaaS (quanto mais S, menos você gerencia)",
            'ITIL': "📚 ITIL v4 = processos + práticas + cadeia de valor",
            'Scrum': "⏱️ Sprint = tempo fixo | escopo flexível"
        }
        
        return dicas.get(disciplina, "💡 Estude o padrão de questões e as pegadinhas comuns")

# Instância global do serviço
ia_service = IAService()
