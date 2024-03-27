# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 20:08:06 2024

@author: Vanilson Fula
"""

from featuresExtraction_UP import extract_features_UP
from featuresExtraction_WEDA import extract_features_WEDA
from featuresExtraction_UMA import extract_features_UMA

def main():
    
    # Definir tamanho da janela
    t_window = ('3&1.5',)
    
    # # Chamar a função process
    # # Caminho do diretorio onde está a base de dados UMA Fall
    # pasta_UP = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados\UP\\"
    # extract_features_UP(pasta_UP, pasta_UP, t_window)
    
    # print('Feature extraction completed')
    # print("UP Fall Dataset Done")
    # print("__________________________________________________")
    
    
    
    
    
    
    
    # # Chamar a função process
    # # Caminho do diretorio onde está a base de dados WEDA Fall
    # pasta_WEDA = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados\WEDA\\"
    # extract_features_WEDA(pasta_WEDA, pasta_WEDA, t_window)
    
    # print('Feature extraction completed')
    # print("WEDA Fall Dataset Done")
    # print("__________________________________________________")
    
    
    
    
    
    
    
    
    # # Chamar a função process
    # # Caminho do diretorio onde está a base de dados UMA Fall
    # pasta_UMA = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados\UMA\\"
    # extract_features_UMA(pasta_UMA, pasta_UMA, t_window)
    
    # print('Feature extraction completed')
    # print("UMA Fall Dataset Done")
    # print("__________________________________________________")
    
    
    #__________________________________________________________________________
    ###____________ Dados Normalizados_________________________________________
    
    
    # Chamar a função process
    # Caminho do diretorio onde está a base de dados UMA Fall
    pasta_UP = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados_Normalizados\UP\\"
    extract_features_UP(pasta_UP, pasta_UP, t_window)
    
    print('Feature extraction completed')
    print("UP Fall Dataset Done")
    print("__________________________________________________")
    
    
    
    
    
    
    
    # Chamar a função process
    # Caminho do diretorio onde está a base de dados WEDA Fall
    pasta_WEDA = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados_Normalizados\WEDA\\"
    extract_features_WEDA(pasta_WEDA, pasta_WEDA, t_window)
    
    print('Feature extraction completed')
    print("WEDA Fall Dataset Done")
    print("__________________________________________________")
    
    
    
    
    
    
    
    
    # Chamar a função process
    # Caminho do diretorio onde está a base de dados UMA Fall
    pasta_UMA = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados_Normalizados\UMA\\"
    extract_features_UMA(pasta_UMA, pasta_UMA, t_window)
    
    print('Feature extraction completed')
    print("UMA Fall Dataset Done")
    print("__________________________________________________")
    
    
    
    

if __name__ == "__main__":
    main()




