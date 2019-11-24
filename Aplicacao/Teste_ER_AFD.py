from Leitor import Leitor
from src.operacoes_automatos_gr import er_para_afd

leitor = Leitor('../Testes/ER_AFD/ER1.txt')
er1 = leitor.ler_arquivo()
print(f'\n\n====> Testando conversão de ER para AF com a ER abaixo, lida do arquivo `{leitor.arquivo}`')
er1.display()

af1 = er_para_afd(er1)
print('\n====> Saída:')
af1.display()

leitor.arquivo = '../Testes/ER_AFD/ER2.txt'
er2 = leitor.ler_arquivo()
print(f'\n\n====> Testando conversão de ER para AF com a ER abaixo, lida do arquivo `{leitor.arquivo}`')
er2.display()

af2 = er_para_afd(er2)
print('\n====> Saída:')
af2.display()

leitor.arquivo = '../Testes/ER_AFD/ER3.txt'
er3 = leitor.ler_arquivo()
print(f'\n\n====> Testando conversão de ER para AF com a ER abaixo, lida do arquivo `{leitor.arquivo}`')
er3.display()

af3 = er_para_afd(er3)
print('\n====> Saída:')
af3.display()
