'''
Testa algoritmos para remoção de simbolos inalcançáveis de gramáticas
'''

from Leitor import Leitor
from src.operacoes import remover_inalcancaveis_glc

leitor = Leitor('../Testes/Inuteis/teste1simbolos_inuteis.txt')
glc1 = leitor.ler_arquivo()
print(f"\n\n====> Remoção de símbolos inúteis para a GLC abaixo, lida do arquivo `{leitor.arquivo}`:")
glc1.display()
remover_inalcancaveis_glc(glc1)
print('\n====> Saída:')
glc1.display()

leitor.arquivo = '../Testes/Inuteis/teste2simbolos_inuteis.txt'
glc2 = leitor.ler_arquivo()
print(f"\n\n====> Remoção de símbolos inúteis para a GLC abaixo, lida do arquivo `{leitor.arquivo}`:")
glc2.display()
remover_inalcancaveis_glc(glc2)
print('\n====> Saída:')
glc2.display()

leitor.arquivo = '../Testes/Inuteis/teste3simbolos_inuteis.txt'
glc3 = leitor.ler_arquivo()
print(f"\n\n====> Remoção de símbolos inúteis para a GLC abaixo, lida do arquivo `{leitor.arquivo}`:")
glc3.display()
remover_inalcancaveis_glc(glc3)
print('\n====> Saída:')
glc3.display()
