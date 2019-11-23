from Leitor import Leitor

leitor = Leitor('../Testes/Determinizacao/Automato1.txt')
automato1 = leitor.ler_arquivo()
automato1.determinizar()
automato1.display()

leitor.arquivo = '../Testes/Determinizacao/Automato2.txt'
automato2 = leitor.ler_arquivo()
automato2.determinizar()
automato2.display()

leitor.arquivo = '../Testes/Determinizacao/Automato3.txt'
automato3 = leitor.ler_arquivo()
automato3.determinizar()
automato3.display()
