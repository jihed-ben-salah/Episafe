import os
import pandas as pd
import shutil


csv_file = "epileptic_records2.csv"
df = pd.read_csv(csv_file)
file_names_list = df["filepath"].tolist()


directory_path = "/home/Djoo/Orange/Episafe/parquetFiles" 
destination_directory = "/home/Djoo/Orange/Episafe/FetchedFiles" 

matching_files = []

for file_name in file_names_list:
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file_name in file:
                matching_files.append(os.path.join(root, file))


# Step 4: Move the matching files to the new location
for file_path in matching_files:
    shutil.move(file_path, destination_directory)

print("Files moved successfully!")
