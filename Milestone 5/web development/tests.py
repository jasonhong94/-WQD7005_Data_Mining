  
import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import date

def web_scraper(target):
    headers = {'User-Agent' : 'Chrome/74.0.3729.169'}
    cryptocurrency = ['bitcoin','ethereum','litecoin']
    if target in cryptocurrency:
        

        today = date.today().strftime("%Y%m%d")
    
        base_url = 'https://coinmarketcap.com/currencies/'+ target + '/historical-data/?start=20100101&end=' + today
    
        heading = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Market Capacity']
    
    #for cc in cryptocurrency:
        url = base_url.format(target)
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.content, 'html.parser')
    
        #find html code for table
        table = soup.findAll('div', class_='cmc-table__table-wrapper-outer')
        table = table[2]
    
        data = []
        for rows in table.findAll('tr'):
            row = {}
            for cols, head in zip(rows.findAll('td'), heading):
                row[head] = cols.text.replace('\n','').strip()
            data.append(row)
    
        df = pd.DataFrame(data)
        df = df.drop(df.index[0]) # remove empty row
        df['Date'] = pd.to_datetime(df["Date"]).dt.strftime('%Y-%m-%d')
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

        
    return df

#value = 'bitcoin'
#a = web_scraper(value).reset_index(drop=True).set_index('Date').sort_index()
#print(a)
