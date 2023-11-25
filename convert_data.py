import pandas as pd

data = pd.read_parquet('D:/Orange/Episafe_local/EpilepticData/1904_1/UTC-2020_10_21-03_40_00.parquet')

data.to_csv('2_test.csv',index=False)