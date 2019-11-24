# ===================================== TODO
# [ ] COMENTAR CADA METODO
# [ ] AJUSTAR CADA CHAMADA DE METODOS P/ OS AUXILIARES
# ===================================== TODO

from src.operacoes_auxiliares_glc import *

# REMOCAO DE SIMBOLOS IMPRODUTIVOS DE UMA GRAMATICA
def remover_simbolos_improdutivos(glc):
    simbolos_produtivos = []
    simbolos_produtivos.extend(glc.terminais)
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

def remover_producoes_por_epsilon(glc):
    anulaveis = encontrar_anulaveis(glc.producoes, glc.nao_terminais)
    # ===================================================================== DEBUG
    # print("Anuláveis = %s" % anulaveis)
    # ===================================================================== DEBUG
    producoes_novas = buscar_producoes_sem_epsilon(glc.producoes, glc.nao_terminais)
    # ===================================================================== DEBUG
    # print("P' = %s" % producoes_novas)
    # ===================================================================== DEBUG
    for nao_terminal in glc.nao_terminais:
        for producao in producoes_novas[nao_terminal]:
            # ===================================================================== DEBUG
            # print("Produção = %s" % producao)
            # ===================================================================== DEBUG
            lista_alfa_beta = pegar_alfas_e_betas(producao, anulaveis)
            # ===================================================================== DEBUG
            # print("Lista_Alfa_Beta = %s" % lista_alfa_beta)
            # ===================================================================== DEBUG
            for alfa_beta in lista_alfa_beta:
                if alfa_beta not in producoes_novas[nao_terminal]:
                    producoes_novas[nao_terminal].append(alfa_beta)
    producoes = {}
    if glc.simbolo_inicial in anulaveis:
        novo_simbolo_inicial = 'S_inicial'
        # S_inicial -> S | &
        producoes[novo_simbolo_inicial] = [glc.simbolo_inicial,'&']
        # N' = N U {S_inicial}
        glc.nao_terminais.insert(0, novo_simbolo_inicial)
        # Adiciona S_inicial como o novo simbolo inicial
        glc.simbolo_inicial = novo_simbolo_inicial
    producoes.update(producoes_novas)
    glc.producoes = producoes


def remover_producoes_unitarias(glc):
    remover_producoes_circulares(glc)
    simbolos_alcancaveis = pegando_simbolos_alcancaveis(glc)
    novas_producoes = {}
    for nao_terminal in glc.nao_terminais:
        novas_producoes[nao_terminal] = []

    for nao_terminal in glc.nao_terminais:
        pertinencias = descobrir_pertinencia_alcancaveis(nao_terminal, simbolos_alcancaveis)
        for producao in glc.producoes[nao_terminal]:
            if not eh_producao_unitaria(glc, producao):
                for nao_terminal_pertencente in pertinencias:
                    if producao not in novas_producoes[nao_terminal_pertencente]:
                        novas_producoes[nao_terminal_pertencente].append(producao)
    glc.producoes = novas_producoes


def transformar_em_fnc(glc):
    print("\nVAZIAS:")
    remover_producoes_por_epsilon(glc)
    print("\nUNITÁRIAS:")
    remover_producoes_unitarias(glc)
    print("\nIMPRODUTIVOS:")
    remover_simbolos_improdutivos(glc)
    print("\nINCALCANÇÁVEIS:")
    remover_inalcancaveis_glc(glc)
    i = 1
    while(True):
        mudanca = False
        for nao_terminal in glc.nao_terminais:
            for producao in glc.producoes[nao_terminal]:
                # ========================================================= DEBUG
                # print(glc.producoes[nao_terminal])
                # print("========================= %s -> %s" % (nao_terminal, producao))
                # ========================================================= DEBUG
                pertence_a_fnc = validar_pertinencia_fnc(producao, glc)
                if not pertence_a_fnc:
                    if verificar_tamanho(producao, glc) == 2:
                        i = tratar_tamanho_dois(nao_terminal, producao, glc, i)
                        mudanca = True
                    else:
                        i = tratar_tamanho_maior(nao_terminal, producao, glc, i)
                        mudanca = True
                    # ========================================================= DEBUG
                    # print(glc.producoes[nao_terminal])
                    # ========================================================= DEBUG
        if not mudanca:
            break


def fatorar(glc):
    j = 0
    # RESOLVE PRIMEIRO O NAO DETERMINISMO DIRETO
    for nao_terminal in glc.nao_terminais:
        j = resolver_nao_determinismo_direto(glc, nao_terminal, j)
    # SE ENCONTRAR UMA NAO DETERMINISMO INDIRETO, RESOLVA-O
    contador = 0
    for nao_terminal in glc.nao_terminais:
        if contador > 10:
            print("====> ERRO: Não foi possível fatorar a gramática.")
            return None
        existe_nao_determinismo_indireto = encontrar_nao_determinismo_indireto(glc, nao_terminal)
        if existe_nao_determinismo_indireto:
            contador += 1
            j = resolver_nao_determinismo_direto(glc, nao_terminal, j)
    print("====> SAÍDA:")


def remover_recursao_esquerda_dir_indir(glc):
    
    remover_recursao_esquerda_direta(glc)
    remover_producoes_por_epsilon(glc)
    remover_recursao_esquerda_indireta(glc)

    return glc

def remover_recursao_esquerda_indireta(glc):
    novas_producoes = {N : [] for N in glc.nao_terminais}
    for i, Ai in enumerate(glc.nao_terminais):
        for j in range(i):
            Aj = glc.nao_terminais[j]
            for prodAi in glc.producoes[Ai]:
                if Aj == prodAi[: len(Aj)]:
                    glc.producoes[Ai].remove(prodAi)
                    for prodAj in glc.producoes[Aj]:
                        prod = prodAj + prodAi[len(Aj):]
                        if prod not in novas_producoes[Ai]:
                            novas_producoes[Ai].append(prod)

                else:
                    prod = prodAi
                    if prod not in novas_producoes[Ai]:
                        novas_producoes[Ai].append(prod)
        else:
            for prodAi in glc.producoes[Ai]:
                prod = prodAi
                if prod not in novas_producoes[Ai]:
                    novas_producoes[Ai].append(prod)

    glc.producoes = novas_producoes

    return glc

    
def remover_recursao_esquerda_direta(glc):
    new_prods = dict()
    for head, bodies in glc.producoes.items():
        recursive_bodies = []
        for body in bodies:
            if body[0] == head:
                recursive_bodies.append(body)

        if recursive_bodies:
            new_head = head + "'"
            new_head_bodies = ['&']
            head_bodies = []
            for body in bodies:
                if body in recursive_bodies:
                    new_head_bodies.append(body[1:] + new_head)
                else:
                    head_bodies.append(body + new_head)

            new_prods[head] = head_bodies
            new_prods[new_head] = new_head_bodies

        else:
            new_prods[head] = bodies

    glc.nao_terminais = list(set(new_prods.keys()))
    glc.producoes = new_prods

    return glc
            
            