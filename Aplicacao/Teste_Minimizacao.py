'''
Teste algoritmo de minimizaçãod e autômatos finitos
'''

from Leitor import Leitor
from src.operacoes_automatos_gr import minimizar

leitor = Leitor('../Testes/Minimizacao/teste1minimizacao.txt')
af1 = leitor.ler_arquivo()
print(f"\n\n====> Minimização para o AF abaixo, lido do arquivo `{leitor.arquivo}`:")
af1.display()
minimizar(af1)
print('\n====> Saída:')
af1.display()


leitor.arquivo = '../Testes/Minimizacao/teste2minimizacao.txt'
af2 = leitor.ler_arquivo()
print(f"\n\n====> Minimização para o AF abaixo, lido do arquivo `{leitor.arquivo}`:")
af2.display()
minimizar(af2)
print('\n====> Saída:')
af2.display()


leitor.arquivo = '../Testes/Minimizacao/teste3minimizacao.txt'
af3 = leitor.ler_arquivo()
print(f"\n\n====> Minimização para o AF abaixo, lido do arquivo `{leitor.arquivo}`:")
af3.display()
minimizar(af3)
print('\n====> Saída:')
af3.display()
