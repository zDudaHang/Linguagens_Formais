'''
Este teste usa três exemplos de autômatos finitos, os converte para gramaticas regulares
e converte de volta para autômato finito.
'''

from Leitor import Leitor
from src.operacoes_automatos_gr import af_para_gr, gr_para_af

leitor = Leitor('../Testes/AFD_para_GR_para_AFD/teste1afd_para_gr_para_afd.txt')
automato1 = leitor.ler_arquivo()
print(f'\n\n====> Teste de conversão de AF para GR para o AF abaixo, lido do arquivo `{leitor.arquivo}`')
automato1.display()

gr1 = af_para_gr(automato1)
print('\n====> Saída de AF para GR')
gr1.display()

af1 = gr_para_af(gr1)
print('\n====> Saída, voltando para AF')
af1.display()

leitor.arquivo = '../Testes/AFD_para_GR_para_AFD/teste2afd_para_gr_para_afd.txt'
automato2 = leitor.ler_arquivo()
print(f'\n\n====> Teste de conversão de AF para GR para o AF abaixo, lido do arquivo `{leitor.arquivo}`')
automato2.display()

gr2 = af_para_gr(automato2)
print('\n====> Saída de AF para GR')
gr2.display()

af2 = gr_para_af(gr2)
print('\n====> Saída, voltando para AF')
af2.display()

leitor.arquivo = '../Testes/AFD_para_GR_para_AFD/teste3afd_para_gr_para_afd.txt'
automato3 = leitor.ler_arquivo()
print(f'\n\n====> Teste de conversão de AF para GR para o AF abaixo, lido do arquivo `{leitor.arquivo}`')
automato3.display()

gr3 = af_para_gr(automato3)
print('\n====> Saída de AF para GR')
gr3.display()

af3 = gr_para_af(gr3)
print('\n====> Saída, voltando para AF')
af3.display()
