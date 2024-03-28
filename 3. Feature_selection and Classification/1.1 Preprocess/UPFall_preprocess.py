# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 02:01:43 2023

@author: Vanilson Fula
"""

import os
import shutil
import csv
import glob
import math
import pandas as pd
from datetime import datetime , timedelta



def process_UP(pasta_entrada, pasta_saida):
    
    # Diretório raiz onde os arquivos CSV estão localizados
    diretorio_raiz = pasta_entrada
    
    # Índices das colunas que serão removidas
    indices_colunas_remover = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 
                               20, 21, 22, 23, 24, 25, 26, 27, 28, 35, 36, 37, 38, 39, 40, 41, 42]  # Por exemplo, remover as colunas de índice

    
    # Cria a pasta de saída (caso não exista)
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
    
    # Percorrer todas as subpastas e arquivos CSV
    for pasta_atual, subpastas, arquivos in os.walk(diretorio_raiz):
        # Cria a estrutura de pastas na pasta de saída
        pasta_saida_atual = os.path.join(pasta_saida, os.path.relpath(pasta_atual, diretorio_raiz))
        if not os.path.exists(pasta_saida_atual):
            os.makedirs(pasta_saida_atual)
        
        for arquivo_entrada in arquivos:
            if arquivo_entrada.endswith('.csv'):
                caminho_arquivo = os.path.join(pasta_atual, arquivo_entrada)
                nome_arquivo = os.path.splitext(arquivo_entrada)[0]
                
                # Define o caminho de saída para o arquivo selecionado
                arquivo_saida = os.path.join(pasta_saida_atual, "UPFALL_" + nome_arquivo + ".csv")            
                
                # Inicializa a lista para armazenar as linhas selecionadas
                linhas_selecionadas = []
                 
                
                try: 
                    with open(caminho_arquivo, 'r') as arquivo_csv:
                        leitor_csv = csv.reader(arquivo_csv)
                        linhas = list(leitor_csv)
                        
                        
                        # Criar um novo cabeçalho com as colunas existentes mais as colunas "Subject" e "Trial"
                        novo_cabecalho = ['TimeStamp', 'Accelerometer: x-axis (g)', 'Accelerometer: y-axis (g)', 
                                          'Accelerometer: z-axis (g)', 'Gyroscope: x-axis (rad/s)','Gyroscope: y-axis (rad/s)',
                                          'Gyroscope: z-axis (rad/s)', 'Subject', 'Activity','Trial', 'Tag']
                        
                        for linha_original in linhas[2:]:
                            linha_selecionada = [linha_original[posicao] for posicao in range(len(linha_original)) if posicao not in indices_colunas_remover]

                            # Definir o valor da coluna "Tag" de formas a binarizar os dados, queda = 1 e não queda = 0
                            tag = int(linha_selecionada[-1])  # Valor da última coluna (assumindo que a coluna "Tag" é a última)
                            if tag >= 1 and tag <= 4:
                                linha_selecionada[-1] = '1'
                            else:
                                linha_selecionada[-1] = '0'
     
                            
                             # Converter os valores da quarta à oitava colunas de graus por segundo para radianos por segundo 
                            for i in range(4, 7):
                                valor_graus_s = float(linha_selecionada[i])
                                valor_radianos_s = valor_graus_s*(math.pi/180)
                                linha_selecionada[i] = valor_radianos_s
                             
                            linhas_selecionadas.append(linha_selecionada)
                            
                        # Verificar se o número de linhas é menor que 3
                    if len(linhas_selecionadas) < 3:
                        os.remove(caminho_arquivo)  # Remover o arquivo CSV
                        
                    else:
                        # Salvar as linhas selecionadas em um novo arquivo CSV
                        with open(arquivo_saida, 'w', newline='') as arquivo:
                            escritor_csv = csv.writer(arquivo)
                            # Escrever o novo cabeçalho
                            escritor_csv.writerow(novo_cabecalho)
                            escritor_csv.writerows(linhas_selecionadas)
        
                except FileNotFoundError:
                    print("Arquivo não encontrado.")

                except csv.Error as e:
                    print(f"Erro ao processar o arquivo CSV: {e}")

    
    
    
    print("Processamento concluído.") 





def main():      
    
    # Caminho do diretorio onde está a base de dados UP Fall tal como foi baixado
    pasta_entrada = r"C:\Users\Vanilson Fula\Downloads\Aulas\Tese\DataBaseDownload"
    
    # Caminho do diretorio onde queremos salvar os conjuntos de dados
    pasta_saida = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados\UP"
    # 1.
    process_UP(pasta_entrada, pasta_saida)
    
    
    
if __name__ == "__main__":
     main()
