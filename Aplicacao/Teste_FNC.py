from Leitor import Leitor
from src.operacoes import transformar_em_fnc

input_file = '../Testes/Producoes_Vazias/Vazio1.txt'
leitor = Leitor(input_file)
glc1 = leitor.ler_arquivo()
print(f'\n\n====> Transformação em FNC para a GLC abaixo, lida do arquivo `{leitor.arquivo}`')
glc1.display()
transformar_em_fnc(glc1)
print('\n====> Saída:')
glc1.display()

input_file = '../Testes/Producoes_Vazias/Vazio2.txt'
leitor.arquivo = input_file
glc2 = leitor.ler_arquivo()
print(f'\n\n====> Transformação em FNC para a GLC abaixo, lida do arquivo `{leitor.arquivo}`')
glc2.display()
transformar_em_fnc(glc2)
print('\n====> Saída:')
glc2.display()
