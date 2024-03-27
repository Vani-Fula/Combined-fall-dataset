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
        
        taxa_amostragem_original = old_freq  # Hz
        taxa_amostragem_desejada = new_freq  # Hz
        # Fator de downsampling desejado
        fator_downsampling = int(taxa_amostragem_original/taxa_amostragem_desejada)
        
        
        
        # Percorrer todas as subpastas e arquivos CSV
        for pasta_atual, subpastas, arquivos in os.walk(diretorio_raiz):
            for arquivo_entrada in arquivos:
                if arquivo_entrada.endswith('.csv'):
                    caminho_arquivo = os.path.join(pasta_atual, arquivo_entrada)
            
                    
                    # Leitura do arquivo CSV para um DataFrame
                    df = pd.read_csv(caminho_arquivo)
        
                    # Extrair o cabeçalho do arquivo original
                    cabeçalho = list(df.columns)
        
                    # Selecionar apenas as colunas de interesse para o downsampling
                    colunas_interesse = cabeçalho[1:7]
        
                    # Realizar o downsampling nos dados
                    dados_downsampled = df[colunas_interesse].iloc[::fator_downsampling]
                    tempo_downsampled = df['TimeStamp'].iloc[::fator_downsampling]
                    info_downsampled = df.iloc[::fator_downsampling, 7:]
        
                    # Criar um novo DataFrame com os dados downsampled e informações originais
                    df_downsampled = pd.concat([tempo_downsampled, dados_downsampled, info_downsampled], axis=1)
        
                    # Criar o caminho de destino para o novo arquivo CSV
                    nome_arquivo = os.path.splitext(arquivo_entrada)[0]
                    caminho_arquivo_downsampled = os.path.join(pasta_atual, nome_arquivo + '.csv')
        
                    # Salvar os dados downsampled em um novo arquivo CSV, mantendo o cabeçalho original
                    df_downsampled.to_csv(caminho_arquivo_downsampled, index=False, header=cabeçalho)

                    