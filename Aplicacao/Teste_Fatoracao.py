from Leitor import Leitor
from src.operacoes_glc import fatorar

leitor = Leitor('../Testes/Fatoracao/fatoracao1.txt')
glc1 = leitor.ler_arquivo()

print("========================================= FATORAÇÃO: =========================================")
print("====> ENTRADA:")
glc1.display()
fatorar(glc1)

leitor.arquivo = '../Testes/Fatoracao/fatoracao2.txt'
glc2 = leitor.ler_arquivo()
print("========================================= FATORAÇÃO: =========================================")
print("====> ENTRADA:")
glc2.display()
fatorar(glc2)

leitor.arquivo = '../Testes/Fatoracao/fatoracao3.txt'
glc3 = leitor.ler_arquivo()
print("========================================= FATORAÇÃO: =========================================")
print("====> ENTRADA:")
glc3.display()
fatorar(glc3)

leitor.arquivo = '../Testes/Fatoracao/fatoracao4.txt'
glc4 = leitor.ler_arquivo()
print("========================================= FATORAÇÃO: =========================================")
print("====> ENTRADA:")
glc4.display()
fatorar(glc4)

leitor.arquivo = '../Testes/Fatoracao/fatoracao5.txt'
glc5 = leitor.ler_arquivo()
print("========================================= FATORAÇÃO: =========================================")
print("====> ENTRADA:")
glc5.display()
fatorar(glc5)
