# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 20:09:06 2023

@author: Vanilson Fula
"""

import os
import shutil
import pandas as pd

def min_max_normalize(axis_data, min_val, max_val):
    normalized_axis = -1 + 2 * ((axis_data - min_val) / (max_val - min_val))
    return normalized_axis

def calculate_min_max(df):
    min_vals = df.min()
    max_vals = df.max()
    return min_vals, max_vals

root_directory = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Combined_Datasets\Scripts_Datasets\Data"
output_root_directory = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Combined_Datasets\Scripts_Datasets\Normalized_data"

# Check if the output directory already exists
if not os.path.exists(output_root_directory):
    # Copy the folder structure and files from the input directory to the output directory
    shutil.copytree(root_directory, output_root_directory)
    print("Output directory created and folder structure and files copied.")
else:
    print("Output directory already exists. Normalization will be performed on existing files.")

for dataset_name in ["UMA", "UP", "WEDA"]:   
    dataset_directory = os.path.join(output_root_directory, dataset_name)
    
    # Check if the dataset directory exists
    if not os.path.exists(dataset_directory):
        print(f"Dataset '{dataset_name}' not found. Skipping normalization.")
        continue
    
    all_min_values_accel = []
    all_max_values_accel = []
    all_min_values_gyro = []
    all_max_values_gyro = []
    
    # Process all CSV files in the output directory to calculate min and max values
    for root, dirs, files in os.walk(dataset_directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                
                # Convert non-numeric values to NaN in the columns of interest
                df.iloc[:, 1:7] = df.iloc[:, 1:7].apply(pd.to_numeric, errors='coerce')
                
                # Drop rows with NaN values in the columns of interest
                df_clean = df.dropna(subset=df.columns[1:7]).copy()  # Create a DataFrame copy
                
                # Calculate min and max values before normalization
                min_value_accel, max_value_accel = calculate_min_max(df_clean.iloc[:, 1:4])
                min_value_gyro, max_value_gyro = calculate_min_max(df_clean.iloc[:, 4:7])
                
                all_min_values_accel.append(min_value_accel.min())
                all_max_values_accel.append(max_value_accel.max())
                all_min_values_gyro.append(min_value_gyro.min())
                all_max_values_gyro.append(max_value_gyro.max())
                
                # Normalize accelerometer columns (columns 2 to 4)
                df_clean.loc[:, df_clean.columns[1:4]] = min_max_normalize(df_clean.loc[:, df_clean.columns[1:4]], min_value_accel.min(), max_value_accel.max())
                
                # Normalize gyroscope columns (columns 5 to 7)
                df_clean.loc[:, df_clean.columns[4:7]] = min_max_normalize(df_clean.loc[:, df_clean.columns[4:7]], min_value_gyro.min(), max_value_gyro.max())
                
                # Save normalized data back to CSV file in the output directory
                df_clean.to_csv(file_path, index=False)
    
    print(f"Dataset: {dataset_name}")
    print(f"Maximum accelerometer value: {max(all_max_values_accel)}")
    print(f"Minimum accelerometer value: {min(all_min_values_accel)}")
    print(f"Maximum gyroscope value: {max(all_max_values_gyro)}")
    print(f"Minimum gyroscope value: {min(all_min_values_gyro)}")
    print("\n")
    
print("All data normalized and saved in the output directory.")
