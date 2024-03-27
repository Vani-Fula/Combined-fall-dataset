# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 20:08:06 2024

@author: Vanilson Fula
"""

import os
from UmaFall_preprocess import process_UMA
from UPFall_preprocess import process_UP
from WedaFall_preprocess import process_WEDA

# Function to create destination folders if they don't exist
def create_folder(destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

# Path of input and output directories for UMA Fall Dataset
input_folder_UMA = r"C:\Users\Vanilson Fula\Downloads\Aulas\Tese\Bases de dados\UMAFall_Dataset\Subjects"
output_folder_UMA = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Combined_Datasets\Scripts_Datasets\Data\UMA"

# Check and create the output folder if necessary
create_folder(output_folder_UMA)

# Call the process function for UMA Fall Dataset
process_UMA(input_folder_UMA, output_folder_UMA)
print("UMA Fall Dataset Done")
print("__________________________________________________")

# Path of input and output directories for UP Fall Dataset
input_folder_UP = r"C:\Users\Vanilson Fula\Downloads\Aulas\Tese\DataBaseDownload"
output_folder_UP = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Combined_Datasets\Scripts_Datasets\Data\UP"

# Check and create the output folder if necessary
create_folder(output_folder_UP)

# Call the process function for UP Fall Dataset
process_UP(input_folder_UP, output_folder_UP)
print("UP Fall Dataset Done")
print("__________________________________________________")

# Path of input and output directories for WEDA Fall Dataset
input_folder_WEDA = r"C:\Users\Vanilson Fula\Downloads\Aulas\Tese\Bases de dados\Weda\WEDA\dataset\50Hz"
output_folder_WEDA = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Combined_Datasets\Scripts_Datasets\Data\WEDA"

# Check and create the output folder if necessary
create_folder(output_folder_WEDA)

# Call the process function for WEDA Fall Dataset
process_WEDA(input_folder_WEDA, output_folder_WEDA)
print("WEDA Fall Dataset Done")
print("__________________________________________________")
