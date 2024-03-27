# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 22:13:42 2023

@author: Vanilson Fula
"""

import os
import random
import shutil

# Function to create a new directory (if it doesn't exist)
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to copy a file to a new directory
def copy_file(source, destination):
    shutil.copy2(source, destination)

# Root directories of the datasets
root_directories = {
    "WEDA": r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados\WEDA\\",
    "UMA": r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados\UMA\\",
    "UP": r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\Dados\UP\\"
}

# Percentage of data for each set (training, testing)
percent_training = 0.7
percent_testing = 0.3

# Window sizes
window_sizes = "3&1.5"

# Destination directories for the datasets
destination_directory_base = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\dataset_original"
#destination_directory_base = r"C:\Users\Vanilson Fula\Desktop\Tese_Soft\Scripts_Datasets\dataset_normalized"
destination_directories = {
    "training": os.path.join(destination_directory_base, "Training"),
    "testing": os.path.join(destination_directory_base, "Testing")
}

# Create folders for the datasets, divided by window size
for set_type, destination_directory in destination_directories.items():
    create_directory(destination_directory)
    window_directory = os.path.join(destination_directory, window_sizes)
    create_directory(window_directory)

# Process each dataset
for dataset, root_directory in root_directories.items():
    # Find files of interest in the subdirectories
    interest_files = []
    for root, _, files in os.walk(root_directory):
        for file in files:
            if f"Features{window_sizes}.csv" in file:
                interest_files.append(os.path.join(root, file))

    # Group files by subject and activity
    grouped_files = {}
    for file in interest_files:
        parts = os.path.basename(file).split('_')
        subject, activity = parts[0] + parts[1], parts[2]
        key = f"{subject}_{activity}"
        if key not in grouped_files:
            grouped_files[key] = []
        grouped_files[key].append(file)

    # Shuffle the order of groups (to ensure randomness)
    group_keys = list(grouped_files.keys())
    random.shuffle(group_keys)

    # Divide the groups into training and testing sets
    total_groups = len(group_keys)
    total_training = int(total_groups * percent_training)
    total_testing = total_groups - total_training
    
    groups_training = group_keys[:total_training]
    groups_testing = group_keys[total_training:]

    # Copy the files to the training and testing sets
    for set_type, groups_set in [("training", groups_training), ("testing", groups_testing)]:
        destination_directory_set = os.path.join(destination_directories[set_type], window_sizes, dataset)
        create_directory(destination_directory_set)
        for group in groups_set:
            files_group = grouped_files[group]
            for file in files_group:
                destination_path = os.path.join(destination_directory_set, os.path.basename(file))
                copy_file(file, destination_path)

print('Data division completed')
