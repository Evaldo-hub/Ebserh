import sqlite3

def excluir_questoes_incompletas():
    """Exclui questões com enunciados muito curtos (incompletos)"""
    
    conn = sqlite3.connect('ebserh_study.db')
    cursor = conn.cursor()
    
    # Buscar questões com enunciados muito curtos (menos de 50 caracteres)
    cursor.execute('''
        SELECT id, disciplina, enunciado, LENGTH(enunciado) as tamanho
        FROM questoes 
        WHERE LENGTH(enunciado) < 50
        ORDER BY id DESC
    ''')
    
    questoes_problematicas = cursor.fetchall()
    
    if not questoes_problematicas:
        print("Nenhuma questão com enunciado incompleto encontrada.")
        return
    
    print(f"Encontradas {len(questoes_problematicas)} questões com enunciados incompletos:")
    print("=" * 70)
    
    # Mostrar as questões que serão excluídas
    for questao in questoes_problematicas:
        print(f"ID: {questao[0]} | Disciplina: {questao[1]} | Tamanho: {questao[3]} chars")
        print(f"Enunciado: \"{questao[2]}\"")
        print("-" * 50)
    
    # Confirmar exclusão
    confirmacao = input(f"\nDeseja excluir estas {len(questoes_problematicas)} questões? (S/N): ").strip().upper()
    
    if confirmacao == 'S':
        # Excluir as questões
        ids_para_excluir = [str(questao[0]) for questao in questoes_problematicas]
        
        cursor.execute(f'''
            DELETE FROM questoes 
            WHERE id IN ({','.join(ids_para_excluir)})
        ''')
        
        # Também excluir registros de desempenho relacionados
        cursor.execute(f'''
            DELETE FROM desempenho 
            WHERE questao_id IN ({','.join(ids_para_excluir)})
        ''')
        
        conn.commit()
        print(f"\n{len(questoes_problematicas)} questoes excluidas com sucesso!")
        
        # Verificar quantas restaram
        cursor.execute('SELECT COUNT(*) FROM questoes')
        total_restantes = cursor.fetchone()[0]
        print(f"Total de questoes restantes: {total_restantes}")
        
    else:
        print("\nOperacao cancelada.")
    
    conn.close()

if __name__ == "__main__":
    excluir_questoes_incompletas()
