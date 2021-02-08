import pandas as pd
from pandas import DataFrame

df = DataFrame(pd.read_csv('positivo.csv'), columns = ['tweet', 'emocao'])
df1 = DataFrame(pd.read_csv('negativo.csv'), columns = ['tweet', 'emocao'])

df = df.append(df1, ignore_index=True)
df = df.drop_duplicates(['tweet'])
df.to_csv('total_geral.csv', index= False)