from Leitor import Leitor
from src.operacoes_glc import remover_producoes_por_epsilon, remover_producoes_unitarias
#
# leitor = Leitor('../Testes/Producoes_Vazias/Vazio1.txt')
# glc1 = leitor.ler_arquivo()
# remover_producoes_por_epsilon(glc1)
# print("\n----> UNITÁRIAS:")
# remover_producoes_unitarias(glc1)
# print("-----------------------------------------------------------")

# leitor.arquivo = '../Testes/Producoes_Vazias/Vazio2.txt'
# glc2 = leitor.ler_arquivo()
# remover_producoes_por_epsilon(glc2)
# print("\n----> UNITÁRIAS:")
# remover_producoes_unitarias(glc2)
#
# print("-----------------------------------------------------------")
#
# leitor.arquivo = '../Testes/Producoes_Vazias/Vazio3.txt'
# glc3 = leitor.ler_arquivo()
# remover_producoes_por_epsilon(glc3)
# print("\n----> UNITÁRIAS:")
# remover_producoes_unitarias(glc3)

leitor = Leitor('../Testes/Producoes_Vazias/Vazio4.txt')
glc1 = leitor.ler_arquivo()
remover_producoes_por_epsilon(glc1)
