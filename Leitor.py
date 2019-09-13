from structures.AutomatoFinito import Automato_Finito
from structures.GramaticaRegular import Gramatica_Regular
from structures.ExpressaoRegular import Expressao_Regular

import os
from os import path
from sys import argv

class Leitor:

    def __init__(self,arquivo):
        self.arquivo = arquivo

    def ler_arquivo(self):
        texto = None
        try:
            arquivo = open(self.arquivo)
            texto = arquivo.read().split('\n')
            arquivo.close()
        except OSError:
            print('Não foi possível abrir o arquivo %s' % self.arquivo)
            arquivo.close()

        tipo = self.pegar_tipo(texto)

        if (tipo == '*AF') : # Encontrou um automato finito
            return self.ler_automato(texto)
        elif (tipo == '*GR') : # Encontrou uma gramatica regular
            return self.ler_gramatica(texto)
        elif (tipo == '*ER') : # Encontrou uma expressao regular
            return self.ler_expressao(texto)
        else:
            print('O tipo descrito no arquivo não é compatível com AF, GR ou ER :/')
            exit()

    def ler_automato(self, texto):
        estados = self.pegar_estados(texto)
        alfabeto = self.pegar_alfabeto(texto)
        transicoes = self.pegar_transicoes(texto)
        estado_inicial = self.pegar_estado_inicial(texto)
        estados_aceitacao = self.pegar_estados_aceitacao(texto)

        automato = Automato_Finito(estados, alfabeto, transicoes, estado_inicial, estados_aceitacao)
        automato.arrumar_transicoes()

        # ========================== DEBUG
        # print(automato.alfabeto)
        # print(automato.transicoes)
        # print(automato.transicoes[len(automato.alfabeto)])
        # ========================== DEBUG

        return automato

    def ler_gramatica(self, texto):
        nao_terminais = self.pegar_nao_terminais(texto)
        terminais = self.pegar_terminais(texto)
        producoes = self.pegar_producoes(texto)
        simbolo_inicial = self.pegar_simbolo_inicial(texto)

        gramatica = Gramatica_Regular(nao_terminais, terminais, producoes, simbolo_inicial)

        gramatica.arrumar_producoes()

        # ========================== DEBUG
        # print(gramatica.producoes)
        # ========================== DEBUG

        return gramatica

    def ler_expressao(self, texto):
        alfabeto = self.pegar_alfabeto(texto)
        expressao = self.pegar_expressao(texto)

        expressao_reg = Expressao_Regular(alfabeto,expressao)

        return expressao_reg

    def pegar_tipo(self,texto):
        return texto[0]

    # ========================== AUTOMATOS

    def pegar_estados(self, texto):
        indice = texto.index('*Estados')
        return texto[indice+1].split()

    def pegar_estado_inicial(self, texto):
        indice = texto.index('*EstadoInicial')
        return texto[indice+1]

    def pegar_estados_aceitacao(self, texto):
        indice = texto.index('*EstadosDeAceitacao')
        return texto[indice+1].split()

    def pegar_alfabeto(self, texto):
        indice = texto.index('*Alfabeto')
        return texto[indice+1].split()

    def pegar_transicoes(self, texto):
        indice = texto.index('*Transicoes')
        return texto[indice+1:-1]

    # ========================== GRAMATICAS

    def pegar_nao_terminais(self, texto):
        indice = texto.index('*NaoTerminais')
        return texto[indice+1].split()

    def pegar_terminais(self, texto):
        indice = texto.index('*Terminais')
        return texto[indice+1].split()

    def pegar_simbolo_inicial(self, texto):
        indice = texto.index('*SimboloInicial')
        return texto[indice+1]

    def pegar_producoes(self, texto):
        indice = texto.index('*Producoes')
        return texto[indice+1:-1]

    # ========================== EXPRESSOES REGULARES

    def pegar_expressao(self, texto):
        indice = texto.index('*Expressao')
        return texto[indice+1]

if __name__ == "__main__":

    if len(argv) < 2:
        print('Não deu :<')
        exit()

    arquivo = argv[1]

    if not path.isfile(arquivo):
        print('Arquivo não encontrado')
        exit()

    leitor = Leitor(arquivo)
    af = leitor.ler_arquivo()
    af.determinizar()
