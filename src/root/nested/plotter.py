'''
Created on 3 Mar 2018

@author: seantmcmahon
'''

import matplotlib
matplotlib.use("macosx")
from matplotlib import pyplot as plt


def plotGraph(self, fileName, title, xName, yName, dataSeries):
    fig = plt.figure(figsize=(6, 2))
    plt.title(title)
    plt.xlabel(xName)
    plt.ylabel(yName)
    for x in dataSeries:
        plt.plot(x)
    plt.grid(True)
    plt.savefig(self.path + "/imgs/" + fileName + ".png")
    plt.close(fig)
