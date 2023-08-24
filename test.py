import pandas as pd

data_path = 'D:/Orange/Episafe/generated-data/1869_001.csv'
data = pd.read_csv(data_path)

print(data['path'][0].split('/'))