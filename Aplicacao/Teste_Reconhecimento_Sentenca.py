from Leitor import Leitor

leitor = Leitor('../Testes/Reconhecimento_Sentenca/Automato1.txt')
automato1 = leitor.ler_arquivo()
print(f'\n\n====> Reconhecimento de sentença para o AF abaixo, lido do arquivo `{leitor.arquivo}`')
automato1.display()

print('\n====> Saídas:')
print(f'Sentença: aacbb\nResultado: {automato1.reconhecer("aacbb")}')
print(f'\nSentença: aacbb\nResultado: {automato1.reconhecer("")}')
print(f'\nSentença: aacbb\nResultado: {automato1.reconhecer("aacbbb")}')
# L1 = {#a + #c % 3 == 0 & #b % 2 == 0}
assert (automato1.reconhecer('aacbb') == True)
assert (automato1.reconhecer('') == True)
assert (automato1.reconhecer('aacbbb') == False)

leitor.arquivo = '../Testes/Reconhecimento_Sentenca/Automato2.txt'
automato2 = leitor.ler_arquivo()
print(f'\n\n====> Reconhecimento de sentença para o AF abaixo, lido do arquivo `{leitor.arquivo}`')
automato2.display()

print('\n====> Saídas:')
print(f'Sentença: bab\nResultado: {automato2.reconhecer("bab")}')
print(f'\nSentença: bab\nResultado: {automato2.reconhecer("")}')
print(f'\nSentença: bab\nResultado: {automato2.reconhecer("bb")}')
# L2 = {|w| impar & sem b's consecutivos}
assert (automato2.reconhecer('bab') == True)
assert (automato2.reconhecer('') == False)
assert (automato2.reconhecer('bb') == False)

leitor.arquivo = '../Testes/Reconhecimento_Sentenca/Automato3.txt'
automato3 = leitor.ler_arquivo()
print(f'\n\n====> Reconhecimento de sentença para o AF abaixo, lido do arquivo `{leitor.arquivo}`')
automato3.display()

print('\n====> Saídas:')
print(f'Sentença: aaaabbabab\nResultado: {automato3.reconhecer("aaaabbabab")}')
print(f'\nSentença: aaaabbabab\nResultado: {automato3.reconhecer("")}')
print(f'\nSentença: aaaabbabab\nResultado: {automato3.reconhecer("bababa")}')
# L3 = {w contem a substring 'bb'}
assert (automato3.reconhecer('aaaabbabab') == True)
assert (automato3.reconhecer('') == False)
assert (automato3.reconhecer('bababa') == False)
