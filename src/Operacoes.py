from structures.AutomatoFinito import Automato_Finito
from structures.GramaticaRegular import Gramatica_Regular

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
    novo_automato = Automato_Finito(novos_estados, automato_A.alfabeto, novas_transicoes, novo_estado_inicial, novos_estados_de_aceitacao)

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

def transformar_em_GR(automato):
    producoes = {}
    nao_terminais = gerar_nao_terminais(automato)
    for nao_terminal in nao_terminais:
        producoes[nao_terminal] = []
    i = 0
    for estado in automato.estados:
        for j in range(0, len(automato.alfabeto)):
            transicao = automato.transicoes[estado][j]
            nao_terminal_correspondente = nao_terminais[i]
            for estado_transicao in transicao.split(','):
                indice = automato.estados.index(estado_transicao)
                nao_terminal = nao_terminais[indice]
                letra = automato.alfabeto[j]
                producao = letra + nao_terminal
                producoes[nao_terminal_correspondente].append(producao)
                if estado_transicao in automato.estados_aceitacao:
                    producoes[nao_terminal_correspondente].append(letra)
        i += 1
    gramatica_regular = Gramatica_Regular(nao_terminais, automato.alfabeto, producoes, nao_terminais[0])
    return gramatica_regular

def gerar_nao_terminais(automato):
    nao_terminais = ['S']
    nao_terminal = 'A'
    for i in range(0, len(automato.estados) - 1):
        nao_terminais.append(nao_terminal)
        nao_terminal = chr(ord(nao_terminal) + 1)
    return nao_terminais
