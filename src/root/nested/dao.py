'''
Created on 9 Jan 2018

@author: seantmcmahon
'''

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("macosx")
import os 
import itertools
from matplotlib import pyplot as plt



class Dao:
    
    def _loadStationData(self, stationName):
        df = pd.read_csv(self.path +'/stationData/'+ stationName +'.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python')
        df['date'] = pd.to_datetime(df.apply(lambda row: str(row.yyyy) + "-" + str(row.mm), axis=1)) # found at https://kaijento.github.io/2017/04/22/pandas-create-new-column-sum/
        df.set_index('date', inplace=True)
        return df
    
    def _createStationDictionary(self):
        return {
            "Aberporth"             : self._loadStationData('aberporth'),
            "Armagh"                : self._loadStationData('armagh'),
            "Ballypatrick Forest"   : self._loadStationData('ballypatrickForest'),
            "Bradford"              : self._loadStationData('bradford'),
            "Braemar"               : self._loadStationData('braemar'),
            "Camborne"              : self._loadStationData('camborne'),
            "Cambridge NIAB"        : self._loadStationData('cambridgeNIAB'),
            "Cardiff Bute Park"     : self._loadStationData('cardiffButePark'),
            "Chivenor"              : self._loadStationData('chivenor'),
            "Cwmystwyth"            : self._loadStationData('cwmystwyth'),
            "Dunstaffnage"          : self._loadStationData('dunstaffnage'),
            "Durham"                : self._loadStationData('durham'),
            "Eastbourne"            : self._loadStationData('eastbourne'),
            "Eskdalemuir"           : self._loadStationData('eskdalemuir'),
            "Heathrow"              : self._loadStationData('heathrow'),
            "Hurn"                  : self._loadStationData('hurn'),
            "Lerwick"               : self._loadStationData('lerwick'),
            "Leuchars"              : self._loadStationData('leuchars'),
            "Lowestoft"             : self._loadStationData('lowestoft'),
            "Manston"               : self._loadStationData('manston'),
            "Nairn"                 : self._loadStationData('nairn'),
            "Newton Rigg"           : self._loadStationData('newtonRigg'),
            "Oxford"                : self._loadStationData('oxford'),
            "Paisley"               : self._loadStationData('paisley'),
            "Ringway"               : self._loadStationData('ringway'),
            "Ross-On-Wye"             : self._loadStationData('rossOnWye'),
            "Shawbury"              : self._loadStationData('shawbury'),
            "Sheffield"             : self._loadStationData('sheffield'),
            "Southampton"           : self._loadStationData('southampton'),
            "Stornoway"             : self._loadStationData('stornoway'),
            "Sutton Bonington"      : self._loadStationData('suttonBonington'),
            "Tiree"                 : self._loadStationData('tiree'),
            "Valley"                : self._loadStationData('valley'),
            "Waddington"            : self._loadStationData('waddington'),
            "Whitby"                : self._loadStationData('whitby'),
            "Wick Airport"          : self._loadStationData('wickAirport'),
            "Yeovilton"             : self._loadStationData('yeovilton')
        }

    def __init__(self):
        # Turn interactive plotting off - found on StackOverflow -> https://stackoverflow.com/questions/15713279/calling-pylab-savefig-without-display-in-ipython
        plt.ioff()
        self.path = os.path.abspath(os.path.dirname(__file__))
        self._stations = self._createStationDictionary()
        self._countryStationsMap =  {
            "Scotland"          : ["Braemar", "Dunstaffnage", "Eskdalemuir", "Lerwick", "Leuchars", "Nairn", "Paisley", "Stornoway", "Tiree", "Wick Airport"],
            "England"           : ["Bradford", "Camborne", "Cambridge NIAB", "Chivenor", "Durham", "Eastbourne", "Heathrow", "Hurn", "Lowestoft", "Manston", "Newton Rigg", "Oxford", "Ringway", "Shawbury", "Sheffield", "Southampton", "Sutton Bonington", "Waddington", "Whitby", "Yeovilton"],
            "Wales"             : ["Aberporth", "Cardiff Bute Park", "Cwmystwyth", "Ross-On-Wye", "Valley"],
            "Northern Ireland"  : ["Armagh", "Ballypatrick Forest"]
        }
        
    def getRegionNames(self):
        return ['UK'] + self._countryStationsMap.keys() + self._stations.keys()
    
    def getAvailableYearsForRegion(self, regionName, data_type):
        if regionName == "UK":
            ukList = list(set(list(itertools.chain.from_iterable([self.getAvailableYearsForRegion(x, data_type) for x in self._countryStationsMap.keys()]))))
            ukList.sort()
            return ukList
        elif regionName in self._countryStationsMap.keys():
            sortedList = list(set(list(itertools.chain.from_iterable([self.getAvailableYearsForRegion(x, data_type) for x in self._countryStationsMap.get(regionName)]))))
            sortedList.sort()
            return sortedList
        else:
            df = []
            try:
                if data_type == "Max Temp" : 
                    df = self._stations.get(regionName).loc[self._stations.get(regionName)['tmax'] != "---"][['yyyy']]
                elif data_type == "Min Temp" : 
                    df = self._stations.get(regionName).loc[self._stations.get(regionName)['tmin'] != "---"][['yyyy']]
                elif data_type == "Avg Temp" : 
                    df = self._stations.get(regionName).loc[(self._stations.get(regionName)['tmax'] != "---") | (self._stations.get(regionName)['tmin'] != "---")][['yyyy']]
                elif data_type == "Air Frost": 
                    df = self._stations.get(regionName).loc[self._stations.get(regionName)['af'] != "---"][['yyyy']]
                elif data_type == "Total Rainfall" : 
                    df = self._stations.get(regionName).loc[self._stations.get(regionName)['rain'] != "---"][['yyyy']]
                elif data_type == "Avg Rainfall" : 
                    df = self._stations.get(regionName).loc[self._stations.get(regionName)['rain'] != "---"][['yyyy']]
                elif data_type == "Total Sun Hours": 
                    df = self._stations.get(regionName).loc[self._stations.get(regionName)['sun'] != "---"][['yyyy']]
                else: # "Avg Sun Hours" 
                    df = self._stations.get(regionName).loc[self._stations.get(regionName)['sun'] != "---"][['yyyy']]
                years = list(set(df['yyyy'].tolist()))
            except TypeError:
                # Reaches here when a column has no missing data
                df = self._stations.get(regionName)[['yyyy']]
                years = list(set(df['yyyy'].tolist()))
            return list(map(lambda x: str(x) , years))
    def create_graph(self, details, width, height):
        df = self._stations.get(details.get("region")).loc[details.get("start_year"):details.get("end_year")][['yyyy', 'mm', 'rain']]
        fig = plt.figure(figsize=(width/96, height/96)) # sizing found at https://stackoverflow.com/questions/13714454/specifying-and-saving-a-figure-with-exact-size-in-pixels/13714720
        plt.plot([pd.to_datetime(str(y) + "-" + str(m)) for y, m in zip(df['yyyy'], df['mm'])], [float(x) if x != "---" else np.NaN for x in df['rain']]) # NaN code from https://stackoverflow.com/questions/34794067/how-to-set-a-cell-to-nan-in-a-pandas-dataframe
        plt.ylabel('Rainfall (mm)')
        plt.title(details.get('region') + ' ' + details.get('data_type'))
        plt.grid(True)
        plt.savefig(self.path + "/imgs/graph.png")
        plt.close(fig)
    
    