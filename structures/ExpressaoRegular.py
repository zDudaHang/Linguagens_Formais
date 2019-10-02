class ExpressaoRegular:
    def __init__(self,alfabeto,expressao):
        self.alfabeto = alfabeto
        self.expressao = expressao

    def exportar(self, filename):
        t = '*ER\n*Alfabeto\n' + \
            f'{" ".join(self.alfabeto)}\n' + \
            '*Expressao\n' + \
            f'{self.expressao}'

        with open(filename, 'w') as f:
            f.write(t)

