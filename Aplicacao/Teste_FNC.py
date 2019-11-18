from Leitor import Leitor
from src.operacoes import transformar_em_fnc

leitor = Leitor('../Testes/Producoes_Vazias/Vazio1.txt')
glc1 = leitor.ler_arquivo()
glc1.display()
transformar_em_fnc(glc1)

leitor.arquivo = '../Testes/Producoes_Vazias/Vazio2.txt'
glc2 = leitor.ler_arquivo()
glc2.display()
transformar_em_fnc(glc2)
