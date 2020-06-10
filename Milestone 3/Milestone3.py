# -*- coding: utf-8 -*-
"""
@author: Tan Chang Jung
"""
import pandas as pd
from hdfs import InsecureClient
import pyodbc

#%% 
# hive connection
conn = pyodbc.connect(DSN = "hive_connection", autocommit = True, ansi = True)
print(conn)

db = pd.read_sql("show databases;", conn)

bitcoin_df = pd.read_sql("SELECT * FROM bitcoin", conn)
ethereum_df = pd.read_sql("SELECT * FROM ethereum", conn)
litecoin_df = pd.read_sql("SELECT * FROM litecoin", conn)


#%% 
# hdfs connection
client_hdfs = InsecureClient('http://' + 'localhost' + ':50070')

with client_hdfs.read('/user/root/datamining/data/ethereum.csv', encoding = 'utf-8') as reader:
    df = pd.read_csv(reader,index_col=0)
