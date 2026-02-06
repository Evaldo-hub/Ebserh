import sqlite3

conn = sqlite3.connect('ebserh_study.db')
cursor = conn.cursor()

# Buscar especificamente por questões com 'O Decreto n' que estejam claramente cortadas
cursor.execute("SELECT id, disciplina, enunciado, LENGTH(enunciado) as tamanho FROM questoes WHERE enunciado LIKE 'O Decreto n%' ORDER BY id DESC")

questoes_decreto = cursor.fetchall()

if questoes_decreto:
    print('Questões com Decreto (verificando se estão completas):')
    print('=' * 60)
    for questao in questoes_decreto:
        print(f'ID: {questao[0]} | Tamanho: {questao[3]} chars')
        print(f'Enunciado completo: {questao[2]}')
        print('-' * 40)
else:
    print('Nenhuma questão com O Decreto n encontrada.')

# Verificar status geral
cursor.execute('SELECT COUNT(*) FROM questoes')
total = cursor.fetchone()[0]

cursor.execute('SELECT COUNT(*) FROM questoes WHERE LENGTH(enunciado) < 50')
muito_curtas = cursor.fetchone()[0]

print(f'\nRESUMO:')
print(f'Total de questões: {total}')
print(f'Questões muito curtas (< 50 chars): {muito_curtas}')

conn.close()
