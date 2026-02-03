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
    
    # Inserir questões exemplo
    questoes = [
        # Semana 1 - Lei 12.550/2011 - Nível Básico
        {
            'disciplina': 'Lei 12.550/2011',
            'semana': 1,
            'nivel': 'Básico',
            'banca': 'IBFC',
            'enunciado': 'A Lei nº 12.550/2011 criou a EBSERH com a finalidade de:',
            'alternativas': '{"A": "Prestar serviços de saúde privada", "B": "Prestar serviços de assistência à saúde por meio da execução de objetos de acordo com as necessidades da SUS", "C": "Gerenciar hospitais privados", "D": "Fornecer planos de saúde"}',
            'resposta_correta': 'B',
            'comentario': 'A EBSERH foi criada para prestar serviços de assistência à saúde, executando objetos de acordo com as necessidades do SUS, sem fins lucrativos.'
        },
        
        # Semana 1 - Lei 12.550/2011 - Nível Alto
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
        
        # Semana 1 - Lei 12.550/2011 - Pegadinha
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
        
        # Semana 1 - Fundamentos de TI - Nível Básico
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
        
        # Semana 2 - Redes - Nível Básico
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
        
        # Semana 2 - Redes - Nível Alto
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
        
        # Semana 3 - LGPD - Pegadinha
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
        
        # Semana 3 - Segurança da Informação - Nível Alto
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
        
        # Mais questões para outras semanas...
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

        questoes = [

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
    }

]

        
        # Lei 12.550/2011 - Mais questões
        {
            'disciplina': 'Lei 12.550/2011',
            'semana': 1,
            'nivel': 'Básico',
            'banca': 'CESPE',
            'enunciado': 'A EBSERH tem como objetivo principal:',
            'alternativas': '{"A": 'Gerar lucros para o governo', 'B': 'Prestar serviços de assistência à saúde', 'C': 'Vender medicamentos', 'D': 'Formar médicos'}',
            'resposta_correta': 'B',
            'comentario': 'O objetivo principal da EBSERH é prestar serviços de assistência à saúde, conforme Art. 1º da Lei 12.550/2011.'
        },
        
        {
            'disciplina': 'Lei 12.550/2011',
            'semana': 1,
            'nivel': 'Alto',
            'banca': 'IBFC',
            'enunciado': 'Sobre a natureza jurídica da EBSERH, é correto afirmar que:',
            'alternativas': '{"A": 'É uma empresa privada', 'B': 'É uma empresa pública federal de direito privado', 'C': 'É uma autarquia', 'D': 'É uma fundação pública'}',
            'resposta_correta': 'B',
            'comentario': 'A EBSERH é uma empresa pública federal de direito privado. Não é empresa privada (A), nem autarquia (C) ou fundação pública (D), que são entidades de direito público.'
        },
        
        # Redes - Mais questões
        {
            'disciplina': 'Redes',
            'semana': 2,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'O protocolo TCP é responsável por:',
            'alternativas': '{"A": 'Traduzir nomes em IPs', 'B': 'Garantir entrega confiável de dados', 'C': 'Atribuir IPs automaticamente', 'D': 'Rotear pacotes'}',
            'resposta_correta': 'B',
            'comentario': 'TCP (Transmission Control Protocol) garante entrega confiável e ordenada dos dados, com controle de fluxo e correção de erros.'
        },
        
        {
            'disciplina': 'Redes',
            'semana': 2,
            'nivel': 'Pegadinha',
            'banca': 'CESPE',
            'enunciado': 'O endereço MAC é único globalmente e nunca muda.',
            'alternativas': '{"A": 'Certo', 'B': 'Errado'}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha! Embora o endereço MAC seja único por fabricante, ele pode ser alterado (MAC spoofing) e não é imutável como muitos pensam.'
        },
        
        # LGPD - Mais questões
        {
            'disciplina': 'LGPD',
            'semana': 3,
            'nivel': 'Básico',
            'banca': 'IBFC',
            'enunciado': 'A LGPD estabelece regras para o tratamento de:',
            'alternativas': '{"A": 'Dados de empresas apenas', 'B': 'Dados pessoais', 'C': 'Dados governamentais', 'D': 'Dados financeiros'}',
            'resposta_correta': 'B',
            'comentario': 'A LGPD (Lei 13.709/2018) estabelece regras para o tratamento de dados pessoais, independentemente do meio ou do setor.'
        },
        
        {
            'disciplina': 'LGPD',
            'semana': 3,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre a base legal para tratamento de dados na LGPD, assinale a alternativa correta:',
            'alternativas': '{"A": 'O consentimento é a única base legal possível', 'B': 'O tratamento para cumprimento de obrigação legal não requer consentimento', 'C': 'Dados públicos nunca podem ser tratados', 'D': 'A LGPD não se aplica a dados anonimizados'}',
            'resposta_correta': 'B',
            'comentario': 'O tratamento para cumprimento de obrigação legal é base legal prevista no Art. 7º, II, e não requer consentimento. A alternativa A está errada pois existem 10 bases legais. C está errada pois dados públicos podem ser tratados. D está parcialmente correta mas a B é mais precisa.'
        },
        
        # Segurança da Informação - Mais questões
        {
            'disciplina': 'Segurança da Informação',
            'semana': 3,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'Criptografia é o processo de:',
            'alternativas': '{"A": 'Ocultar informações através de códigos', 'B': 'Apagar dados permanentemente', 'C': 'Backup de informações', 'D': 'Comprimir arquivos'}',
            'resposta_correta': 'A',
            'comentario': 'Criptografia é o processo de transformar informações em formato codificado para que apenas pessoas autorizadas possam acessá-las.'
        },
        
        {
            'disciplina': 'Segurança da Informação',
            'semana': 3,
            'nivel': 'Pegadinha',
            'banca': 'IBFC',
            'enunciado': 'Firewall protege contra todos os tipos de ataques cibernéticos.',
            'alternativas': '{"A": 'Certo', 'B': 'Errado'}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha! Firewall é importante mas não protege contra tudo. Ataques de engenharia social, malware em e-mails e vulnerabilidades em aplicações podem bypassar firewalls.'
        },
        
        # Agilidade - Mais questões
        {
            'disciplina': 'Agilidade',
            'semana': 4,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre os papéis no Scrum, assinale a alternativa correta:',
            'alternativas': '{"A": 'O Product Owner é o gerente do projeto', 'B': 'O Scrum Master deve comandar o time', 'C': 'O Development Team é auto-organizado', 'D': 'O Product Owner define como o trabalho será realizado'}',
            'resposta_correta': 'C',
            'comentario': 'O Development Team é auto-organizado e define como realizar o trabalho. A está errada pois PO não é gerente. B está errada pois SM não comanda. D está errada pois PO define o quê, não como.'
        },
        
        # Banco de Dados - Mais questões
        {
            'disciplina': 'Banco de Dados',
            'semana': 4,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'SQL é a linguagem utilizada para:',
            'alternativas': '{"A": 'Programar interfaces web', 'B': 'Manipular dados em bancos relacionais', 'C': 'Criar redes neurais', 'D': 'Design gráfico'}',
            'resposta_correta': 'B',
            'comentario': 'SQL (Structured Query Language) é a linguagem padrão para manipular e consultar dados em bancos de dados relacionais.'
        },
        
        {
            'disciplina': 'Banco de Dados',
            'semana': 4,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre normalização em bancos de dados, a Forma Normal 3FN elimina:',
            'alternativas': '{"A": 'Dependências parciais', 'B": 'Dependências transitivas', 'C": 'Dependências funcionais', 'D": 'Redundância total'}',
            'resposta_correta': 'B',
            'comentario': '3FN elimina dependências transitivas. Dependências parciais são eliminadas na 2FN. Dependências funcionais são a base da normalização, não são eliminadas.'
        },
        
        # Novas disciplinas - Gestão de TI
        {
            'disciplina': 'Gestão de TI',
            'semana': 5,
            'nivel': 'Básico',
            'banca': 'IBFC',
            'enunciado': 'ITIL é um framework para:',
            'alternativas': '{"A": 'Desenvolvimento de software', 'B": 'Gestão de serviços de TI', 'C": 'Segurança da informação', 'D": 'Banco de dados'}',
            'resposta_correta': 'B',
            'comentario': 'ITIL (Information Technology Infrastructure Library) é um framework de melhores práticas para gestão de serviços de TI.'
        },
        
        {
            'disciplina': 'Gestão de TI',
            'semana': 5,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre os processos do ITIL, o Change Management está relacionado a:',
            'alternativas': '{"A": 'Gerenciamento de incidentes', 'B": 'Gerenciamento de mudanças', 'C": 'Gerenciamento de problemas', 'D": 'Gerenciamento de configuração'}',
            'resposta_correta': 'B',
            'comentario': 'Change Management (Gerenciamento de Mudanças) controla todas as mudanças na infraestrutura de TI para minimizar interrupções.'
        },
        
        {
            'disciplina': 'Gestão de TI',
            'semana': 5,
            'nivel': 'Pegadinha',
            'banca': 'IBFC',
            'enunciado': 'COBIT e ITIL são a mesma coisa.',
            'alternativas': '{"A": 'Certo', 'B": 'Errado'}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha! COBIT foca em governança (o que fazer), ITIL foca em gestão de serviços (como fazer). São complementares, não iguais.'
        },
        
        # Cloud Computing
        {
            'disciplina': 'Cloud Computing',
            'semana': 5,
            'nivel': 'Básico',
            'banca': 'FGV',
            'enunciado': 'IaaS significa:',
            'alternativas': '{"A": 'Infrastructure as a Service', 'B": 'Software as a Service', 'C": 'Platform as a Service', 'D": 'Database as a Service'}',
            'resposta_correta': 'A',
            'comentario': 'IaaS (Infrastructure as a Service) fornece infraestrutura computacional como servidores virtuais, storage e redes.'
        },
        
        {
            'disciplina': 'Cloud Computing',
            'semana': 5,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre os modelos de serviço em cloud, o PaaS oferece:',
            'alternativas': '{"A": 'Controle total do sistema operacional', 'B": 'Apenas aplicações prontas', 'C": 'Plataforma para desenvolver e deploy', 'D": 'Apenas infraestrutura básica'}',
            'resposta_correta': 'C',
            'comentario': 'PaaS (Platform as a Service) oferece plataforma completa para desenvolvimento, deploy e gerenciamento de aplicações sem preocupação com infraestrutura.'
        },
        
        {
            'disciplina': 'Cloud Computing',
            'semana': 5,
            'nivel': 'Pegadinha',
            'banca': 'IBFC',
            'enunciado': 'Cloud computing é sempre mais barato que on-premise.',
            'alternativas': '{"A": 'Certo', 'B": 'Errado'}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha! Cloud pode ser mais barata em muitos casos, mas não sempre. Cargas de trabalho constantes e previsíveis podem ser mais baratas on-premise.'
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
        
        {
            'disciplina': 'Desenvolvimento Web',
            'semana': 6,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre o modelo MVC, assinale a alternativa correta:',
            'alternativas': '{"A": "View controla o fluxo da aplicação", "B": "Model contém apenas dados visuais", "C": "Controller intermediia View e Model", "D": "MVC é usado apenas em aplicações web"}',
            'resposta_correta': 'C',
            'comentario': 'No MVC, Controller intermediia as interações entre View (interface) e Model (dados e lógica). A está errada pois Controller controla o fluxo. B está errada pois Model contém dados e lógica de negócio. D está errada pois MVC é usado em vários tipos de aplicações.'
        },
        
        {
            'disciplina': 'Desenvolvimento Web',
            'semana': 6,
            'nivel': 'Pegadinha',
            'banca': 'IBFC',
            'enunciado': 'JavaScript e Java são a mesma linguagem.',
            'alternativas': '{"A": "Certo", "B": "Errado"}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha! Apesar do nome similar, JavaScript e Java são linguagens completamente diferentes. JavaScript é interpretada e roda no navegador, Java é compilada e roda na JVM.'
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
        
        {
            'disciplina': 'APIs',
            'semana': 6,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre os métodos HTTP, DELETE é idempotente e seguro?',
            'alternativas': '{"A": "Idempotente e seguro", "B": "Idempotente mas não seguro", "C": "Não idempotente mas seguro", "D": "Não idempotente e não seguro"}',
            'resposta_correta': 'B',
            'comentario': 'DELETE é idempotente (múltiplas chamadas têm mesmo efeito) mas não é seguro (altera o estado do servidor). Métodos seguros (GET, HEAD) não alteram estado.'
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
        
        {
            'disciplina': 'Testes de Software',
            'semana': 7,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre as pirâmides de teste, a camada mais ampla é:',
            'alternativas': '{"A": "Testes unitários", "B": "Testes de integração", "C": "Testes E2E", "D": "Testes de aceitação"}',
            'resposta_correta': 'A',
            'comentario': 'Na pirâmide de testes, testes unitários são a base (mais numerosos), seguidos por integração e E2E no topo (menos numerosos).'
        },
        
        {
            'disciplina': 'Testes de Software',
            'semana': 7,
            'nivel': 'Pegadinha',
            'banca': 'IBFC',
            'enunciado': 'Teste pode garantir que um software não tem bugs.',
            'alternativas': '{"A": "Certo", "B": "Errado"}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha! Teste pode reduzir bugs e aumentar confiança, mas nunca pode garantir ausência total de bugs. Testing shows the presence, not the absence of bugs.'
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
        
        {
            'disciplina': 'DevOps',
            'semana': 7,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre containers, Docker é:',
            'alternativas': '{"A": "Uma máquina virtual completa", "B": "Virtualização em nível de sistema operacional", "C": "Um banco de dados", "D": "Um editor de código"}',
            'resposta_correta': 'B',
            'comentario': 'Docker usa virtualização em nível de SO (containers), compartilhando o kernel do host. Diferente de VMs que virtualizam hardware completo.'
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
        
        {
            'disciplina': 'Business Intelligence',
            'semana': 8,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre data warehouse, assinale a alternativa correta:',
            'alternativas': '{"A": "Dados são voláteis e atuais", "B": "Otimizado para transações", "C": "Dados históricos e agregados", "D": "Pequeno volume de dados"}',
            'resposta_correta': 'C',
            'comentario': 'Data warehouse armazena dados históricos, agregados e não voláteis para análise. Diferente de OLTP que é otimizado para transações com dados atuais.'
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
        
        {
            'disciplina': 'Analytics',
            'semana': 8,
            'nivel': 'Pegadinha',
            'banca': 'IBFC',
            'enunciado': 'Machine Learning e Inteligência Artificial são a mesma coisa.',
            'alternativas': '{"A": "Certo", "B": "Errado"}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha! Machine Learning é um subconjunto de IA. IA é o campo amplo de criar sistemas inteligentes, ML é uma abordagem específica usando algoritmos que aprendem com dados.'
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
        
        {
            'disciplina': 'Governança de TI',
            'semana': 9,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre COBIT, os princípios incluem:',
            'alternativas': '{"A": "Apenas foco em tecnologia", "B": "Atendimento a stakeholders holístico", "C": "Ignorar governança corporativa", "D": "Foco apenas em segurança"}',
            'resposta_correta': 'B',
            'comentario': 'COBIT 2019 inclui princípios como atendimento holístico a stakeholders, abordagem integrada e alinhamento com governança corporativa.'
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
        
        {
            'disciplina': 'COBIT',
            'semana': 9,
            'nivel': 'Pegadinha',
            'banca': 'IBFC',
            'enunciado': 'COBIT substitui completamente ITIL.',
            'alternativas': '{"A": "Certo", "B": "Errado"}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha! COBIT e ITIL são complementares. COBIT foca em governança (o que fazer), ITIL foca em gestão de serviços (como fazer).'
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
        
        {
            'disciplina': 'ITIL',
            'semana': 10,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre o Service Value System, o componente central é:',
            'alternativas': '{"A": "Service Value Chain", "B": "Continual Improvement", "C": "Governance", "D": "Practices"}',
            'resposta_correta': 'A',
            'comentario': 'Service Value Chain é o componente central do SVS, com 6 atividades: Plan, Improve, Engage, Design & Transition, Obtain/Build, Deliver & Support.'
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
        
        {
            'disciplina': 'Service Desk',
            'semana': 10,
            'nivel': 'Pegadinha',
            'banca': 'IBFC',
            'enunciado': 'Service Desk e Help Desk são a mesma coisa.',
            'alternativas': '{"A": "Certo", "B": "Errado"}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha! Help Desk foca em resolver incidentes. Service Desk tem escopo maior: gestão de serviços, comunicação proativa e suporte estratégico.'
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
        
        {
            'disciplina': 'Projetos',
            'semana': 11,
            'nivel': 'Alto',
            'banca': 'CESPE',
            'enunciado': 'Sobre as áreas de conhecimento do PMBOK, Risk Management está relacionado a:',
            'alternativas': '{"A": "Apenas riscos positivos", "B": "Identificação, análise e resposta a riscos", "C": "Apenas riscos técnicos", "D": "Eliminação total de riscos"}',
            'resposta_correta': 'B',
            'comentario': 'Risk Management inclui identificação, análise qualitativa e quantitativa, planejamento de respostas e monitoramento de riscos (positivos e negativos).'
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
        },
        
        {
            'disciplina': 'Scrum',
            'semana': 11,
            'nivel': 'Pegadinha',
            'banca': 'IBFC',
            'enunciado': 'Scrum Master é o chefe do time.',
            'alternativas': '{"A": "Certo", "B": "Errado"}',
            'resposta_correta': 'B',
            'comentario': '❌ Pegadinha! Scrum Master não é chefe, é um facilitador e servant leader que remove impedimentos e garante que Scrum seja entendido e executado.'
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
