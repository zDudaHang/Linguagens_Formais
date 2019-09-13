class Automato_Finito:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao

    def arrumar_transicoes(self):
        novas_transicoes = {}
        for estado in self.estados:
            novas_transicoes[estado] = []
        i = 0
        for transicao in self.transicoes:
            transicoes = transicao.split()
            for estado_a_transitar in transicoes:
                novas_transicoes[self.estados[i]].append(estado_a_transitar)
            i += 1
        self.transicoes = novas_transicoes

    def determinizar(self):

        transicoes_referencia = self.transicoes

        (e_fecho,sem_transicoes_e) = self.calcular_e_fecho()

        if(e_fecho[self.estado_inicial] != self.estado_inicial):
            self.estado_inicial = e_fecho[self.estado_inicial]
            self.verificar_estado_de_aceitacao(self.estado_inicial)

        if (not sem_transicoes_e):
            self.estados = [self.estado_inicial]
            self.transicoes = {}
            self.transicoes[self.estado_inicial] = [None]*len(self.alfabeto)
        else:
            self.transicoes = {}
            for estado in self.estados:
                self.transicoes[estado] = [None]*len(self.alfabeto)

        # self.encontrar_estados_novos(lista_epsilons, transicoes_referencia)
        self.definir_novas_transicoes(e_fecho, transicoes_referencia)

        self.mostrar_transicoes()

    def calcular_e_fecho(self):
        e_fecho = self.inicializar_e_fecho()
        for estado in self.estados:
            estados = []
            j = len(self.alfabeto)
            try:
                transicao = self.transicoes[estado][j]
            except IndexError:
                return (e_fecho,True)
            else:
                estados.append(estado)
                if (transicao != 'V'):
                    transicao = transicao.split(',')
                    estados.extend(transicao)
                estados.sort()
                e_fecho[estado] = ','.join(map(str,estados))
        return (e_fecho,False)

    def inicializar_e_fecho(self):
        e_fecho = {}
        for estado in self.estados:
            e_fecho[estado] = estado
        return e_fecho

    def verificar_estado_de_aceitacao(self, transicao):
        estados = transicao.split(',')
        for estado in estados:
            if estado in self.estados_aceitacao :
                self.estados_aceitacao.append(transicao)

    def definir_novas_transicoes(self, e_fecho, transicoes_referencia):

        estado_novo_encontrado = 0

        for estado in self.estados:
            for j in range(len(self.alfabeto)):
                if self.transicoes[estado][j] == None:
                    # Pegando todos os estados, ex: {q0,q1,q2} -> [q0,q1,q2]
                    # para recuperar suas transicoes
                    lista_estados = estado.split(',')

                    # Pegar transicoes
                    lista_estados_a_transitar = []
                    for estado_lista in lista_estados:
                        lista_estados_a_transitar.append(transicoes_referencia[estado_lista][j])

                    # Verificar as transicoes por E nos estados da nova_transicao
                    estado_a_transitar = []
                    for estado_transicao in lista_estados_a_transitar:
                        if (estado_transicao != 'V'):
                            if (len(estado_transicao.split(',')) > 1):
                                estado_transicao = estado_transicao.split(',')
                                for e in estado_transicao:
                                    estado_a_transitar.extend(e_fecho[e].split(','))
                            else:
                                estado_a_transitar.extend(e_fecho[estado_transicao].split(','))

                    estado_a_transitar = set(estado_a_transitar)
                    estado_a_transitar = list(estado_a_transitar)
                    estado_a_transitar.sort()
                    estado_a_transitar = ','.join(map(str,estado_a_transitar))

                    if estado_a_transitar not in self.estados:
                        estado_novo_encontrado = 1
                        nova_transicao = [None]*len(self.alfabeto)
                        self.estados.append(estado_a_transitar)
                        self.transicoes[estado_a_transitar] = [None]*len(self.alfabeto)
                        self.verificar_estado_de_aceitacao(estado_a_transitar)

                    self.transicoes[estado][j] = estado_a_transitar

    def mostrar_transicoes(self):
        print("======= Estados do AF =======")
        for estado in self.estados:
            texto = ''
            if estado == self.estado_inicial:
                texto += '-> '
            if estado in self.estados_aceitacao:
                texto += '* '
            texto += estado + ': '
            transicoes = ' | '.join(map(str, self.transicoes[estado]))
            print(texto + transicoes)
