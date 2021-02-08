import tweepy as tp
import pandas as pd
from pandas import DataFrame
import re

#Acesso as chaves disponibilizadas pelo Twitter e salvos em um arquivo txt
with open('twitter-tokens.txt', 'r') as tfile:
    consumer_key = tfile.readline().strip('\n')
    consumer_secret = tfile.readline().strip('\n')
    token_key = tfile.readline().strip('\n')
    token_secret = tfile.readline().strip('\n')
    
#Autênticação com a api do twitter 
auth = tp.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(token_key, token_secret)
api = tp.API(auth, wait_on_rate_limit=True)

query = "mal :(" + "-filter:retweets"

#Limpeza dos tweets
limpar_users='(@[a-zA-z0-9]+)*'
limpar_links=r'https?:\/\/.*[\r\n]*'
limpar_espacos='\s+'
limpar_aspas_simples="'"
limpar_aspas_duplas='"'
happy_face1=':\)+'
happy_face2=':D+'
hastag_clear='(#[\w]+)'
limpa_tuto='[^a-zA-Z_áéíóúàèìòùâêîôûãõç\s]'

#query de pesquisa com a api
tweets = tp.Cursor(api.search,  tweet_mode='extended',q=query, lang="pt", ).items(4500)

#Criando somente as colunas do data frame
df = pd.read_csv('negativo.csv')

#Inserindo os dados no dataframe
for tweet in tweets:
    text = tweet.full_text
    text = re.sub(limpar_users, '', text)
    text = re.sub(limpar_links, '', text, flags=re.MULTILINE)
    text = re.sub(happy_face2,' ', text)
    text = re.sub(hastag_clear,' ', text)
    text = text.lower()
    text = re.sub(limpa_tuto,' ', text)
    text = re.sub(limpar_espacos, ' ', text)
    text = re.sub('^'+limpar_espacos, '', text)
    if 'mal' in text:
        d = {'tweet': [text],
            'emocao': ['0']}
        df2 =  DataFrame(d, columns = ['tweet', 'emocao'])
        df = df.append(df2, ignore_index=True)
        df = df.drop_duplicates(['tweet'])
df.to_csv('negativo.csv', index= False)
