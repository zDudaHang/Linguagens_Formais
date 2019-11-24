from Leitor import Leitor
from src.operacoes_reconhecimento_ap import criar_tabela_de_analise

leitor = Leitor('../Testes/Analise_Sintatica/GLC1.txt')
glc1 = leitor.ler_arquivo()
print(f'\n\n====> Reconhecimento de sentença para a GLC abaixo, lido do arquivo `{leitor.arquivo}`')
glc1.display()

print('\n====> Saídas:')
print(f'Sentença: idvid^id\nResultado: {glc1.reconhecer("idvid^id")}')
print(f'Sentença: idvid\nResultado: {glc1.reconhecer("idvid")}')
print(f'Sentença: idvid^\nResultado: {glc1.reconhecer("idvid^")}')
print(f'Sentença: !id^idvid\nResultado: {glc1.reconhecer("!id^idvid")}')

leitor.arquivo = '../Testes/Analise_Sintatica/GLC2.txt'
glc2 = leitor.ler_arquivo()
print(f'\n\n====> Reconhecimento de sentença para a GLC abaixo, lido do arquivo `{leitor.arquivo}`')
glc2.display()

print('\n====> Saídas:')
print(f'Sentença: abdc\nResultado: {glc2.reconhecer("abdc")}')

leitor.arquivo = '../Testes/Analise_Sintatica/GLC3.txt'
glc3 = leitor.ler_arquivo()
print(f'\n\n====> Reconhecimento de sentença para a GLC abaixo, lido do arquivo `{leitor.arquivo}`')
glc3.display()

print('\n====> Saídas:')
print(f'Sentença: a\nResultado: {glc3.reconhecer("a")}')
print(f'Sentença: (a)\nResultado: {glc3.reconhecer("(a)")}')
print(f'Sentença: ((a,a),a,(a))\nResultado: {glc3.reconhecer("((a,a),a,(a))")}')
print(f'Sentença: (a,a)a\nResultado: {glc3.reconhecer("(a,a)a")}')

leitor.arquivo = '../Testes/Analise_Sintatica/GLC4.txt'
glc4 = leitor.ler_arquivo()
print(f'\n\n====> Reconhecimento de sentença para a GLC abaixo, lido do arquivo `{leitor.arquivo}`')
glc4.display()

print('\n====> Saídas:')
print(f'Sentença: a\nResultado: {glc4.reconhecer("a")}')

leitor.arquivo = '../Testes/Analise_Sintatica/GLC5.txt'
glc5 = leitor.ler_arquivo()
print(f'\n\n====> Reconhecimento de sentença para a GLC abaixo, lido do arquivo `{leitor.arquivo}`')
glc5.display()

print('\n====> Saídas:')
print(f'Sentença: 01\nResultado: {glc5.reconhecer("01")}')

leitor.arquivo = '../Testes/Analise_Sintatica/GLC6.txt'
glc6 = leitor.ler_arquivo()
print(f'\n\n====> Reconhecimento de sentença para a GLC abaixo, lido do arquivo `{leitor.arquivo}`')
glc6.display()

print('\n====> Saídas:')
print(f'Sentença: 01\nResultado: {glc6.reconhecer("01")}')
