class AutomatoFinito:
    def __init__(self, estados, alfabeto, transicoes, estado_inicial, estados_aceitacao):
        self.estados = estados
        self.alfabeto = alfabeto
        self.transicoes = transicoes
        # Ajusta as transições para terem forma de dicionário
        if type(transicoes) != dict:
            self._arrumar_transicoes()
        self.estado_inicial = estado_inicial
        self.estados_aceitacao = estados_aceitacao

    def _arrumar_transicoes(self):
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

        (e_fecho, tem_e_fecho) = self.calcular_e_fecho()

        if e_fecho[self.estado_inicial] != self.estado_inicial:
            self.estado_inicial = e_fecho[self.estado_inicial]
            self.verificar_estado_de_aceitacao(self.estado_inicial)

        if tem_e_fecho:
            self.estados = [self.estado_inicial]
            self.transicoes = {}
            self.transicoes[self.estado_inicial] = [None]*len(self.alfabeto)
        else:
            self.transicoes = {}
            for estado in self.estados:
                self.transicoes[estado] = [None]*len(self.alfabeto)

        self.definir_novas_transicoes(e_fecho, transicoes_referencia)

    def calcular_e_fecho(self):
        e_fecho = self.inicializar_e_fecho()
        for estado in self.estados:
            estados = []
            j = len(self.alfabeto)
            try:
                transicao = self.transicoes[estado][j]
            except IndexError:
                return (e_fecho, False)
            else:
                estados.append(estado)
                if (transicao != 'V'):
                    transicao = transicao.split(',')
                    estados.extend(transicao)
                estados.sort()
                e_fecho[estado] = ','.join(set(map(str, estados)))
        return (e_fecho, True)

    def inicializar_e_fecho(self):
        e_fecho = {}
        for estado in self.estados:
            e_fecho[estado] = estado
        return e_fecho

    def verificar_estado_de_aceitacao(self, transicao):
        estados = transicao.split(',')
        for estado in estados:
            if estado in self.estados_aceitacao and transicao not in self.estados_aceitacao:
                self.estados_aceitacao.append(transicao)

    def definir_novas_transicoes(self, e_fecho, transicoes_referencia):

        estado_novo_encontrado = 0

        for estado in self.estados:
            for j, caracter in enumerate(self.alfabeto):
                if self.transicoes[estado][j] == None:
                    # Pegando todos os estados, ex: {q0,q1,q2} -> [q0,q1,q2]
                    # para recuperar suas transicoes
                    lista_estados = estado.split(',')

                    # Pegar transicoes
                    lista_estados_a_transitar = []
                    for estado_lista in lista_estados:
                        lista_estados_a_transitar.append(
                            transicoes_referencia[estado_lista][j])

                    # Verificar as transicoes por E nos estados da nova_transicao
                    estado_a_transitar = []
                    for estado_transicao in lista_estados_a_transitar:
                        if (estado_transicao != 'V'):
                            if (len(estado_transicao.split(',')) > 1):
                                estado_transicao = estado_transicao.split(',')
                                for e in estado_transicao:
                                    estado_a_transitar.extend(
                                        e_fecho[e].split(','))
                            else:
                                estado_a_transitar.extend(
                                    e_fecho[estado_transicao].split(','))

                    estado_a_transitar = set(estado_a_transitar)
                    estado_a_transitar = list(estado_a_transitar)
                    estado_a_transitar.sort()
                    estado_a_transitar = ','.join(map(str, estado_a_transitar))

                    # Evitando adicionar estados vazios a lista de estados
                    if estado_a_transitar not in self.estados and estado_a_transitar:
                        estado_novo_encontrado = 1
                        nova_transicao = [None]*len(self.alfabeto)
                        self.estados.append(estado_a_transitar)
                        self.transicoes[estado_a_transitar] = [
                            None]*len(self.alfabeto)
                        self.verificar_estado_de_aceitacao(estado_a_transitar)

                    # Formaliza o estado vazio como V
                    if not estado_a_transitar:
                        estado_a_transitar = 'V'

                    self.transicoes[estado][j] = estado_a_transitar
        self.limpar_estados_aceitacao()

    def limpar_estados_aceitacao(self):
        for estado_aceitacao in self.estados_aceitacao:
            if estado_aceitacao not in self.estados:
                self.estados_aceitacao.remove(estado_aceitacao)


    def negar(self):
        novos_estados_de_aceitacao = []
        for estado in self.estados:
            if estado not in self.estados_aceitacao:
                novos_estados_de_aceitacao.append(estado)
        self.estados_aceitacao = novos_estados_de_aceitacao

    def display(self):
        print('Estados (K): ', ' | '.join(self.estados))
        print('Estados de aceitação (F): ', ' | '.join(self.estados_aceitacao))
        print('Estado inicial (q0): %s' % self.estado_inicial)
        print('Alfabeto: ', ' | '.join(self.alfabeto))
        print('Transições:')
        for estado, transicao in self.transicoes.items():
            print(f'{estado} -> {" | ".join(transicao)}')

    def exportar(self, filename):
        t = f'*AF\n*Estados\n' +\
            f'{" ".join(self.estados)}\n' + \
            f'*EstadoInicial\n{self.estado_inicial}\n' + \
            '*EstadosDeAceitacao\n' +\
            f'{" ".join(self.estados_aceitacao)}\n' +\
            '*Alfabeto\n' +\
            f'{" ".join(self.alfabeto)}\n' + \
            '*Transicoes\n'

        for trans in self.transicoes.values():
            t += ' '.join(trans) + '\n'

        with open(filename, 'w') as f:
            f.write(t)

    def reconhecer(self, sentenca):
        # Opera apenas com AF determinizado
        self.determinizar()
        # Checa se todos os caracteres estão no alfabeto
        if not all([c in self.alfabeto for c in sentenca]):
            return False

        current_state = self.estado_inicial
        for c in sentenca:
            i = self.alfabeto.index(c)
            current_state = self.transicoes[current_state][i]

        return current_state in self.estados_aceitacao
