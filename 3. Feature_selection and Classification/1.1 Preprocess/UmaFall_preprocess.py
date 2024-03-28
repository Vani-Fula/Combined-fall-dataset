# -*- coding: utf-8 -*-
"""
Created on Fri May 26 01:41:49 2023

@author: Vanilson Fula
"""
import csv
import glob
import os
import math
import numpy as np
import shutil
import pandas as pd
from datetime import datetime , timedelta
from UmaFall_Downsampling import Downsampled





def formatar_timestamp(timestamp):
    
    if timestamp == 'TimeStamp':
        return timestamp

    data_hora = datetime.strptime(timestamp, "%Y-%m-%d %H-%M-%S")
    data_hora_formatada = data_hora.strftime("%Y/%m/%dT%H:%M:%S")

    return data_hora_formatada


def adicionar_milissegundos(timestamp, milissegundos):
    
    # Converter o tempo em string para um objeto datetime
    tempo_objeto = datetime.strptime(timestamp[11:], '%H:%M:%S')
    
    tempo_novo = tempo_objeto + timedelta(milliseconds=int(milissegundos))
    
    return tempo_novo.strftime(timestamp[:11] + '%H:%M:%S.%f')

    


def process_UMA(pasta_entrada, pasta_saida):
    # Lista todos os arquivos CSV na pasta de entrada
    arquivos_csv = glob.glob(pasta_entrada + "/*.csv")
    
    
    # Itera sobre cada arquivo CSV
    for arquivo_entrada in arquivos_csv:
        # Extrai o nome do arquivo sem a extensão
        nome_arquivo = os.path.splitext(os.path.basename(arquivo_entrada))[0]
    
        # Extrai o sujeito do nome do arquivo
        #subject = nome_arquivo.split('_')[0] + " " + nome_arquivo.split('_')[2]
        subject = nome_arquivo.split('_')[2].lstrip('0')
        # Conta o número de ocorrências do caractere "_"
        num_underscores = nome_arquivo.count("_")
        
        # Condição baseada no número de "_"
        if num_underscores == 7:
            timeS = nome_arquivo.split('_')[6] + " " + nome_arquivo.split('_')[7]
            trial = nome_arquivo.split('_')[5] 
            timestamp_formatado = formatar_timestamp(timeS)
            
        else:
            timeS = nome_arquivo.split('_')[7] + " " + nome_arquivo.split('_')[8]
            trial = nome_arquivo.split('_')[6]        
            timestamp_formatado = formatar_timestamp(timeS)            
              
        # Extrai a atividade do nome do arquivo
        if nome_arquivo.split('_')[3] == 'Fall':
            tag = 0
            
        else:
            tag = 0
        
       
        activity = None
        file_name = os.path.basename(arquivo_entrada)
        file_info = file_name.split('_')
        activity_name = file_info[4]
        
        if activity_name == 'Walking':
            activity = 1
        elif activity_name == 'Jogging':
            activity = 2
        elif activity_name == 'Bending':
            activity = 3
        elif activity_name == 'Hopping':
            activity = 4
        elif activity_name == 'GoDownstairs':
            activity = 5
        elif activity_name == 'GoUpstairs':
            activity = 6
        elif activity_name == 'LyingDown' and file_info[5] == 'OnABed':
            activity = 7
        elif activity_name == 'Sitting' and file_info[5] == 'GettingUpOnAChair':
            activity = 8
        elif activity_name == 'Aplausing':
            activity = 9
        elif activity_name == 'HandsUp':
            activity = 10
        elif activity_name == 'MakingACall':
            activity = 11
        elif activity_name == 'OpeningDoor':
            activity = 12
        elif activity_name == 'backwardFall':
            activity = 13
        elif activity_name == 'forwardFall':
            activity = 14
        elif activity_name == 'lateralFall':
            activity = 15
            
                    
        # Define o caminho de saída para o arquivo selecionado
        arquivo_saida = os.path.join(pasta_saida, nome_arquivo + ".csv")
        
        
        # Inicializa a lista para armazenar as linhas selecionadas
        linhas_selecionadas = []
        linhas_selecionadasGyro = []
        linhas_selecionadasAcc = []
    
        # Ler o arquivo CSV em uma lista de linhas
        with open(arquivo_entrada, 'r') as arquivo:
            leitor_csv = csv.reader(arquivo)
            linhas = list(leitor_csv)
    
            # Criar um novo cabeçalho com as colunas existentes mais as colunas "Subject" e "Trial"
            novo_cabecalho = ['TimeStamp', 'Accelerometer: x-axis (g)', 'Accelerometer: y-axis (g)', 'Accelerometer: z-axis (g)', 
                              'Gyroscope: x-axis (rad/s)','Gyroscope: y-axis (rad/s)','Gyroscope: z-axis (rad/s)','Subject', 'Activity','Trial', 'Tag']
                            
                            
            for i in range(41, len(linhas)):
                linha = linhas[i][0].split(';')
                if len(linha) >= 7:  # Verificar se a linha tem elementos suficientes
                    sensor_type = linha[5]
                    sensor_id = linha[6]
                    if sensor_type.isdigit() and sensor_id.isdigit():
                        sensor_type = int(sensor_type)
                        sensor_id = int(sensor_id)
                        if (sensor_type == 0 and sensor_id == 3):
                            linha = linha[2:5] # Atualizar os valores de "Subject", "Trial" e "Tag"
                            linhas_selecionadasAcc.append(linha)
                        elif (sensor_type == 1 and sensor_id == 3):
                            #timeStamp = adicionar_milissegundos(timestamp_formatado, linha[0])
                            linha[0] = int(linha[0]) /1000 # levar o tempo de milissegundos a segundos
                            linha = linha[:1] + linha[2:5] + [subject, activity, trial, tag]  # Atualizar os valores de "Subject", "Trial" e "Tag"
                            linhas_selecionadasGyro.append(linha)
                
        
            
        
        for i in range(len(linhas_selecionadasAcc)):
            linha_gyro = linhas_selecionadasGyro[i]
            linha_acc = linhas_selecionadasAcc[i]
            nova_linha = linha_gyro[:1] + linha_acc[0:] + linha_gyro[1:]
            linhas_selecionadas.append(nova_linha)
        
        
        
        for linha_selecionada in linhas_selecionadas[0:]:
            for i in range(4, 7):
                valor_graus_s = linha_selecionada[i]   
                try:
                    valor_graus_s = float(valor_graus_s)
                    valor_radianos_s = valor_graus_s*(math.pi/180)
                except ValueError:
                    valor_radianos_s = valor_graus_s  # Atribuir NaN ao valor inválido        
                
                linha_selecionada[i] = valor_radianos_s
            
          
        
        # Salvar as linhas selecionadas em um novo arquivo CSV
        with open(arquivo_saida, 'w', newline='') as arquivo:
            escritor_csv = csv.writer(arquivo)
            # Escrever o novo cabeçalho
            escritor_csv.writerow(novo_cabecalho)
            escritor_csv.writerows(linhas_selecionadas)
            
    
    Downsampled(pasta_saida,20,18)
    print("Downsample completo")
    process_to_up(pasta_saida)
    print("Processamento concluído.") 
    
def process_to_up(pasta_saida):
    # Diretório raiz onde os arquivos CSV estão localizados
    diretorio_raiz = pasta_saida
    
    # Percorra todos os arquivos CSV no diretório raiz
    for arquivo in os.listdir(diretorio_raiz):
        if arquivo.endswith('.csv'):
            # Extraia as informações do nome do arquivo
            nome_arquivo = os.path.splitext(arquivo)[0]
            partes_nome = nome_arquivo.split('_')
            sujeito = partes_nome[1] + partes_nome[2].lstrip('0')  # Remover zero à esquerda
            
            activity = None
            activity_name = partes_nome[4]
            
            if activity_name == 'Walking':
                activity = 1
            elif activity_name == 'Jogging':
                activity = 2
            elif activity_name == 'Bending':
                activity = 3
            elif activity_name == 'Hopping':
                activity = 4
            elif activity_name == 'GoDownstairs':
                activity = 5
            elif activity_name == 'GoUpstairs':
                activity = 6
            elif activity_name == 'LyingDown' and partes_nome[5] == 'OnABed':
                activity = 7
            elif activity_name == 'Sitting' and partes_nome[5] == 'GettingUpOnAChair':
                activity = 8
            elif activity_name == 'Aplausing':
                activity = 9
            elif activity_name == 'HandsUp':
                activity = 10
            elif activity_name == 'MakingACall':
                activity = 11
            elif activity_name == 'OpeningDoor':
                activity = 12
            elif activity_name == 'backwardFall':
                activity = 13
            elif activity_name == 'forwardFall':
                activity = 14
            elif activity_name == 'lateralFall':
                activity = 15
            
            # Conta o número de ocorrências do caractere "_"
            num_underscores = nome_arquivo.count("_")
            
            # Condição baseada no número de "_"
            if num_underscores == 7:
                tentativa = partes_nome[5]
                
            else:
                tentativa = partes_nome[6]
            
            
            
    
            # Crie o diretório para o sujeito, atividade e tentativa
            diretorio_destino = os.path.join(diretorio_raiz, f'{sujeito}', f'Activity{activity}', f'Trial{tentativa}')
            os.makedirs(diretorio_destino, exist_ok=True)
            
            novo_nome = f'UMAFALL_{sujeito}Activity{activity}Trial{tentativa}.csv'
    
            # Mova o arquivo para o diretório de destino com o novo nome
            shutil.move(os.path.join(diretorio_raiz, arquivo), os.path.join(diretorio_destino, novo_nome))





def main():      
    
    
    # Caminho do diretorio onde está a base de dados UMA Fall tal como foi baixado
    pasta_entrada = r"C:\Users\Vanilson Fula\Downloads\Aulas\Tese\Bases de dados\UMAFall_Dataset\Subjects"
    
    # Caminho do diretorio onde queremos salvar os conjuntos de dados
    pasta_saida = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados\UMA"
    
    # 1.
    process_UMA(pasta_entrada, pasta_saida)

    # 2.
    #process_to_up(pasta_saida)
    
      
if __name__ == "__main__":
     main()
