import sqlite3

DB_NAME = 'ebserh_study.db'

def update_database_for_ia():
    """
    Atualiza o banco de dados para suporte a IA
    Adiciona colunas opcionais sem quebrar estrutura existente
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    print("🔄 Atualizando banco de dados para suporte a IA...")
    
    # Adicionar colunas opcionais à tabela questoes (se não existirem)
    try:
        cursor.execute('ALTER TABLE questoes ADD COLUMN tags TEXT')
        print("✅ Coluna 'tags' adicionada à tabela questoes")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️ Coluna 'tags' já existe")
        else:
            print(f"❌ Erro ao adicionar coluna 'tags': {e}")
    
    try:
        cursor.execute('ALTER TABLE questoes ADD COLUMN dificuldade_num INTEGER')
        print("✅ Coluna 'dificuldade_num' adicionada à tabela questoes")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️ Coluna 'dificuldade_num' já existe")
        else:
            print(f"❌ Erro ao adicionar coluna 'dificuldade_num': {e}")
    
    # Criar tabela para feedback da IA
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ia_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            questao_id INTEGER NOT NULL,
            usuario_id TEXT DEFAULT 'anonymous',
            tipo TEXT NOT NULL,
            conteudo TEXT NOT NULL,
            utilidade INTEGER DEFAULT 0,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (questao_id) REFERENCES questoes (id)
        )
    ''')
    print("✅ Tabela 'ia_feedback' criada/verificada")
    
    # Atualizar dificuldade_num baseado no nível existente
    cursor.execute('''
        UPDATE questoes 
        SET dificuldade_num = CASE 
            WHEN nivel = 'Básico' THEN 1
            WHEN nivel = 'Alto' THEN 2
            WHEN nivel = 'Pegadinha' THEN 3
            ELSE 1
        END
        WHERE dificuldade_num IS NULL
    ''')
    print("✅ Valores de 'dificuldade_num' atualizados baseados no nível")
    
    # Adicionar tags para algumas questões (exemplo)
    atualizacoes_tags = [
        ('Lei 12.550/2011', 'EBSERH,empresa_publica,administracao_indireta,lei_12550'),
        ('LGPD', 'dados_sensiveis,saude,base_legal,art5'),
        ('Segurança da Informação', 'CIA,confidencialidade,integridade,disponibilidade'),
        ('Banco de Dados', 'chave_primaria,chave_estrangeira,relacionamento,normalizacao'),
        ('Cloud Computing', 'IaaS,PaaS,SaaS,infraestrutura,provedor'),
        ('ITIL', 'processos,praticas,cadeia_valor,governanca,servicos'),
        ('Scrum', 'sprint,time_box,product_owner,scrum_master,agil')
    ]
    
    for disciplina, tags in atualizacoes_tags:
        cursor.execute('''
            UPDATE questoes 
            SET tags = ? 
            WHERE disciplina = ? AND tags IS NULL
        ''', (tags, disciplina))
    
    print("✅ Tags adicionadas às questões")
    
    conn.commit()
    conn.close()
    
    print("\n🎉 Banco de dados atualizado com sucesso para suporte a IA!")
    print("\n📊 Resumo das atualizações:")
    print("• Coluna 'tags' adicionada")
    print("• Coluna 'dificuldade_num' adicionada") 
    print("• Tabela 'ia_feedback' criada")
    print("• Tags populadas para disciplinas principais")
    print("• Dificuldade numérica configurada")

if __name__ == '__main__':
    update_database_for_ia()
