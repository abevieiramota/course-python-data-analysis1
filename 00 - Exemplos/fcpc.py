# importa a biblioteca pandas
import pandas as pd
# importa a biblioteca numpy
import numpy as np
# importa o módulo pyplot, do matplotlib
from matplotlib import pyplot as plt

# Configuração de formatação de numéricos
# configura a formatação de inteiros, adicionando um separador de milhares
class _IntArrayFormatter(pd.formats.format.GenericArrayFormatter):

    def _format_strings(self):
        formatter = self.formatter or (lambda x: '{:,}'.format(x).replace(',', '.'))
        fmt_values = [formatter(x) for x in self.values]
        return fmt_values
pd.formats.format.IntArrayFormatter = _IntArrayFormatter

# função que formata float adicionando separador de milhares e separador de decimal
def format_float(f):
# https://www.python.org/dev/peps/pep-0378/#main-proposal-from-nick-coghlan-originally-called-proposal-i    
    return "{:,.2f}".format(f).replace(",", "X").replace(".", ",").replace("X", ".")
pd.set_option("display.float_format", format_float)

# leitura de arquivo .CSV
fcpc = pd.read_csv("../../dataset-fcpc/pagamento pessoa fisica/dataset.csv")
fcpc["DATA"] = pd.to_datetime(fcpc.DATA, format="%d/%m/%Y")

# reconstitui as colunas normalizadas
base_path = "../../dataset-fcpc/pagamento pessoa fisica/"
for fk in (col for col in fcpc.columns if col.endswith("-ID")):
    
    filepath = "{}{}.csv".format(base_path, fk.split("-")[0])
    col_df = pd.read_csv(filepath)
    fcpc = pd.merge(fcpc, col_df)
    fcpc.drop(fk, axis=1, inplace=True)
    
fcpc["PROJETO_ID"] = fcpc.PROJETO.apply(lambda v: v.split("-", maxsplit=1)[0].strip())