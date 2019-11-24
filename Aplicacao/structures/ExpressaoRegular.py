from .nodo import Nodo

class ExpressaoRegular:
    def __init__(self, alfabeto, expressao):
        self.alfabeto = alfabeto
        self.expressao = expressao
        self.mapa_tipos = {
            '*': Nodo.STAR,
            '.': Nodo.CAT,
            '+': Nodo.OR,
        }
        self.tipos = ['*', '.', '+']

        self.root = self.parse(self.expressao + '.#')
        max_index = self.root.make_index(1)

        self.indexes = [i for i in range(1, max_index)]

        self.alfabeto = list(self.root.pegar_alfabeto())
        self.alfabeto.sort()
        self.correspondentes = self.root.pegar_correspondentes()

    def exportar(self, filename):
        t = '*ER\n*Alfabeto\n' + \
            f'{" ".join(self.alfabeto)}\n' + \
            '*Expressao\n' + \
            f'{self.expressao}'

        with open(filename, 'w') as f:
            f.write(t)

    def display(self):
        print(self.expressao)


    def parse(self, expressao):
        # Caso base para recursão
        if len(expressao) == 1:
            return Nodo(None, None, Nodo.LEAF, expressao)

        # Lidando com o resto da expressão
        # Caso for um fecho
        if expressao[-1] == '*':
            esquerda, tipo, direita = self.pegar_ramos(expressao[:-1])
            c2 = self.parse(direita)
            if esquerda is None:
                # Nesse caso, o nodo estrela é sobre o restante da expressão
                return Nodo(c2, c2, Nodo.STAR, None)

            else:
                c1 = self.parse(esquerda)

            star = Nodo(c2, c2, Nodo.STAR, None)
            return Nodo(c1, star, tipo, None)
            
        else:
            esquerda, tipo, direita = self.pegar_ramos(expressao)
            # Processando parênteses redudantes
            while esquerda is None:
                esquerda, tipo, direita = self.pegar_ramos(direita)

            c1 = self.parse(esquerda)
            c2 = self.parse(direita)

            return Nodo(c1, c2, tipo, None)


    def pegar_ramos(self, expressao):
        # Checa se tem parêntesis
        if expressao[-1] == ')':
            # Se tem, pega tudo q tem dentro do parêntesis como
            # o ramo da direita, o restando como esquerda e pega
            # o símbolo que relaciona os dois
            stack = ['(']
            i = -1
            while len(stack) > 0:
                i -= 1
                if expressao[i] == stack[-1]:
                    stack.pop()

                elif expressao[i] == ')':
                    stack.append('(')

            if len(expressao) is - i:
                return None, None, expressao[1:-1]

            else:
                return expressao[:i-1], expressao[i-1], expressao[i+1: -1]

        
        else:
            # Caso contrário, só pega o símbolo e retorna como
            # o ramo da direita
            return expressao[:-2], expressao[-2], expressao[-1]