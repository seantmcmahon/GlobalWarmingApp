'''
Created on 9 Jan 2018

@author: seantmcmahon
'''

import pandas as pd
import matplotlib
matplotlib.use("macosx")
import os 
from matplotlib import pyplot as plt



class Dao:
    
    def _loadStationData(self, stationName):
        return pd.read_csv(self.path +'/stationData/'+ stationName +'.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python')
    
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
            "RossOnWye"             : self._loadStationData('rossOnWye'),
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
            "Wales"             : ["Aberporth", "Cardiff Bute Park", "Cwmystwyth", "Ross-On-Wye"],
            "Northern Ireland"  : ["Armagh", "Ballypatrick Forest"]
        }
        
    def getRegionNames(self):
        return ['UK'] + self._countryStationsMap.keys() + self._stations.keys()
    
    def getAvailableYearsForRegion(self, regionName):
        return list(map(lambda x: str(x) , list(set(self._stations.get(regionName)['yyyy'].tolist()))))

    def getAvailableMonthsForRegion(self, regionName, year):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        return list(map(lambda x: months[x-1], self._stations.get(regionName).loc[self._stations.get(regionName)['yyyy'] == int(year)]['mm'].tolist()))
    
    def create_graph(self, details, width, height):
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        df = self._stations.get("Paisley").loc[self._stations.get("Paisley")['yyyy'] == 2008][['mm', 'rain']]
        fig = plt.figure(figsize=(width/96, height/96)) # sizing found at https://stackoverflow.com/questions/13714454/specifying-and-saving-a-figure-with-exact-size-in-pixels/13714720
        plt.plot(df['mm'], [float(x) for x in df['rain']])
        plt.ylabel('Rainfall (mm)')
        plt.title('Paisley Rainfall')
        plt.grid(True)
        plt.savefig(self.path + "/imgs/graph.png")
        plt.close(fig)
    
    