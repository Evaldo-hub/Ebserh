import sqlite3
import json

DB_NAME = 'ebserh_study.db'

def populate_database():
    # Inicializar o banco primeiro
    from app import init_db
    init_db()
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Limpar tabelas existentes
    cursor.execute('DELETE FROM desempenho')
    cursor.execute('DELETE FROM questoes')
    cursor.execute('DELETE FROM plano_estudos')
    
    # Inserir plano de estudos (12 semanas)
    plano_estudos = [
        (1, "Lei 12.550/2011\nFundamentos de TI", "Lei 12.550/2011,Fundamentos de TI"),
        (2, "Estatuto Social\nRedes (TCP/IP, DNS, DHCP)", "Estatuto Social,Redes"),
        (3, "LGPD\nSegurança da Informação", "LGPD,Segurança da Informação"),
        (4, "Agilidade\nBanco de Dados", "Agilidade,Banco de Dados"),
        (5, "Gestão de TI\nCloud Computing", "Gestão de TI,Cloud Computing"),
        (6, "Desenvolvimento Web\nAPIs", "Desenvolvimento Web,APIs"),
        (7, "Testes de Software\nDevOps", "Testes de Software,DevOps"),
        (8, "Business Intelligence\nAnalytics", "Business Intelligence,Analytics"),
        (9, "Governança de TI\nCOBIT", "Governança de TI,COBIT"),
        (10, "ITIL\nService Desk", "ITIL,Service Desk"),
        (11, "Projetos (PMBOK)\nScrum", "Projetos,Scrum"),
        (12, "Revisão Geral\nSimulados", "Revisão,Simulados")
    ]
    
    cursor.executemany('INSERT INTO plano_estudos (semana, conteudo, disciplinas) VALUES (?, ?, ?)', plano_estudos)
    
    # Inserir questões exemplo - Versão corrigida e expandida
    questoes = [
        # Lei 12.550/2011
    {
        'disciplina': 'Lei 12.550/2011',
        'semana': 1,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'Sobre a atuação da EBSERH, conforme a Lei nº 12.550/2011, assinale a alternativa correta.',
        'alternativas': '{"A":"Atua exclusivamente na assistência privada","B":"Presta serviços de apoio à gestão hospitalar universitária","C":"Exerce função reguladora do SUS","D":"Administra unidades básicas de saúde municipais"}',
        'resposta_correta': 'B',
        'comentario': 'A EBSERH foi criada para prestar serviços de apoio à gestão dos hospitais universitários federais, sem exercer função reguladora ou atuar exclusivamente na iniciativa privada.'
    },

    # Estatuto Social
    {
        'disciplina': 'Estatuto Social',
        'semana': 2,
        'nivel': 'Alto',
        'banca': 'IBFC',
        'enunciado': 'Segundo o Estatuto Social da EBSERH, a estrutura organizacional da empresa é definida com o objetivo de:',
        'alternativas': '{"A":"Centralizar decisões operacionais","B":"Assegurar eficiência administrativa e transparência","C":"Eliminar controle externo","D":"Substituir a legislação federal"}',
        'resposta_correta': 'B',
        'comentario': 'O Estatuto Social define a estrutura organizacional visando eficiência administrativa, transparência e cumprimento da finalidade institucional.'
    },

    # LGPD
    {
        'disciplina': 'LGPD',
        'semana': 3,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'No tratamento de dados pessoais sensíveis, a LGPD exige:',
        'alternativas': '{"A":"Consentimento genérico","B":"Base legal específica e medidas de segurança","C":"Autorização judicial","D":"Registro público obrigatório"}',
        'resposta_correta': 'B',
        'comentario': 'O tratamento de dados sensíveis exige base legal específica e adoção de medidas de segurança técnicas e administrativas.'
    },

    # Segurança da Informação
    {
        'disciplina': 'Segurança da Informação',
        'semana': 3,
        'nivel': 'Alto',
        'banca': 'CESPE',
        'enunciado': 'A integridade da informação está relacionada à:',
        'alternativas': '{"A":"Disponibilidade contínua","B":"Proteção contra acesso indevido","C":"Garantia de que dados não sejam alterados indevidamente","D":"Autenticação do usuário"}',
        'resposta_correta': 'C',
        'comentario': 'Integridade assegura que a informação não seja alterada ou destruída de forma não autorizada.'
    },

    # Agilidade
    {
        'disciplina': 'Agilidade',
        'semana': 4,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'Um dos princípios do Manifesto Ágil é:',
        'alternativas': '{"A":"Processos acima de pessoas","B":"Documentação extensa","C":"Colaboração com o cliente","D":"Planejamento rígido"}',
        'resposta_correta': 'C',
        'comentario': 'O Manifesto Ágil valoriza colaboração com o cliente mais que negociação de contratos.'
    },

    # Banco de Dados
    {
        'disciplina': 'Banco de Dados',
        'semana': 4,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'A terceira forma normal (3FN) tem como objetivo:',
        'alternativas': '{"A":"Eliminar dependências transitivas","B":"Eliminar chaves primárias","C":"Permitir redundância controlada","D":"Criar tabelas temporárias"}',
        'resposta_correta': 'A',
        'comentario': 'A 3FN elimina dependências transitivas, melhorando a integridade dos dados.'
    },

    # Redes
    {
        'disciplina': 'Redes',
        'semana': 2,
        'nivel': 'Alto',
        'banca': 'CESPE',
        'enunciado': 'No modelo TCP/IP, o protocolo responsável pelo endereçamento lógico é:',
        'alternativas': '{"A":"TCP","B":"UDP","C":"IP","D":"ARP"}',
        'resposta_correta': 'C',
        'comentario': 'O protocolo IP é responsável pelo endereçamento lógico e roteamento de pacotes.'
    },

    # Gestão de TI
    {
        'disciplina': 'Gestão de TI',
        'semana': 5,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'A gestão de serviços de TI busca entregar valor por meio de:',
        'alternativas': '{"A":"Tecnologia isolada","B":"Serviços alinhados ao negócio","C":"Automação exclusiva","D":"Redução de pessoal"}',
        'resposta_correta': 'B',
        'comentario': 'Gestão de TI foca na entrega de valor por meio de serviços alinhados às necessidades do negócio.'
    },

    # Cloud Computing
    {
        'disciplina': 'Cloud Computing',
        'semana': 5,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'No modelo PaaS, o provedor é responsável por:',
        'alternativas': '{"A":"Aplicações do usuário","B":"Infraestrutura e plataforma","C":"Dados corporativos","D":"Código-fonte"}',
        'resposta_correta': 'B',
        'comentario': 'PaaS fornece infraestrutura e plataforma para desenvolvimento e execução de aplicações.'
    },

    # Desenvolvimento Web
    {
        'disciplina': 'Desenvolvimento Web',
        'semana': 6,
        'nivel': 'Alto',
        'banca': 'IBFC',
        'enunciado': 'O uso de HTTPS contribui principalmente para:',
        'alternativas': '{"A":"Performance","B":"Segurança na comunicação","C":"Estilização","D":"Persistência de dados"}',
        'resposta_correta': 'B',
        'comentario': 'HTTPS utiliza criptografia para garantir segurança na comunicação entre cliente e servidor.'
    },

    # APIs
    {
        'disciplina': 'APIs',
        'semana': 6,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'Em APIs REST, o conceito de idempotência está associado ao método:',
        'alternativas': '{"A":"POST","B":"GET","C":"PUT","D":"PATCH"}',
        'resposta_correta': 'C',
        'comentario': 'PUT é idempotente, pois múltiplas execuções produzem o mesmo efeito.'
    },

    # Testes de Software
    {
        'disciplina': 'Testes de Software',
        'semana': 7,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'Teste de regressão tem como objetivo:',
        'alternativas': '{"A":"Avaliar desempenho","B":"Garantir que mudanças não afetem funcionalidades existentes","C":"Testar interface","D":"Eliminar bugs antigos"}',
        'resposta_correta': 'B',
        'comentario': 'Testes de regressão verificam se alterações no código não impactaram funcionalidades já existentes.'
    },

    # DevOps
    {
        'disciplina': 'DevOps',
        'semana': 7,
        'nivel': 'Alto',
        'banca': 'IBFC',
        'enunciado': 'Um dos pilares do DevOps é:',
        'alternativas': '{"A":"Isolamento de equipes","B":"Automação de processos","C":"Controle manual","D":"Separação de responsabilidades"}',
        'resposta_correta': 'B',
        'comentario': 'DevOps enfatiza automação, colaboração e integração contínua.'
    },

    # Business Intelligence
    {
        'disciplina': 'Business Intelligence',
        'semana': 8,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'Data Warehouse é caracterizado por ser:',
        'alternativas': '{"A":"Operacional","B":"Orientado a assuntos","C":"Volátil","D":"Não integrado"}',
        'resposta_correta': 'B',
        'comentario': 'Data Warehouse é orientado a assuntos, integrado, não volátil e histórico.'
    },

    # Analytics
    {
        'disciplina': 'Analytics',
        'semana': 8,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'Analytics prescritivo tem como objetivo:',
        'alternativas': '{"A":"Descrever eventos","B":"Prever resultados","C":"Sugerir ações","D":"Organizar dados"}',
        'resposta_correta': 'C',
        'comentario': 'Analytics prescritivo recomenda ações com base em análises avançadas.'
    },

    # Governança de TI
    {
        'disciplina': 'Governança de TI',
        'semana': 9,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'A governança de TI é responsabilidade de:',
        'alternativas': '{"A":"Equipe técnica","B":"Alta administração","C":"Usuários finais","D":"Service Desk"}',
        'resposta_correta': 'B',
        'comentario': 'A governança de TI é responsabilidade da alta administração.'
    },

    # COBIT
    {
        'disciplina': 'COBIT',
        'semana': 9,
        'nivel': 'Alto',
        'banca': 'IBFC',
        'enunciado': 'O COBIT organiza seus objetivos em domínios para:',
        'alternativas': '{"A":"Executar código","B":"Gerenciar e governar TI","C":"Criar aplicações","D":"Auditar contratos"}',
        'resposta_correta': 'B',
        'comentario': 'COBIT estrutura objetivos para governança e gestão da TI.'
    },

    # ITIL
    {
        'disciplina': 'ITIL',
        'semana': 10,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'O conceito central do ITIL v4 é:',
        'alternativas': '{"A":"Processos","B":"Cadeia de valor de serviços","C":"Infraestrutura","D":"Governança corporativa"}',
        'resposta_correta': 'B',
        'comentario': 'ITIL v4 introduz a Cadeia de Valor de Serviços como conceito central.'
    },

    # Service Desk
    {
        'disciplina': 'Service Desk',
        'semana': 10,
        'nivel': 'Alto',
        'banca': 'IBFC',
        'enunciado': 'Uma função essencial do Service Desk é:',
        'alternativas': '{"A":"Desenvolver sistemas","B":"Gerenciar incidentes","C":"Governar TI","D":"Planejar projetos"}',
        'resposta_correta': 'B',
        'comentario': 'Service Desk é responsável pelo registro, classificação e resolução inicial de incidentes.'
    },

    # Projetos
    {
        'disciplina': 'Projetos',
        'semana': 11,
        'nivel': 'Alto',
        'banca': 'FGV',
        'enunciado': 'O caminho crítico em um projeto indica:',
        'alternativas': '{"A":"Atividades sem risco","B":"Atividades que determinam a duração do projeto","C":"Custos totais","D":"Recursos disponíveis"}',
        'resposta_correta': 'B',
        'comentario': 'O caminho crítico define a duração mínima do projeto.'
    },

    # Scrum
    {
        'disciplina': 'Scrum',
        'semana': 11,
        'nivel': 'Alto',
        'banca': 'IBFC',
        'enunciado': 'Sprint Retrospective tem como finalidade:',
        'alternativas': '{"A":"Planejar backlog","B":"Inspecionar e melhorar o processo","C":"Apresentar incremento","D":"Avaliar produto"}',
        'resposta_correta': 'B',
        'comentario': 'Sprint Retrospective busca melhoria contínua do processo do time.'
    },

    # Lei 12.550/2011
    {
        'disciplina': 'Lei 12.550/2011',
        'semana': 1,
        'nivel': 'Pegadinha',
        'banca': 'IBFC',
        'enunciado': 'A EBSERH integra a administração direta.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': 'Gabarito: Errado.\nA EBSERH é uma empresa pública federal, com personalidade jurídica de direito privado, integrante da administração indireta.\nA pegadinha está em associar "direito privado" com "administração direta", o que está errado.\n⚠️ Dica de prova: Administração direta = União, Estados, DF e Municípios. Empresas públicas sempre são indiretas.'
    },

    # Estatuto Social
    {
        'disciplina': 'Estatuto Social',
        'semana': 2,
        'nivel': 'Pegadinha',
        'banca': 'IBFC',
        'enunciado': 'O Estatuto Social da EBSERH pode contrariar disposições previstas em lei federal.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': 'Gabarito: Errado.\nConceito correto: Estatuto Social é norma interna e deve obedecer à legislação federal, jamais contrariá-la.\nA banca tenta confundir autonomia estatutária com supremacia sobre a lei.\n⚠️ Dica de prova: Hierarquia das normas: Constituição > Leis > Estatuto/Regulamento.'
    },

    # LGPD
    {
        'disciplina': 'LGPD',
        'semana': 3,
        'nivel': 'Pegadinha',
        'banca': 'IBFC',
        'enunciado': 'O tratamento de dados sensíveis pode ocorrer sem base legal, se for para saúde.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': 'Gabarito: Errado.\nMesmo para fins de saúde, o tratamento de dados pessoais sensíveis exige base legal, conforme a LGPD.\nA banca explora a ideia de "exceção automática", que não existe.\n⚠️ Dica: Saúde facilita a base legal, mas não elimina a exigência.'
    },

    # Segurança da Informação
    {
        'disciplina': 'Segurança da Informação',
        'semana': 3,
        'nivel': 'Pegadinha',
        'banca': 'CESPE',
        'enunciado': 'Disponibilidade garante que a informação não seja alterada.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': 'Gabarito: Errado.\nA disponibilidade garante que a informação esteja acessível quando necessária.\nQuem protege contra alteração indevida é a integridade.\nA banca mistura os pilares do CID (Confidencialidade, Integridade e Disponibilidade).\n⚠️ Dica:\nConfidencialidade → acesso\nIntegridade → alteração\nDisponibilidade → tempo/acesso'
    },

    # Agilidade
    {
        'disciplina': 'Agilidade',
        'semana': 4,
        'nivel': 'Pegadinha',
        'banca': 'FGV',
        'enunciado': 'No Scrum, o Scrum Master é o responsável final pela entrega do produto.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ A responsabilidade pelo valor do produto é do Product Owner; o Scrum Master atua como facilitador.'
    },

    # Banco de Dados
    {
        'disciplina': 'Banco de Dados',
        'semana': 4,
        'nivel': 'Pegadinha',
        'banca': 'IBFC',
        'enunciado': 'A chave estrangeira identifica registros da própria tabela.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': 'Gabarito: Errado.\nA chave primária identifica unicamente registros da própria tabela.\nA chave estrangeira estabelece relacionamento com outra tabela.\nA banca troca os conceitos para induzir erro rápido.\n⚠️ Dica: Primária = identidade | Estrangeira = relacionamento.'
    },

    # Redes
    {
        'disciplina': 'Redes',
        'semana': 2,
        'nivel': 'Pegadinha',
        'banca': 'CESPE',
        'enunciado': 'O protocolo UDP garante entrega confiável e ordenada dos pacotes.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ UDP não garante entrega, ordem ou controle de erros. Essas são características do TCP.'
    },

    # Gestão de TI
    {
        'disciplina': 'Gestão de TI',
        'semana': 5,
        'nivel': 'Pegadinha',
        'banca': 'FGV',
        'enunciado': 'Gestão de TI e Governança de TI possuem exatamente os mesmos objetivos.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ Governança direciona e controla; gestão executa. São complementares, mas não iguais.'
    },

    # Cloud Computing
    {
        'disciplina': 'Cloud Computing',
        'semana': 5,
        'nivel': 'Pegadinha',
        'banca': 'IBFC',
        'enunciado': 'No modelo IaaS, o provedor é responsável pelas aplicações do cliente.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': 'Gabarito: Errado.\nNo modelo IaaS, o provedor fornece infraestrutura (servidores, rede e armazenamento).\nO cliente é responsável por sistema operacional e aplicações.\nA banca costuma inverter responsabilidades entre IaaS, PaaS e SaaS.\n⚠️ Dica de prova: Quanto mais "S", menos o cliente gerencia.'
    },

    # Desenvolvimento Web
    {
        'disciplina': 'Desenvolvimento Web',
        'semana': 6,
        'nivel': 'Pegadinha',
        'banca': 'FGV',
        'enunciado': 'HTML é responsável pela estilização visual das páginas web.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ HTML estrutura conteúdo; CSS é responsável pela estilização.'
    },

    # APIs
    {
        'disciplina': 'APIs',
        'semana': 6,
        'nivel': 'Pegadinha',
        'banca': 'IBFC',
        'enunciado': 'O método HTTP POST é idempotente.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ POST não é idempotente; múltiplas requisições podem gerar efeitos diferentes.'
    },

    # Testes de Software
    {
        'disciplina': 'Testes de Software',
        'semana': 7,
        'nivel': 'Pegadinha',
        'banca': 'FGV',
        'enunciado': 'Testes de regressão são realizados apenas após a entrega do sistema.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ Testes de regressão ocorrem sempre que há mudanças no sistema.'
    },

    # DevOps
    {
        'disciplina': 'DevOps',
        'semana': 7,
        'nivel': 'Pegadinha',
        'banca': 'IBFC',
        'enunciado': 'DevOps elimina completamente a necessidade de testes de software.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ DevOps integra e automatiza testes, não os elimina.'
    },

    # Business Intelligence
    {
        'disciplina': 'Business Intelligence',
        'semana': 8,
        'nivel': 'Pegadinha',
        'banca': 'FGV',
        'enunciado': 'Business Intelligence é utilizado exclusivamente para decisões operacionais.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ BI apoia decisões estratégicas, táticas e operacionais.'
    },

    # Analytics
    {
        'disciplina': 'Analytics',
        'semana': 8,
        'nivel': 'Pegadinha',
        'banca': 'IBFC',
        'enunciado': 'Analytics descritivo tem como foco prever cenários futuros.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ Previsão é função do analytics preditivo; o descritivo analisa o passado.'
    },

    # Governança de TI
    {
        'disciplina': 'Governança de TI',
        'semana': 9,
        'nivel': 'Pegadinha',
        'banca': 'FGV',
        'enunciado': 'A governança de TI é responsabilidade exclusiva da área técnica.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ Governança é responsabilidade da alta administração.'
    },

    # COBIT
    {
        'disciplina': 'COBIT',
        'semana': 9,
        'nivel': 'Pegadinha',
        'banca': 'IBFC',
        'enunciado': 'COBIT é um framework voltado apenas para auditoria de TI.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ COBIT trata de governança e gestão, não apenas auditoria.'
    },

    # ITIL
    {
        'disciplina': 'ITIL',
        'semana': 10,
        'nivel': 'Pegadinha',
        'banca': 'FGV',
        'enunciado': 'ITIL v4 eliminou os processos.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': 'Gabarito: Errado.\nO ITIL v4 não elimina processos, mas amplia a visão ao introduzir o conceito de práticas.\nA banca explora a palavra "substituiu totalmente", que invalida a afirmativa.\n⚠️ Dica: Em prova, desconfie de termos absolutos: totalmente, exclusivamente, apenas.'
    },

    # Service Desk
    {
        'disciplina': 'Service Desk',
        'semana': 10,
        'nivel': 'Pegadinha',
        'banca': 'IBFC',
        'enunciado': 'Service Desk e Central de Serviços são conceitos distintos.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ São termos equivalentes dentro do ITIL.'
    },

    # Projetos
    {
        'disciplina': 'Projetos',
        'semana': 11,
        'nivel': 'Pegadinha',
        'banca': 'FGV',
        'enunciado': 'Projetos possuem natureza contínua e repetitiva.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': '❌ Projetos são temporários e produzem resultados únicos.'
    },

    # Scrum
    {
        'disciplina': 'Scrum',
        'semana': 11,
        'nivel': 'Pegadinha',
        'banca': 'IBFC',
        'enunciado': 'A Sprint pode ter duração variável.',
        'alternativas': '{"A":"Certo","B":"Errado"}',
        'resposta_correta': 'B',
        'comentario': 'Gabarito: Errado.\nA Sprint possui duração fixa (time-box), definida pelo time Scrum.\nA variação ocorre no escopo, nunca no tempo.\n⚠️ Dica: No Scrum, tempo é fixo; escopo é flexível.'
    },

        # Lei 12.550/2011
    {
        'disciplina': 'Lei 12.550/2011',
        'semana': 1,
        'nivel': 'Básico',
        'banca': 'IBFC',
        'enunciado': 'A Empresa Brasileira de Serviços Hospitalares (EBSERH) foi criada pela Lei nº 12.550/2011 como:',
        'alternativas': '{"A":"Autarquia federal","B":"Empresa pública federal","C":"Sociedade de economia mista","D":"Fundação pública"}',
        'resposta_correta': 'B',
        'comentario': 'A Lei nº 12.550/2011 criou a EBSERH como empresa pública federal, integrante da administração indireta, com personalidade jurídica de direito privado.'
    },

    # Estatuto Social
    {
        'disciplina': 'Estatuto Social',
        'semana': 2,
        'nivel': 'Básico',
        'banca': 'IBFC',
        'enunciado': 'O Estatuto Social da EBSERH tem como finalidade principal:',
        'alternativas': '{"A":"Definir normas trabalhistas","B":"Estabelecer a estrutura organizacional e competências","C":"Criar leis complementares","D":"Regular contratos privados"}',
        'resposta_correta': 'B',
        'comentario': 'O Estatuto Social define a estrutura organizacional, competências dos órgãos e diretrizes de funcionamento da EBSERH.'
    },

    # LGPD
    {
        'disciplina': 'LGPD',
        'semana': 3,
        'nivel': 'Básico',
        'banca': 'FGV',
        'enunciado': 'Segundo a LGPD, dados relacionados à saúde são classificados como:',
        'alternativas': '{"A":"Dados públicos","B":"Dados anonimizados","C":"Dados pessoais sensíveis","D":"Dados administrativos"}',
        'resposta_correta': 'C',
        'comentario': 'A LGPD classifica dados de saúde como dados pessoais sensíveis, exigindo maior nível de proteção (art. 5º, II).'
    },

    # Segurança da Informação
    {
        'disciplina': 'Segurança da Informação',
        'semana': 3,
        'nivel': 'Básico',
        'banca': 'FGV',
        'enunciado': 'O princípio da confidencialidade tem como objetivo:',
        'alternativas': '{"A":"Garantir acesso contínuo","B":"Evitar alteração não autorizada","C":"Restringir acesso a pessoas autorizadas","D":"Garantir autenticidade"}',
        'resposta_correta': 'C',
        'comentario': 'Confidencialidade assegura que apenas pessoas autorizadas tenham acesso às informações.'
    },

    # Agilidade
    {
        'disciplina': 'Agilidade',
        'semana': 4,
        'nivel': 'Básico',
        'banca': 'IBFC',
        'enunciado': 'No Scrum, o responsável por priorizar o Product Backlog é o:',
        'alternativas': '{"A":"Scrum Master","B":"Product Owner","C":"Time de Desenvolvimento","D":"Gerente de Projetos"}',
        'resposta_correta': 'B',
        'comentario': 'O Product Owner é responsável por maximizar o valor do produto e priorizar o Product Backlog.'
    },

    # Banco de Dados
    {
        'disciplina': 'Banco de Dados',
        'semana': 4,
        'nivel': 'Básico',
        'banca': 'FGV',
        'enunciado': 'A normalização em bancos de dados tem como objetivo principal:',
        'alternativas': '{"A":"Aumentar redundância","B":"Eliminar inconsistências e redundâncias","C":"Aumentar performance","D":"Criar mais tabelas"}',
        'resposta_correta': 'B',
        'comentario': 'A normalização reduz redundâncias e inconsistências, melhorando a integridade dos dados.'
    },

    # Redes
    {
        'disciplina': 'Redes',
        'semana': 2,
        'nivel': 'Básico',
        'banca': 'IBFC',
        'enunciado': 'O protocolo TCP tem como característica principal:',
        'alternativas': '{"A":"Transmissão sem conexão","B":"Entrega confiável de dados","C":"Não controle de erros","D":"Uso exclusivo em redes locais"}',
        'resposta_correta': 'B',
        'comentario': 'O TCP é um protocolo orientado à conexão, garantindo entrega confiável e ordenada dos dados.'
    },

    # Gestão de TI
    {
        'disciplina': 'Gestão de TI',
        'semana': 5,
        'nivel': 'Básico',
        'banca': 'FGV',
        'enunciado': 'A gestão de TI busca principalmente:',
        'alternativas': '{"A":"Substituir processos","B":"Alinhar TI aos objetivos do negócio","C":"Eliminar riscos","D":"Centralizar decisões"}',
        'resposta_correta': 'B',
        'comentario': 'Gestão de TI tem como foco alinhar tecnologia aos objetivos estratégicos da organização.'
    },

    # Cloud Computing
    {
        'disciplina': 'Cloud Computing',
        'semana': 5,
        'nivel': 'Básico',
        'banca': 'IBFC',
        'enunciado': 'No modelo SaaS, o usuário:',
        'alternativas': '{"A":"Gerencia infraestrutura","B":"Gerencia sistema operacional","C":"Utiliza aplicações prontas via internet","D":"Administra redes físicas"}',
        'resposta_correta': 'C',
        'comentario': 'SaaS fornece aplicações prontas acessadas via internet, sem gestão de infraestrutura pelo usuário.'
    },

    # Desenvolvimento Web
    {
        'disciplina': 'Desenvolvimento Web',
        'semana': 6,
        'nivel': 'Básico',
        'banca': 'FGV',
        'enunciado': 'CSS é utilizado principalmente para:',
        'alternativas': '{"A":"Estruturação de conteúdo","B":"Estilização de páginas","C":"Persistência de dados","D":"Segurança"}',
        'resposta_correta': 'B',
        'comentario': 'CSS é responsável pela apresentação visual e estilização das páginas web.'
    },

    # APIs
    {
        'disciplina': 'APIs',
        'semana': 6,
        'nivel': 'Básico',
        'banca': 'IBFC',
        'enunciado': 'O método HTTP GET é utilizado para:',
        'alternativas': '{"A":"Criar recursos","B":"Atualizar dados","C":"Excluir recursos","D":"Obter informações"}',
        'resposta_correta': 'D',
        'comentario': 'GET é utilizado para recuperar informações sem alterar o estado do servidor.'
    },

    # Testes de Software
    {
        'disciplina': 'Testes de Software',
        'semana': 7,
        'nivel': 'Básico',
        'banca': 'FGV',
        'enunciado': 'Teste de integração verifica:',
        'alternativas': '{"A":"Funções isoladas","B":"Interação entre módulos","C":"Interface gráfica","D":"Segurança"}',
        'resposta_correta': 'B',
        'comentario': 'Teste de integração avalia a interação entre diferentes módulos do sistema.'
    },

    # DevOps
    {
        'disciplina': 'DevOps',
        'semana': 7,
        'nivel': 'Básico',
        'banca': 'IBFC',
        'enunciado': 'DevOps busca principalmente:',
        'alternativas': '{"A":"Separar equipes","B":"Automatizar e integrar desenvolvimento e operações","C":"Eliminar testes","D":"Substituir metodologias ágeis"}',
        'resposta_correta': 'B',
        'comentario': 'DevOps promove integração, automação e colaboração entre desenvolvimento e operações.'
    },

    # Business Intelligence
    {
        'disciplina': 'Business Intelligence',
        'semana': 8,
        'nivel': 'Básico',
        'banca': 'FGV',
        'enunciado': 'Dashboards em BI têm como objetivo:',
        'alternativas': '{"A":"Armazenar dados","B":"Visualizar indicadores","C":"Criar códigos","D":"Executar backups"}',
        'resposta_correta': 'B',
        'comentario': 'Dashboards permitem visualizar indicadores e apoiar a tomada de decisão.'
    },

    # Analytics
    {
        'disciplina': 'Analytics',
        'semana': 8,
        'nivel': 'Básico',
        'banca': 'IBFC',
        'enunciado': 'Analytics preditivo tem como foco:',
        'alternativas': '{"A":"Descrever o passado","B":"Prever cenários futuros","C":"Organizar dados","D":"Armazenar informações"}',
        'resposta_correta': 'B',
        'comentario': 'Analytics preditivo utiliza dados históricos para prever tendências e cenários futuros.'
    },

    # Governança de TI
    {
        'disciplina': 'Governança de TI',
        'semana': 9,
        'nivel': 'Básico',
        'banca': 'FGV',
        'enunciado': 'Governança de TI está relacionada a:',
        'alternativas': '{"A":"Execução técnica","B":"Direcionamento e controle","C":"Codificação","D":"Suporte operacional"}',
        'resposta_correta': 'B',
        'comentario': 'Governança de TI trata do direcionamento estratégico e controle da TI.'
    },

    # COBIT
    {
        'disciplina': 'COBIT',
        'semana': 9,
        'nivel': 'Básico',
        'banca': 'IBFC',
        'enunciado': 'COBIT tem como foco principal:',
        'alternativas': '{"A":"Gestão de projetos","B":"Governança e gestão de TI","C":"Desenvolvimento ágil","D":"Segurança física"}',
        'resposta_correta': 'B',
        'comentario': 'COBIT é um framework voltado à governança e gestão da TI corporativa.'
    },

    # ITIL
    {
        'disciplina': 'ITIL',
        'semana': 10,
        'nivel': 'Básico',
        'banca': 'FGV',
        'enunciado': 'No ITIL, incidente é:',
        'alternativas': '{"A":"Mudança planejada","B":"Interrupção não planejada de serviço","C":"Melhoria contínua","D":"Projeto estratégico"}',
        'resposta_correta': 'B',
        'comentario': 'Incidente é qualquer interrupção não planejada ou redução da qualidade de um serviço.'
    },

    # Service Desk
    {
        'disciplina': 'Service Desk',
        'semana': 10,
        'nivel': 'Básico',
        'banca': 'IBFC',
        'enunciado': 'Service Desk atua como:',
        'alternativas': '{"A":"Equipe de desenvolvimento","B":"Ponto único de contato","C":"Auditoria","D":"Governança"}',
        'resposta_correta': 'B',
        'comentario': 'Service Desk é o ponto único de contato entre usuários e a TI.'
    },

    # Projetos
    {
        'disciplina': 'Projetos',
        'semana': 11,
        'nivel': 'Básico',
        'banca': 'FGV',
        'enunciado': 'Segundo o PMBOK, projetos possuem:',
        'alternativas': '{"A":"Natureza contínua","B":"Resultado repetitivo","C":"Início e fim definidos","D":"Execução indefinida"}',
        'resposta_correta': 'C',
        'comentario': 'Projetos são esforços temporários, com início e fim definidos.'
    },

    # Scrum
    {
        'disciplina': 'Scrum',
        'semana': 11,
        'nivel': 'Básico',
        'banca': 'IBFC',
        'enunciado': 'Sprint Review tem como objetivo:',
        'alternativas': '{"A":"Planejar sprint","B":"Inspecionar incremento","C":"Avaliar equipe","D":"Corrigir erros"}',
        'resposta_correta': 'B',
        'comentario': 'Sprint Review inspeciona o incremento e adapta o Product Backlog se necessário.'
    },
        # Lei 12.550/2011
        {
            'disciplina': 'Lei 12.550/2011',
            'semana': 1,
            'nivel': 'Básico',
            'banca': 'IBFC',
            'enunciado': 'A Lei nº 12.550/2011 criou a EBSERH com a finalidade de:',
            'alternativas': '{"A": "Prestar serviços de saúde privada", "B": "Prestar serviços de assistência à saúde por meio da execução de objetos de acordo com as necessidades do SUS", "C": "Gerenciar hospitais privados", "D": "Fornecer planos de saúde"}',
            'resposta_correta': 'B',
            'comentario': 'A EBSERH foi criada para prestar serviços de assistência à saúde, executando objetos de acordo com as necessidades do SUS, sem fins lucrativos.'
        },
        {
            'disciplina': 'Lei 12.550/2011',
            'semana': 1,
            'nivel': 'Alto',
            'banca': 'IBFC',
            'enunciado': 'Sobre a vinculação da EBSERH ao Ministério da Educação, assinale a alternativa correta:',
            'alternativas': '{"A": "A EBSERH é vinculada ao Ministério da Saúde", "B": "A EBSERH não possui vinculação ministerial", "C": "A EBSERH é vinculada ao Ministério da Educação", "D": "A EBSERH é autônoma e não se vincula a nenhum ministério"}',
            'resposta_correta': 'C',
            'comentario': 'Segundo o Art. 1º da Lei 12.550/2011, a EBSERH é empresa pública vinculada ao Ministério da Educação. As alternativas A e B estão incorretas pois a vinculação é ao MEC, e a D está incorreta pois toda empresa pública possui vinculação ministerial.'
        },
        {
            'disciplina': 'Lei 12.550/2011',
            'semana': 1,
            'nivel': 'Pegadinha',
            'banca': 'IBFC',
            'enunciado': 'A EBSERH possui personalidade jurídica de direito privado e integra a administração direta.',
            'alternativas': '{"A": "Certo", "B": "Errado"}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha clássica da IBFC. Apesar de ser empresa pública (direito privado), a EBSERH integra a administração indireta, não a direta. Empresa pública é entidade da administração indireta.'
        },
        
        # Fundamentos de TI
        {
            'disciplina': 'Fundamentos de TI',
            'semana': 1,
            'nivel': 'Básico',
            'banca': 'CESPE',
            'enunciado': 'O hardware é a parte física do computador, enquanto o software é:',
            'alternativas': '{"A": "A parte física dos periféricos", "B": "A parte lógica, composta por programas e instruções", "C": "Os cabos de conexão", "D": "A energia elétrica"}',
            'resposta_correta': 'B',
            'comentario': 'Software é a parte lógica do computador, composta por programas, aplicativos e instruções que executam tarefas no hardware.'
        },
        
        # Redes
        {
            'disciplina': 'Redes',
            'semana': 2,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'O protocolo DNS é responsável por:',
            'alternativas': '{"A": "Atribuir endereços IP aos dispositivos", "B": "Traduzir nomes de domínio em endereços IP", "C": "Configurar roteadores", "D": "Prover segurança na rede"}',
            'resposta_correta': 'B',
            'comentario': 'DNS (Domain Name System) traduz nomes de domínio (como www.google.com) em endereços IP numéricos que os computadores entendem.'
        },
        {
            'disciplina': 'Redes',
            'semana': 2,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre o protocolo DHCP, assinale a alternativa correta:',
            'alternativas': '{"A": "DHCP atribui endereços IP estáticos manualmente", "B": "DHCP funciona apenas em redes IPv6", "C": "DHCP atribui automaticamente endereços IP e outras configurações de rede", "D": "DHCP é um protocolo de roteamento"}',
            'resposta_correta': 'C',
            'comentario': 'DHCP (Dynamic Host Configuration Protocol) atribui automaticamente endereços IP, máscara de sub-rede, gateway e DNS. A alternativa A está errada pois DHCP é dinâmico, B está errada pois funciona em IPv4 e IPv6, e D está errada pois não é protocolo de roteamento.'
        },
        
        # LGPD
        {
            'disciplina': 'LGPD',
            'semana': 3,
            'nivel': 'Pegadinha',
            'banca': 'IBFC',
            'enunciado': 'A LGPD não se aplica ao setor de saúde, pois os dados médicos são protegidos por outras leis.',
            'alternativas': '{"A": "Certo", "B": "Errado"}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha! A LGPD se aplica a todos os setores, inclusive o de saúde. Na verdade, dados de saúde são considerados dados sensíveis pela LGPD e possuem proteção especial. Art. 11º, II, da LGPD.'
        },
        
        # Segurança da Informação
        {
            'disciplina': 'Segurança da Informação',
            'semana': 3,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre os princípios da segurança da informação, assinale a alternativa correta:',
            'alternativas': '{"A": "Confidencialidade garante que os dados não sejam alterados", "B": "Integridade garante que apenas pessoas autorizadas acessem os dados", "C": "Disponibilidade garante que os sistemas estejam acessíveis quando necessário", "D": "Autenticidade é o mesmo que confidencialidade"}',
            'resposta_correta': 'C',
            'comentario': 'Disponibilidade garante acesso aos sistemas e informações quando necessário. Confidencialidade garante acesso restrito (não integridade), Integridade garante que dados não sejam alterados (não confidencialidade), e Autenticidade é diferente de confidencialidade.'
        },
        
        # Agilidade
        {
            'disciplina': 'Agilidade',
            'semana': 4,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'O Scrum é um framework ágil que utiliza:',
            'alternativas': '{"A": "Sprints de duração fixa", "B": "Planejamento detalhado inicial", "C": "Documentação extensiva", "D": "Ciclo em cascata"}',
            'resposta_correta': 'A',
            'comentario': 'Scrum utiliza sprints (iterações) de duração fixa, geralmente de 2 a 4 semanas, para entregar valor incrementalmente.'
        },
        
        # Banco de Dados
        {
            'disciplina': 'Banco de Dados',
            'semana': 4,
            'nivel': 'Pegadinha',
            'banca': 'IBFC',
            'enunciado': 'Chave primária é o mesmo que chave estrangeira.',
            'alternativas': '{"A": "Certo", "B": "Errado"}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha! Chave primária identifica unicamente um registro na tabela atual. Chave estrangeira referencia uma chave primária em outra tabela, estabelecendo relacionamentos.'
        },
        
        # Gestão de TI
        {
            'disciplina': 'Gestão de TI',
            'semana': 5,
            'nivel': 'Básico',
            'banca': 'IBFC',
            'enunciado': 'ITIL é um framework para:',
            'alternativas': '{"A": "Desenvolvimento de software", "B": "Gestão de serviços de TI", "C": "Segurança da informação", "D": "Banco de dados"}',
            'resposta_correta': 'B',
            'comentario': 'ITIL (Information Technology Infrastructure Library) é um framework de melhores práticas para gestão de serviços de TI.'
        },
        
        # Cloud Computing
        {
            'disciplina': 'Cloud Computing',
            'semana': 5,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'IaaS significa:',
            'alternativas': '{"A": "Infrastructure as a Service", "B": "Software as a Service", "C": "Platform as a Service", "D": "Database as a Service"}',
            'resposta_correta': 'A',
            'comentario': 'IaaS (Infrastructure as a Service) fornece infraestrutura computacional como servidores virtuais, storage e redes.'
        },
        
        # Desenvolvimento Web
        {
            'disciplina': 'Desenvolvimento Web',
            'semana': 6,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'HTML é usado para:',
            'alternativas': '{"A": "Estilizar páginas", "B": "Estruturar conteúdo", "C": "Programar interações", "D": "Gerenciar bancos de dados"}',
            'resposta_correta': 'B',
            'comentario': 'HTML (HyperText Markup Language) é usado para estruturar o conteúdo das páginas web. CSS é para estilização e JavaScript para interações.'
        },
        
        # APIs
        {
            'disciplina': 'APIs',
            'semana': 6,
            'nivel': 'Básico',
            'banca': 'IBFC',
            'enunciado': 'REST é um estilo arquitetural para:',
            'alternativas': '{"A": "Bancos de dados", "B": "Interfaces de programação", "C": "Design gráfico", "D": "Redes neurais"}',
            'resposta_correta': 'B',
            'comentario': 'REST (Representational State Transfer) é um estilo arquitetural para projetar APIs web, usando métodos HTTP como GET, POST, PUT, DELETE.'
        },
        
        # Testes de Software
        {
            'disciplina': 'Testes de Software',
            'semana': 7,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'Teste unitário verifica:',
            'alternativas': '{"A": "Integração entre sistemas", "B": "Unidades individuais de código", "C": "Performance do sistema", "D": "Experiência do usuário"}',
            'resposta_correta': 'B',
            'comentario': 'Teste unitário verifica unidades individuais de código (funções, métodos, classes) isoladamente.'
        },
        
        # DevOps
        {
            'disciplina': 'DevOps',
            'semana': 7,
            'nivel': 'Básico',
            'banca': 'IBFC',
            'enunciado': 'CI/CD significa:',
            'alternativas': '{"A": "Continuous Integration/Continuous Deployment", "B": "Code Inspection/Code Debugging", "C": "Customer Interface/Customer Delivery", "D": "Cloud Integration/Cloud Deployment"}',
            'resposta_correta': 'A',
            'comentario': 'CI/CD (Continuous Integration/Continuous Deployment) é uma prática de automatizar integração e deploy de software.'
        },
        
        # Business Intelligence
        {
            'disciplina': 'Business Intelligence',
            'semana': 8,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'BI (Business Intelligence) é o processo de:',
            'alternativas': '{"A": "Desenvolver software", "B": "Analisar dados para decisões", "C": "Configurar redes", "D": "Criar designs"}',
            'resposta_correta': 'B',
            'comentario': 'BI é o processo de coletar, analisar e apresentar dados para apoiar decisões de negócio.'
        },
        
        # Analytics
        {
            'disciplina': 'Analytics',
            'semana': 8,
            'nivel': 'Básico',
            'banca': 'IBFC',
            'enunciado': 'Data Mining é o processo de:',
            'alternativas': '{"A": "Extrair padrões de grandes conjuntos de dados", "B": "Apagar dados desnecessários", "C": "Comprimir arquivos", "D": "Backup de informações"}',
            'resposta_correta': 'A',
            'comentario': 'Data Mining é o processo de descobrir padrões, correlações e anomalias em grandes conjuntos de dados.'
        },
        
        # Governança de TI
        {
            'disciplina': 'Governança de TI',
            'semana': 9,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'Governança de TI garante:',
            'alternativas': '{"A": "Alinhamento de TI com o negócio", "B": "Desenvolvimento rápido", "C": "Redução de custos máxima", "D": "Substituição de todos os sistemas"}',
            'resposta_correta': 'A',
            'comentario': 'Governança de TI garante que TI esteja alinhada com os objetivos de negócio, entregando valor e gerenciando riscos.'
        },
        
        # COBIT
        {
            'disciplina': 'COBIT',
            'semana': 9,
            'nivel': 'Básico',
            'banca': 'IBFC',
            'enunciado': 'COBIT é um framework de:',
            'alternativas': '{"A": "Governança e gestão de TI", "B": "Desenvolvimento ágil", "C": "Banco de dados", "D": "Design gráfico"}',
            'resposta_correta': 'A',
            'comentario': 'COBIT é um framework de governança e gestão de TI empresarial, ajudando a otimizar valor e gerenciar riscos.'
        },
        
        # ITIL
        {
            'disciplina': 'ITIL',
            'semana': 10,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'ITIL v4 foca em:',
            'alternativas': '{"A": "Value co-creation", "B": "Apenas processos técnicos", "C": "Somente infraestrutura", "D": "Apenas desenvolvimento"}',
            'resposta_correta': 'A',
            'comentario': 'ITIL v4 introduziu o conceito de value co-creation (cocriação de valor) entre provedor e consumidor de serviços.'
        },
        
        # Service Desk
        {
            'disciplina': 'Service Desk',
            'semana': 10,
            'nivel': 'Básico',
            'banca': 'IBFC',
            'enunciado': 'Service Desk é o ponto único de contato para:',
            'alternativas': '{"A": "Usuários de TI", "B": "Vendedores", "C": "Concorrentes", "D": "Imprensa"}',
            'resposta_correta': 'A',
            'comentario': 'Service Desk é o ponto único de contato (SPOC) entre usuários e o provedor de serviços de TI.'
        },
        
        # Projetos
        {
            'disciplina': 'Projetos',
            'semana': 11,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'Projeto segundo PMBOK é:',
            'alternativas': '{"A": "Esforço temporário com resultado único", "B": "Operação contínua", "C": "Processo repetitivo", "D": "Manutenção sistemática"}',
            'resposta_correta': 'A',
            'comentario': 'Segundo PMBOK, projeto é um esforço temporário empreendido para criar um produto, serviço ou resultado único.'
        },
        
        # Scrum
        {
            'disciplina': 'Scrum',
            'semana': 11,
            'nivel': 'Básico',
            'banca': 'IBFC',
            'enunciado': 'Daily Scrum é uma reunião diária de:',
            'alternativas': '{"A": "15 minutos para sincronização", "B": "2 horas para planejamento", "C": "1 dia para retrospectiva", "D": "30 minutos para demo"}',
            'resposta_correta': 'A',
            'comentario': 'Daily Scrum (Daily Meeting) é uma reunião de 15 minutos para sincronização do time, respondendo: O que fiz? O que farei? Algo impede?'
        }
    ]
    
    for questao in questoes:
        cursor.execute('''
            INSERT INTO questoes (disciplina, semana, nivel, banca, enunciado, alternativas, resposta_correta, comentario)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            questao['disciplina'],
            questao['semana'],
            questao['nivel'],
            questao['banca'],
            questao['enunciado'],
            questao['alternativas'],
            questao['resposta_correta'],
            questao['comentario']
        ))
    
    conn.commit()
    conn.close()
    print("Banco de dados populado com sucesso!")

if __name__ == '__main__':
    populate_database()
