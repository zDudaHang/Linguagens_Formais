from structures.AutomatoFinito import AutomatoFinito
from Leitor import Leitor
from src.operacoes import minimizar,remover_inalcancaveis,remover_mortos,remover_equivalentes

leitor = Leitor('../Testes/Minimizacao/1.txt')
af1 = leitor.ler_arquivo()
minimizar(af1)

print("-----------------------------------------------------------")

leitor.arquivo = '../Testes/Minimizacao/2.txt'
af2 = leitor.ler_arquivo()
minimizar(af2)
