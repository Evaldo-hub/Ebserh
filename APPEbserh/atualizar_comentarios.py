import sqlite3
import json

DB_NAME = 'ebserh_study.db'

def atualizar_comentarios_padrao_ouro():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Buscar todas as questões
    cursor.execute('SELECT id, disciplina, enunciado, comentario FROM questoes WHERE nivel = "Pegadinha"')
    questoes = cursor.fetchall()
    
    # Mapeamento de comentários para o padrão ouro
    novos_comentarios = {
        # Lei 12.550/2011
        'A EBSERH, apesar de possuir personalidade jurídica de direito privado, integra a administração direta.': 
            'Gabarito: Errado.\nConceito correto: A EBSERH é uma empresa pública federal, com personalidade jurídica de direito privado, integrante da administração indireta.\nA banca tenta confundir "direito privado" com "administração direta", o que está errado.\n⚠️ Dica de prova: Administração direta = União, Estados, DF e Municípios. Empresas públicas sempre são indiretas.',
            
        # Estatuto Social
        'O Estatuto Social da EBSERH pode contrariar disposições previstas em lei federal.':
            'Gabarito: Errado.\nConceito correto: Estatuto Social é norma interna e deve obedecer à legislação federal, jamais contrariá-la.\nA banca tenta confundir autonomia estatutária com supremacia sobre a lei.\n⚠️ Dica de prova: Hierarquia das normas: Constituição > Leis > Estatuto/Regulamento.',
            
        # LGPD
        'O tratamento de dados pessoais sensíveis pode ocorrer sem base legal, desde que para fins de saúde.':
            'Gabarito: Errado.\nConceito correto: Mesmo na saúde, o tratamento de dados sensíveis exige base legal específica prevista na LGPD.\nA banca tenta confundir finalidade de saúde com ausência de exigência legal.\n⚠️ Dica de prova: Dados sensíveis SEMPRE precisam de base legal, mesmo em saúde.',
            
        # Segurança da Informação
        'Disponibilidade garante que a informação não seja alterada indevidamente.':
            'Gabarito: Errado.\nConceito correto: Alteração indevida é tratada pela integridade. Disponibilidade garante acesso quando necessário.\nA banca tenta confundir disponibilidade com integridade.\n⚠️ Dica de prova: CIA = Confidencialidade, Integridade, Disponibilidade.',
            
        # Agilidade
        'No Scrum, o Scrum Master é o responsável final pela entrega do produto.':
            'Gabarito: Errado.\nConceito correto: A responsabilidade pelo valor do produto é do Product Owner; o Scrum Master atua como facilitador.\nA banca tenta confundir liderança técnica com responsabilidade pelo produto.\n⚠️ Dica de prova: PO = valor do produto; SM = processo; Time = execução.',
            
        # Banco de Dados
        'A chave estrangeira identifica unicamente os registros da própria tabela.':
            'Gabarito: Errado.\nConceito correto: Chave estrangeira referencia chave primária de outra tabela; quem identifica registros é a chave primária.\nA banca tenta confundir função da chave estrangeira com da chave primária.\n⚠️ Dica de prova: PK = identificação própria; FK = relacionamento com outra tabela.',
            
        # Redes
        'O protocolo UDP garante entrega confiável e ordenada dos pacotes.':
            'Gabarito: Errado.\nConceito correto: UDP não garante entrega, ordem ou controle de erros. Essas são características do TCP.\nA banca tenta confundir características do TCP com UDP.\n⚠️ Dica de prova: TCP = confiável; UDP = rápido (sem garantias).',
            
        # Gestão de TI
        'Gestão de TI e Governança de TI possuem exatamente os mesmos objetivos.':
            'Gabarito: Errado.\nConceito correto: Governança direciona e controla; gestão executa. São complementares, mas não iguais.\nA banca tenta confundir governança com gestão.\n⚠️ Dica de prova: Governança = o que fazer; Gestão = como fazer.',
            
        # Cloud Computing
        'No modelo IaaS, o provedor é responsável pelas aplicações do cliente.':
            'Gabarito: Errado.\nConceito correto: Em IaaS, o cliente gerencia sistema operacional e aplicações.\nA banca tenta confundir responsabilidade do cliente com do provedor.\n⚠️ Dica de prova: IaaS = cliente gerencia tudo acima da infraestrutura.',
            
        # Desenvolvimento Web
        'HTML é responsável pela estilização visual das páginas web.':
            'Gabarito: Errado.\nConceito correto: HTML estrutura conteúdo; CSS é responsável pela estilização.\nA banca tenta confundir função do HTML com do CSS.\n⚠️ Dica de prova: HTML = estrutura; CSS = aparência; JS = interação.',
            
        # APIs
        'O método HTTP POST é idempotente.':
            'Gabarito: Errado.\nConceito correto: POST não é idempotente; múltiplas requisições podem gerar efeitos diferentes.\nA banca tenta confundir POST com PUT (que é idempotente).\n⚠️ Dica de prova: GET e PUT são idempotentes; POST não é.',
            
        # Testes de Software
        'Testes de regressão são realizados apenas após a entrega do sistema.':
            'Gabarito: Errado.\nConceito correto: Testes de regressão ocorrem sempre que há mudanças no sistema.\nA banca tenta confundir momento dos testes com fase do projeto.\n⚠️ Dica de prova: Regressão = sempre que mudar algo.',
            
        # DevOps
        'DevOps elimina completamente a necessidade de testes de software.':
            'Gabarito: Errado.\nConceito correto: DevOps integra e automatiza testes, não os elimina.\nA banca tenta confundir automação com eliminação.\n⚠️ Dica de prova: DevOps = mais testes, mais rápidos, mais automatizados.',
            
        # Business Intelligence
        'Business Intelligence é utilizado exclusivamente para decisões operacionais.':
            'Gabarito: Errado.\nConceito correto: BI apoia decisões estratégicas, táticas e operacionais.\nA banca tenta limitar o escopo do BI apenas ao operacional.\n⚠️ Dica de prova: BI = todas as decisões, do estratégico ao operacional.',
            
        # Analytics
        'Analytics descritivo tem como foco prever cenários futuros.':
            'Gabarito: Errado.\nConceito correto: Previsão é função do analytics preditivo; o descritivo analisa o passado.\nA banca tenta confundir analytics descritivo com preditivo.\n⚠️ Dica de prova: Descritivo = o que aconteceu; Preditivo = o que acontecerá.',
            
        # Governança de TI
        'A governança de TI é responsabilidade exclusiva da área técnica.':
            'Gabarito: Errado.\nConceito correto: Governança é responsabilidade da alta administração.\nA banca tenta confundir governança com gestão técnica.\n⚠️ Dica de prova: Governança = diretores; Gestão = técnicos.',
            
        # COBIT
        'COBIT é um framework voltado apenas para auditoria de TI.':
            'Gabarito: Errado.\nConceito correto: COBIT trata de governança e gestão, não apenas auditoria.\nA banca tenta limitar o COBIT apenas à auditoria.\n⚠️ Dica de prova: COBIT = governança + gestão + auditoria.',
            
        # ITIL
        'ITIL v4 substituiu totalmente os processos pelas práticas.':
            'Gabarito: Errado.\nConceito correto: ITIL v4 amplia o conceito, mas não elimina processos.\nA banca tenta confundir evolução com substituição total.\n⚠️ Dica de prova: ITIL v4 = processos + práticas + cadeia de valor.',
            
        # Service Desk
        'Service Desk e Central de Serviços são conceitos distintos.':
            'Gabarito: Errado.\nConceito correto: São termos equivalentes dentro do ITIL.\nA banca tenta criar distinção inexistente.\n⚠️ Dica de prova: Service Desk = Central de Serviços (mesma coisa).',
            
        # Projetos
        'Projetos possuem natureza contínua e repetitiva.':
            'Gabarito: Errado.\nConceito correto: Projetos são temporários e produzem resultados únicos.\nA banca tenta confundir projetos com operações.\n⚠️ Dica de prova: Projeto = temporário + único; Operação = contínua + repetitiva.',
            
        # Scrum
        'A Sprint possui duração variável conforme o andamento do projeto.':
            'Gabarito: Errado.\nConceito correto: Sprints têm duração fixa (time-box).\nA banca tenta confundir flexibilidade com variação de tempo.\n⚠️ Dica de prova: Sprint = time-box fixo (geralmente 2-4 semanas).'
    }
    
    # Atualizar comentários
    atualizados = 0
    for questao in questoes:
        id_questao, disciplina, enunciado, comentario_atual = questao
        
        # Encontrar o comentário correspondente
        for enunciado_chave, novo_comentario in novos_comentarios.items():
            if enunciado_chave in enunciado:
                cursor.execute('UPDATE questoes SET comentario = ? WHERE id = ?', (novo_comentario, id_questao))
                atualizados += 1
                print(f'Atualizado: {disciplina} - ID {id_questao}')
                break
    
    conn.commit()
    conn.close()
    
    print(f'\n✅ {atualizados} comentários atualizados para o padrão ouro!')

if __name__ == '__main__':
    atualizar_comentarios_padrao_ouro()
