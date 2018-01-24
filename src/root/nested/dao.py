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
import decimal
import re
from matplotlib import pyplot as plt

class Dao:
    
    def setDFIndex(self, df):
        df['date'] = pd.to_datetime(df.apply(lambda row: str(int(row.yyyy)) + "-" + str(int(row.mm)), axis=1)) # found at https://kaijento.github.io/2017/04/22/pandas-create-new-column-sum/
        df.set_index('date', inplace=True)
        return df
    
    def _loadStationData(self, stationName):
        df = pd.read_csv(self.path +'/stationData/'+ stationName +'.txt', sep="\s+|\t+|\s+\t+|\t+\s+", engine='python')
        df = self.setDFIndex(df)
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
                elif data_type == "Air Frost Days": 
                    df = self._stations.get(regionName).loc[self._stations.get(regionName)['af'] != "---"][['yyyy']]
                elif "Rainfall" in data_type: 
                    df = self._stations.get(regionName).loc[self._stations.get(regionName)['rain'] != "---"][['yyyy']]
                else: #"Sun Hours": 
                    df = self._stations.get(regionName).loc[self._stations.get(regionName)['sun'] != "---"][['yyyy']]
                years = list(set(df['yyyy'].tolist()))
            except TypeError:
                # Reaches here when a column has no missing data
                df = self._stations.get(regionName)[['yyyy']]
                years = list(set(df['yyyy'].tolist()))
            return list(map(lambda x: str(x) , years))

    def prepare_values_for_display(self, values):
        return [float(re.sub('[^0-9\.-]', '', str(x))) for x in values if x != "---"]
    
    def combine_month_data(self, table, value, operation):
        groupingColumns = ['yyyy', 'mm']
        years = [x[0] for x in table.groupby(groupingColumns)['yyyy'].apply(list)]
        values = [x for x in table.groupby(groupingColumns)[value].apply(list)]
        months = [x[0] for x in table.groupby(groupingColumns)['mm'].apply(list)]
        if operation == "avg":
            values = [sum(self.prepare_values_for_display(x)) / len(self.prepare_values_for_display(x)) if self.prepare_values_for_display(x) != [] else 0 for x in values]
        else:
            values = [operation(self.prepare_values_for_display(x))if self.prepare_values_for_display(x) != [] else 0 for x in values ]
        df = pd.DataFrame({'yyyy': years, 'mm': months, value: values})
        df = self.setDFIndex(df)
        return df
    
    def get_combined_table_for_country(self, country, value, operation):
        countryStations = pd.concat([self._stations.get(x) for x in self._countryStationsMap.get(country)])[['yyyy', 'mm', value]]
        return self.combine_month_data(countryStations, value, operation)
    
    def get_combined_table_for_uk(self, value, operation):
        ukStations =  pd.concat([self.get_combined_table_for_country(x, value, operation) for x in self._countryStationsMap.keys()])
        return self.combine_month_data(ukStations, value, operation)
    
    def total_values_by_year(self, valueTable, value, operation):  
        df = valueTable.groupby('yyyy')[value].apply(list)
        summedValues = []
        for x in df.tolist():
            if operation == "avg":
                summedValues.append(sum([float(y) for y in x if y != "---"]) / len([float(y) for y in x if y != "---"]))
            else:
                summedValues.append(operation([float(y) for y in x if y != "---"]))
        years = valueTable["yyyy"].unique().tolist()
        table = pd.DataFrame({"yyyy": years, value: summedValues})
        return table[['yyyy', value]]
    
    def total_values_by_month(self, valueTable, value): 
        index = [str(x) + "-" + str(y) for x, y in zip(valueTable['yyyy'].tolist(), valueTable['mm'].tolist()) ]
        df = pd.DataFrame({"index": index, value: valueTable[value]})
        return df
    
    def total_month_every_year(self, table, value, month):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        month = months.index(month) + 1
        df = table.loc[table['mm'] == month][['yyyy', value]]
        return df
    
    def total_season_every_year(self, table, value, season):
        seasons = {
            "Spring": [3,4,5],
            "Summer": [6,7,8],
            "Autumn": [9,10,11],
            "Winter": [12, 1, 2]
            }
        # df = table.loc[table['mm'] == month][['yyyy', value]]
        # return df
    
    def get_table(self, region, value, operation):
        if region == "UK":
            return self.get_combined_table_for_uk(value, operation)
        elif region in self._countryStationsMap:
            return self.get_combined_table_for_country(region, value, operation)
        else:
            return self._stations.get(region)[['yyyy', 'mm', value]]
        
    def group_data_by_time_step(self, df, timeStep, value, operation, monthRange=None):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        seasons = ["Spring", "Summer", "Autumn", "Winter"]
        print timeStep
        if timeStep == "Month":
            return self.total_values_by_month(df, value)
        elif timeStep == "Season":
            pass
        elif timeStep == "Entire Year":
            return self.total_values_by_year(df, value, operation)
        elif timeStep.replace(" Annually", '') in months:
            return self.total_month_every_year(df, value, timeStep.replace(" Annually", ''))
        elif timeStep.replace(" Annually", '') in seasons:
            pass
        else: # Custom Month Range
            pass
    
    def create_graph(self, details, width, height):
        regionName = details.get("region")
        data_type = details.get("data_type")
        fig = plt.figure(figsize=(width/96, height/96)) # sizing found at https://stackoverflow.com/questions/13714454/specifying-and-saving-a-figure-with-exact-size-in-pixels/13714720
        graphDetails = {
            "Max Temp": {"value" : "tmax", "label": "Max Temp (deg. C)", "operation": max},
            "Min Temp": {"value" : "tmin", "label": "Min Temp (deg. C)", "operation": min},
            "Avg Max Temp": {"value" : "tmax", "label": "Avg Max Temp (deg. C)", "operation": "avg"},
            "Avg Min Temp": {"value" : "tmin", "label": "Avg Min Temp (deg. C)", "operation": min},
            "Air Frost Days": {"value" : "af", "label": "Air Frost Days", "operation": sum},
            "Total Rainfall": {"value" : "rain", "label": "Total Rainfall (mm)", "operation": sum},
            "Avg Rainfall": {"value" : "rain", "label": "Avg Rainfall (mm)", "operation": "avg"},
            "Max Sun Hours": {"value" : "tmax", "label": "Max Sun Hours", "operation": max},
            "Min Sun Hours": {"value" : "tmax", "label": "Min Sun Hours", "operation": min},
            "Avg Sun hours": {"value" : "tmax", "label": "Avg Sun Hours", "operation": "avg"},
        }
        if data_type in graphDetails.keys():
            df = self.group_data_by_time_step(self.get_table(regionName, graphDetails.get(data_type).get("value"), graphDetails.get(data_type).get("operation"))
                                              .loc[details.get("start_year"):details.get("end_year")],
                                               details.get("time_step"), 
                                               graphDetails.get(data_type).get("value"),
                                               graphDetails.get(data_type).get("operation"))
            plt.plot([pd.to_datetime(str(x)) for x in df[df.columns[0]]], [float(x) if x != "---" else np.NaN for x in df[graphDetails.get(data_type).get("value")]]) # NaN code from https://stackoverflow.com/questions/34794067/how-to-set-a-cell-to-nan-in-a-pandas-dataframe
            plt.ylabel(graphDetails.get(data_type).get("label"))
        else: # Avg temp
            pass
        plt.title(regionName + ' ' + data_type)
        plt.grid(True)
        plt.savefig(self.path + "/imgs/graph.png")
        plt.close(fig)
    
    