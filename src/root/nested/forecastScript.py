'''
Created on 13 Mar 2018

@author: seantmcmahon
'''

import pandas as pd
import numpy
from statsmodels.tsa.arima_model import ARIMA
from numpy import nanmean
from plotter import plotGraph
from datetime import datetime

# df = pd.read_csv('stationData/paisley.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python')
df = pd.read_csv('stationData/stornoway.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python')
df = df.astype('str')
for x in ["tmax", "tmin", "af", "rain", "sun"]:
    df[x] = df[x].str.replace("[^0-9\.-]", "")
    df[x] = pd.to_numeric(df[x], errors='coerce')
df['tmean'] = df[['tmax', 'tmin']].mean(axis=1)
for x in ["tmax", "tmin", "af", "rain", "sun", "tmean"]:
    df[x] = df[x].astype('float')
df['mm'] = df['mm'].astype('int')
df['date'] = pd.to_datetime(df.apply(lambda row: str(int(row.yyyy)) + "-" + str(int(row.mm)), axis=1))
df.set_index('date', inplace=True)


tmax = df.groupby('yyyy')['tmax'].apply(list).apply(nanmean)
current = df.groupby('yyyy')['tmax'].apply(list).apply(nanmean)


def difference(dataset):
    diff = list()
    for i in range(1, len(dataset)):
        value = dataset[i] - dataset[i - 1]
        diff.append(value)
    return numpy.array(diff)


# invert differenced value
def inverse_difference(history, yhat, interval=1):
    return yhat + history[-interval]


def forecast(X):
    for j in range(10):
        differenced = difference(X)
        # fit model
        model = ARIMA(differenced, order=(7, 0, 1))
        model_fit = model.fit(disp=0)
        # one-step out-of sample forecast
        forecast = model_fit.forecast()[0]
        # invert the differenced forecast to something usable
        forecast = inverse_difference(X, forecast)
        X.append(forecast[0])
    return X[-10:]


X = list(tmax.values)
futures = [list(current)[-1]] + forecast(list(tmax.values))
past = forecast(list(tmax.values)[::-1])[::-1] + [list(current)[0]]
futuresIndex = [datetime(int(current.index[-1]), 1, 1)] + [datetime(x, 1, 1) for x in range(int(current.index[-1])+1, int(current.index[-1])+11)]
pastIndex = [datetime(x, 1, 1) for x in range(int(current.index[0])-10, int(current.index[0]))] + [datetime(int(current.index[0]), 1, 1)]
currentIndex = pastIndex[:-1] + [datetime(int(x), 1, 1) for x in current.index] + futuresIndex[1:]
pastSeries = (pd.Series(past, index=pastIndex), "Past Prediction")
futureSeries = (pd.Series(futures, index=futuresIndex), "Future Prediction")
pastPadding = [numpy.nan for x in range(10)]
futurePadding = [numpy.nan for x in range(10)]
current = list(pastPadding)+list(current.values)+list(futurePadding)

currentSeries = (pd.Series(current, index=currentIndex), "Existing Data")
print pastSeries
print currentSeries
print futureSeries
plotGraph("Test", "Forecast", "", "Values", [pastSeries, currentSeries, futureSeries])