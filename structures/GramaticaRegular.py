class Gramatica_Regular:
    def __init__(self, nao_terminais, terminais, producoes, simbolo_inicial):
        self.nao_terminais = nao_terminais
        self.terminais = terminais
        self.producoes = producoes
        self.simbolo_inicial = simbolo_inicial

    def arrumar_producoes(self):
        novas_producoes = {}
        novas_producoes[self.simbolo_inicial] = []
        for simbolo in self.nao_terminais:
            novas_producoes[simbolo] = []
        for producao in self.producoes:
            par = producao.split('->')
            novas_producoes[par[0]].append(par[1])
        self.producoes = novas_producoes
