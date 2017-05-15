# IPython log file

from numpy.random import randn

a = {"b": "c", "d": randn(), "c": {"a": "hehe", "e": {"f": {i : randn() for i in range(4)}}}}

a
from pprint import pprint

pprint(a, depth=2)
get_ipython().magic('who')
get_ipython().magic('reset -f')
get_ipython().magic('who')
get_ipython().magic('reset -f')
get_ipython().magic('who')
get_ipython().magic('hist # histórico de código/comandos executado')
def soma(a, b):
    
    return a + b
get_ipython().magic('hist # histórico de código/comandos executado')
get_ipython().magic('hist ? # histórico de código/comandos executado')
get_ipython().magic('pinfo %hist')
get_ipython().magic('history')
get_ipython().magic('hist')
get_ipython().magic('hist')
10 + 23
_ # último output
_3
a = 10 + 33

a
_i # último input
_i1 # primeiro input
exec(_i1) # reexecuta o primeiro input
get_ipython().magic('logstart')
get_ipython().system('head ipython_log.py')
get_ipython().magic('logstop')
