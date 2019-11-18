from structures.GLC import GLC
from Leitor import Leitor
from src.operacoes import remover_simbolos_improdutivos

leitor = Leitor('../Testes/Inuteis/Inuteis1.txt')
glc = leitor.ler_arquivo()
remover_simbolos_improdutivos(glc)

leitor.arquivo = '../Testes/Inuteis/Inuteis2.txt'
glc2 = leitor.ler_arquivo()
remover_simbolos_improdutivos(glc2)