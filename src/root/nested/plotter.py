'''
Created on 3 Mar 2018

@author: seantmcmahon
'''

import os
import matplotlib
matplotlib.use('module://kivy.garden.matplotlib.backend_kivy')
from matplotlib import pyplot as plt


def plotGraph(fileName, title, xName, yName, dataSeries):

    fig = plt.figure(figsize=(6, 2))
    plt.title(title)
    plt.ylabel(yName)
    for x in dataSeries:
        print x
        plt.plot(x[0], label=x[1])
    ticks = max([x[0] for x in dataSeries], key=len).index
    while len(ticks) > 10:
        ticks = ticks[::2]
    plt.xticks(ticks)
    # plt.set_xlabel(xName)
    plt.legend()
    plt.savefig(os.path.abspath(os.path.dirname(__file__)) + "/imgs/" + fileName + ".png")
    plt.close(fig)


def plot2Graphs(filename, title1, ylabel1, series1, title2, ylabel2, series2):
    fig = plt.figure(figsize=(8, 4))
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.set_title(title1)
    ax1.set_ylabel(ylabel1)
    for x in series1:
        ax1.plot(x)
    ax1.set_xticks([])

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.set_title(title2)
    ax2.set_ylabel(ylabel2)
    for x in series2:
        ax2.plot(x)

    plt.xlabel("Time")
    fig.tight_layout()
    fig.savefig(os.path.abspath(os.path.dirname(__file__)) + "/imgs/" + filename + ".png")
    plt.close(fig)
