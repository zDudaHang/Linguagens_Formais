from Leitor import Leitor
from src.operacoes_automatos_gr import afnd_para_afd

leitor = Leitor('../Testes/Determinizacao/Automato1.txt')
automato1 = leitor.ler_arquivo()
afnd_para_afd(automato1)
