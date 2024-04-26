from ydata_profiling import ProfileReport
import pandas as pd
import re


def data_profiling(df, df_name, output_file=None):

    title = "Profiling Report - " + df_name
    filename = output_file + df_name + "_report.html"

    # criar relatório
    profile = ProfileReport(df, title= title) 

    # salvar resultados em um arquivo
    profile.to_file(filename)




def process_dataframe(df, df_name):

    print('Analisando a tabela ' + df_name + '\n')

    # Remover colunas com valores ausentes

    cols_df = df.columns

    print("Removendo colunas que possuem 100% de valores faltantes ...")
    df_cln = df.dropna(axis=1, how='all')

    cols_df_cln = df_cln.columns
    cols_removed = list(set(cols_df) - set(cols_df_cln))

    print('Colunas removidas da tabela ', df_name, ': \n', cols_removed)


    # Remover campos duplicados
    df_len = len(df_cln)

    print("\nRemovendo dados duplicados ...")

    df_cln = df_cln.drop_duplicates()

    dup_lines = len(df_cln) - df_len

    print('Foram removidas ', dup_lines, 'linhas da tabela ' + df_name)


    # Remover colunas constantes (opcional)
    print("\nRemovendo colunas constantes ...")

    list_constant = [col for col in df_cln.columns if df_cln[col].nunique() == 1]
    df_cln = df_cln.drop(list_constant, axis=1)

    print('Colunas constantes removidas da tabela ' + df_name + ': \n', list_constant)

    return df_cln    




def remove_outliers(df, cols_list):
    """
    Remover outliers de colunas específicas. Considera-se outliers em colunas numéricas 
    selecionadas com valor acima ou abaixo de 2 desvios padrão da média.

    Parameters
    ----------
    df: dataframe
        Dataframe processado.
        
    cols_list: list
        Lista de colunas para considerar a eliminação de outliers.

    Returns
    -------
    df: dataframe
        Dataframe sem outliers.

    """
    qtd_lines = len(df)

    df_aux = df.copy()
    for col in cols_list:
        low_limit = df_aux[col].quantile(.02) 
        high_limit = df_aux[col].quantile(.98) 

        df = df[(df[col]>low_limit) & (df[col]<high_limit)] 

    qtd_lines = qtd_lines - len(df)

    print("\nQuantidade de linhas (outliers) eliminadas: ", qtd_lines )

    return df

def remove_special_caracters(texto):
    if pd.isnull(texto):  # Verifica se o valor é nulo
        return None  # Retorna nulo se for o caso
    
    # Define a expressão regular para encontrar caracteres especiais
    padrao = r'[^a-zA-Z0-9\s.()]'  # Remove tudo que não é letra, número, espaço, ponto ou parênteses

    # Substitui os caracteres especiais por uma string vazia
    texto_limpo = re.sub(padrao, '', texto)
    
    return texto_limpo