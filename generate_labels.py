import os 
import pandas as pd

# Directory containing your Parquet files
data_directory = "D:/Orange/Episafe_local/data/parquet/train/1869"
first_path = "D:/Orange/Episafe_local/data/parquet/train/1869/066"

# Assuming you have labels for each Parquet file
labels = pd.read_csv('train_labels.csv')
#generating each session labels 
for directory in os.listdir(data_directory):
    path = os.path.join(data_directory,directory).replace(os.path.sep,'/')
    df_name = []
    df_label = []
    for i in range(labels.shape[0]): 
        if labels['filepath'][i].split('/')[1] == directory and labels['filepath'][i].split('/')[0] == '1869' :
            df_name.append(labels['filepath'][i])
            df_label.append(labels['label'][i])
    data = {'filename': df_name, 'label': df_label}
    df = pd.DataFrame(data)
    df.to_csv('1869_'+directory+'_labels.csv')

