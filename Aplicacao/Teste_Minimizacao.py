from Leitor import Leitor
from src.operacoes_automatos_gr import minimizar

leitor = Leitor('../Testes/Minimizacao/Automato1.txt')
af1 = leitor.ler_arquivo()
print(f"\n\n====> Minimização para o AF abaixo, lido do arquivo `{leitor.arquivo}`:")
af1.display()
minimizar(af1)
print('\n====> Saída:')
af1.display()


leitor.arquivo = '../Testes/Minimizacao/Automato2.txt'
af2 = leitor.ler_arquivo()
print(f"\n\n====> Minimização para o AF abaixo, lido do arquivo `{leitor.arquivo}`:")
af2.display()
minimizar(af2)
print('\n====> Saída:')
af2.display()


leitor.arquivo = '../Testes/Minimizacao/Automato3.txt'
af3 = leitor.ler_arquivo()
print(f"\n\n====> Minimização para o AF abaixo, lido do arquivo `{leitor.arquivo}`:")
af3.display()
minimizar(af3)
print('\n====> Saída:')
af3.display()
