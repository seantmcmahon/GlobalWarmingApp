'''
Created on 3 Feb 2018

@author: seantmcmahon

Class follows example code found at 
https://machinelearningmastery.com/make-sample-forecasts-arima-python/

'''

import pandas as pd
import os
import numpy as np
import itertools
import math
import constants
from plotter import plotGraph
from statsmodels.tsa.arima_model import ARIMA
from datetime import datetime


class Predictor:

    # taken from https://machinelearningmastery.com/
    # arima-for-time-series-forecasting-with-python/
    def arima(self, ts, p, d, q):
        try:
            X = ts.values
            size = int(len(X) * 0.66)
            train, test = X[0:size], X[size:len(X)]
            history = [x for x in train]
            predictions = list()
            model = None
            model_fit = None
            for t in range(len(test)):
                model = ARIMA(history, order=(p, d, q))
                model_fit = model.fit(disp=0)
                output = model_fit.forecast()
                yhat = output[0]
                predictions.append(yhat)
                obs = test[t]
                history.append(obs)
            return model_fit.aic
        except:
            return None

    def getBestFitModel(self, ts):
        bestResult = 1000000000
        bestModel = None
        for x in list(itertools.product(range(3), range(2), range(3))):
            (p, d, q) = x
            if not p == d == q:
                res = self.arima(ts, p, d, q)
                if res and res < bestResult:
                    bestResult = res
                    bestModel = x
        return bestModel

    def difference(self, dataset):
        diff = list()
        for i in range(1, len(dataset)):
            value = dataset[i] - dataset[i - 1]
            diff.append(value)
        return np.array(diff)

    # invert differenced value
    def inverse_difference(self, history, yhat, interval=1):
        return yhat + history[-interval]

    def forecast(self, X, p, d, q):
        for j in range(10):
            differenced = self.difference(X)
            # fit model
            model = ARIMA(differenced, order=(p, d, q))
            model_fit = model.fit(disp=0)
            # one-step out-of sample forecast
            forecast = model_fit.forecast()[0]
            # invert the differenced forecast to something usable
            forecast = self.inverse_difference(X, forecast)
            X.append(forecast[0])
        return X[-10:]

    def get_forecast(self, series):
        print "series", series
        (p, d, q) = self.getBestFitModel(series)
        print p, d, q
        X = list(series.values)
        futures = [list(series.values)[-1]] + self.forecast(list(series.values), p, d, q)
        past = self.forecast(list(series.values)[::-1], p, d, q)[::-1] + [list(series.values)[0]]

        futuresIndex = [datetime(int(series.index[-1]), 1, 1)] +\
            [datetime(x, 1, 1) for x in range(int(series.index[-1])+1, int(series.index[-1])+11)]
        pastIndex = [datetime(x, 1, 1) for x in range(int(series.index[0])-10, int(series.index[0]))]\
            + [datetime(int(series.index[0]), 1, 1)]
        currentIndex = pastIndex[:-1] + [datetime(int(x), 1, 1) for x in series.index] + futuresIndex[1:]

        pastSeries = (pd.Series(past, index=pastIndex), "Past Prediction")
        futureSeries = (pd.Series(futures, index=futuresIndex), "Future Prediction")

        pastPadding = [np.nan for x in range(10)]
        futurePadding = [np.nan for x in range(10)]
        current = list(pastPadding)+list(series.values)+list(futurePadding)

        currentSeries = (pd.Series(current, index=currentIndex), "Existing Data")
        return (pastSeries, currentSeries, futureSeries)

    def plot_predictions(self, region, data_type, prediction_type,
                         time_step, operation, month_range, width, height):
        years = self.dao.getAvailableYearsForRegion(region, data_type)
        start_year = years[0]
        end_year = years[-1]
        ts = self.dao.get_values(region, data_type, start_year,
                                 end_year, time_step, operation,
                                 month_range)
        ts = pd.DataFrame({"ts": ts})
        (past, current, future) = self.get_forecast(ts)
        results = []
        if prediction_type == constants.FUTURE_VALUE:
            results = [current, future]
        elif prediction_type == constants.PAST_VALUE:
            results = [past, current]
        else:
            results = [past, current, future]
        plotGraph("newModel", "Forecast: " + region + " " + operation + " " +
                  data_type, "Years", data_type, results)

    def __init__(self, dao):
        self.dao = dao
        self.path = os.path.abspath(os.path.dirname(__file__))
