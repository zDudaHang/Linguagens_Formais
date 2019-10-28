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

# PEGANDO TODAS AS TRANSICOES DE UM AUTOMATO PARA ADICIONAR AS NOVAS TRANSICOES
def pegando_transicoes(automato, novas_transicoes, novos_estados, indice_base, novos_estados_de_aceitacao):
    j = indice_base
    for estado in automato.estados:
        for i in range(0, len(automato.alfabeto)):
            estado_correspondente = novos_estados[j]
            transicao = automato.transicoes[estado][i]
            # TRANSICAO POR VAZIO
            if transicao == 'V':
                novas_transicoes[estado_correspondente].append('V')
                continue
            nova_transicao = []
            # PEGANDO CADA ESTADO DA TRANSICAO
            for estado_transicao in transicao.split(','):
                indice = automato.estados.index(estado_transicao)
                nova_transicao.append(novos_estados[indice + indice_base])
            nova_transicao = ','.join(map(str, nova_transicao))
            novas_transicoes[estado_correspondente].append(nova_transicao)
            if estado in automato.estados_aceitacao:
                novos_estados_de_aceitacao.append(estado_correspondente)
        j += 1

# PROCURANDO TRANSICOES POR E-FECHO PARA ADICIONAR AS NOVAS TRANSICOES
def verificar_transicoes_por_e(automato, novas_transicoes, novos_estados, indice_base):
    i = len(automato.alfabeto)
    j = indice_base
    transica = ''
    for estado in automato.estados:
        estado_correspondente = novos_estados[j]
        j += 1
        # VERIFICANDO SE EXISTE UMA TRANSICAO POR E-FECHO NO AUTOMATO
        try:
            transicao = automato.transicoes[estado][i]
        # NAO EXISTE, LOGO BASTA COLOCAR O VAZIO
        except IndexError:
            novas_transicoes[estado_correspondente].append('V')
        else:
            if transicao == 'V':
                novas_transicoes[estado_correspondente].append('V')
                continue
            nova_transicao = []
            # EXISTE UMA TRANSICAO DIFERENTE DE VAZIO, LOGO BASTA COLOCAR CADA UMA
            # NAS NOVAS TRANSICOES DO RESPECTIVO ESTADO
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

# MINIMIZACAO DE UM AUTOMATO FINITO DETERMINISTICO
def minimizar(automato):
    remover_inalcancaveis(automato)
    remover_mortos(automato)
    remover_equivalentes(automato)
    automato.mostrar_transicoes()

# REMOCAO DOS ESTADOS INALCANCAVEIS
def remover_inalcancaveis(automato):
    alcancaveis = [automato.estado_inicial]
    while (True):
        mudanca = False
        for estado in alcancaveis:
            novos_alcancaveis = []
            transicao = automato.transicoes[estado]
            for estado_transicao in transicao:
                if (estado_transicao not in alcancaveis) and (estado_transicao not in novos_alcancaveis):
                    # UMA MUDANCA OCORREU, LOGO PRECISO AVALIAR NOVAMENTE OS ESTADOS
                    # QUE JA TINHA AVALIADO
                    mudanca = True
                    novos_alcancaveis.append(estado_transicao)
            alcancaveis.extend(novos_alcancaveis)
        if not mudanca:
            break
    automato.estados = intersecao(automato.estados, alcancaveis)
    automato.estados_aceitacao = intersecao(automato.estados_aceitacao, alcancaveis)
    automato.transicoes = pegar_novas_transicoes(automato.transicoes, alcancaveis)

# PEGA APENAS AS TRANSICOES DO AUTOMATO QUE ESTAO NA LISTA_ESTADOS
# CASO CONTRARIO, COLOCA O VAZIO
def pegar_novas_transicoes(transicoes, lista_estados):
    novas_transicoes = {}
    for estado in lista_estados:
        transicao = transicoes[estado]
        novas_transicoes[estado] = []
        for estado_transicao in transicao:
            if estado_transicao in lista_estados:
                novas_transicoes[estado].append(estado_transicao)
            else:
                novas_transicoes[estado].append('V')
    return novas_transicoes

# INTERSECAO ENTRE DUAS LISTAS
def intersecao(lista1, lista2):
    lista_intersecao = []
    for elemento in lista1:
        if elemento in lista2:
            lista_intersecao.append(elemento)
    return lista_intersecao

# REMOCAO DOS ESTADOS MORTOS
# =================================== ! VERIFICAR SE A MUDANCA AINDA O FAZ OPERANTE
def remover_mortos(automato):
    # vivos = automato.estados_aceitacao
    vivos = []
    vivos.extend(automato.estados_aceitacao)
    while (True):
        mudanca = False
        for estado in automato.estados:
            novos_vivos = []
            transicao = automato.transicoes[estado]
            for estado_transicao in transicao:
                if (estado_transicao in vivos) and (estado not in vivos) and (estado not in novos_vivos):
                    # UMA MUDANCA OCORREU, LOGO PRECISO AVALIAR NOVAMENTE OS ESTADOS
                    # QUE JA TINHA AVALIADO
                    mudanca = True
                    novos_vivos.append(estado)
            vivos.extend(novos_vivos)
        if not mudanca:
            break
    automato.estados = intersecao(automato.estados, vivos)
    automato.transicoes = pegar_novas_transicoes(automato.transicoes, vivos)

# REMOVER ESTADOS EQUIVALENTES
# UTILIZOU-SE A FORMA DE PARTICOES DE HOPCROFT
def remover_equivalentes(automato):
    F = automato.estados_aceitacao
    K_sem_F = diferenca(automato.estados, automato.estados_aceitacao)
    P0 = [F,K_sem_F]
    P = [P0]
    k = 0
    while (True):
        mudanca = False
        for particao in P[k]:
            distinguiveis_encontrados = procurar_distinguiveis(P, k, particao, automato.alfabeto, automato.transicoes)
            mudanca = mudanca or distinguiveis_encontrados
            if distinguiveis_encontrados:
                break
        if (not mudanca):
            modificar_transicoes(P, k, automato)
            break
        k += 1

def modificar_transicoes(P, k, automato):
    novos_estados = []
    novos_estados_de_aceitacao = []
    novas_transicoes = {}

    # COLOCANDO O NOVO ESTADO INICIAL
    indice_estado_inicial = encontrar_indice(automato.estado_inicial, P[k])
    automato.estado_inicial = 'q' + str(indice_estado_inicial)

    # INICIALIZANDO AS KEYS DAS NOVAS TRANSICOES
    for i in range(0,len(P[k])):
        estado_equivalente = 'q' + str(i)
        novas_transicoes[estado_equivalente] = []

    # RETIRANDO TRANSICOES REDUNDANTES
    for i in range (0,len(P[k])):
        estado_equivalente = 'q' + str(i)
        novos_estados.append(estado_equivalente)
        estado = P[k][i][0]
        if estado in automato.estados_aceitacao:
            novos_estados_de_aceitacao.append(estado_equivalente)
        for j in range(0,len(automato.alfabeto)):
            transicao = automato.transicoes[estado][j]
            indice = encontrar_indice(transicao,P[k])
            if indice == -1:
                novas_transicoes[estado_equivalente].append('V')
            else:
                transicao_estado_equivalente = 'q' + str(indice)
                novas_transicoes[estado_equivalente].append(transicao_estado_equivalente)

    automato.estados = novos_estados
    automato.transicoes = novas_transicoes
    automato.estados_aceitacao = novos_estados_de_aceitacao

# DIFERENCA ENTRE DUAS LISTAS
def diferenca(lista_1, lista_2):
    lista_diferenca = []
    for elemento in lista_1:
        if elemento not in lista_2:
            lista_diferenca.append(elemento)
    return lista_diferenca

# PROCURANDO POR ESTADOS COM CLASSES DE EQUIVALENCIA DIFERENTES
def procurar_distinguiveis(P, k, particao, alfabeto, transicoes):
    mapeamento = {}

    for i in range(0,len(P[k])):
        mapeamento[i] = []

    # INDICE DO VAZIO
    mapeamento[-1] = []

    for j in range(0,len(alfabeto)):
        limpar_mapeamento(mapeamento)
        for estado in particao:
            transicao = transicoes[estado][j]
            indice = encontrar_indice(transicao, P[k])
            mapeamento[indice].append(estado)
        if existem_distinguiveis(mapeamento):
            nova_particao = transformar_mapeamento_em_particao(mapeamento)
            # ADICIONA UM P[K+1]
            P.append([])
            # ADICIONA A NOVA PARTICAO A P[K+1]
            P[k+1].extend(nova_particao)
            P[k+1].extend(P[k])
            P[k+1].remove(particao)
            return True

    # NAO ACHOU DISTINGUIVEIS
    return False

# LIMPA O MAPEAMENTO MANTENDO AS KEYS
def limpar_mapeamento(mapeamento):
    for indice in mapeamento:
        mapeamento[indice] = []

# TRANSFORMA O MAPEAMENTO DOS INDICES EM PARTICAO
def transformar_mapeamento_em_particao(mapeamento):
    particao = []
    for indice in mapeamento:
        if len(mapeamento[indice]) > 0:
            particao.append(mapeamento[indice])
    return particao

# PROCURAR POR INDICES ONDE A LISTA NAO EH VAZIA
# SE EXISTIR MAIS DE UM INDICE COM A LISTA NAO VAZIA
# ENTAO EXISTEM CLASSES DE EQUIVALENCIA DIFERENTES PARA CADA INDICE
def existem_distinguiveis(mapeamento):
    quantidade_indices_nao_vazios = 0
    for indice in mapeamento:
        if len(mapeamento[indice]) > 0:
            quantidade_indices_nao_vazios += 1
    return (quantidade_indices_nao_vazios > 1)

# PROCURAR O INDICE EM UMA PARTICAO P[K]
def encontrar_indice(estado, Pk):
    indice = -1
    for i in range(0,len(Pk)):
        for estado_particao in Pk[i]:
            if estado_particao == estado:
                return i
    return indice

# REMOCAO DE SIMBOLOS IMPRODUTIVOS DE UMA GRAMATICA
def remover_simbolos_improdutivos(glc):
    simbolos_produtivos = glc.terminais
    if '&' not in simbolos_produtivos:
        simbolos_produtivos.append('&')
    while (True):
        mudanca = False
        for nao_terminal in glc.nao_terminais:
            # CONJUNTO Q
            novos_produtivos = []
            for producao in glc.producoes[nao_terminal]:
                corpo_marcado = verificar_corpo_marcado(producao, simbolos_produtivos)
                if corpo_marcado and (nao_terminal not in simbolos_produtivos) and (nao_terminal not in novos_produtivos):
                    # EXISTE UMA PRODUCAO X -> ABC...Z ONDE A,B,C,...,Z PERTENCEM A SP
                    novos_produtivos.append(nao_terminal)
                    mudanca = True
            # SP = SP U Q
            simbolos_produtivos.extend(novos_produtivos)
        if not mudanca:
            break
    # GERACAO DO P'
    glc.producoes = alterar_producoes(simbolos_produtivos, glc.producoes, glc.nao_terminais)
    # N' = N INTERSECAO SP
    glc.nao_terminais = intersecao(simbolos_produtivos, glc.nao_terminais)
    glc.display()

# REMOCAO DE SIMBOLOS INALCANCAVEIS EM UMA GRAMATICA
def remover_inalcancaveis_glc(glc):
    simbolos_alcancaveis = [glc.simbolo_inicial]
    while (True):
        mudanca = False
        for nao_terminal in glc.nao_terminais:
            # CONJUNTO M
            novos_alcancaveis = []
            # SE O TERMINAL PERTENCE AOS ALCANCAVEIS, BASTA ADICIONAR AS SUAS PRODUCOES A LISTA
            # SE ELAS JA NAO PERTENCEREM A LISTA DE SIMBOLOS ALCANCAVEIS
            if nao_terminal in simbolos_alcancaveis:
                for producao in glc.producoes[nao_terminal]:
                    novos_simbolos_alcancaveis = pegar_simbolos_alcancaveis_novos(producao, simbolos_alcancaveis)
                    if len(novos_simbolos_alcancaveis) > 0:
                        # OCORREU UMA MUDANCA, PRECISO VARRER AS PRODUCOES NOVAMENTE
                        mudanca = True
                    # VERIFICA SE ESSE SIMBOLO JA NAO FOI ADICIONADO A LISTA DOS NOVOS SIMBOLOS ALCANCAVEIS
                    for simbolo in novos_simbolos_alcancaveis:
                        if (simbolo not in novos_alcancaveis):
                            novos_alcancaveis.append(simbolo)
                # SA = SA U M
                simbolos_alcancaveis.extend(novos_alcancaveis)
        if not mudanca:
            break
    # GERACAO DO P'
    glc.producoes = alterar_producoes(simbolos_alcancaveis, glc.producoes, glc.nao_terminais)
    # N' = N INTERSECAO SA
    glc.nao_terminais = intersecao(simbolos_alcancaveis, glc.nao_terminais)
    # T' = T INTERSECAO SA
    glc.terminais = intersecao(simbolos_alcancaveis, glc.terminais)
    glc.display()

def remover_producoes_por_epsilon()

def encontrar_anulaveis(producoes, nao_terminais):


# PROCURAR POR NOVOS SIMBOLSO ALCANCAVEIS PARA UMA DETERMINADA PRODUCAO
def pegar_simbolos_alcancaveis_novos(producao, simbolos_alcancaveis):
    alcancaveis = []
    for simbolo in producao:
        if simbolo not in simbolos_alcancaveis:
            alcancaveis.append(simbolo)
    return alcancaveis

# VERIFICA SE TODOS OS SIMBOLOS DE UMA PRODUCAO ESTAO NA LISTA DE SIMBOLOS PRODUTIVOS
def verificar_corpo_marcado(producao, simbolos_produtivos):
    for simbolo in producao:
        if simbolo not in simbolos_produtivos:
            return False
    return True

# CRIA UM NOVO CONJUNTO DE PRODUCOES
# APENAS ADICIONARA A PRODUCAO SE TODOS OS SIMBOLOS PERTENCEREM A LISTA DE SIMBOLOS
def alterar_producoes(lista_simbolos, producoes, nao_terminais):
    novas_producoes = {}
    for nao_terminal in nao_terminais:
        if nao_terminal in lista_simbolos:
            novas_producoes[nao_terminal] = []

    for nao_terminal in nao_terminais:
        for producao in producoes[nao_terminal]:
            pertence = verificar_pertinencia_producao(producao, lista_simbolos)
            if pertence:
                novas_producoes[nao_terminal].append(producao)
    return novas_producoes

# VERIFICA SE TODOS OS SIMBOLOS DE UMA PRODUCAO PERTENCEM A UMA DETERMINADA LISTA
def verificar_pertinencia_producao(producao, lista_simbolos):
    for simbolo in producao:
        if simbolo not in lista_simbolos:
            return False
    return True
