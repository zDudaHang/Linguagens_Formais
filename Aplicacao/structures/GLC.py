from src.operacoes_reconhecimento_ap import criar_tabela_de_analise, split_into_symbols

class GLC:
    def __init__(self, nao_terminais, terminais, producoes, simbolo_inicial):
        self.nao_terminais = nao_terminais
        self.terminais = terminais
        self.producoes = producoes
        self.simbolo_inicial = simbolo_inicial
        self.mapeamento = None
        if type(producoes) != dict:
            self._arrumar_producoes()
        self.tabela_analise = criar_tabela_de_analise(self)

    def _arrumar_producoes(self):
        novas_producoes = {}
        novas_producoes[self.simbolo_inicial] = []
        for simbolo in self.nao_terminais:
            novas_producoes[simbolo] = []
        for producao in self.producoes:
            par = producao.split('->')
            novas_producoes[par[0]].append(par[1])
        self.producoes = novas_producoes

    def display(self):
        print('Terminais (T): ', ', '.join(self.terminais))
        print('Não-terminais (N): ', ', '.join(self.nao_terminais))
        print('Símbolo inicial (S): ', self.simbolo_inicial)
        print('Produções:')
        for simb, prod in self.producoes.items():
            print(f'{simb} -> {" | ".join(prod)}')

    def exportar(self, filename):
        t = '*GLC\n' + \
            '*NaoTerminais\n' + \
            f'{" ".join(self.nao_terminais)}\n' + \
            '*Terminais\n' + \
            f'{" ".join(self.terminais)}\n' + \
            '*SimboloInicial\n' + \
            f'{self.simbolo_inicial}\n' + \
            '*Producoes\n'
        for simb, prods in self.producoes.items():
            for prod in prods:
                t += f'{simb}->{prod}\n'

        with open(filename, 'w') as f:
            f.write(t)

    def reconhecer(self, sentenca):
        if self.tabela_analise == None:
            print("==> Erro: Não foi possível criar a tabela de análise porque a GLC não é LL(1)")
            return False
        # INSERIR: APPEND
        # RETIRAR: POP
        # TOPO: STACK[len(stack)-1]
        sentenca += '$'
        sentenca = split_into_symbols(sentenca,self.terminais + ['$'],self.nao_terminais)
        stack = []
        stack.append('$')
        stack.append(self.simbolo_inicial)

        # INDICE PARA AVALIAR A SENTENCA
        cabecote = 0
        while(True):
            topo = stack[len(stack)-1]
            if topo == sentenca[cabecote]:
                # Aceite
                if topo == '$':
                    return True
                # TOPO == CABECOTE != $
                if topo in self.terminais:
                    # DESEMPILHE O TOPO
                    antigo_topo = stack.pop()
                    # AVANCA NA ENTRADA
                    cabecote += 1
                else:
                    # ======================================= DEBUG
                    # print("==> ERRO: Esperava um terminal no topo e no cabeçote")
                    # ======================================= DEBUG
                    return False
            elif topo in self.nao_terminais and sentenca[cabecote] in self.terminais:
                acao = self.tabela_analise[topo][sentenca[cabecote]]
                if acao == -1:
                    # ======================================= DEBUG
                    # print("==> ERRO: Tabela[%s][%s] = Erro" % (topo, sentenca[cabecote]))
                    # ======================================= DEBUG
                    return False
                else:
                    # RETIRA O TOPO DA PILHA
                    stack.pop()
                    producao = self.mapeamento[acao]
                    simbolos = producao.split('->')
                    corpo = ''.join(simbolos[1::])
                    corpo = split_into_symbols(corpo,self.terminais + ['$'],self.nao_terminais)
                    if corpo != ['&']:
                        while(corpo != []):
                            stack.append(corpo.pop())
            else:
                return False
