from Leitor import Leitor
from src.operacoes_automatos_gr import er_para_afd

leitor = Leitor('../Testes/ER_AFD/ER1.txt')
er1 = leitor.ler_arquivo()

af1 = er_para_afd(er1)
af1.display()

leitor.arquivo = '../Testes/ER_AFD/ER2.txt'
er2 = leitor.ler_arquivo()

af2 = er_para_afd(er2)
af2.display()

leitor.arquivo = '../Testes/ER_AFD/ER3.txt'
er3 = leitor.ler_arquivo()

af3 = er_para_afd(er3)
af3.display()
