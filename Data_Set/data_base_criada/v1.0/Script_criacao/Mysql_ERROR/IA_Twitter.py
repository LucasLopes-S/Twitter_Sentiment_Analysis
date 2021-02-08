import tweepy as tp
import pandas as pd
import re
import mysql.connector

#Conexão com o banco de dados local
con = mysql.connector.connect(host='localhost', database='tweets', user='root', password='')
cursor = con.cursor()

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

query = ":)" + "-filter:retweets"

limpar_users='(@[a-zA-z0-9]+)*'
limpar_links=r'https?:\/\/.*[\r\n]*'
limpar_espacos='\s+'
limpar_aspas_simples="'"
limpar_aspas_duplas='"'


tweets = tp.Cursor(api.search,  tweet_mode='extended',q=query, lang="pt", ).items(2000)

for tweet in tweets:
    text = tweet.full_text
    text = re.sub(limpar_users, '', text)
    text = re.sub(limpar_links, '', text, flags=re.MULTILINE)
    text = re.sub(limpar_espacos, ' ', text)
    text = re.sub(limpar_aspas_simples+'|'+limpar_aspas_duplas, ' ', text)
    text = re.sub('^'+limpar_espacos, '', text)
    cursor.execute('SELECT count(tweet) FROM tweets.positivo where tweet="{}";'.format(text))
    for repetido in cursor.fetchone():
        if repetido>0:
            print(text)
            continue
        else:
            print(text)
            cursor.execute("insert into positivo(tweet, sentimento) values('{}',1);".format(text))
            con.commit()
cursor.close()
con.close()
    