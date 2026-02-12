from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import sqlite3
import json
from datetime import datetime
import random
import os
from functools import wraps
import secrets
from supabase_service import supabase_service
from flask_sqlalchemy import SQLAlchemy

# Importar serviços
from ia_service import ia_service

# ================= BANCO DE DADOS =================
db_url = os.environ.get("DATABASE_URL")

# 🔥 CORREÇÃO AQUI
if db_url:
    db_url = db_url.strip()

# Permite rodar local com SQLite
if not db_url:
    db_url = "sqlite:///ebserh_study.db"
    print("DATABASE_URL nao encontrada. Usando SQLite local.")

# Corrige padrão antigo do Render
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))

# Inicializar SQLAlchemy
db = SQLAlchemy(app)

def init_db():
    """Inicializa o banco de dados"""
    try:
        if db_url.startswith('sqlite'):
            # SQLite local
            conn = sqlite3.connect("ebserh_study.db")
            cursor = conn.cursor()
            
            # Tabela de questões
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS questoes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    disciplina TEXT NOT NULL,
                    semana INTEGER NOT NULL,
                    nivel TEXT NOT NULL CHECK (nivel IN ('Básico', 'Alto', 'Pegadinha')),
                    banca TEXT NOT NULL,
                    enunciado TEXT NOT NULL,
                    alternativas TEXT NOT NULL,
                    resposta_correta TEXT NOT NULL,
                    comentario TEXT NOT NULL
                )
            ''')
            
            # Tabela de desempenho
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS desempenho (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    questao_id INTEGER NOT NULL,
                    resposta_usuario TEXT NOT NULL,
                    acerto BOOLEAN NOT NULL,
                    data_resposta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (questao_id) REFERENCES questoes (id)
                )
            ''')
            
            # Tabela do plano de estudos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS plano_estudos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    semana INTEGER NOT NULL UNIQUE,
                    conteudo TEXT NOT NULL,
                    disciplinas TEXT NOT NULL
                )
            ''')
            
            # Tabela de feedback da IA
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ia_feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    questao_id INTEGER NOT NULL,
                    tipo TEXT NOT NULL,
                    conteudo TEXT NOT NULL,
                    utilidade INTEGER DEFAULT 0,
                    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (questao_id) REFERENCES questoes (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            print("Banco SQLite inicializado com sucesso!")
            
        else:
            # PostgreSQL - SQLAlchemy cria tabelas automaticamente
            print("Usando PostgreSQL - SQLAlchemy gerenciará as tabelas")
            
    except Exception as e:
        print(f"Erro ao inicializar banco: {e}")

def get_db_connection():
    """Obtém conexão com o banco de dados correto"""
    if db_url.startswith('sqlite'):
        conn = sqlite3.connect("ebserh_study.db")
        conn.row_factory = sqlite3.Row
        return conn
    else:
        # PostgreSQL via SQLAlchemy
        return db

# Configuração de ambiente
if os.getenv('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
else:
    app.config['DEBUG'] = True
    app.config['TESTING'] = True

# Adicionar filtro personalizado para JSON
@app.template_filter('from_json')
def from_json(value):
    return json.loads(value)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plano')
def plano():
    try:
        conn = get_db_connection()
        
        if db_url.startswith('sqlite'):
            # SQLite local
            plano = conn.execute('SELECT * FROM plano_estudos ORDER BY semana').fetchall()
            conn.close()
        else:
            # PostgreSQL via SQLAlchemy
            from sqlalchemy import text
            result = conn.session.execute(text('SELECT * FROM plano_estudos ORDER BY semana'))
            plano = result.fetchall()
        
        return render_template('plano.html', plano=plano)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check para Render"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'environment': os.getenv('FLASK_ENV', 'development')
    }), 200

@app.route('/questoes')
def questoes():
    disciplina = request.args.get('disciplina', '')
    semana = request.args.get('semana', '')
    nivel = request.args.get('nivel', '')
    
    conn = get_db_connection()
    query = 'SELECT DISTINCT disciplina FROM questoes ORDER BY disciplina'
    disciplinas = conn.execute(query).fetchall()
    
    query = 'SELECT DISTINCT semana FROM questoes ORDER BY semana'
    semanas = conn.execute(query).fetchall()
    
    # Construir query de questões com filtros
    query = 'SELECT * FROM questoes WHERE 1=1'
    params = []
    
    if disciplina:
        query += ' AND disciplina = ?'
        params.append(disciplina)
    
    if semana:
        query += ' AND semana = ?'
        params.append(semana)
    
    if nivel:
        query += ' AND nivel = ?'
        params.append(nivel)
    
    query += ' ORDER BY disciplina, semana, nivel'
    
    questoes = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template('questoes.html', 
                         questoes=questoes, 
                         disciplinas=disciplinas,
                         semanas=semanas,
                         filtros={'disciplina': disciplina, 'semana': semana, 'nivel': nivel})

@app.route('/questao/<int:questao_id>')
def questao_detalhe(questao_id):
    conn = get_db_connection()
    questao = conn.execute('SELECT * FROM questoes WHERE id = ?', (questao_id,)).fetchone()
    conn.close()
    
    if questao is None:
        return "Questão não encontrada", 404
    
    return render_template('questao.html', questao=questao)

@app.route('/responder', methods=['POST'])
def responder_questao():
    questao_id = request.form.get('questao_id')
    resposta = request.form.get('resposta')
    
    conn = get_db_connection()
    questao = conn.execute('SELECT * FROM questoes WHERE id = ?', (questao_id,)).fetchone()
    
    acerto = resposta == questao['resposta_correta']
    
    # Registrar resposta
    conn.execute('''
        INSERT INTO desempenho (questao_id, resposta_usuario, acerto)
        VALUES (?, ?, ?)
    ''', (questao_id, resposta, acerto))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        'acerto': acerto,
        'resposta_correta': questao['resposta_correta'],
        'comentario': questao['comentario']
    })

@app.route('/desempenho')
def desempenho():
    conn = get_db_connection()
    
    # Estatísticas gerais
    stats = conn.execute('''
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN acerto = 1 THEN 1 ELSE 0 END) as acertos,
            ROUND(SUM(CASE WHEN acerto = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as percentual_acerto
        FROM desempenho
    ''').fetchone()
    
    # Desempenho por disciplina
    desempenho_disciplina = conn.execute('''
        SELECT 
            q.disciplina,
            COUNT(*) as total,
            SUM(CASE WHEN d.acerto = 1 THEN 1 ELSE 0 END) as acertos,
            ROUND(SUM(CASE WHEN d.acerto = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) as percentual_acerto
        FROM desempenho d
        JOIN questoes q ON d.questao_id = q.id
        GROUP BY q.disciplina
        ORDER BY percentual_acerto DESC
    ''').fetchall()
    
    # Erros recorrentes
    erros_recorrentes = conn.execute('''
        SELECT 
            q.disciplina,
            q.nivel,
            COUNT(*) as erros,
            q.enunciado
        FROM desempenho d
        JOIN questoes q ON d.questao_id = q.id
        WHERE d.acerto = 0
        GROUP BY q.id
        HAVING erros > 1
        ORDER BY erros DESC
        LIMIT 10
    ''').fetchall()
    
    conn.close()
    
    return render_template('desempenho.html', 
                         stats=stats,
                         desempenho_disciplina=desempenho_disciplina,
                         erros_recorrentes=erros_recorrentes)

@app.route('/simulado')
def simulado():
    return render_template('simulado.html')

@app.route('/gerar_simulado', methods=['POST'])
def gerar_simulado():
    num_questoes = int(request.form.get('num_questoes', 10))
    disciplinas = request.form.getlist('disciplinas')
    niveis = request.form.getlist('niveis')
    
    conn = get_db_connection()
    
    query = 'SELECT * FROM questoes WHERE 1=1'
    params = []
    
    if disciplinas:
        placeholders = ','.join(['?' for _ in disciplinas])
        query += f' AND disciplina IN ({placeholders})'
        params.extend(disciplinas)
    
    if niveis:
        placeholders = ','.join(['?' for _ in niveis])
        query += f' AND nivel IN ({placeholders})'
        params.extend(niveis)
    
    questoes_disponiveis = conn.execute(query, params).fetchall()
    
    # Selecionar questões aleatórias
    questoes_simulado = random.sample(
        [dict(q) for q in questoes_disponiveis], 
        min(num_questoes, len(questoes_disponiveis))
    )
    
    conn.close()
    
    # Armazenar simulado na sessão
    session['simulado_atual'] = questoes_simulado
    session['simulado_index'] = 0
    
    return redirect(url_for('realizar_simulado'))

@app.route('/realizar_simulado')
def realizar_simulado():
    if 'simulado_atual' not in session:
        return redirect(url_for('simulado'))
    
    questoes = session['simulado_atual']
    index = session.get('simulado_index', 0)
    
    if index >= len(questoes):
        return redirect(url_for('resultado_simulado'))
    
    questao_atual = questoes[index]
    
    return render_template('simulado_questao.html', 
                         questao=questao_atual, 
                         numero=index + 1, 
                         total=len(questoes))

@app.route('/responder_simulado', methods=['POST'])
def responder_simulado():
    if 'simulado_atual' not in session:
        return redirect(url_for('simulado'))
    
    resposta = request.form.get('resposta')
    questao_id = request.form.get('questao_id')
    
    # Registrar resposta do simulado
    if 'respostas_simulado' not in session:
        session['respostas_simulado'] = []
    
    session['respostas_simulado'].append({
        'questao_id': questao_id,
        'resposta': resposta
    })
    
    # Avançar para próxima questão
    session['simulado_index'] = session.get('simulado_index', 0) + 1
    
    return redirect(url_for('realizar_simulado'))

@app.route('/resultado_simulado')
def resultado_simulado():
    if 'simulado_atual' not in session or 'respostas_simulado' not in session:
        return redirect(url_for('simulado'))
    
    questoes = session['simulado_atual']
    respostas = session['respostas_simulado']
    
    conn = get_db_connection()
    
    acertos = 0
    resultados = []
    
    for i, resposta in enumerate(respostas):
        questao = questoes[i]
        questao_db = conn.execute('SELECT * FROM questoes WHERE id = ?', (questao['id'],)).fetchone()
        
        acerto = resposta['resposta'] == questao_db['resposta_correta']
        if acerto:
            acertos += 1
        
        resultados.append({
            'questao': dict(questao_db),
            'resposta_usuario': resposta['resposta'],
            'acerto': acerto
        })
    
    conn.close()
    
    percentual = round((acertos / len(questoes)) * 100, 2)
    
    # Limpar sessão do simulado
    session.pop('simulado_atual', None)
    session.pop('simulado_index', None)
    session.pop('respostas_simulado', None)
    
    return render_template('resultado_simulado.html', 
                         resultados=resultados,
                         acertos=acertos,
                         total=len(questoes),
                         percentual=percentual)

# ==================== ROTAS DA IA ====================

@app.route('/ia/explicar_erro/<int:questao_id>', methods=['POST'])
def ia_explicar_erro(questao_id):
    """Rota para IA explicar erro do aluno"""
    try:
        # Obter resposta do usuário
        data = request.get_json()
        resposta_usuario = data.get('resposta_usuario', '')
        
        # Buscar questão no banco
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM questoes WHERE id = ?', (questao_id,))
        questao_data = cursor.fetchone()
        conn.close()
        
        if not questao_data:
            return jsonify({'error': 'Questão não encontrada'}), 404
        
        # Montar dicionário da questão
        questao = {
            'id': questao_data[0],
            'disciplina': questao_data[1],
            'semana': questao_data[2],
            'nivel': questao_data[3],
            'banca': questao_data[4],
            'enunciado': questao_data[5],
            'alternativas': questao_data[6],
            'resposta_correta': questao_data[7],
            'comentario': questao_data[8]
        }
        
        # Gerar explicação com IA
        explicacao = ia_service.explicar_erro(questao, resposta_usuario)
        
        # Salvar feedback da IA
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ia_feedback (questao_id, tipo, conteudo)
            VALUES (?, ?, ?)
        ''', (questao_id, 'explicacao_erro', explicacao))
        conn.commit()
        conn.close()
        
        return jsonify({
            'explicacao': explicacao,
            'status': 'sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ia/gerar_dica/<int:questao_id>', methods=['POST'])
def ia_gerar_dica(questao_id):
    """Rota para IA gerar dica de memória"""
    try:
        # Buscar questão no banco
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM questoes WHERE id = ?', (questao_id,))
        questao_data = cursor.fetchone()
        conn.close()
        
        if not questao_data:
            return jsonify({'error': 'Questão não encontrada'}), 404
        
        # Montar dicionário da questão
        questao = {
            'id': questao_data[0],
            'disciplina': questao_data[1],
            'semana': questao_data[2],
            'nivel': questao_data[3],
            'banca': questao_data[4],
            'enunciado': questao_data[5],
            'alternativas': questao_data[6],
            'resposta_correta': questao_data[7],
            'comentario': questao_data[8]
        }
        
        # Gerar dica com IA
        dica = ia_service.gerar_dica_memoria(questao)
        
        # Salvar feedback da IA
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ia_feedback (questao_id, tipo, conteudo)
            VALUES (?, ?, ?)
        ''', (questao_id, 'dica_memoria', dica))
        conn.commit()
        conn.close()
        
        return jsonify({
            'dica': dica,
            'status': 'sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ia/sugerir_revisao', methods=['POST'])
def ia_sugerir_revisao():
    """Rota para IA sugerir plano de revisão baseado em erros"""
    try:
        # Obter erros recentes do usuário
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Buscar últimas 10 respostas erradas
        cursor.execute('''
            SELECT q.* FROM desempenho d
            JOIN questoes q ON d.questao_id = q.id
            WHERE d.acerto = 0
            ORDER BY d.data_resposta DESC
            LIMIT 10
        ''')
        erros_data = cursor.fetchall()
        conn.close()
        
        # Montar lista de erros
        erros_recentes = []
        for erro_data in erros_data:
            erros_recentes.append({
                'id': erro_data[0],
                'disciplina': erro_data[1],
                'semana': erro_data[2],
                'nivel': erro_data[3],
                'banca': erro_data[4],
                'enunciado': erro_data[5],
                'alternativas': erro_data[6],
                'resposta_correta': erro_data[7],
                'comentario': erro_data[8]
            })
        
        # Gerar sugestão com IA
        sugestao = ia_service.sugerir_revisao(erros_recentes)
        
        return jsonify({
            'sugestao': sugestao,
            'total_erros': len(erros_recentes),
            'status': 'sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ia/gerar_questoes', methods=['POST'])
def ia_gerar_questoes():
    """Rota para IA gerar questões inéditas (função admin)"""
    try:
        data = request.get_json()
        disciplina = data.get('disciplina', '')
        nivel = data.get('nivel', 'Básico')
        quantidade = data.get('quantidade', 1)
        
        # Gerar questões com IA
        questoes_geradas = ia_service.gerar_questao_inedita(disciplina, nivel, quantidade)
        
        return jsonify({
            'questoes': questoes_geradas,
            'status': 'sucesso'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test_ia')
def test_ia():
    """Teste simples do serviço de IA"""
    try:
        resultado = ia_service.explicar_erro(
            {'enunciado': 'Teste', 'resposta_correta': 'A', 'comentario': 'Teste'},
            'B'
        )
        return f"IA Service funcionando: {resultado}"
    except Exception as e:
        return f"Erro no IA Service: {e}"

@app.route('/importar')
def importar():
    """Página de importação automática de questões"""
    return render_template('importar.html')

@app.route('/ia/importar_questao_texto', methods=['POST'])
def ia_importar_questao_texto():
    """Importa questão automaticamente a partir de texto colado"""
    try:
        print("DEBUG: Rota /ia/importar_questao_texto chamada")
        
        # Verificar se tem JSON
        if not request.is_json:
            print("DEBUG: Request não é JSON")
            return jsonify({'error': 'Request deve ser JSON'}), 400
        
        data = request.get_json()
        print(f"DEBUG: JSON recebido: {data}")
        
        if not data:
            print("DEBUG: JSON está vazio")
            return jsonify({'error': 'JSON está vazio'}), 400
        
        texto_questao = data.get('texto', '')
        disciplina = data.get('disciplina', 'Lei 12.550/2011')
        nivel = data.get('nivel', 'Básico')
        semana = data.get('semana', '1')
        banca = data.get('banca', 'CESPE')
        tipo = data.get('tipo', 'Múltipla Escolha')
        
        print(f"DEBUG: texto_questao: '{texto_questao[:100]}...'")
        print(f"DEBUG: disciplina: {disciplina}")
        print(f"DEBUG: nivel: {nivel}")
        print(f"DEBUG: semana: {semana}")
        print(f"DEBUG: banca: {banca}")
        print(f"DEBUG: tipo: {tipo}")
        
        if not texto_questao or texto_questao.strip() == '':
            print("DEBUG: Texto da questão está vazio")
            return jsonify({'error': 'Texto da questão não fornecido'}), 400
        
        # Importar questão usando o serviço de IA
        print("DEBUG: Chamando ia_service.importar_questao_texto")
        questao = ia_service.importar_questao_texto(texto_questao, disciplina, nivel)
        
        print(f"DEBUG: Questão parseada: {questao}")
        
        if not questao:
            print("DEBUG: Não foi possível parsear a questão")
            return jsonify({'error': 'Não foi possível parsear a questão. Verifique o formato.'}), 400
        
        # Adicionar metadados da questão
        questao['semana'] = semana
        questao['banca'] = banca
        questao['tipo'] = tipo
        
        # Armazenar temporariamente para salvar depois
        session['questao_temp'] = questao
        
        print("DEBUG: Questão importada com sucesso")
        
        return jsonify({
            'status': 'sucesso',
            'questao': questao,
            'mensagem': f'Questão importada com sucesso para {disciplina} - {nivel}'
        })
        
    except Exception as e:
        print(f"DEBUG: Exceção: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/ia/salvar_questao_importada', methods=['POST'])
def ia_salvar_questao_importada():
    """Salva a questão importada no banco de dados"""
    try:
        data = request.get_json()
        
        # Obter questão temporária da sessão
        questao_temp = session.get('questao_temp')
        if not questao_temp:
            return jsonify({'error': 'Nenhuma questão para salvar. Importe uma questão primeiro.'}), 400
        
        # Atualizar metadados com os dados do formulário
        disciplina = data.get('disciplina', questao_temp.get('disciplina', 'Lei 12.550/2011'))
        semana = data.get('semana', questao_temp.get('semana', '1'))
        banca = data.get('banca', questao_temp.get('banca', 'CESPE'))
        nivel = data.get('nivel', questao_temp.get('nivel', 'Básico'))
        tipo = data.get('tipo', questao_temp.get('tipo', 'Múltipla Escolha'))
        
        # Salvar no banco de dados
        if db_url.startswith('sqlite'):
            # SQLite local
            conn = sqlite3.connect("ebserh_study.db")
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO questoes (
                    disciplina, semana, nivel, banca, enunciado, 
                    alternativas, resposta_correta, comentario
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                disciplina,
                int(semana),
                nivel,
                banca,
                questao_temp['enunciado'],
                json.dumps(questao_temp['alternativas']),
                questao_temp['resposta'],
                questao_temp.get('comentario', 'Questão importada automaticamente')
            ))
            
            conn.commit()
            conn.close()
        else:
            # PostgreSQL via SQLAlchemy
            from sqlalchemy import text
            result = db.session.execute(text('''
                INSERT INTO questoes (
                    disciplina, semana, nivel, banca, enunciado, 
                    alternativas, resposta_correta, comentario
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''), (
                disciplina,
                int(semana),
                nivel,
                banca,
                questao_temp['enunciado'],
                json.dumps(questao_temp['alternativas']),
                questao_temp['resposta'],
                questao_temp.get('comentario', 'Questão importada automaticamente')
            ))
            db.session.commit()
        
        # Obter ID da questão inserida
        if db_url.startswith('sqlite'):
            questao_id = cursor.lastrowid
        else:
            # PostgreSQL - obter o último ID inserido
            result = db.session.execute(text('SELECT lastval()'))
            questao_id = result.scalar()
        
        # Limpar sessão
        session.pop('questao_temp', None)
        
        return jsonify({
            'status': 'sucesso',
            'questao_id': questao_id,
            'mensagem': 'Questão salva com sucesso!'
        })
        
    except Exception as e:
        print(f"DEBUG: Erro ao salvar questão: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/ia/feedback', methods=['POST'])
def ia_feedback():
    """Rota para registrar feedback do usuário sobre a IA"""
    try:
        data = request.get_json()
        questao_id = data.get('questao_id')
        tipo = data.get('tipo')  # explicacao_erro, dica_memoria, etc.
        utilidade = data.get('utilidade', 0)  # 1-5
        
        # Atualizar feedback existente ou registrar novo
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE ia_feedback 
            SET utilidade = ?
            WHERE questao_id = ? AND tipo = ?
            ORDER BY data DESC
            LIMIT 1
        ''', (utilidade, questao_id, tipo))
        
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'feedback_registrado'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ROTAS ADMIN ====================

@app.route('/admin')
def admin():
    """Painel administrativo para gerenciamento de questões"""
    return render_template('admin.html')

@app.route('/admin/adicionar_questoes', methods=['POST'])
def admin_adicionar_questoes():
    """Adiciona questões geradas pela IA ao banco"""
    try:
        data = request.get_json()
        questoes = data.get('questoes', [])
        
        if not questoes:
            return jsonify({'error': 'Nenhuma questão para adicionar'}), 400
        
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        adicionadas = 0
        for questao in questoes:
            # Validação básica
            if not all(key in questao for key in ['disciplina', 'enunciado', 'alternativas', 'resposta_correta']):
                continue
            
            # Adicionar semana padrão (última semana)
            cursor.execute('SELECT MAX(semana) FROM questoes')
            max_semana = cursor.fetchone()[0] or 12
            
            cursor.execute('''
                INSERT INTO questoes (
                    disciplina, semana, nivel, banca, enunciado, 
                    alternativas, resposta_correta, comentario, tags, dificuldade_num
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                questao['disciplina'],
                max_semana,
                questao.get('nivel', 'Básico'),
                questao.get('banca', 'IA-Gerada'),
                questao['enunciado'],
                questao['alternativas'],
                questao['resposta_correta'],
                questao.get('comentario', 'Questão gerada por IA'),
                f"IA-gerada,{questao.get('disciplina', '').lower().replace(' ', '_')}",
                3 if questao.get('nivel') == 'Pegadinha' else 2 if questao.get('nivel') == 'Alto' else 1
            ))
            adicionadas += 1
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'sucesso',
            'adicionadas': adicionadas,
            'total_recebidas': len(questoes)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/estatisticas')
def api_estatisticas():
    """API para estatísticas do banco de questões"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Total de questões
        cursor.execute('SELECT COUNT(*) FROM questoes')
        total_questoes = cursor.fetchone()[0]
        
        # Questões geradas por IA
        cursor.execute('SELECT COUNT(*) FROM questoes WHERE banca = "IA-Gerada"')
        questoes_ia = cursor.fetchone()[0]
        
        # Número de disciplinas
        cursor.execute('SELECT COUNT(DISTINCT disciplina) FROM questoes')
        disciplinas = cursor.fetchone()[0]
        
        # Questões pegadinha
        cursor.execute('SELECT COUNT(*) FROM questoes WHERE nivel = "Pegadinha"')
        pegadinhas = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_questoes': total_questoes,
            'questoes_ia': questoes_ia,
            'disciplinas': disciplinas,
            'pegadinhas': pegadinhas
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/admin/limpar_questoes_ia', methods=['POST'])
def admin_limpar_questoes_ia():
    """Remove questões geradas por IA (função de limpeza)"""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM questoes WHERE banca = "IA-Gerada"')
        removidas = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'status': 'sucesso',
            'removidas': removidas
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
