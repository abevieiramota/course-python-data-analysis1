from lxml import etree
from lxml import objectify
import codecs
import pandas as pd
import os
import re
import logging
import sys
from sklearn.preprocessing import LabelEncoder

logger = logging.getLogger("GastosDiretosExtractor")

# LÊ XMLS E CONVERTE EM CSVS

cols = ['ANO-PAGAMENTO',
        'MODALIDADE-DO-PROCESSO',
        #'MOEDA', removido por, à época da criação do script ser tudo REAL
        'NOME-COMPLETO',
        'NOME-CURSO',
        'NOME-DA-AREA-DO-CONHECIMENTO',
        'NOME-DA-ESPECIALIDADE',
        'NOME-DA-SUB-AREA-DO-CONHECIMENTO',
        'NOME-GRANDE-AREA-DO-CONHECIMENTO',
        'PAIS-INSTITUICAO',
        'PAIS-NASCIMENTO',
        'QUANTIDADE-MESES-PAGOS',
        'QUANTIDADE-BOLSA-ANO',
        'SEXO',
        'SIGLA-INSTITUICAO',
        'SIGLA-UF-INSTITUICAO',
        'TITULO-DO-PROCESSO',
        'VALOR-PAGO']

def read_xml(filepath):

    parsed = None

    iso_8859_1_parser = etree.XMLParser(encoding="iso-8859-1")

    with codecs.open(filepath, encoding="iso-8859-1") as f:

        parsed = objectify.parse(f, parser=iso_8859_1_parser)

    bolsa_elements = parsed.getroot().getchildren()

    data = []

    for bolsa_element in bolsa_elements:
        
        attributes = [attribute for attribute in bolsa_element.getchildren() if attribute.tag in cols]

        bolsa_data = {attribute.tag: attribute.text for attribute in attributes}

        data.append(bolsa_data)
        
    return data

def convert_xml_to_csv():

    logger.info("CONVERTENDO XML PARA CSV")

    for filename in [filename for filename in os.listdir('.') if filename.endswith('.xml')]:

        logger.info(">{}".format(filename))

        data = read_xml(filename)
        
        df = pd.DataFrame(data)

        df.to_csv(filename.split('.')[0] + '.csv', index=False, encoding='utf-8')

# NORMALIZA COLUNAS STRING

categorical_colnames = ['NOME-CURSO',
                        'NOME-DA-AREA-DO-CONHECIMENTO',
                        'NOME-DA-ESPECIALIDADE',
                        'NOME-DA-SUB-AREA-DO-CONHECIMENTO',
                        'NOME-GRANDE-AREA-DO-CONHECIMENTO',
                        'PAIS-INSTITUICAO',
                        'PAIS-NASCIMENTO',
                        'TITULO-DO-PROCESSO',
                        'SIGLA-INSTITUICAO',
                        'MODALIDADE-DO-PROCESSO',
                        'NOME-COMPLETO']

datasets_filename_re = re.compile(r'hst_pgt_bolsas_cnpq_\d{4}\.csv')

def make_encoders():

    logger.info("NORMALIZANDO COLUNAS")

    encoders = {}

    dfs = []

    for filename in [filename for filename in os.listdir('.') if datasets_filename_re.match(filename)]:
        
        df = pd.read_csv(filename, encoding='utf-8', usecols=categorical_colnames, dtype='str')
        
        dfs.append(df)

    df = pd.concat(dfs).fillna("NÃO-ESPECIFICADO")

    for categorical_colname in categorical_colnames:

        logger.info(">{}".format(categorical_colname))

        encoder = LabelEncoder().fit(df[categorical_colname].unique())
    
        encoder_df = pd.DataFrame(encoder.classes_, columns=[categorical_colname])
        encoder_df.index.name = categorical_colname + '-ID'
        encoder_df.to_csv(categorical_colname + ".csv", encoding='utf-8')
        
        encoders[categorical_colname] = encoder

    return encoders

def make_dataset(encoders):

    logger.info("CRIANDO DATASET FINAL")

    categorical_id_colnames = [colname + "-ID" for colname in categorical_colnames]

    dfs = []

    for filename in [filename for filename in os.listdir('.') if datasets_filename_re.match(filename)]:

        logger.info(">{}".format(filename))
        
        df = pd.read_csv(filename, encoding='utf-8', dtype='str')
        
        df[categorical_colnames] = df[categorical_colnames].fillna("NÃO-ESPECIFICADO")
        
        df[categorical_id_colnames] = df[categorical_colnames].apply(lambda col: encoders[col.name].transform(col))
        df.drop(categorical_colnames, axis=1, inplace=True)
        
        dfs.append(df)
    df = pd.concat(dfs)

    df.to_csv("dataset.csv", encoding='utf-8', index=False)

def read_dataset(filepath):

    df = pd.read_csv(filepath)

    df['ANO-PAGAMENTO'] = pd.to_numeric(df['ANO-PAGAMENTO'])
    df['QUANTIDADE-BOLSA-ANO'] = pd.to_numeric(df['QUANTIDADE-BOLSA-ANO'])
    df['QUANTIDADE-MESES-PAGOS'] = pd.to_numeric(df['QUANTIDADE-MESES-PAGOS'])
    df['VALOR-PAGO'] = pd.to_numeric(df['VALOR-PAGO'])

    return df


if __name__ == '__main__':

    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    #convert_xml_to_csv()
    encoders = make_encoders()
    make_dataset(encoders)
