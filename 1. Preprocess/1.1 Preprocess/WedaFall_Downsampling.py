# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 23:36:18 2023

@author: Vanilson Fula
"""
import os
import shutil
import numpy as np
import csv
import glob
import pandas as pd
from scipy import signal
from scipy import interpolate




def Downsampled(diretorio_raiz, old_freq, new_freq):
    
    taxa_amostragem_original = old_freq   # Hz
    taxa_amostragem_desejada = new_freq    # Hz
    # Fator de downsampling desejado
    fator_downsampling = int(taxa_amostragem_original/taxa_amostragem_desejada)
    fator_decimacao = fator_downsampling
    
    
    
    # Percorrer todas as subpastas e arquivos CSV
    for pasta_atual, subpastas, arquivos in os.walk(diretorio_raiz):
        for arquivo_entrada in arquivos:
            if arquivo_entrada.endswith('.csv'):
                caminho_arquivo = os.path.join(pasta_atual, arquivo_entrada)
        
                # Leitura do arquivo CSV para um DataFrame
                df = pd.read_csv(caminho_arquivo)
                
                colunas = df.columns[1:]
                dados = df.iloc[:, 1:].values.astype(float)
                tempo = df.iloc[:, 0].values
                
                
                
                
                #_________________ Downsampled: Outros  ______________
    
                # Calcular o novo intervalo de tempo
                intervalo_tempo_antigo = 1 / taxa_amostragem_original
                intervalo_tempo_novo = 1 / taxa_amostragem_desejada
                
                
                # Realizar o downsampling
                num_linhas_downsampled = int(len(dados) / fator_downsampling)
                dados_downsampled = dados[::fator_downsampling]
                tempo_downsampled = tempo[::fator_downsampling]
                
                # Criar um novo DataFrame com os dados downsampled e tempo downsampled
                colunas_downsampled = colunas.insert(0, 'tempo')
                dados_downsampled = np.hstack((tempo_downsampled.reshape(-1, 1), dados_downsampled))
                df_downsampled = pd.DataFrame(dados_downsampled, columns=colunas_downsampled)
                
                # Obter o nome do arquivo sem a extensão
                nome_arquivo = os.path.splitext(arquivo_entrada)[0]
                
                # Criar o caminho de destino para o novo arquivo CSV
                caminho_arquivo_downsampled = os.path.join(pasta_atual, nome_arquivo + '.csv')
                
                # Salvar os dados downsampled em um novo arquivo CSV
                df_downsampled.to_csv(caminho_arquivo_downsampled, index=False)
                
                return
            
            
            
            
            
            
            