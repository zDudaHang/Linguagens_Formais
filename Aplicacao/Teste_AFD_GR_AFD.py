from Leitor import Leitor
from src.operacoes_automatos_gr import af_para_gr, gr_para_af

leitor = Leitor('../Testes/AFD_para_GR_para_AFD/Automato1.txt')
automato1 = leitor.ler_arquivo()
automato1.display()

gr1 = af_para_gr(automato1)
gr1.display()

af1 = gr_para_af(gr1)
af1.display()

leitor.arquivo = '../Testes/AFD_para_GR_para_AFD/Automato2.txt'
automato2 = leitor.ler_arquivo()
automato2.display()

gr2 = af_para_gr(automato2)
gr2.display()

af2 = gr_para_af(gr2)
af2.display()

leitor.arquivo = '../Testes/AFD_para_GR_para_AFD/Automato3.txt'
automato3 = leitor.ler_arquivo()
automato3.display()

gr3 = af_para_gr(automato3)
gr3.display()

af3 = gr_para_af(gr3)
af3.display()
