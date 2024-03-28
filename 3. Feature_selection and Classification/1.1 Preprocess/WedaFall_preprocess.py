# -*- coding: utf-8 -*-
"""
Created on Sun Jun 11 22:14:52 2023

@author: Vanilson Fula
"""

import os
import shutil
import csv
import glob
import math
import numpy as np
import pandas as pd
from datetime import datetime , timedelta
from WedaFall_Downsampling import Downsampled


def process_WEDA(pasta_atual, nova_pasta):
    
    # Dicionário para armazenar os sujeitos, tentativas e arquivos "accel" e "gyro"
    dados_sujeitos = {}

    # Percorrer todas as subpastas na pasta atual
    for atividade in os.listdir(pasta_atual):
        pasta_atividade = os.path.join(pasta_atual, atividade)
        
        activity = None
        activity_name = atividade
        
        if activity_name == 'D01':
            activity = 1
        elif activity_name == 'D02':
            activity = 2
        elif activity_name == 'D03':
            activity = 3
        elif activity_name == 'D04':
            activity = 4
        elif activity_name == 'D05':
            activity = 5
        elif activity_name == 'D06':
            activity = 6
        elif activity_name == 'D07':
            activity = 7
        elif activity_name == 'D08':
            activity = 8
        elif activity_name == 'D09':
            activity = 9
        elif activity_name == 'D10':
            activity = 10
        elif activity_name == 'D11':
            activity = 11
        elif activity_name == 'D12':
            activity = 12
        elif activity_name == 'F01':
            activity = 13
        elif activity_name == 'F02':
            activity = 14
        elif activity_name == 'F03':
            activity = 15
        elif activity_name == 'F04':
            activity = 16
        elif activity_name == 'F05':
            activity = 17
        elif activity_name == 'F06':
            activity = 18
        elif activity_name == 'F07':
            activity = 19
        elif activity_name == 'F08':
            activity = 20
            


        # Verificar se é uma pasta
        if os.path.isdir(pasta_atividade):
            # Criar a nova pasta para armazenar os arquivos agrupados
            os.makedirs(nova_pasta, exist_ok=True)
        
            # Percorrer todos os arquivos CSV na subpasta atual
            for nome_arquivo in os.listdir(pasta_atividade):
                if nome_arquivo.endswith('.csv') and 'accel' in nome_arquivo:
                    # Extrair informações do nome do arquivo
                    sujeito = nome_arquivo.split('_')[0][1:].lstrip('0')
                    tentativa = nome_arquivo.split('_')[1][2]
            
                    # Verificar se existe um arquivo de giroscópio correspondente
                    nome_arquivo_gyro = nome_arquivo.replace('accel', 'gyro')
                    if nome_arquivo_gyro in os.listdir(pasta_atividade):
                        sujeito = nome_arquivo.split('_')[0][1:].lstrip('0')
                        tentativa = nome_arquivo.split('_')[1][2]
                        
                    
                        # Definir o nome do arquivo combinado
                        novo_nome = f'WEDAFALL_Subject{sujeito}Activity{activity}Trial{tentativa}.csv'
                        # Criar estrutura de pastas na nova pasta
                        nova_pasta_sujeito = os.path.join(nova_pasta, f'Subject{sujeito}')
                        nova_pasta_atividade = os.path.join(nova_pasta_sujeito, f'Activity{activity}')
                        nova_pasta_tentativa = os.path.join(nova_pasta_atividade, f'Trial{tentativa}')
                        os.makedirs(nova_pasta_tentativa, exist_ok=True)

                        novo_caminho = os.path.join(nova_pasta_tentativa, novo_nome)

                        with open(os.path.join(pasta_atividade, nome_arquivo), 'r') as arquivo_accel, \
                                open(os.path.join(pasta_atividade, nome_arquivo_gyro), 'r') as arquivo_gyro, \
                                open(novo_caminho, 'w', newline='') as arquivo_combinado:
            
                            leitor_accel = csv.reader(arquivo_accel)
                            leitor_gyro = csv.reader(arquivo_gyro)
                            escritor_combinado = csv.writer(arquivo_combinado)
            
                            # Obter os cabeçalhos dos arquivos de aceleração e giroscópio
                            cabecalho_accel = next(leitor_accel)
                            cabecalho_gyro = next(leitor_gyro)
            
                            # Identificar as colunas de interesse (exceto a primeira coluna)
                            colunas_accel = cabecalho_accel[1:]
                            colunas_gyro = cabecalho_gyro[1:]
            
                            # Escrever o cabeçalho no arquivo combinado
                            cabecalho_combinado = ['Value'] + colunas_accel + colunas_gyro
                            escritor_combinado.writerow(cabecalho_combinado)
            
                            # Ler os dados dos arquivos de aceleração e giroscópio
                            dados_accel = list(leitor_accel)
                            dados_gyro = list(leitor_gyro)
            
                            # Verificar o tamanho dos dados
                            tamanho_dados = min(len(dados_accel), len(dados_gyro))
            
                            # Comparar os valores e escrever as linhas combinadas no arquivo combinado
                            for i in range(tamanho_dados):
                                linha_accel = dados_accel[i]
                                linha_gyro = dados_gyro[i]
            
                                # Obter os valores das primeiras colunas
                                valor_accel = float(linha_accel[0])
                                valor_gyro = float(linha_gyro[0])
            
                                # Determinar a ordem das colunas no arquivo combinado
                                if valor_accel >= valor_gyro:
                                    linha_combinada = [valor_accel] + linha_accel[1:] + linha_gyro[1:]
                                else:
                                    linha_combinada = [valor_gyro] + linha_accel[1:] + linha_gyro[1:]
            
                                escritor_combinado.writerow(linha_combinada)
         
                   
    Downsampled(nova_pasta,50,18)
    print("Downsample completo")
    
    process_to_up(nova_pasta)
    print("Processamento concluído")


def process_to_up(pasta_saida):
    
    # Diretório raiz onde os arquivos CSV estão localizados
    diretorio_raiz = pasta_saida
    
    # Percorrer todas as subpastas e arquivos CSV
    for pasta_atual, subpastas, arquivos in os.walk(diretorio_raiz):
        for arquivo_entrada in arquivos:
            if arquivo_entrada.endswith('.csv'):
                caminho_arquivo = os.path.join(pasta_atual, arquivo_entrada)
                nome_arquivo = os.path.splitext(arquivo_entrada)[0]
                
                #Remover os dados a partir do nome dos arquivos
                partes = nome_arquivo.split("WEDAFALL_Subject")[1].split("Activity")
                subject = int(partes[0])
                activity, trial = map(int, partes[1].split("Trial"))    
    
                # Extrair a tag pela actividade
                if activity >=12 and activity <=19:
                # será feita posteriormente e inicializamos com "0" porque uma atividade normal antecede uma queda
                    tag = "0"                       
                else:
                    tag = "0"
                    
                # Define o caminho de saída para o arquivo selecionado
                arquivo_saida = os.path.join(pasta_atual, nome_arquivo + ".csv")
                
                # Inicializa a lista para armazenar as linhas selecionadas
                linhas_selecionadas = []
                
                # Ler o arquivo CSV em uma lista de linhas
            with open(caminho_arquivo, 'r') as arquivo_csv:
                leitor_csv = csv.reader(arquivo_csv)
                linhas = list(leitor_csv)
        
                # Criar um novo cabeçalho com as colunas existentes mais as colunas "Subject" e "Trial"
                novo_cabecalho = ['TimeStamp', 'Accelerometer: x-axis (g)', 'Accelerometer: y-axis (g)', 
                                  'Accelerometer: z-axis (g)', 'Gyroscope: x-axis (rad/s)','Gyroscope: y-axis (rad/s)',
                                  'Gyroscope: z-axis (rad/s)', 'Subject', 'Activity','Trial', 'Tag']
                
                
                for linha_original in linhas[1:]:
                    linha = linha_original.copy()  # Copia a linha original para evitar modificar a lista original
                    # Converter os valores da segunda à quarta colunas de m/s² para g
                    for i in range(1, 4):
                        valor_m_s2 = float(linha[i])
                        valor_g = valor_m_s2 / 9.81
                        linha[i] = valor_g
                        
                    
                     
                    # Adicionar as colunas "Subject", "Activity", "Trial" e "Tag" na linha
                    linha = linha[:7] + [subject, activity, trial, tag] 
                    
                    # Adicionar a linha modificada na lista de linhas selecionadas
                    linhas_selecionadas.append(linha)
                    
            # Salvar as linhas selecionadas em um novo arquivo CSV
            with open(arquivo_saida, 'w', newline='') as arquivo:
                escritor_csv = csv.writer(arquivo)
                # Escrever o novo cabeçalho
                escritor_csv.writerow(novo_cabecalho)
                escritor_csv.writerows(linhas_selecionadas)
             
   




def main():      
    
    # Caminho do diretorio onde está a base de dados WEDA Fall tal como foi baixado
    pasta_entrada = r"C:\Users\Vanilson Fula\Downloads\Aulas\Tese\Bases de dados\Weda\WEDA\dataset\50Hz"
   
    # Caminho do diretorio onde queremos salvar os conjuntos de dados
    pasta_saida = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados\WEDA"
    # 1.
    process_WEDA(pasta_entrada, pasta_saida)
    

if __name__ == "__main__":
     main()
