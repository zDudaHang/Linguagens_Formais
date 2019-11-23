from Leitor import Leitor
from src.operacoes_automatos_gr import uniao, intersecao

leitor = Leitor('../Testes/Uniao_Intersecao/R1.txt')
r1 = leitor.ler_arquivo()

print("========================================= UNIÃO E INTERSEÇÃO =========================================")
print("====> ENTRADAS:")
r1.display()

leitor.arquivo = '../Testes/Uniao_Intersecao/S1.txt'
s1 = leitor.ler_arquivo()

s1.display()

r1_uniao_s1 = uniao(r1,s1)
r1_inter_s1 = intersecao(r1,s1)

print("====> UNIÃO:")
r1_uniao_s1.display()

print("====> INTESEÇÃO:")
r1_inter_s1.display()

print("========================================= UNIÃO E INTERSEÇÃO =========================================")
print("====> ENTRADAS:")
leitor.arquivo = '../Testes/Uniao_Intersecao/R2.txt'
r2 = leitor.ler_arquivo()

r2.display()

leitor.arquivo = '../Testes/Uniao_Intersecao/S2.txt'
s2 = leitor.ler_arquivo()

s2.display()

r2_uniao_s2 = uniao(r2,s2)
r2_inter_s2 = intersecao(r2,s2)

print("====> UNIÃO:")
r2_uniao_s2.display()

print("====> INTESEÇÃO:")
r2_inter_s2.display()

print("========================================= UNIÃO E INTERSEÇÃO =========================================")
print("====> ENTRADAS:")
leitor.arquivo = '../Testes/Uniao_Intersecao/R3.txt'
r3 = leitor.ler_arquivo()

r3.display()

leitor.arquivo = '../Testes/Uniao_Intersecao/S3.txt'
s3 = leitor.ler_arquivo()

s3.display()

r3_uniao_s3 = uniao(r3,s3)
r3_inter_s3 = intersecao(r3,s3)

print("====> UNIÃO:")
r3_uniao_s3.display()

print("====> INTESEÇÃO:")
r3_inter_s3.display()
