from Leitor import Leitor
from src.operacoes import remover_simbolos_improdutivos

leitor = Leitor('../Testes/Inuteis/Inuteis1.txt')
glc1 = leitor.ler_arquivo()
print(f'\n\n====> Remoção de improdutivos da GLC abaixo, lida do arquivo`{leitor.arquivo}`')
glc1.display()
remover_simbolos_improdutivos(glc1)
print('\n====> Saída:')
glc1.display()


leitor.arquivo = '../Testes/Inuteis/Inuteis2.txt'
glc2 = leitor.ler_arquivo()
print(f'\n\n====> Remoção de improdutivos da GLC abaixo, lida do arquivo`{leitor.arquivo}`')
glc2.display()
remover_simbolos_improdutivos(glc2)
print('\n====> Saída:')
glc2.display()


leitor.arquivo = '../Testes/Inuteis/Inuteis3.txt'
glc3 = leitor.ler_arquivo()
print(f'\n\n====> Remoção de improdutivos da GLC abaixo, lida do arquivo`{leitor.arquivo}`')
glc3.display()
remover_simbolos_improdutivos(glc3)
print('\n====> Saída:')
glc3.display()

