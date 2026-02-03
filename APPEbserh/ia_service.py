"""
Serviço de IA para o EBSERH Study App
Regra de ouro: IA apoia o estudo, nunca responde prova ao vivo
"""

import json
import random

class IAService:
    def __init__(self):
        self.version = "1.0.0"
        
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
        disciplina = questao.get('disciplina', '')
        nivel = questao.get('nivel', '')
        
        prompt = f"""
        Disciplina: {disciplina}
        Nível: {nivel}
        Tema: {questao.get('enunciado', '')[:100]}...
        
        Gere uma dica de memória curta e eficaz para esta questão.
        Máximo 1 frase.
        """
        
        return self._gerar_dica_simulada(prompt, disciplina)
    
    def sugerir_revisao(self, erros_recentes):
        """
        Sugere plano de revisão baseado em erros
        Args:
            erros_recentes: lista de questões erradas
        Returns:
            str: plano de revisão sugerido
        """
        if not erros_recentes:
            return "Continue estudando! Você está no caminho certo."
        
        # Analisa padrões de erro
        disciplinas_com_erro = {}
        for erro in erros_recentes:
            disc = erro.get('disciplina', '')
            if disc not in disciplinas_com_erro:
                disciplinas_com_erro[disc] = 0
            disciplinas_com_erro[disc] += 1
        
        # Gera sugestão
        disciplina_critica = max(disciplinas_com_erro, key=disciplinas_com_erro.get)
        
        return f"""
        📋 Plano de Revisão Sugerido:
        
        🔥 Prioridade: {disciplina_critica} ({disciplinas_com_erro[disciplina_critica]} erros)
        
        ✅ Ações recomendadas:
        • Revise os conceitos fundamentais
        • Faça 5 questões extras sobre o tema
        • Foque em entender as "pegadinhas"
        
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
        # Banco de conhecimento por disciplina e nível
        banco_conhecimento = {
            'Lei 12.550/2011': {
                'Básico': [
                    {
                        'enunciado': 'A EBSERH foi criada como empresa pública vinculada ao:',
                        'alternativas': {'A': 'Ministério da Saúde', 'B': 'Ministério da Educação', 'C': 'Ministério da Economia', 'D': 'Presidência da República'},
                        'resposta': 'A',
                        'comentario': 'Gabarito: A. A EBSERH é empresa pública vinculada ao Ministério da Saúde.'
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
                        'enunciado': 'O Product Owner é responsável por:',
                        'alternativas': {'A': 'Facilitar o processo', 'B': 'Maximizar valor do produto', 'C': 'Desenvolver código', 'D': 'Testar software'},
                        'resposta': 'B',
                        'comentario': 'Gabarito: B. PO maximiza valor do produto.'
                    }
                ],
                'Alto': [
                    {
                        'enunciado': 'O Daily Scrum deve ter duração máxima de:',
                        'alternativas': {'A': '15 minutos', 'B': '30 minutos', 'C': '1 hora', 'D': '2 horas'},
                        'resposta': 'A',
                        'comentario': 'Gabarito: A. Daily Scrum máximo 15 minutos.'
                    }
                ],
                'Pegadinha': [
                    {
                        'enunciado': 'O Scrum Master participa ativamente das decisões técnicas.',
                        'alternativas': {'A': 'Certo', 'B': 'Errado'},
                        'resposta': 'B',
                        'comentario': 'Gabarito: Errado. Scrum Master facilita, não decide tecnicamente.'
                    }
                ]
            }
        }
        
        # Para outras disciplinas, gera questões genéricas
        disciplinas_genericas = [
            'Estatuto Social', 'Agilidade', 'Banco de Dados', 'Redes', 'Gestão de TI',
            'Cloud Computing', 'Desenvolvimento Web', 'APIs', 'Testes de Software',
            'DevOps', 'Business Intelligence', 'Analytics', 'Governança de TI',
            'COBIT', 'ITIL', 'Service Desk', 'Projetos'
        ]
        
        questoes = []
        
        for i in range(quantidade):
            if disciplina in banco_conhecimento and nivel in banco_conhecimento[disciplina]:
                # Usa questões pré-definidas
                template = random.choice(banco_conhecimento[disciplina][nivel])
                questao = {
                    'disciplina': disciplina,
                    'semana': 12,  # Semana padrão para questões IA
                    'nivel': nivel,
                    'banca': 'IA-Gerada',
                    'enunciado': template['enunciado'],
                    'alternativas': json.dumps(template['alternativas']),
                    'resposta_correta': template['resposta'],
                    'comentario': template['comentario'],
                    'tags': f"IA-gerada,{disciplina.lower().replace(' ', '_')},{nivel.lower()}",
                    'dificuldade_num': 3 if nivel == 'Pegadinha' else 2 if nivel == 'Alto' else 1
                }
            else:
                # Gera questões genéricas para outras disciplinas
                questao = {
                    'disciplina': disciplina,
                    'semana': 12,
                    'nivel': nivel,
                    'banca': 'IA-Gerada',
                    'enunciado': f'Questão sobre {disciplina} - nível {nivel} - gerada pela IA #{i+1}',
                    'alternativas': json.dumps({
                        'A': f'Alternativa A sobre {disciplina}',
                        'B': f'Alternativa B sobre {disciplina}',
                        'C': f'Alternativa C sobre {disciplina}',
                        'D': f'Alternativa D sobre {disciplina}'
                    }),
                    'resposta_correta': 'B',
                    'comentario': f'Comentário gerado pela IA para questão de {disciplina} nível {nivel}',
                    'tags': f"IA-gerada,{disciplina.lower().replace(' ', '_')},{nivel.lower()}",
                    'dificuldade_num': 3 if nivel == 'Pegadinha' else 2 if nivel == 'Alto' else 1
                }
            
            questoes.append(questao)
        
        return questoes
    
    def _gerar_explicacao_simulada(self, prompt, questao, resposta_usuario):
        """
        Simulação de geração de explicação (substituído por API real no futuro)
        """
        disciplina = questao.get('disciplina', '')
        
        # Explicações simuladas baseadas na disciplina
        explicacoes = {
            'Lei 12.550/2011': f"Você confundiu administração direta com indireta. Lembre-se: empresas públicas sempre fazem parte da administração indireta, mesmo tendo personalidade de direito privado.",
            'LGPD': f"Dados sensíveis na saúde precisam de base legal específica. A exceção de saúde facilita, mas não elimina a necessidade de base legal conforme LGPD.",
            'Segurança da Informação': f"Você misturou os pilares da segurança. Disponibilidade = acesso quando necessário. Integridade = proteção contra alteração. São conceitos diferentes!",
            'Banco de Dados': f"Chave primária identifica registros na própria tabela. Chave estrangeira cria relacionamento com outra tabela. São funções distintas!",
            'Cloud Computing': f"No IaaS, o provedor só dá infraestrutura. Aplicações e sistema operacional são responsabilidade do cliente. Quanto mais 'S', menos você gerencia.",
            'ITIL': f"ITIL v4 não eliminou processos, apenas ampliou com práticas. Cuidado com termos absolutos como 'totalmente' em provas.",
            'Scrum': f"No Scrum, tempo da Sprint é fixo (time-box). O que varia é o escopo, nunca a duração. Tempo fixo, escopo flexível!"
        }
        
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
        
        analise = {
            "total_respostas": len(historico_respostas),
            "taxa_acerto": 0,
            "disciplinas_dificeis": [],
            "tipos_erro": [],
            "recomendacoes": []
        }
        
        # Calcular taxa de acerto
        acertos = sum(1 for r in historico_respostas if r.get('acerto', False))
        analise["taxa_acerto"] = (acertos / len(historico_respostas)) * 100
        
        # Identificar disciplinas difíceis
        erros_por_disciplina = {}
        for resposta in historico_respostas:
            if not resposta.get('acerto', False):
                disc = resposta.get('disciplina', 'Desconhecida')
                erros_por_disciplina[disc] = erros_por_disciplina.get(disc, 0) + 1
        
        if erros_por_disciplina:
            analise["disciplinas_dificeis"] = sorted(
                erros_por_disciplina.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:3]
        
        return analise

# Instância global do serviço
ia_service = IAService()
