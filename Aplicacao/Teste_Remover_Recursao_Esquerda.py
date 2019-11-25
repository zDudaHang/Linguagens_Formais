'''
Testa remoção de recursão a esquerda de gramáticas
'''

from structures import GLC
from Leitor import Leitor
from src.operacoes_glc import remover_recursao_esquerda_direta, remover_recursao_esquerda_indireta

input_file = '../Testes/Recursao_Esquerda/teste1rec_direta.txt'
glc = Leitor(input_file).ler_arquivo()
print(f'\n\n===> Removendo recursão direta da GLC abaixo, lida de `{input_file}`:')
glc.display()

glc = remover_recursao_esquerda_direta(glc)

print('\n===> Saída::')
glc.display()

input_file = '../Testes/Recursao_Esquerda/teste1rec_indireta.txt'
glc = Leitor(input_file).ler_arquivo()
print(f'\n\n===> Removendo recursão indireta da GLC abaixo, lida de `{input_file}`:')
glc.display()

glc = remover_recursao_esquerda_indireta(glc)

print('\n===> Saída::')
glc.display()

print(f'\n\n====> Removendo recursão direta da GLC gerada pela remoção de indireta acima:')
glc = remover_recursao_esquerda_direta(glc)
print('\n====> Saída:')
glc.display()