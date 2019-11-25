'''
Testa remoção de produções vazias e unitárias de gramáticas
'''

from Leitor import Leitor
from src.operacoes_glc import remover_producoes_por_epsilon, remover_producoes_unitarias

leitor = Leitor('../Testes/Producoes_Vazias/teste1fnc.txt')
glc1 = leitor.ler_arquivo()
print(f'\n\nTestando remoção de produções vazias e unitárias para a GLC abaixo, lida do arquivo `{leitor.arquivo}`')
glc1.display()
remover_producoes_por_epsilon(glc1)

remover_producoes_unitarias(glc1)
print('\n====> Saída:')
glc1.display()

leitor.arquivo = '../Testes/Producoes_Vazias/teste2fnc.txt'
glc2 = leitor.ler_arquivo()
print(f'\n\nTestando remoção de produções vazias e unitárias para a GLC abaixo, lida do arquivo `{leitor.arquivo}`')
glc2.display()
remover_producoes_por_epsilon(glc2)
remover_producoes_unitarias(glc2)
print('\n====> Saída:')
glc2.display()

leitor.arquivo = '../Testes/Producoes_Vazias/teste3fnc.txt'
glc3 = leitor.ler_arquivo()
print(f'\n\nTestando remoção de produções vazias e unitárias para a GLC abaixo, lida do arquivo `{leitor.arquivo}`')
glc3.display()
remover_producoes_por_epsilon(glc3)
remover_producoes_unitarias(glc3)
print('\n====> Saída:')
glc3.display()