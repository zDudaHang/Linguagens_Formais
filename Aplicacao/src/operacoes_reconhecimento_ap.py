from src.operacoes_glc import fatorar, remover_recursao_esquerda_dir_indir

def criar_tabela_de_analise(glc):
    firsts = calculate_firsts(glc)

    follows = calculate_follows(glc, firsts)

    intersections = isLL1(glc.nao_terminais, firsts, follows)

    if len(intersections) != 0:
        # print('==> ERRO: A gramática não é LL(1)')
        # print("Existe interseção entre os conjuntos First e Follow nos seguintes não-terminais: ", intersections)
        return None

    map = map_productions(glc)
    glc.mapeamento = map
    # ======================================= DEBUG
    # print("Mapeamento:")
    # display_dict(map)
    # ======================================= DEBUG
    analysis_table = init_analysis_table(glc.terminais, glc.nao_terminais)

    # PREENCHENDO A TABELA DE ANALISE
    # CUIDADO: ANALISAR SE JÁ NAO EXISTE UMA ENTRADA DEFINIDA QUANDO FOR COLOCAR ALGO
    # SE EXISTIR, INDIQUE QUE HOUVE CONFLITO NA CÉLULA
    for non_terminal in analysis_table.keys():
        for production in glc.producoes[non_terminal]:
            number = map[non_terminal+'->'+production]
            symbols_alfa = split_into_symbols(production, glc.terminais, glc.nao_terminais)
            first_alfa = first_of_sequence(production, firsts, symbols_alfa)
            for a in (first_alfa - set('&')):
                if analysis_table[non_terminal][a] == -1:
                    analysis_table[non_terminal][a] = number
                else:
                    # CONFLITO
                    # print("==> ERRO: Conflito em T[%s,%s]" % (non_terminal,a))
                    return None
            if '&' in first_alfa:
                for b in follows[non_terminal]:
                    if analysis_table[non_terminal][b] == -1:
                        analysis_table[non_terminal][b] = number
                    else:
                        # print("==> ERRO: Conflito em T[%s,%s]" % (non_terminal,b))
                        return None
    # ======================================= DEBUG
    # print("Tabela de análise:")
    # display_dict(analysis_table)
    # ======================================= DEBUG
    return analysis_table

def display_dict(dict):
    for key in dict.keys():
        print("%s : %s" %(key, dict[key]))

def isLL1(N, firsts, follows):
    intersections = []
    for non_terminal in N:
        if firsts[non_terminal].intersection(follows[non_terminal]) != set():
            intersections.append(non_terminal)
    return intersections

def init_analysis_table(T, N):
    analysis_table = dict()
    T.append('$')
    for non_terminal in N:
        analysis_table[non_terminal] = dict()
        for terminal in T:
            analysis_table[non_terminal][terminal] = -1
    return analysis_table

def map_productions(glc):
    map = dict()
    i = 0
    for non_terminal in glc.nao_terminais:
        for production in glc.producoes[non_terminal]:
            value = non_terminal+'->'+production
            map[value] = i
            map[i] = value
            i += 1
    return map

def calculate_firsts(glc):
    '''
    Function to mount the FIRST of each symbol on a GLC

    Return
    ----------

    {X : FIRST(X) for X} in (N U T)
    '''
    first = {s: set((s,)) for s in glc.terminais + ['&']}
    for X in glc.nao_terminais:
        first[X] = set()

    new_added = True
    while new_added:
        new_added = False
        for head, bodies in glc.producoes.items():
            for body in bodies:
                symbol = get_first_symbol(body, glc.terminais, glc.nao_terminais)

                if symbol in glc.terminais + ['&']:
                    new_first = first[head].union(first[symbol])

                elif symbol in glc.nao_terminais:
                    f = first[symbol]
                    new_first = first[head].union(f - set('&'))

                    while '&' in f:
                        # Take a body without the first symbol
                        body = body[len(symbol):]
                        if body == '':
                            new_first = new_first.union('&')
                            break

                        symbol = get_first_symbol(body, glc.terminais, glc.nao_terminais)
                        f = first[symbol]
                        new_first = new_first.union(f - set('&'))

                else:
                    raise Exception(f'Symbol {symbol} not in GLC (N U T)')

                if new_first != first[head]:
                    new_added = True
                    first[head] = new_first

    return first

def split_into_symbols(body, T, N):
    '''
    Split body of a production into a list of symbols in T U N

    Return
    ----------

    list of symbols, ordered
    '''

    # ======================================= DEBUG
    # print("----> Body received = %s" % body)
    # ======================================= DEBUG

    symbols = []
    while len(body) > 0:
        symbol = get_first_symbol(body, T, N)
        symbols.append(symbol)

        body = body[len(symbol) :]

    # ======================================= DEBUG
    # print("Symbols = %s" % symbols)
    # ======================================= DEBUG

    return symbols

def get_first_symbol(body, T, N):
    '''
    Funcion to get the first symbol of body of a production,
    to deal with multiple-digits symbols

    Return
    ----------

    The first pattern on body that matches a symbol in (T U N)
    '''

    symbols = T + N
    symbols.append('&')
    for i, _ in enumerate(body):
        if body[: i + 1] in symbols:
            return body[: i + 1]

    return body


def calculate_follows(glc, firsts=None):
    '''
    Function to mount the FIRST of each symbol on a GLC

    Return
    ----------

    {X : FOLLOW(X) for X} in (N U T)
    '''

    # If first was not passed, calculate it
    if firsts is None:
        firsts = calculate_firsts(glc)

    follows = {s: set(()) for s in glc.nao_terminais}
    follows[glc.simbolo_inicial] = set('$')

    # DICIONARIO PARA GUARDAR OS CASOS: FOLLOW(A) EM FOLLOW(B)
    # SERAH GUARDADODA DESSA FORMA: inside[A] = [B]
    inside = {n: set(()) for n in glc.nao_terminais}


    new_added = True
    while(new_added):
        new_added = False
        for head, bodies in glc.producoes.items():
            for body in bodies:
                # ======================================= DEBUG
                # print("==== Head = %s" % head)
                # print("Body = %s" % body)
                # ======================================= DEBUG
                symbols = split_into_symbols(body, glc.terminais, glc.nao_terminais)
                for i in range(len(symbols)):
                    # CASO 1: PRODUCAO X -> aBC ou X -> ABC
                    if symbols[i] in glc.nao_terminais:
                        target = symbols[i]
                        # PARA VERIFICAR SE HOUVE MUDANCA
                        old = follows[target]

                        beta = ''.join(symbols[i+1:])
                        # ======================================= DEBUG
                        # print("Target = %s" % target)
                        # print("Beta = %s" % beta)
                        # ======================================= DEBUG
                        # CASO 1.1: BETA É DIFERENTE DA SENTENCA VAZIA
                        # ACAO: FIRST(BETA)/{&} EM FOLLOW(TARGET)
                        if beta != '':
                            # ======================================= DEBUG
                            # print("==> Beta != vazio -----> First(%s) em Follow(%s)" % (beta, target))
                            # ======================================= DEBUG
                            symbols_beta = split_into_symbols(beta, glc.terminais, glc.nao_terminais)
                            first_beta = first_of_sequence(beta, firsts, symbols_beta)

                            # FIRST(BETA)\{&} EM FOLLOW(TARGET)
                            follows[target].update((first_beta - set('&')))
                            # ======================================= DEBUG
                            # print("First[%s] = %s" % (beta, first_beta))
                            # print("Follow[%s] = %s" % (target, follows[target]))
                            # ======================================= DEBUG
                            if '&' in first_beta:
                                # FOLLOW(HEAD) EM FOLLOW(TARGET)
                                if head != target:
                                    inside[head].add(target)
                                    # ======================================= DEBUG
                                    # print("==> & in first(beta) -----> Follow(%s) em Follow(%s)" % (head, target))
                                    # print("Inside[%s] = %s" % (head, inside[head]))
                                    # ======================================= DEBUG
                        # CASO 1.2: BETA É IGUAL A SENTENCA VAZIA (X->alfaB)
                        # ACAO: FOLLOW(HEAD) EM FOLLOW(TARGET)
                        else:
                            if head != target:
                                inside[head].add(target)
                                # ======================================= DEBUG
                                # print("==> & in first(beta) -----> Follow(%s) em Follow(%s)" % (head, target))
                                # print("Inside[%s] = %s" % (head, inside[head]))
                                # ======================================= DEBUG
                        if old != follows[target]:
                            new_added = True

    new_added = True
    while(new_added):
        new_added = False
        for non_terminal in inside.keys():
            for dependent in inside[non_terminal]:
                old = follows[dependent]
                follows[dependent].update(follows[non_terminal])
                # ======================================= DEBUG
                # print("Dependente %s de %s" % (dependent, non_terminal))
                # print("Follow[%s] = %s" % (non_terminal, follows[non_terminal]))
                # print("Old follow[%s] = %s" % (dependent, old))
                # print("New follow[%s] = %s" % (dependent, follows[dependent]))
                # ======================================= DEBUG
                if old != follows[dependent]:
                    new_added = True
    return follows

# If A→αBβ, then everything in FIRST(β) except ε is in FOLLOW(B).
def first_of_sequence(beta, firsts, symbols):
    first_sequence = set()
    for i in range(len(symbols)):
        if '&' not in firsts[symbols[i]]:
            first_sequence.update(firsts[symbols[i]])
            break
        first_sequence.update((firsts[symbols[i]] - set('&')))
        if i == len(symbols) - 1:
            first_sequence.add('&')
    return first_sequence
