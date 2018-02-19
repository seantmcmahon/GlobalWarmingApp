'''
Created on 3 Feb 2018

@author: seantmcmahon

Class follows example code found at https://www.analyticsvidhya.com/blog/2016/02/time-series-forecasting-codes-python/

'''

import pandas as pd
import numpy as np
import os
import itertools
import matplotlib
import math
matplotlib.use("macosx")
from matplotlib import pyplot as plt
from statsmodels.tsa.arima_model import ARIMA 

class Predictor:
    
    def arima(self, ts, p, d, q): # taken from https://machinelearningmastery.com/arima-for-time-series-forecasting-with-python/
        try:
            X = ts.values
            size = int(len(X) * 0.66)
            train, test = X[0:size], X[size:len(X)]
            history = [x for x in train]
            predictions = list()
            model = None
            model_fit = None
            for t in range(len(test)):
                model = ARIMA(history, order=(p,d,q))
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
        for x in list(itertools.product(range(3), range(2),range(3))):
            (p, d, q) = x
            res = self.arima(ts, p, d, q)
            if res and res < bestResult:
                bestResult = res
                bestModel = x
        return bestModel
            
    def predict(self, ts, p, d, q):
        X = ts.values
        size = int(len(X) * 0.66)
        train, test = X[0:size], X[size:len(X)]
        history = [x for x in train]
        predictions = list()
        model = None
        model_fit = None
        #model existing data
        for t in range(len(test)):
            model = ARIMA(history, order=(0,1,1))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
        #model future data
        for t in range(20):
            model = ARIMA(history, order=(0,1,1))
            model_fit = model.fit(disp=0)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            history.append(yhat)
        preds = [np.nan for x in range(len(ts) - (len(predictions)-20))]
        forecast = preds + [x[0] for x in predictions]
        df = pd.DataFrame({"orig": ts.iloc[:,0], "forecast": forecast[:-20]})
        data = [pd.to_datetime("01-01-"+str(2016+x)) for x in range(20)]
        orig = [np.nan for x in range(20)]
        futures = forecast[-20:]
        df2 = pd.DataFrame({"orig": orig, "forecast": futures, "ind": data})
        df2.set_index("ind", inplace=True)
        df = pd.concat([df, df2])
        # get first row of forecast that aren't nan
        index = 0
        for x in range(len(forecast)):
            if not math.isnan(forecast[x]):
                index = x
                break
            
        # plot
        fig = plt.figure(figsize=(5, 2))
        plt.plot(df[['orig']].iloc[index:], color='red')
        plt.plot(df[['forecast']].iloc[index:], color='green')
        plt.savefig(self.path + "/imgs/newModel.png")
        plt.close(fig)
        
    def predict_future_values(self):
        pass
    
    def predict_past_values(self):
        pass
    
    def plot_predictions(self, params, width, height):
        years = self.dao.getAvailableYearsForRegion(params.get("region"), params.get("data_type"))
        params['start_year'] = years[0]
        params['end_year'] = years[-1]
        times, ts = self.dao.retrieve_data(params)
        ts = pd.DataFrame({"ts": ts, "times": times})
        ts.set_index("times", inplace= True)
        #(p, d, q) = self.getBestFitModel(ts)
        #self.predict(ts, p, d, q)
        self.predict(ts, 0, 1, 1)
        
    def __init__(self, dao):
        self.dao = dao 
        self.path = os.path.abspath(os.path.dirname(__file__))