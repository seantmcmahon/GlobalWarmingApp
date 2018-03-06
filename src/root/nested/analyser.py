'''
Created on 24 Feb 2018

@author: seantmcmahon
'''

import pandas as pd
# from plotter import plotGraph
# import numpy as np
import os
import matplotlib
from newDao import Dao
from numpy import std, mean
matplotlib.use("macosx")


class Analyser:

    """
    ANALYSIS STEPS:
    For each time step grouping:
        Graph 1 - plot mean with range bars
        Graph 2 - plot mean with best fit line
        gradient mx (y = mx + c) determines trend of increase/decreasing values
    """

    def __init__(self, dao):
        self.dao = Dao()
        self.path = os.path.abspath(os.path.dirname(__file__))

    def plotGraph(self, series, graphName):
        """
        Plot all points, then plot line of best and return its gradient in the
        tuple (m, c) as in y = mx + c
        Best fit gradient equation adapted from https://stackoverflow.com/
        questions/22239691/code-for-line-of-best-fit-of-a-scatter-plot-in-python
        """
        ys = series.tolist()
        xs = range(1, len(ys)+1)
        n = len(xs)  # or len(ys)

        xbar = sum(xs)/float(len(xs))
        ybar = sum(ys)/float(len(ys))

        numer = sum([xi*yi for xi, yi in zip(xs, ys)]) - n * xbar * ybar
        denum = sum([xi**2 for xi in xs]) - n * xbar**2

        m = numer / denum
        c = ybar - m * xbar

        return m, c

    def remove_initial_NaNs(self, series):
        pass

    def remove_NaNs(self, df):
        newValues = []
        for x in df.tolist():
            newYs = []
            ys = x.tolist()
            for y in ys:
                if str(y) != "nan":
                    newYs.append(y)
            newValues.append(newYs)
        df.columns['oldTS']
        print df.head()
        df['ts'] = pd.Series(newValues, index=df.index)
        df.drop('oldTS', axis=1, inplace=True)
        print df.head()
        return df

    def analyse_seasonal(self, df):
        pass

    def analyse_annual(self, df):
        pass

    def analyse_decades(self, df):
        df[(df.ts != float("nan")).idxmax():]
        print df
        df = df.groupby((df.index.year//10)*10)["ts"]
        stddevs = df.std()
        means = df.mean()
        # plot the std. devs with a line of best fit, get gradient of this line
        # positive gradient means increased values for data type and vice versa
        # same for means
        stdDevM, stdDevC = self.plotGraph(stddevs, "decadeStdDev")
        meanM, meanC = self.plotGraph(means, "decadeMean")
        print "Std. Dev. best fine line: y = {:.3f}x + {:.3f}".format(
            stdDevM, stdDevC)
        print "Mean best fine line: y = {:.3f}x + {:.3f}".format(meanM, meanC)

    def analyse_individual_station(self, region, dataType):
        print "Start Analysis"
        years = self.dao.getAvailableYearsForRegion(region, dataType)
        df = self.dao.get_values(region, dataType, "Decade", years[0], years[-1], "Decade", std)
        df = self.dao.get_values(region, dataType, "Decade", years[0], years[-1], "Decade", mean)
        # ts = pd.DataFrame({"ts": ts}, index=times, dtype=float)
        print df
        """if params['data_type'] != "All Data":
            decadeResults = self.analyse_decades(ts)
            annualResults = self.analyse_annual(ts)
            seasonalResults = self.analyse_seasonal(ts) """

    def analyse_country(self, params):
        pass

    def analyse_data(self, region, dataType, width, height):
        if region in self.dao._stations:
            self.analyse_individual_station(region, dataType)
        else:
            self.analyse_country(region, dataType)
