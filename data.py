import os
import pandas as pd
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed


# testing pandas parquet reading
#df = pd.read_parquet('/home/Djoo/Orange/Episafe/UTC-2019_11_11-17_00_00.parquet')



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



    
if __name__ == "__main__":
    # Directory containing the Parquet files
    parquet_directory_epileptic = "/home/Djoo/Orange/Episafe/FetchedFiles"
    parquet_directory ="/home/Djoo/Orange/Episafe/parquetFiles/1869/000"

    # Get a list of all Parquet files in the directory

    parquet_files = [os.path.join(parquet_directory, file) for file in os.listdir(parquet_directory) if file.endswith(".parquet")]

    # Read the Parquet files in parallel using multiple threads
    data_frames = read_parquet_files_in_parallel(parquet_files)
        
    print(data_frames)

    all_eda = []
    for i in range(6): #len(data_frames)
        print('*******************************')
        all_eda.append(data_frames[i]['eda'])
    concatenated_series = pd.concat(all_eda, axis=0).reset_index(drop=True)
    print(concatenated_series)


    #for i in range(len(data_frames)):
        #plot_EDA(data_frames[i]['eda'])
        #plot_EDA(data_frames[i]['hr'])
        #plot_EDA(data_frames[i]['temp'])
    def plot_EDA(EDA):
        x_range = 1
        x_values = [i * x_range for i in range(len(EDA))]

        # Create the scatter plot
        plt.plot(x_values, EDA, label='Line Plot', color='blue')

        # Add labels and title
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('EDA Line Plot with Fixed X Range')

        # Show legend
        plt.legend()

        # Show the plot
        plt.show()

    plot_EDA(concatenated_series)
    
    #plot_data(parquet_directory_safe)
    #plot_data(parquet_directory_safe)
