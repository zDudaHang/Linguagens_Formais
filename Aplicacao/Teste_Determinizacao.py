from Leitor import Leitor

leitor = Leitor('../Testes/Determinizacao/Automato1.txt')
automato1 = leitor.ler_arquivo()
print(f'\n\n====> Teste de determinização para o AF abaixo, lido do arquivo `{leitor.arquivo}`')
automato1.determinizar()
print('\n====> Saída:')
automato1.display()

leitor.arquivo = '../Testes/Determinizacao/Automato2.txt'
automato2 = leitor.ler_arquivo()
print(f'\n\n====> Teste de determinização para o AF abaixo, lido do arquivo `{leitor.arquivo}`')
automato2.determinizar()
print('\n====> Saída:')
automato2.display()

leitor.arquivo = '../Testes/Determinizacao/Automato3.txt'
automato3 = leitor.ler_arquivo()
print(f'\n\n====> Teste de determinização para o AF abaixo, lido do arquivo `{leitor.arquivo}`')
automato3.determinizar()
print('\n====> Saída:')
automato3.display()
