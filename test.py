import pandas as pd
import pickle
pkl_file = open(r'D:\QQ\294103703\FileRecv\d30c14b3-4039-3ad8-9cc3-025485863b7c-61939.pickle', 'rb')
data1=pd.read_pickle(pkl_file)  
print(data1.groupby('type').count())
input()