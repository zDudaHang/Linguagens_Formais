# ===================================== TODO
# [ ] COMENTAR CADA METODO
# ===================================== TODO
from structures.nodo import Nodo

# PEGANDO TODAS AS TRANSICOES DE UM AUTOMATO PARA ADICIONAR AS NOVAS TRANSICOES
def pegando_transicoes(automato, novas_transicoes, novos_estados, indice_base, novos_estados_de_aceitacao):
    j = indice_base
    for estado in automato.estados:
        for i in range(0, len(automato.alfabeto)):
            estado_correspondente = novos_estados[j]
            transicao = automato.transicoes[estado][i]
            # ADICIONANDO ESTADOS DE ACEITACAO
            if estado in automato.estados_aceitacao and estado_correspondente not in novos_estados_de_aceitacao:
                novos_estados_de_aceitacao.append(estado_correspondente)
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
        j += 1

def ajustar_estados_novos(qtd_estados_A, qtd_estado_B):
    novos_estados = []
    for i in range(1, qtd_estados_A+qtd_estado_B+1):
        novo_estado = 'q' + str(i)
        novos_estados.append(novo_estado)
    return novos_estados

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

def modificar_transicoes(P, k, automato):
    mapeamento = {}
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
        mapeamento[estado] = estado_equivalente
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
    return mapeamento

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

# PROCURAR O INDICE DE UM ESTADO EM UMA PARTICAO P[K]
def encontrar_indice(estado, Pk):
    indice = -1
    for i in range(0,len(Pk)):
        for estado_particao in Pk[i]:
            if estado_particao == estado:
                return i
    return indice

# INTERSECAO ENTRE DUAS LISTAS
def intersecao_listas(lista1, lista2):
    lista_intersecao = []
    for elemento in lista1:
        if elemento in lista2:
            lista_intersecao.append(elemento)
    return lista_intersecao
