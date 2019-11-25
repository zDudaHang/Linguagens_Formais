'''
Este arquivo demonstra o método de determinização implementado nos
autômatos finitos.
'''

from Leitor import Leitor

leitor = Leitor('../Testes/Determinizacao/teste1determinizacao.txt')
automato1 = leitor.ler_arquivo()
print(f'\n\n====> Teste de determinização para o AF abaixo, lido do arquivo `{leitor.arquivo}`')
automato1.determinizar()
print('\n====> Saída:')
automato1.display()

leitor.arquivo = '../Testes/Determinizacao/teste2determinizacao.txt'
automato2 = leitor.ler_arquivo()
print(f'\n\n====> Teste de determinização para o AF abaixo, lido do arquivo `{leitor.arquivo}`')
automato2.determinizar()
print('\n====> Saída:')
automato2.display()

leitor.arquivo = '../Testes/Determinizacao/teste3determinizacao.txt'
automato3 = leitor.ler_arquivo()
print(f'\n\n====> Teste de determinização para o AF abaixo, lido do arquivo `{leitor.arquivo}`')
automato3.determinizar()
print('\n====> Saída:')
automato3.display()
