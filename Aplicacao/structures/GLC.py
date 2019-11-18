class GLC:
    def __init__(self, nao_terminais, terminais, producoes, simbolo_inicial):
        self.nao_terminais = nao_terminais
        self.terminais = terminais
        self.producoes = producoes
        self.simbolo_inicial = simbolo_inicial
        if type(producoes) != dict:
            self._arrumar_producoes()

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

    # def exportar(self, filename):
    #     t = '*GLC\n' + \
    #         '*NaoTerminais\n' + \
    #         f'{" ".join(self.nao_terminais)}\n' + \
    #         '*Terminais\n' + \
    #         f'{" ".join(self.terminais)}\n' + \
    #         '*SimboloInicial\n' + \
    #         f'{self.simbolo_inicial}\n' + \
    #         '*Producoes\n'
    #     for simb, prods in self.producoes.items():
    #         for prod in prods:
    #             t += f'{simb}->{prod}\n'
    #
    #     with open(filename, 'w') as f:
    #         f.write(t)
