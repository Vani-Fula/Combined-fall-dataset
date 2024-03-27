# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 23:14:29 2023

@author: Vanilson Fula
"""

import os
import pandas as pd
import numpy as np

# Diretório raiz onde estão as pastas
diretorio_raiz = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados\UMA"
# Lista de nomes das atividades de interesse
atividades_interesse = ['Activity13', 'Activity14', 'Activity15']

# Índice da coluna que deseja substituir (assumindo que a primeira coluna tem índice 0)
indice_coluna = "Tag"

# Função para detectar mudanças bruscas
def detectar_mudancas_bruscas(dados, limiar):
    mudancas = []
    for i in range(1, len(dados)):
        diff = abs(dados[i] - dados[i-1])
        if diff > limiar:
            mudancas.append(i)
    return mudancas

def encontrar_indice_valor_max(dados, mudancas):
    indice_max = max(mudancas, key=lambda i: abs(dados[i] - dados[i-1]))
    return indice_max

# Função para encontrar os índices de início e fim da janela
def find_window_indices(dados, limiar=0.7, duracao_janela=3.0):
    aceleracao_x = dados['Accelerometer: x-axis (g)']
    aceleracao_y = dados['Accelerometer: y-axis (g)']
    aceleracao_z = dados['Accelerometer: z-axis (g)']

    mudancas_x = detectar_mudancas_bruscas(aceleracao_x, limiar)
    mudancas_y = detectar_mudancas_bruscas(aceleracao_y, limiar)
    mudancas_z = detectar_mudancas_bruscas(aceleracao_z, limiar)

    inicio_janela_x = encontrar_indice_valor_max(aceleracao_x, mudancas_x)
    inicio_janela_y = encontrar_indice_valor_max(aceleracao_y, mudancas_y)
    inicio_janela_z = encontrar_indice_valor_max(aceleracao_z, mudancas_z)
    inicio_janela = int(np.mean([inicio_janela_x, inicio_janela_y, inicio_janela_z])) if mudancas_x and mudancas_y and mudancas_z else 0

    # Definindo o tempo de maior mudança
    tempo_maior_mudanca = dados['TimeStamp'][inicio_janela]
    # Definindo o término da janela 1.5 segundos antes da maior mudança
    tempo_inicio_janela = tempo_maior_mudanca - 1
    # Definindo o término da janela 1.5 segundos após a maior mudança
    tempo_fim_janela = tempo_maior_mudanca + 1.5

    idx_inicio_janela = dados.index[dados['TimeStamp'] >= tempo_inicio_janela]
    idx_fim_janela = dados.index[dados['TimeStamp'] >= tempo_fim_janela]

    # Verificando se o índice de fim da janela foi encontrado
    if len(idx_fim_janela) == 0:
        # Caso não tenha sido encontrado, definimos o índice de fim como o último índice do DataFrame
        idx_fim_janela = len(dados) - 1
    else:
        # Caso contrário, pegamos o primeiro índice encontrado
        idx_fim_janela = idx_fim_janela[0]

    # Verificando se o índice de início da janela foi encontrado
    if len(idx_inicio_janela) == 0:
        # Caso não tenha sido encontrado, definimos o índice de início como o primeiro índice do DataFrame
        idx_inicio_janela = 0
    else:
        # Caso contrário, pegamos o primeiro índice encontrado
        idx_inicio_janela = idx_inicio_janela[0]

    return idx_inicio_janela, idx_fim_janela

# Função para alterar os valores da última coluna dentro da janela para 1
def alterar_valores_janela(dados, idx_inicio_janela, idx_fim_janela, coluna_alterar):
    dados_alterados = dados.copy()
    dados_alterados.loc[idx_inicio_janela:idx_fim_janela, coluna_alterar] = "1"
    return dados_alterados

# Função para procurar arquivos CSV em vários diretórios, incluindo subdiretórios,
# e filtrar apenas os arquivos que possuem os nomes de atividades de interesse
def procurar_arquivos_csv(diretorio):
    arquivos_csv = []
    for pasta_atual, _, arquivos in os.walk(diretorio):
        for arquivo in arquivos:
            if arquivo.endswith('.csv'):
                for atividade in atividades_interesse:
                    if atividade in arquivo:
                        caminho_completo = os.path.join(pasta_atual, arquivo)
                        arquivos_csv.append(caminho_completo)
                        break
                
    return arquivos_csv

# Procurar arquivos CSV nos diretórios de interesse
arquivos_csv = procurar_arquivos_csv(diretorio_raiz)

# Processar os arquivos CSV um a um
for arquivo_csv in arquivos_csv:
    # Abrir o arquivo para leitura e carregar os dados em um DataFrame
    try:
        dados = pd.read_csv(arquivo_csv)
        
        # Verifica se o DataFrame não está vazio
        if not dados.empty:
            # Verifica se a atividade do arquivo está entre as atividades de interesse
            atividade_encontrada = any(atividade in arquivo_csv for atividade in atividades_interesse)

            if atividade_encontrada:
                # Encontra os índices de início e fim da janela
                idx_inicio_janela, idx_fim_janela = find_window_indices(dados)

                # Altera os valores da última coluna dentro da janela para 1
                dados_alterados = alterar_valores_janela(dados, idx_inicio_janela, idx_fim_janela, indice_coluna)

                # Salva os dados alterados no mesmo arquivo original
                dados_alterados.to_csv(arquivo_csv, index=False)
            else:
                print(f"Atividade do arquivo não está entre as atividades de interesse: {arquivo_csv}")
        else:
            print(f"DataFrame vazio no arquivo: {arquivo_csv}")

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {arquivo_csv}")
    except Exception as e:
        print(f"Erro ao processar o arquivo {arquivo_csv}: {str(e)}")

