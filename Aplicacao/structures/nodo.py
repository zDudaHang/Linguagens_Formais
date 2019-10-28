class Nodo:
    '''
        Classe para representar o novo da árvore sintática usada na conversão de ER
        para AFD 
    '''

    CAT = '.'
    OR = '+'
    STAR = '*'
    LEAF = None
    tipos = [CAT, OR, STAR, LEAF]

    def __init__(self, c1, c2, tipo, simb):
        self.tipo = tipo
        self.c1 = c1
        self.c2 = c2
        self.simb = simb
        self.index = None

    @property
    def eh_folha(self):
        # TODO arrumar os índices dessa ponhoca
        return self.c1 is None and self.c2 is None

    @property
    def anulavel(self):
        if self.simb == '&':
            return True

        elif self.eh_folha:
            return False

        elif self.tipo == self.CAT:
            return self.c1.anulavel and self.c2.anulavel

        elif self.tipo == self.OR:
            return self.c1.anulavel or self.c2.anulavel

        elif self.tipo == self.STAR:
            return True

    @property
    def firstpos(self):
        if self.simb == '&':
            return set()

        elif self.eh_folha:
            return set([self.index])

        elif self.tipo == self.CAT:
            if self.c1.anulavel:
                return self.c1.firstpos.union(self.c2.firstpos)
            
            else:
                return self.c1.firstpos

        elif self.tipo == self.OR:
            return self.c1.firstpos.union(self.c2.firstpos)

        elif self.tipo == self.STAR:
            return self.c1.firstpos

    @property
    def secondpos(self):
        if self.simb == '&':
            return set()

        elif self.eh_folha:
            return set([self.index])

        elif self.tipo == self.CAT:
            if self.c2.anulavel:
                return self.c1.secondpos.union(self.c2.secondpos)
            
            else:
                return self.c2.secondpos

        elif self.tipo == self.OR:
            return self.c1.secondpos.union(self.c2.secondpos)

        elif self.tipo == self.STAR:
            return self.c2.secondpos
        

    def __str__(self, level=0):
        ret = "  " * level
        if self.eh_folha:
            ret += f'{self.simb} {self.index} \n'
        else:
            ret += f'{self.tipo} \n'

        if self.tipo == self.STAR:
            ret += self.c1.__str__(level+1)
        else:
            for child in (self.c2, self.c1):
                if child is not None:
                    ret += child.__str__(level+1)
        return ret

    def make_index(self, i):
        if not self.eh_folha and self.tipo != self.STAR:
            i = self.c1.make_index(i)
            i = self.c2.make_index(i)
        
        elif self.tipo == self.STAR:
            i = self.c1.make_index(i)

        else:
            self.index = i
            i += 1

        return i


    def pegar_alfabeto(self, alfabeto=None):
        if alfabeto is None:
            alfabeto = set()

        if self.eh_folha:
            if self.simb != '#':
                alfabeto.add(self.simb)

        else:
            alfabeto = self.c1.pegar_alfabeto(alfabeto)
            alfabeto = self.c2.pegar_alfabeto(alfabeto)

        return alfabeto
        
    def pegar_correspondentes(self, correspondentes=None):
        if correspondentes is None:
            correspondentes = dict()

        if self.eh_folha:
            correspondentes[self.index] = self.simb

        else:
            correspondentes = self.c1.pegar_correspondentes(correspondentes)
            correspondentes = self.c2.pegar_correspondentes(correspondentes)

        return correspondentes
