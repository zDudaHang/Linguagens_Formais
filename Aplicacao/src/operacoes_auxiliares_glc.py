# ===================================== TODO
# [ ] COMENTAR CADA METODO
# ===================================== TODO

def pegar_alfas_e_betas(producao, anulaveis):
    # PEGANDO  OS ALFAS E BETAS
    lista_alfa_beta = []
    for simbolo_anulavel in anulaveis:
        if simbolo_anulavel in producao:
            producao_dividida = producao.split(simbolo_anulavel)
            alfa = producao_dividida[0]
            beta = producao_dividida[1]
            # Alfa.Beta != Vazio
            if len(alfa) != 0 or len(beta) != 0:
                if alfa+beta not in lista_alfa_beta:
                    lista_alfa_beta.append(alfa+beta)
    return lista_alfa_beta

# PEGA APENAS AS PRODUCOES SEM &
def buscar_producoes_sem_epsilon(producoes, nao_terminais):
    producoes_novas = {}
    for nao_terminal in nao_terminais:
        producoes_novas[nao_terminal] = []
        for producao in producoes[nao_terminal]:
            if producao != '&':
                producoes_novas[nao_terminal].append(producao)
    return producoes_novas

# ENCONTRA TODOS OS NAO-TERMINAIS ANULAVEIS DA GRAMATICA
def encontrar_anulaveis(producoes, nao_terminais):
    anulaveis = ['&']
    while(True):
        mudanca = False
        for nao_terminal in nao_terminais:
            novos_anulaveis = []
            for producao in producoes[nao_terminal]:
                corpo_marcado = verificar_corpo_marcado(producao, anulaveis)
                if corpo_marcado and nao_terminal not in novos_anulaveis and nao_terminal not in anulaveis:
                    novos_anulaveis.append(nao_terminal)
                    mudanca = True
            anulaveis.extend(novos_anulaveis)
        if not mudanca:
            break
    return anulaveis

# PROCURAR POR NOVOS SIMBOLSO ALCANCAVEIS PARA UMA DETERMINADA PRODUCAO
def pegar_simbolos_alcancaveis_novos(producao, simbolos_alcancaveis):
    alcancaveis = []
    for simbolo in producao:
        if simbolo not in simbolos_alcancaveis:
            alcancaveis.append(simbolo)
    return alcancaveis

# VERIFICA SE TODOS OS SIMBOLOS DE UMA PRODUCAO ESTAO NA LISTA DE SIMBOLOS PRODUTIVOS
def verificar_corpo_marcado(producao, lista):
    for simbolo in producao:
        if simbolo not in lista:
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

def verificar_pertinencia_producao(producao, lista_simbolos):
    for simbolo in producao:
        if simbolo not in lista_simbolos:
            return False
    return True

def descobrir_pertinencia_alcancaveis(simbolo, simbolos_alcancaveis):
    pertinencias = []
    for nao_terminal in simbolos_alcancaveis.keys():
        if simbolo in simbolos_alcancaveis[nao_terminal]:
            pertinencias.append(nao_terminal)
    return pertinencias

def eh_producao_unitaria(glc, producao):
    return verificar_tamanho(producao, glc) == 1 and producao in glc.nao_terminais

def pegando_simbolos_alcancaveis(glc):
    simbolos_alcancaveis = {}
    for nao_terminal in glc.nao_terminais:
        simbolos_alcancaveis[nao_terminal] = [nao_terminal]
    # PROCURANDO NA
    for nao_terminal in glc.nao_terminais:
        for producao in glc.producoes[nao_terminal]:
            for producao in glc.producoes[nao_terminal]:
                # EH UMA PRODUCAO UNITARIA ?
                if eh_producao_unitaria(glc, producao):
                    if producao not in simbolos_alcancaveis[nao_terminal]:
                        simbolos_alcancaveis[nao_terminal].append(producao)
    for nao_terminal in glc.nao_terminais:
        for simbolo_alcancavel in simbolos_alcancaveis[nao_terminal]:
            novos_simbolos_alcancaveis = simbolos_alcancaveis[simbolo_alcancavel]
            for simbolo in novos_simbolos_alcancaveis:
                if simbolo not in simbolos_alcancaveis[nao_terminal]:
                    simbolos_alcancaveis[nao_terminal].append(simbolo)
    return simbolos_alcancaveis

def remover_producoes_circulares(glc):
    for nao_terminal in glc.nao_terminais:
        for producao in glc.producoes[nao_terminal]:
            if producao == nao_terminal:
                    (glc.producoes[nao_terminal]).remove(producao)

def encontrar_ultimo_simbolo(producao, glc):
    simbolos = ''
    indice = len(producao)-1
    for simbolo in reversed(producao):
        simbolos += simbolo
        if simbolos in glc.nao_terminais or simbolos in glc.terminais:
            return (simbolos, indice)
        indice -= 1
    return None

def verificar_tamanho(producao, glc):
    simbolos = ''
    contador = 0
    for simbolo in producao:
        simbolos += simbolo
        if simbolos in glc.nao_terminais or simbolos in glc.terminais:
            simbolos = ''
            contador += 1
    return contador

def tratar_tamanho_maior(nao_terminal, producao, glc, i):
    # ========================================================= DEBUG
    # print("----------------------- TRATANDO TAMANHO MAIOR")
    # print("Produção = %s" % producao)
    # ========================================================= DEBUG
    (ultimo, indice) = encontrar_ultimo_simbolo(producao,glc)
    resto = producao[0:indice]

    # ========================================================= DEBUG
    # print("Último = %s P[%d::]" % (producao[indice::], indice))
    # print("Resto = %s" % resto)
    # ========================================================= DEBUG

    nao_terminal_subtituinte = encontrar_producao_equivalente(glc,resto)

    if nao_terminal_subtituinte == None:
        nao_terminal_subtituinte = 'X_' + str(i)
        i += 1

    nova_producao = []
    nova_producao.insert(0, nao_terminal_subtituinte)
    nova_producao.append(ultimo)

    nova_producao_str = ''.join(nova_producao)


    # ADICIONANDO O NOVO NAO TERMINAL
    if nao_terminal_subtituinte not in glc.nao_terminais:
        glc.nao_terminais.append(nao_terminal_subtituinte)

    # REMOVENDO A PRODUCAO ANTIGA QUE NAO ATENDIA A FNC
    glc.producoes[nao_terminal].remove(producao)

    # ADICIONANDO A NOVA PRODUCAO CRIADA
    glc.producoes[nao_terminal].append(nova_producao_str)

    # ADICIONANDO O RESTO COMO PRODUCAO DO NOVO NAO TERMINAL
    glc.producoes[nao_terminal_subtituinte] = [resto]

    # ========================================================= DEBUG
    # print("Nova produção str = %s" % nova_producao_str)
    # print("%s -> %s" % (nao_terminal_subtituinte, resto))
    # ========================================================= DEBUG

    return i

def tratar_tamanho_dois(nao_terminal, producao, glc, i):
    # ========================================================= DEBUG
    # print("----------------------- TRATANDO TAMANHO DOIS")
    # print("Produção = %s" % producao)
    # ========================================================= DEBUG
    nao_terminal_subtituinte = None
    indice_nao_terminal = -1
    indice_terminal = -1
    (primeiro, indice) = pegar_primeiro_simbolo(producao, glc)
    parte_do_terminal = ''
    parte_nao_terminal = ''
    if primeiro in glc.terminais:
        # A -> cX_1
        indice_terminal = 0
        indice_nao_terminal = 1
        parte_do_terminal = producao[0]
        parte_nao_terminal = producao[1::]
    else:
        # A -> X_1c
        indice_terminal = indice
        indice_nao_terminal = 0
        parte_do_terminal = producao[indice::]
        parte_nao_terminal = producao[0:indice]

    nao_terminal_subtituinte = encontrar_producao_equivalente(glc,parte_do_terminal)

    if (nao_terminal_subtituinte == None):
        nao_terminal_subtituinte = 'X_' + str(i)
        i += 1

    nova_producao = []
    nova_producao.insert(indice_terminal, nao_terminal_subtituinte)
    nova_producao.insert(indice_nao_terminal, parte_nao_terminal)

    nova_producao_str = ''.join(nova_producao)


    if nao_terminal_subtituinte not in glc.nao_terminais:
        glc.nao_terminais.append(nao_terminal_subtituinte)

    # REMOVENDO A PRODUCAO ANTIGA QUE NAO ATENDIA A FNC
    glc.producoes[nao_terminal].remove(producao)

    # ADICIONANDO A NOVA PRODUCAO CRIADA
    glc.producoes[nao_terminal].append(nova_producao_str)

    # ADICIONANDO O RESTO AO NOVO NAO TERMINAL
    glc.producoes[nao_terminal_subtituinte] = [parte_do_terminal]

    # ========================================================= DEBUG
    # print("Nova produção str = %s" % nova_producao_str)
    # print("%s -> %s" % (nao_terminal_subtituinte, parte_do_terminal))
    # ========================================================= DEBUG

    return(i)

def encontrar_producao_equivalente(glc, terminal):
    # ========================================================= DEBUG
    # print("---------------------------\n PROCURANDO: Terminal %s" % terminal)
    # ========================================================= DEBUG
    for nao_terminal in glc.producoes.keys():
        for producao in glc.producoes[nao_terminal]:
            if (producao == terminal) and ('X_' in nao_terminal):
                # ========================================================= DEBUG
                # print("Encontrado: %s -> %s" % (nao_terminal, producao))
                # ========================================================= DEBUG
                return nao_terminal
    return None

def validar_pertinencia_fnc(producao, glc):
    # ========================================================= DEBUG
    # print("------------- VALIDANDO PERTINENCIA FNC -------------")
    # print("Produção = %s" % producao)
    # ========================================================= DEBUG
    if len(producao) == 1:
        return (producao in glc.terminais)
    elif verificar_tamanho(producao,glc) == 2:
        (primeiro, indice) = pegar_primeiro_simbolo(producao, glc)
        segundo = producao[indice::]
        # ========================================================= DEBUG
        # print("Primeiro símbolo = %s P[0:%d]" % (primeiro, indice))
        # print("Segundo símbolo = %s P[%d::]" % (producao[indice::], indice))
        # ========================================================= DEBUG
        return (primeiro in glc.nao_terminais) and (segundo in glc.nao_terminais)
    else:
        return False

def pegar_primeiro_simbolo(producao, glc):
    simbolos = ''
    indice = 0
    for simbolo in producao:
        simbolos += simbolo
        indice += 1
        if simbolos in glc.nao_terminais or simbolos in glc.terminais:
            return (simbolos, indice)
    return (None,-1)

def verificar_existencia_nao_determinismo_direto(glc, producoes):
    (terminais_producoes,terminais_a_esquerda) = pegar_terminais_a_esquerda(glc, producoes)
    # ========================================================= DEBUG
    # print("Terminais a esquerda = %s" % terminais_a_esquerda)
    # print("Terminais e suas produções = %s" % terminais_producoes)
    # ========================================================= DEBUG
    lista_filtrada = filtrar_lista_de_terminais(terminais_a_esquerda, terminais_producoes)
    return (lista_filtrada != [], lista_filtrada)

def resolver_nao_determinismo_direto(glc, nao_terminal, j):
    # ========================================================= DEBUG
    # print("------------------- DIRETO: Não terminal = %s" % nao_terminal)
    # print("P[%s] = %s" % (nao_terminal, glc.producoes[nao_terminal]))
    # ========================================================= DEBUG
    (existe_nao_determinismo_direto, lista_filtrada) = verificar_existencia_nao_determinismo_direto(glc, glc.producoes[nao_terminal])
    # ========================================================= DEBUG
    # print("Lista Filtrada = %s" % lista_filtrada)
    # ========================================================= DEBUG
    if existe_nao_determinismo_direto:
        mapeamento = mapear_terminais(lista_filtrada)

        # ========================================================= DEBUG
        # print("Mapeamento = %s" % mapeamento)
        # ========================================================= DEBUG

        for terminal in mapeamento.keys():

            # CRIANDO UM NOVO NAO TERMINAL PARA SUBSTITUIR O RESTO
            novo_nao_terminal = 'X_' + str(j)
            j += 1

            # ADICIONANDO O NOVO NAO TERMINAL
            glc.nao_terminais.append(novo_nao_terminal)
            glc.producoes[novo_nao_terminal] = []


            # REMOVENDO AS PRODUCOES VELHAS
            # ========================================================= DEBUG
            # print("--> Terminal: = %s" % terminal)
            # ========================================================= DEBUG
            for producao_alvo in mapeamento[terminal]:
                # ========================================================= DEBUG
                # print("Produção alvo = %s" % producao_alvo)
                # ========================================================= DEBUG
                # PROCURANDO O INDICE DO TERMINAL NA PRODUCAO
                (simbolo, indice) = pegar_primeiro_simbolo(producao_alvo, glc)

                resto = producao_alvo[indice::]

                if resto == '':
                    resto = '&'

                # ========================================================= DEBUG
                # print("Índice de %s = %d" % (terminal, indice))
                # print("Resto = %s" % resto)
                # ========================================================= DEBUG

                # REMOVENDO A PRODUCs = %s" % novas_producoes)
                # print("Relações = %s" % relAO A SER SUBSTITUIDA
                # ========================================================= DEBUG
                # print("Removendo: %s" % producao_alvo)
                # ========================================================= DEBUG
                glc.producoes[nao_terminal].remove(producao_alvo)

                # SUBSTITUINDO PELA PRODUCAO NOVA
                if (terminal + novo_nao_terminal) not in glc.producoes[nao_terminal]:
                    glc.producoes[nao_terminal].append(terminal + novo_nao_terminal)

                # ========================================================= DEBUG
                # print("P[%s] = %s" %(nao_terminal, glc.producoes[nao_terminal]) )
                # ========================================================= DEBUG

                # ADICIONANDO O RESTO DE CADA PRODUCAO VELHA COMO PRODUCAO DO NOVO NAO TERMINAL
                if resto not in glc.producoes[novo_nao_terminal]:
                    glc.producoes[novo_nao_terminal].append(resto)
                    # ========================================================= DEBUG
                    # print("P[%s] = %s" %(novo_nao_terminal, glc.producoes[novo_nao_terminal]) )
                    # ========================================================= DEBUG
    return j

def encontrar_nao_determinismo_indireto(glc, nao_terminal):
    producoes_temporarias = []
    relacoes = []
    # ========================================================= DEBUG
    # print("\nProduções de %s = %s" % (nao_terminal, glc.producoes[nao_terminal]))
    # ========================================================= DEBUG
    for producao in glc.producoes[nao_terminal]:
        (primeiro_simbolo,indice) = pegar_primeiro_simbolo(producao, glc)
        # ========================================================= DEBUG
        # print("Produção : %s" % producao)
        # ========================================================= DEBUG
        if primeiro_simbolo == None:
            continue
        if primeiro_simbolo in glc.terminais and producao not in producoes_temporarias:
            producoes_temporarias.append(producao)
            if primeiro_simbolo not in relacoes:
                relacoes.append((producao, producao))
        if primeiro_simbolo in glc.nao_terminais:
            # ========================================================= DEBUG
            # print("Primeiro símbolo: %s" % primeiro_simbolo)
            # ========================================================= DEBUG
            producoes_primeiro_simbolo = glc.producoes[primeiro_simbolo]
            # ========================================================= DEBUG
            # print("Produções do primeri símbolo : P[%s] = %s"  % (primeiro_simbolo, producoes_primeiro_simbolo))
            # ========================================================= DEBUG
            (producoes_subidas, relacao_entre_producoes) = subir_producoes(producao, producoes_primeiro_simbolo, indice)

            # ADICIONANDO CADA PRODUCAO SUBIDA AS PRODUCOES TEMPORARIAS
            for producao_subida in producoes_subidas:
                if producao_subida not in producoes_temporarias:
                    producoes_temporarias.append(producao_subida)

            # ADICIONANDO A RELACAO ENTRE CADA PRODUCAO NOVA E ANTIGA
            for par in relacao_entre_producoes:
                if par not in relacoes:
                    relacoes.append(par)
    # ========================================================= DEBUG
    # print("Produções temporárias: %s" % producoes_temporarias)
    # ========================================================= DEBUG
    (existe_nao_determinismo_direto, lista_filtrada) = verificar_existencia_nao_determinismo_direto(glc, producoes_temporarias)
    # ========================================================= DEBUG
    # print("Lista filtrada = %s" % lista_filtrada)
    # print("Existe não determinismo direto em %s ? %s" % (producoes_temporarias, existe_nao_determinismo_direto))
    # ========================================================= DEBUG
    if existe_nao_determinismo_direto:
        # SUBSTITUINDO AS PRODUCOES ANTIGAS PELAS TEMPORARIAS
        # ========================================================= DEBUG
        # print("Relações = %s" % relacoes)
        # ========================================================= DEBUG
        for par in relacoes:
            producao_substituida = par[1]
            if producao_substituida in glc.producoes[nao_terminal]:
                glc.producoes[nao_terminal].remove(producao_substituida)
        for producao in producoes_temporarias:
            glc.producoes[nao_terminal].append(producao)
        # ========================================================= DEBUG
        # print("P[%s] = %s" % (nao_terminal, glc.producoes[nao_terminal]))
        # ========================================================= DEBUG
        return True
    else:
        return False


def subir_producoes(producao_candidata, producoes, indice_primeiro_simbolo):
    novas_producoes = []
    relacao_entre_producoes = []
    for producao in producoes:
        nova_producao = producao + producao_candidata[indice_primeiro_simbolo::]
        # ========================================================= DEBUG
        # print("Nova produção = %s" % nova_producao)
        # ========================================================= DEBUG
        par = (nova_producao, producao_candidata)
        if nova_producao not in novas_producoes:
            novas_producoes.append(nova_producao)
        if par not in relacao_entre_producoes:
            relacao_entre_producoes.append(par)
    # ========================================================= DEBUG
    # print("Novas produções = %s" % novas_producoes)
    # print("Relações = %s" % relacao_entre_producoes)
    # ========================================================= DEBUG
    return (novas_producoes, relacao_entre_producoes)

def pegar_terminais_a_esquerda(glc, producoes):
    terminais_a_esquerda = []
    terminais_producoes = []
    for producao in producoes:
        (simbolo,indice) = pegar_primeiro_simbolo(producao, glc)
        if simbolo == None:
            continue
        if simbolo in glc.terminais:
            par_simbolo_producao = (simbolo,producao)
            par_simbolo_indice = (simbolo, indice)
            terminais_producoes.append(par_simbolo_producao)
            terminais_a_esquerda.append(simbolo)
    return (terminais_producoes,terminais_a_esquerda)

def filtrar_lista_de_terminais(terminais, terminais_producoes):
    lista_filtrada = []
    for par in terminais_producoes:
        if terminais.count(par[0]) > 1 and par not in lista_filtrada:
            lista_filtrada.append(par)
    return lista_filtrada

def mapear_terminais(lista):
    mapeamento = {}
    for par in lista:
        terminal = par[0]
        if terminal not in mapeamento.keys():
            mapeamento[terminal] = []
        indice = par[1]
        mapeamento[terminal].append(indice)
    return mapeamento
