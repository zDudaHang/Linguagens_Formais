from Leitor import Leitor
from src.operacoes import remover_inalcancaveis_glc

leitor = Leitor('../Testes/Inuteis/Inuteis1.txt')
glc1 = leitor.ler_arquivo()
remover_inalcancaveis_glc(glc1)

leitor.arquivo = '../Testes/Inuteis/Inuteis2.txt'
glc2 = leitor.ler_arquivo()
remover_inalcancaveis_glc(glc2)
