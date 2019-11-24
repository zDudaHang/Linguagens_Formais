
def firsts(glc):
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
    Split body of a production into a lsit of symbols in T U N

    Return
    ----------

    list of symbols, ordered
    '''
    
    symbols = []
    while len(body) > 0:
        symbol = get_first_symbol(body, T, N)
        symbols.append(symbol)

        body = body[len(symbol) :]

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

def follows(glc, first=None):
    '''
    Function to mount the FIRST of each symbol on a GLC

    Return
    ----------

    {X : FOLLOW(X) for X} in (N U T)
    '''

    # If first was not passed, calculate it
    if first is None:
        first = firsts(glc)

    follow = {s: set(()) for s in glc.nao_terminais}
    follow[glc.simbolo_inicial] = set('$')


    new_added = True
    while new_added:
        new_added = False
        for head, bodies in glc.producoes.items():
            for body in bodies:
                symbols = split_into_symbols(body, glc.terminais, glc.nao_terminais)
                for i in range(len(symbols)):
                    if symbols[i] in glc.nao_terminais:
                        if i == len(symbols) - 1 or '&' in first[symbols[i + 1]]:
                            # Putting follow of the head on follow of symbol when it is the last or
                            # the next symbol's first contain empty set
                            follow[symbols[i]] = follow[symbols[i]].union(follow[head])

                        elif symbols[i + 1] in glc.nao_terminais:
                            # Add first of the following symbol to current symbol's follow
                            follow[symbols[i]] = follow[symbols[i]].union(first[symbols[i+1]])

    return follow