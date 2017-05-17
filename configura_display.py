# importa a biblioteca pandas
import pandas as pd

# Configuração de formatação de numéricos
# configura a formatação de inteiros, adicionando um separador de milhares
class _IntArrayFormatter(pd.io.formats.format.GenericArrayFormatter):

    def _format_strings(self):
        formatter = self.formatter or (lambda x: '{:,}'.format(x).replace(',', '.'))
        fmt_values = [formatter(x) for x in self.values]
        return fmt_values
pd.io.formats.format.IntArrayFormatter = _IntArrayFormatter

# função que formata float adicionando separador de milhares e separador de decimal
def format_float(f):
# https://www.python.org/dev/peps/pep-0378/#main-proposal-from-nick-coghlan-originally-called-proposal-i    
    return "{:,.2f}".format(f).replace(",", "X").replace(".", ",").replace("X", ".")
pd.set_option("display.float_format", format_float)

