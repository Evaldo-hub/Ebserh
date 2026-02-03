"""
App Flask para produção - EBSERH TI Study App
Versão otimizada para Render.com com PostgreSQL
"""

import os
import json
from datetime import datetime
import logging
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory

# Configurações
from config import get_config
from database import init_db, execute_query, execute_update, get_db_connection

# Importar serviço de IA
from ia_service import ia_service

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Criar app Flask
app = Flask(__name__)

# Carregar configuração
config = get_config()
app.config.from_object(config)

# Custom Jinja2 filter
@app.template_filter('from_json')
def from_json(value):
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return {}

# Função auxiliar para converter Row para dict
def row_to_dict(row):
    """Converte Row/RealDictRow para dicionário"""
    if hasattr(row, 'keys'):
        return {key: row[key] for key in row.keys()}
    elif hasattr(row, '__dict__'):
        return row.__dict__
    else:
        return dict(row)

# ==================== ROTAS PRINCIPAIS ====================

@app.route('/')
def index():
    """Página inicial"""
    try:
        # Estatísticas básicas
        stats = execute_query("""
            SELECT 
                COUNT(DISTINCT disciplina) as disciplinas,
                COUNT(*) as total_questoes,
                COUNT(CASE WHEN nivel = 'Pegadinha' THEN 1 END) as pegadinhas
            FROM questoes
        """, fetch_one=True)
        
        return render_template('index.html', stats=stats or {})
    except Exception as e:
        logger.error(f"Erro na página inicial: {e}")
        return render_template('index.html', stats={})

@app.route('/plano')
def plano():
    """Plano de estudos"""
    try:
        plano_data = execute_query("""
            SELECT semana, conteudo, disciplinas 
            FROM plano_estudos 
            ORDER BY semana
        """)
        
        return render_template('plano.html', plano=plano_data or [])
    except Exception as e:
        logger.error(f"Erro no plano: {e}")
        return render_template('plano.html', plano=[])

@app.route('/questoes')
def questoes():
    """Lista de questões"""
    try:
        disciplina = request.args.get('disciplina')
        nivel = request.args.get('nivel')
        
        query = "SELECT * FROM questoes WHERE 1=1"
        params = []
        
        if disciplina:
            query += " AND disciplina = ?"
            params.append(disciplina)
        
        if nivel:
            query += " AND nivel = ?"
            params.append(nivel)
        
        query += " ORDER BY disciplina, semana, nivel"
        
        questoes_data = execute_query(query, params)
        
        # Converter para lista de dicionários
        questoes_list = [row_to_dict(q) for q in questoes_data] if questoes_data else []
        
        return render_template('questoes.html', questoes=questoes_list)
    except Exception as e:
        logger.error(f"Erro nas questões: {e}")
        return render_template('questoes.html', questoes=[])

@app.route('/questao/<int:questao_id>')
def questao(questao_id):
    """Visualizar questão específica"""
    try:
        questao_data = execute_query(
            "SELECT * FROM questoes WHERE id = ?", 
            [questao_id], 
            fetch_one=True
        )
        
        if not questao_data:
            return redirect(url_for('questoes'))
        
        questao_dict = row_to_dict(questao_data)
        
        return render_template('questao.html', questao=questao_dict)
    except Exception as e:
        logger.error(f"Erro na questão: {e}")
        return redirect(url_for('questoes'))

@app.route('/responder_questao/<int:questao_id>', methods=['POST'])
def responder_questao(questao_id):
    """Processar resposta da questão"""
    try:
        resposta = request.form.get('resposta')
        
        # Verificar resposta correta
        questao_data = execute_query(
            "SELECT resposta_correta FROM questoes WHERE id = ?", 
            [questao_id], 
            fetch_one=True
        )
        
        if not questao_data:
            return jsonify({'error': 'Questão não encontrada'}), 404
        
        acerto = resposta == questao_data['resposta_correta']
        
        # Salvar desempenho
        execute_update("""
            INSERT INTO desempenho (questao_id, resposta_usuario, acerto, usuario_id)
            VALUES (?, ?, ?, ?)
        """, [questao_id, resposta, acerto, session.get('user_id', 'anonymous')])
        
        return jsonify({
            'acerto': acerto,
            'resposta_correta': questao_data['resposta_correta']
        })
        
    except Exception as e:
        logger.error(f"Erro ao responder questão: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/simulado')
def simulado():
    """Página de simulado"""
    return render_template('simulado.html')

@app.route('/gerar_simulado', methods=['POST'])
def gerar_simulado():
    """Gerar simulado personalizado"""
    try:
        data = request.get_json()
        quantidade = data.get('quantidade', 10)
        disciplinas = data.get('disciplinas', [])
        niveis = data.get('niveis', ['Básico', 'Alto', 'Pegadinha'])
        
        query = "SELECT * FROM questoes WHERE nivel IN ({})".format(
            ','.join(['?' for _ in niveis])
        )
        params = niveis.copy()
        
        if disciplinas:
            query += " AND disciplina IN ({})".format(
                ','.join(['?' for _ in disciplinas])
            )
            params.extend(disciplinas)
        
        query += " ORDER BY RANDOM() LIMIT ?"
        params.append(quantidade)
        
        # Para PostgreSQL, usar ORDER BY RANDOM()
        # Para SQLite, também funciona
        
        questoes_data = execute_query(query, params)
        questoes_list = [row_to_dict(q) for q in questoes_data] if questoes_data else []
        
        return jsonify({
            'status': 'sucesso',
            'questoes': questoes_list
        })
        
    except Exception as e:
        logger.error(f"Erro ao gerar simulado: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/desempenho')
def desempenho():
    """Página de desempenho"""
    try:
        user_id = session.get('user_id', 'anonymous')
        
        # Estatísticas do usuário
        stats = execute_query("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN acerto = TRUE THEN 1 END) as acertos,
                COUNT(CASE WHEN acerto = FALSE THEN 1 END) as erros,
                ROUND(COUNT(CASE WHEN acerto = TRUE THEN 1 END) * 100.0 / COUNT(*), 2) as taxa_acerto
            FROM desempenho 
            WHERE usuario_id = ?
        """, [user_id], fetch_one=True)
        
        # Desempenho por disciplina
        desempenho_disciplina = execute_query("""
            SELECT 
                q.disciplina,
                COUNT(*) as total,
                COUNT(CASE WHEN d.acerto = TRUE THEN 1 END) as acertos
            FROM desempenho d
            JOIN questoes q ON d.questao_id = q.id
            WHERE d.usuario_id = ?
            GROUP BY q.disciplina
            ORDER BY acertos DESC
        """, [user_id])
        
        # Últimas questões
        ultimas_questoes = execute_query("""
            SELECT 
                q.disciplina,
                q.nivel,
                d.acerto,
                d.data_resposta
            FROM desempenho d
            JOIN questoes q ON d.questao_id = q.id
            WHERE d.usuario_id = ?
            ORDER BY d.data_resposta DESC
            LIMIT 10
        """, [user_id])
        
        return render_template(
            'desempenho.html',
            stats=stats or {},
            desempenho_disciplina=[row_to_dict(d) for d in desempenho_disciplina] if desempenho_disciplina else [],
            ultimas_questoes=[row_to_dict(u) for u in ultimas_questoes] if ultimas_questoes else []
        )
        
    except Exception as e:
        logger.error(f"Erro no desempenho: {e}")
        return render_template('desempenho.html', stats={})

# ==================== ROTAS DE IA ====================

@app.route('/ia/explicar_erro/<int:questao_id>', methods=['POST'])
def ia_explicar_erro(questao_id):
    """IA explica erro do aluno"""
    try:
        data = request.get_json()
        resposta_usuario = data.get('resposta_usuario')
        
        # Obter dados da questão
        questao_data = execute_query(
            "SELECT * FROM questoes WHERE id = ?", 
            [questao_id], 
            fetch_one=True
        )
        
        if not questao_data:
            return jsonify({'error': 'Questão não encontrada'}), 404
        
        questao_dict = row_to_dict(questao_data)
        
        # Gerar explicação com IA
        explicacao = ia_service.explicar_erro(questao_dict, resposta_usuario)
        
        # Salvar feedback
        execute_update("""
            INSERT INTO ia_feedback (questao_id, usuario_id, tipo, conteudo)
            VALUES (?, ?, 'explicacao_erro', ?)
        """, [questao_id, session.get('user_id', 'anonymous'), explicacao])
        
        return jsonify({
            'status': 'sucesso',
            'explicacao': explicacao
        })
        
    except Exception as e:
        logger.error(f"Erro na IA explicação: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/ia/gerar_dica/<int:questao_id>', methods=['POST'])
def ia_gerar_dica(questao_id):
    """IA gera dica de memória"""
    try:
        # Obter dados da questão
        questao_data = execute_query(
            "SELECT * FROM questoes WHERE id = ?", 
            [questao_id], 
            fetch_one=True
        )
        
        if not questao_data:
            return jsonify({'error': 'Questão não encontrada'}), 404
        
        questao_dict = row_to_dict(questao_data)
        
        # Gerar dica com IA
        dica = ia_service.gerar_dica_memoria(questao_dict)
        
        # Salvar feedback
        execute_update("""
            INSERT INTO ia_feedback (questao_id, usuario_id, tipo, conteudo)
            VALUES (?, ?, 'dica_memoria', ?)
        """, [questao_id, session.get('user_id', 'anonymous'), dica])
        
        return jsonify({
            'status': 'sucesso',
            'dica': dica
        })
        
    except Exception as e:
        logger.error(f"Erro na IA dica: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/ia/sugerir_revisao', methods=['POST'])
def ia_sugerir_revisao():
    """IA sugere plano de revisão"""
    try:
        user_id = session.get('user_id', 'anonymous')
        
        # Obter erros recentes do usuário
        erros_data = execute_query("""
            SELECT q.disciplina, q.nivel, q.enunciado, q.comentario
            FROM desempenho d
            JOIN questoes q ON d.questao_id = q.id
            WHERE d.usuario_id = ? AND d.acerto = FALSE
            ORDER BY d.data_resposta DESC
            LIMIT 10
        """, [user_id])
        
        erros_list = [row_to_dict(e) for e in erros_data] if erros_data else []
        
        # Gerar sugestão com IA
        sugestao = ia_service.sugerir_revisao(erros_list)
        
        return jsonify({
            'status': 'sucesso',
            'sugestao': sugestao
        })
        
    except Exception as e:
        logger.error(f"Erro na IA revisão: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/ia/gerar_questoes', methods=['POST'])
def ia_gerar_questoes():
    """IA gera questões inéditas"""
    try:
        data = request.get_json()
        disciplina = data.get('disciplina')
        nivel = data.get('nivel')
        quantidade = data.get('quantidade', 5)
        
        # Gerar questões com IA
        questoes_geradas = ia_service.gerar_questao_inedita(disciplina, nivel, quantidade)
        
        return jsonify({
            'status': 'sucesso',
            'questoes': questoes_geradas
        })
        
    except Exception as e:
        logger.error(f"Erro na IA geração: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/ia/feedback', methods=['POST'])
def ia_feedback():
    """Recebe feedback sobre respostas da IA"""
    try:
        data = request.get_json()
        questao_id = data.get('questao_id')
        tipo = data.get('tipo')
        utilidade = data.get('utilidade', 0)
        
        # Atualizar feedback existente ou criar novo
        execute_update("""
            INSERT INTO ia_feedback (questao_id, usuario_id, tipo, utilidade)
            VALUES (?, ?, ?, ?)
        """, [questao_id, session.get('user_id', 'anonymous'), tipo, utilidade])
        
        return jsonify({'status': 'sucesso'})
        
    except Exception as e:
        logger.error(f"Erro no feedback IA: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== ROTAS ADMIN ====================

@app.route('/admin')
def admin():
    """Painel administrativo"""
    return render_template('admin.html')

@app.route('/admin/adicionar_questoes', methods=['POST'])
def admin_adicionar_questoes():
    """Adiciona questões geradas pela IA ao banco"""
    try:
        data = request.get_json()
        questoes = data.get('questoes', [])
        
        adicionadas = 0
        for questao in questoes:
            try:
                execute_update("""
                    INSERT INTO questoes 
                    (disciplina, semana, nivel, banca, enunciado, alternativas, 
                     resposta_correta, comentario, tags, dificuldade_num, ia_generated)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    questao.get('disciplina'),
                    questao.get('semana', 1),
                    questao.get('nivel'),
                    questao.get('banca', 'IA-Gerada'),
                    questao.get('enunciado'),
                    questao.get('alternativas'),
                    questao.get('resposta_correta'),
                    questao.get('comentario'),
                    questao.get('tags', 'IA-gerada'),
                    questao.get('dificuldade_num', 1),
                    True
                ])
                adicionadas += 1
            except Exception as e:
                logger.error(f"Erro ao adicionar questão: {e}")
                continue
        
        return jsonify({
            'status': 'sucesso',
            'adicionadas': adicionadas
        })
        
    except Exception as e:
        logger.error(f"Erro ao adicionar questões: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/estatisticas')
def api_estatisticas():
    """API de estatísticas do banco"""
    try:
        stats = execute_query("""
            SELECT 
                COUNT(*) as total_questoes,
                COUNT(CASE WHEN ia_generated = TRUE THEN 1 END) as questoes_ia,
                COUNT(DISTINCT disciplina) as disciplinas,
                COUNT(CASE WHEN nivel = 'Pegadinha' THEN 1 END) as pegadinhas
            FROM questoes
        """, fetch_one=True)
        
        return jsonify(row_to_dict(stats) if stats else {})
        
    except Exception as e:
        logger.error(f"Erro nas estatísticas: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/admin/limpar_questoes_ia', methods=['POST'])
def admin_limpar_questoes_ia():
    """Remove questões geradas por IA"""
    try:
        removidas = execute_update(
            "DELETE FROM questoes WHERE ia_generated = TRUE"
        )
        
        return jsonify({
            'status': 'sucesso',
            'removidas': removidas
        })
        
    except Exception as e:
        logger.error(f"Erro ao limpar questões IA: {e}")
        return jsonify({'error': str(e)}), 500

# ==================== ROTAS PWA ====================

@app.route('/manifest.json')
def manifest():
    """Serve manifest.json"""
    return send_from_directory('.', 'manifest.json', mimetype='application/json')

@app.route('/browserconfig.xml')
def browserconfig():
    """Serve browserconfig.xml"""
    return send_from_directory('.', 'browserconfig.xml', mimetype='application/xml')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve arquivos estáticos"""
    return send_from_directory('static', filename)

@app.route('/health')
def health_check():
    """Health check para Render"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

# ==================== INICIALIZAÇÃO ====================

def initialize():
    """Inicializa banco de dados"""
    try:
        init_db()
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco: {e}")

# Inicializar banco ao iniciar o app
with app.app_context():
    initialize()

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Erro 500: {error}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Inicializar banco
    init_db()
    
    # Porta do Render ou padrão
    port = int(os.environ.get('PORT', 5000))
    
    # Iniciar app
    app.run(host='0.0.0.0', port=port, debug=False)
