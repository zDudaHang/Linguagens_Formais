from structures.AutomatoFinito import AutomatoFinito
from structures.GramaticaRegular import GramaticaRegular
from structures.ExpressaoRegular import ExpressaoRegular
from structures.nodo import Nodo

def uniao(automato_A, automato_B):
    # INICIALIZACAO DAS NOVAS TRANSICOES E ESTADOS DE ACEITACAO
    novas_transicoes = {}
    novos_estados_de_aceitacao = []
    qtd_estados_A = len(automato_A.estados)
    qtd_estado_B = len(automato_B.estados)
    novos_estados = ajustar_estados_novos(qtd_estados_A, qtd_estado_B)

    # PREPARANDO O NOVO ESTADO INICIAL
    novo_estado_inicial = 'q0'
    novas_transicoes[novo_estado_inicial] = ['V'] * len(automato_A.alfabeto)
    estado_inicial_A = novos_estados[0]
    estado_inicial_B = novos_estados[len(automato_A.estados)]
    transicao_novo_estado_inicial = estado_inicial_A + ',' + estado_inicial_B
    novas_transicoes[novo_estado_inicial].append(transicao_novo_estado_inicial)

    # INICIALIZANDO AS TRANSICOES COM OS ESTADOS NOVOS
    for estado in novos_estados:
        novas_transicoes[estado] = []

    pegando_transicoes(automato_A, novas_transicoes, novos_estados, 0, novos_estados_de_aceitacao)
    pegando_transicoes(automato_B, novas_transicoes, novos_estados, qtd_estados_A, novos_estados_de_aceitacao)
    verificar_transicoes_por_e(automato_A, novas_transicoes, novos_estados, 0)
    verificar_transicoes_por_e(automato_B, novas_transicoes, novos_estados, qtd_estados_A)

    novos_estados.insert(0, novo_estado_inicial)
    novo_automato = AutomatoFinito(novos_estados, automato_A.alfabeto, novas_transicoes, novo_estado_inicial, novos_estados_de_aceitacao)

    return novo_automato

def pegando_transicoes(automato, novas_transicoes, novos_estados, indice_base, novos_estados_de_aceitacao):
    j = indice_base
    for estado in automato.estados:
        for i in range(0, len(automato.alfabeto)):
            estado_correspondente = novos_estados[j]
            transicao = automato.transicoes[estado][i]
            if transicao == 'V':
                novas_transicoes[estado_correspondente].append('V')
                continue
            nova_transicao = []
            for estado_transicao in transicao.split(','):
                indice = automato.estados.index(estado_transicao)
                nova_transicao.append(novos_estados[indice + indice_base])
            nova_transicao = ','.join(map(str, nova_transicao))
            novas_transicoes[estado_correspondente].append(nova_transicao)
            if estado in automato.estados_aceitacao:
                novos_estados_de_aceitacao.append(estado_correspondente)
        j += 1

def verificar_transicoes_por_e(automato, novas_transicoes, novos_estados, indice_base):
    i = len(automato.alfabeto)
    j = indice_base
    transica = ''
    for estado in automato.estados:
        estado_correspondente = novos_estados[j]
        j += 1
        try:
            transicao = automato.transicoes[estado][i]
        except IndexError:
            novas_transicoes[estado_correspondente].append('V')
        else:
            if transicao == 'V':
                novas_transicoes[estado_correspondente].append('V')
                continue
            nova_transicao = []
            for estado_transicao in transicao.split(','):
                indice = automato.estados.index(estado_transicao)
                nova_transicao.append(novos_estados[indice + indice_base])
            nova_transicao = ','.join(map(str, nova_transicao))
            novas_transicoes[estado_correspondente].append(nova_transicao)

def ajustar_estados_novos(qtd_estados_A, qtd_estado_B):
    novos_estados = []
    for i in range(1, qtd_estados_A+qtd_estado_B+1):
        novo_estado = 'q' + str(i)
        novos_estados.append(novo_estado)
    return novos_estados

def intersecao(automato_A, automato_B):
    automato_A.negar()
    automato_B.negar()
    return uniao(automato_A, automato_B)


def af_para_gr(af: AutomatoFinito):
    # Gerando alias para os estados
    a = dict()
    a[af.estado_inicial] = 'S'
    letra = 'A'
    for estado in af.estados:
        # Pula estado incial que já foi renomeado
        if estado == af.estado_inicial:
            continue
        a[estado] = letra
        letra = chr(ord(letra) + 1)

    N = list(a.values())
    T = af.alfabeto
    S = a[af.estado_inicial]
    P = []
    for estado_atual, proximos_estados in af.transicoes.items():
        for proximo, caracter in zip(proximos_estados, af.alfabeto):
            if proximo == 'V':
                continue
            P.append(f'{a[estado_atual]}->{caracter}{a[proximo]}')

            if proximo in af.estados_aceitacao:
                P.append(f'{a[estado_atual]}->{caracter}')


    # Cria um novo simbolo inicial caso o estado inicial do AF seja
    # de aceitação
    if af.estado_inicial in af.estados_aceitacao:
        S = a[af.estado_inicial] + "'"
        N.append(S)
        for prod in P.copy():
            if prod[0] == a[af.estado_inicial]:
                P.append(f'{S}{prod[1:]}')

        P.append(f'{S}->&')

    return GramaticaRegular(N, T, P, S)


def gr_para_af(gr: GramaticaRegular):
    # Estados
    K = gr.nao_terminais
    novo_simbolo_nao_terminal = 'Z'
    K.append(novo_simbolo_nao_terminal)
    # Alfabeto
    alfabeto = gr.terminais
    
    # Estado inicial
    q0 = gr.simbolo_inicial
    
    # Estados de aceitação
    F = [novo_simbolo_nao_terminal]
    for nt, p in gr.producoes.items():
        if nt == gr.simbolo_inicial and '&' in p:
            F.append(nt)
            break

    # Transições
    trans = dict()
    for simb, prods in gr.producoes.items():
        for prod in prods:
            terminal, nao_terminal, e = pegar_simbolos(prod,
                                                       gr.terminais,
                                                       gr.nao_terminais)
            if e:
                continue

            if (simb, terminal) not in trans.keys():
                trans[(simb, terminal)] = []

            if nao_terminal is None:
                trans[(simb, terminal)].append(novo_simbolo_nao_terminal)

            if nao_terminal is not None and terminal is not None:
                trans[(simb, terminal)].append(nao_terminal)

    for nt in gr.nao_terminais:
        for t in gr.terminais:
            if (nt, t) not in trans.keys():
                trans[(nt, t)] = ['V']

    transicoes = []
    for nt in gr.nao_terminais:
        nexts = []
        for t in gr.terminais:
            for comb, dest in trans.items():
                if comb[0] == nt and comb[1] == t:
                    nexts.append(','.join(dest))

        transicoes.append(' '.join(nexts))

    return AutomatoFinito(K, alfabeto, transicoes, q0, F)

    

def pegar_simbolos(prod, terminais, nao_terminais):
    terminal = None
    for t in terminais:
        if t in prod:
            terminal = t
            break
    
    nao_terminal = None
    for nt in nao_terminais:
        if nt in prod:
            nao_terminal = nt
            break

    e = False
    if '&' in prod:
        e = True

    return terminal, nao_terminal, e


def er_para_afd(er: ExpressaoRegular):
    followpos = {i: set() for i in er.indexes}

    followpos = make_followpos(er.root, followpos)

    estado_inicial = str(er.root.firstpos)
    estados_de_aceitacao = []
    d_states_unmarked = [er.root.firstpos]
    d_states_marked = []
    d_tran = []
    while d_states_unmarked:
        S = d_states_unmarked.pop(0)
        d_states_marked.append(S)
        for a in er.alfabeto:
            U = set()
            for p in S:
                if er.correspondentes[p] == a:
                    fp = followpos[p]
                    U = U.union(fp)

            if U and U not in d_states_marked and U not in d_states_marked:
                d_states_unmarked.append(U)

            n = {'state': S, 'symbol': a, 'next': U}
            if U and n not in d_tran:
                if max(er.indexes) in n['state']:
                    estados_de_aceitacao.append(str(U))
                d_tran.append(n)

    transicoes = {}
    for t in d_tran:
        if str(t['state']) not in transicoes.keys():
            transicoes[str(t['state'])] = {}
        transicoes[str(t['state'])][str(t['symbol'])] = str(t['next'])

    alfabeto = er.alfabeto

    novas_transicoes = {}
    for k in transicoes.keys():
        t = transicoes[k]
        n_t = []
        for a in alfabeto:
            if a in t.keys():
                n_t.append(t[a])
            else:
                n_t.append('V')
        
        novas_transicoes[k] = n_t

    return AutomatoFinito(estados=novas_transicoes.keys(),
                          alfabeto=alfabeto,
                          estado_inicial=estado_inicial,
                          estados_aceitacao=estados_de_aceitacao,
                          transicoes=novas_transicoes)


def make_followpos(node: Nodo, followpos: dict):
    if node.eh_folha:
        return followpos

    if node.tipo == Nodo.STAR:
        for i in node.firstpos:
            followpos[i] = followpos[i].union(node.secondpos)

    elif node.tipo == Nodo.CAT:
        for i in node.c1.secondpos:
            followpos[i] = followpos[i].union(node.c2.firstpos)

    followpos = make_followpos(node.c1, followpos)
    followpos = make_followpos(node.c2, followpos)

    return followpos
    


