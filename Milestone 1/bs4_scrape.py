# -*- coding: utf-8 -*-
"""
@author: Tan Chang Jung & Tan Sia Hong
"""

#%%
import requests 
from bs4 import BeautifulSoup
from datetime import date
import time
import pandas as pd

#%%
headers = {'User-Agent' : 'Chrome/74.0.3729.169'}

# select the top 20 from the ranking of cryptocurrencies
cryptocurrency = ['bitcoin','ethereum','xrp','bitcoin-cash','tether',
                  'bitcoin-sv','litecoin','eos','binance-coin','neo',
                  'chainlink','cardano','stellar','tron','unus-sed-leo',
                  'monero','huobi-token','ethereum-classic','crypto-com-coin',
                  'dash']

#%%
# capture today date
today = date.today().strftime("%Y%m%d")

# format the base url link
base_url = 'https://coinmarketcap.com/currencies/{}/historical-data/?start=20100101&end=' + today

# header
heading = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Capacity']

for cc in cryptocurrency:
    url = base_url.format(cc)
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    #find html code for table
    table = soup.find_all('div', class_='cmc-table__table-wrapper-outer')
    table = table[2]
    
    data = []
    for rows in table.find_all('tr'):
        row = {}
        for cols, head in zip(rows.find_all('td'), heading):
            row[head] = cols.text.replace('\n','').strip()
        data.append(row)
    
    time.sleep(5)
    
    df = pd.DataFrame(data)
    df = df.drop(df.index[0]) # remove empty row
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime('%Y-%m-%d')
    df['Open'] = df['Open'].str.replace(',','')
    df['Open'] = df['Open'].astype('float64').round(2)
    df['High'] = df['High'].str.replace(',','')
    df['High'] = df['High'].astype('float64').round(2)
    df['Low'] = df['Low'].str.replace(',','')
    df['Low'] = df['Low'].astype('float64').round(2)
    df['Close'] = df['Close'].str.replace(',','')
    df['Close'] = df['Close'].astype('float64').round(2)
    df['Volume'] = df['Volume'].str.replace(',','')
    df['Volume'] = df['Volume'].astype('float64').round(2)
    df['Market Capacity'] = df['Market Capacity'].str.replace(',','')
    df['Market Capacity'] = df['Market Capacity'].astype('float64').round(2)
    
    # save to csv
    df.to_csv(cc + '.csv', index = False)