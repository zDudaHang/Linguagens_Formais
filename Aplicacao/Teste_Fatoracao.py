from Leitor import Leitor
from src.operacoes_glc import fatorar

leitor = Leitor('../Testes/Fatoracao/fatoracao1.txt')
glc1 = leitor.ler_arquivo()

print(f"\n\n====> Fatoração para a GLC abaixo, lida do arquivo `{leitor.arquivo}`:")
glc1.display()
fatorar(glc1)
print('\n====> Saída:')
glc1.display()

leitor.arquivo = '../Testes/Fatoracao/fatoracao2.txt'
glc2 = leitor.ler_arquivo()
print(f"\n\n====> Fatoração para a GLC abaixo, lida do arquivo `{leitor.arquivo}`:")
glc2.display()
fatorar(glc2)
print('\n====> Saída:')
glc2.display()

leitor.arquivo = '../Testes/Fatoracao/fatoracao3.txt'
glc3 = leitor.ler_arquivo()
print(f"\n\n====> Fatoração para a GLC abaixo, lida do arquivo `{leitor.arquivo}`:")
glc3.display()
fatorar(glc3)
print('\n====> Saída:')
glc3.display()

leitor.arquivo = '../Testes/Fatoracao/fatoracao4.txt'
glc4 = leitor.ler_arquivo()
print(f"\n\n====> Fatoração para a GLC abaixo, lida do arquivo `{leitor.arquivo}`:")
glc4.display()
fatorar(glc4)
print('\n====> Saída:')
glc4.display()

leitor.arquivo = '../Testes/Fatoracao/fatoracao5.txt'
glc5 = leitor.ler_arquivo()
print(f"\n\n====> Fatoração para a GLC abaixo, lida do arquivo `{leitor.arquivo}`:")
glc5.display()
fatorar(glc5)
print('\n====> Saída:')
glc5.display()
