import pandas as pd
from pandas import DataFrame
d = {
    'tweet':[':('],
    'emocao':['0']
}
df = DataFrame(d, columns = ['tweet', 'emocao'])
df.to_csv('negativo.csv', index= False)