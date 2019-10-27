from structures.ExpressaoRegular import ExpressaoRegular
from src.operacoes import er_para_afd
from Leitor import Leitor
import os
er = ExpressaoRegular(['a', 'b'], '(a+b).a.b.(a+b)*')

afd = er_para_afd(er)
