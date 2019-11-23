from Leitor import Leitor

leitor = Leitor('../Testes/Reconhecimento_Sentenca/Automato1.txt')
automato1 = leitor.ler_arquivo()
automato1.display()

# L1 = {#a + #c % 3 == 0 & #b % 2 == 0}
assert (automato1.reconhecer('aacbb') == True)
assert (automato1.reconhecer('') == True)
assert (automato1.reconhecer('aacbbb') == False)

leitor.arquivo = '../Testes/Reconhecimento_Sentenca/Automato2.txt'
automato2 = leitor.ler_arquivo()
automato2.display()

# L2 = {|w| impar & sem b's consecutivos}
assert (automato2.reconhecer('bab') == True)
assert (automato2.reconhecer('') == False)
assert (automato2.reconhecer('bb') == False)

leitor.arquivo = '../Testes/Reconhecimento_Sentenca/Automato3.txt'
automato3 = leitor.ler_arquivo()
automato3.display()

# L3 = {w contem a substring 'bb'}
assert (automato3.reconhecer('aaaabbabab') == True)
assert (automato3.reconhecer('') == False)
assert (automato3.reconhecer('bababa') == False)
