import pandas as pd
import os 
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools



def read_parquet_file(parquet_file):
    # Read the Parquet file and return the DataFrame
    return pd.read_parquet(parquet_file)


def read_parquet_files_in_parallel(parquet_files, num_threads=4):
    # Create a ThreadPoolExecutor with the specified number of threads
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Submit tasks for reading Parquet files
        futures = {executor.submit(read_parquet_file, file): file for file in parquet_files}

        # Iterate through the completed futures and store the DataFrames
        dfs = []
        for future in as_completed(futures):
            file = futures[future]
            try:
                df = future.result()
                dfs.append(df)
            except Exception as e:
                print(f"Error reading {file}: {e}")

    return dfs

parquet_directory = "/home/Djoo/Orange/Episafe/parquetFiles/1869/000"
def get_directories(path):
    directories = []
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            directories.append(item)
    return directories


directories_list = get_directories(parquet_directory)

print("List of directories:")
print(directories_list)


parquet_files = [os.path.join(parquet_directory, file) for file in os.listdir(parquet_directory) if file.endswith(".parquet")]
#print(parquet_files)
data_frames = read_parquet_files_in_parallel(parquet_files)


"""print(data_frames[0])
print(len(data_frames))"""

eda_feature = []
bvp_feature = []
hr_feature = []
temp_feature = []
timestamp_feature = []
for i in range(len(data_frames)):
    #for j in  range(len(data_frames[i]['eda'])):
    eda_feature.append(data_frames[i]['eda'])
    bvp_feature.append(data_frames[i]['bvp'])
    hr_feature.append(data_frames[i]['hr'])
    temp_feature.append(data_frames[i]['temp'])
    timestamp_feature.append(data_frames[i]['utc_timestamp'])

merged_eda_feature = list(itertools.chain(*eda_feature))
merged_bvp_feature = list(itertools.chain(*bvp_feature))
merged_hr_feature = list(itertools.chain(*hr_feature))
merged_temp_feature = list(itertools.chain(*temp_feature))
merged_tempstamp_feature = list(itertools.chain(*timestamp_feature))

#print(merged_eda_feature)

data = {
    'time_stamp': merged_tempstamp_feature,
    'eda': merged_eda_feature,
    'bvp': merged_bvp_feature,
    'hr': merged_hr_feature,
    'temp': merged_temp_feature
}

print(len(timestamp_feature))
print(len(merged_eda_feature))
print(len(merged_bvp_feature))
print(len(merged_hr_feature))
print(len(merged_temp_feature))

# Creating the DataFrame from the dictionary
df = pd.DataFrame(data)

# Displaying the DataFrame
print(df)

df.to_csv("first_data.csv",index=False)