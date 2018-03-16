'''
Created on 24 Feb 2018

@author: seantmcmahon
'''

import pandas as pd
from plotter import plotGraph, plot2Graphs
import math
from newDao import Dao
from numpy import nanmean, nanstd


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

    def getGradient(self, series):
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

    def analyse_by_year(self, values):
        mx, _ = self.getGradient(values)
        return mx

    def analyse_by_decade(self, series, op):
        operation = self.dao._operations.get(op)
        df = pd.DataFrame({"vals": series, "years": series.index})
        values = df.groupby((df["years"].astype('int')//10)*10)["vals"].apply(list).apply(operation)
        # plot the results with a line of best fit, get gradient of this line
        # positive gradient means increased values for data type and vice versa
        # same for means
        mx, _ = self.getGradient(values)
        return mx

    def analyseMean(self, values, region, dataType):
        m, c = self.getGradient(values)
        if m > 0:
            message = "From the data available, there is evidence of an increase in "\
                + dataType + " in " + region + ", as can be seen in the previous graph."
        else:
            message = "From the data available, there is no evidence of an increase in "\
                + dataType + " in " + region + " as can be seen in the previous graph."\
                + "From this test, there is no evidence of climate change in " + region
        valuelist = values.tolist()
        series = [values, [(m * x) + c for x in range(len(valuelist))]]
        return("Mean " + dataType + " for: " + region, dataType, series, message)

    def analyseStd(self, values, region, dataType):
        m, c = self.getGradient(values)
        if m > 0:
            message = "From the data available, there is evidence of an increase in "\
                + dataType + " variance in " + region + ", as can be seen in the previous graph."
        else:
            message = "From the data available, there is no evidence of an increase in "\
                + dataType + "variance in " + region + ", as can be seen in the previous graph."\
                + "From this test, there is no evidence of climate change in " + region
        valuelist = values.tolist()
        series = [values, [(m * x) + c for x in range(len(valuelist))]]
        return (dataType + " Std. Dev. Data Variance: " + region, dataType, series, message)

    def analyse_data(self, region, dataType, width, height):
        years = self.dao.getAvailableYearsForRegion(region, dataType)
        results = []
        for x in self.dao.months:
            for op in self.dao.getPossibleOperations():
                df = self.dao.get_values(region, dataType, years[0], years[-1], x, op)
                result = self.analyse_by_decade(df, op)
                if not math.isnan(result):
                    results.append((op + " " + dataType + " by decade for " + x, result, op))
                result = self.analyse_by_year(df)
                if not math.isnan(result):
                    results.append((op + " " + dataType + " by decade for " + x, result, op))
        # print results
        highestGrad = max(results, key=lambda item: item[1])
        lowestGrad = min(results, key=lambda item: item[1])
        # Change this from print to add to a label in the UI, then create a graph for each of them
        greatest = "The input combination with the greatest trend increase is " + highestGrad[0] + " with a gradient of {:.3f}".format(highestGrad[1])
        lowest = "The input combination with the greatest trend decrease is " + lowestGrad[0] + " with a gradient of {:.3f}".format(lowestGrad[1]) 

        meanResults = self.analyseMean(self.dao.get_values(region, dataType, years[0], years[-1], "Full Year", "Mean Average"), region, dataType)
        stdDevResults = self.analyseStd(self.dao.get_values(region, dataType, years[0], years[-1], "Full Year", "Standard Deviation"), region, dataType)
        plot2Graphs("globWarmResults", meanResults[0], meanResults[1], meanResults[2],
                    stdDevResults[0], stdDevResults[1], stdDevResults[2])
        return greatest, lowest, meanResults[3], stdDevResults[3]
