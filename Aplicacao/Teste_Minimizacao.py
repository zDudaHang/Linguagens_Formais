from Leitor import Leitor
from src.operacoes_automatos_gr import minimizar

leitor = Leitor('../Testes/Minimizacao/Automato1.txt')
af1 = leitor.ler_arquivo()
minimizar(af1)
af1.display()

print("-----------------------------------------------------------")

leitor.arquivo = '../Testes/Minimizacao/Automato2.txt'
af2 = leitor.ler_arquivo()
minimizar(af2)
af2.display()

print("-----------------------------------------------------------")

leitor.arquivo = '../Testes/Minimizacao/Automato3.txt'
af3 = leitor.ler_arquivo()
minimizar(af3)
af3.display()
