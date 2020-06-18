#%%
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from datetime import date
from tests import web_scraper
import datetime 


#%%
#df = pd.read_csv("bitcoin.csv")
#df = df[:180]
#df = df[::-1].reset_index(drop=True)
#df = df.set_index('Date') 
#df.index = pd.to_datetime(df.index)
def update_prediction(df):
    df = df[-180:]
    df_close = df[['Close']]

    data = df.iloc[:, 0]
    history = []
    target = []
    length = 90

    for i in range(len(data)-length):
        x = data[i:i+length]
        y = data[i+length]
        history.append(x)
        target.append(y)

    history = np.array(history)

    target = np.array(target)
    target = target.reshape(-1,1)

    scaler = MinMaxScaler()
    history_scaled = scaler.fit_transform(history)
    target_scaled = scaler.fit_transform(target)

    history_scaled = history_scaled.reshape((len(history_scaled), length, 1))

    X_train = history_scaled[:89,:,:]
    X_test = history_scaled[89:,:,:]

    y_train = target_scaled[:89,:]
    y_test = target_scaled[89:,:]

    model = tf.keras.models.load_model("full_model.h5")
    prediction = model.predict(X_test)
    prediction_transformed = scaler.inverse_transform(prediction)

    return prediction_transformed

#value = 'bitcoin'
#data_frame = web_scraper(value).reset_index(drop=True).set_index('Date').sort_index()
#data_frame.index = pd.to_datetime(data_frame.index)
#t = datetime.datetime.now()
#all the data from the beginning until current time
#data = data_frame.loc["2016-10-15"
#    : t.strftime(
#    "%Y%m%d" #"2020-06-10"# %H:%M:%S"
#        )
#    ]
#print(data)
#b = update_prediction(data)
#print(b)