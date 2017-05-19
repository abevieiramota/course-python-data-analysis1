# IPython log file

from numpy.random import randn

a = {"b": "c", "d": randn(), "c": {"a": "hehe", "e": {"f": {i : randn() for i in range(4)}}}}

a
from pprint import pprint

pprint(a, depth=2)
minha_variavel = 26
minha_variable = 27
# autocomplete com objeto
lista = [1, 2, 3]
get_ipython().magic('pinfo lista')
import numpy as np

get_ipython().magic('psearch np.*load*')
get_ipython().magic('psearch np.lo*')
get_ipython().system('cat script1.py')
get_ipython().magic('run script1.py # executado sem acesso às variáveis e imports dessa sessão')
get_ipython().system('cat script2.py')
nome = "joão"

get_ipython().magic('run -i script2.py # executado com acesso às variáveis e imports dessa sessão')
import time

def demora_muito():
    
    for _ in range(100):
        
        time.sleep(5)
demora_muito() # botão interrupt kernel
get_ipython().magic('quickref')
import numpy as np
get_ipython().run_cell_magic('time', '', '\nnp.dot(np.random.randn(2, 30), np.random.randn(30, 2))\n# CPU time > tempo de execução em CPU\n# Wall time > tempo passado desde o envio do comando até a resposta')
get_ipython().run_cell_magic('timeit', '', '\nnp.dot(np.random.randn(100, 100), np.random.randn(100, 100))')
get_ipython().magic('who')
get_ipython().magic('reset -f')
get_ipython().magic('who')
get_ipython().magic('hist')
10 + 23
_ # último output
_3
_2
_o2
_1
_i1
_24
_i24
_23
_23 # _X, onde X é o número da célula
_i23 # _iX -> input, onde X é o número da célula
_23 # _X -> output, onde X é o número da célula
_ # último output
_23 # _X -> output, onde X é o número da célula
_i23 # _iX -> input, onde X é o número da célula
print(_i23) # _iX -> input, onde X é o número da célula
_i23 # _iX -> input, onde X é o número da célula
_22 # _X -> output, onde X é o número da célula
_i22 # _iX -> input, onde X é o número da célula
a = 10 + 33

a
_i # último input
exec(_i) # reexecuta o primeiro input
exec(_i) # reexecuta o input
a = 10 + 33

a
exec(_i) # reexecuta o input
get_ipython().magic('logstart')
get_ipython().system('head ipython_log.py')
get_ipython().magic('logstop')
