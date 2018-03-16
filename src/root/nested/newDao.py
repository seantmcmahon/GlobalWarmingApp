'''
Created on 26 Feb 2018

@author: seantmcmahon
'''

import pandas as pd
import os
from numpy import nanmean, nanstd


class Dao:

    def get_season(self, row):
        if row['mm'] in [1, 2, 12]:
            return "Winter"
        elif row['mm'] in [3, 4, 5]:
            return "Spring"
        elif row['mm'] in [6, 7, 8]:
            return "Summer"
        else:
            return "Autumn"

    def _loadStationData(self, stationName):
        """
            1 - Strip out any special chars (#,$, etc) leaving just '[^0-9\.-]'
            2 - Set dtype to float and replace "---" with np.NaN
            3 - Add mean temp column
            4 - Set value column data types to float
            5 - Add season column
            6 - Set index found at https://kaijento.github.io/2017/04/22/
            pandas-create-new-column-sum/
        """
        df = pd.read_csv(self.path + '/stationData/' + stationName + '.txt',
                         sep="\s+|\t+|\s+\t+|\t+\s+", engine='python')
        df = df.astype('str')
        for x in ["tmax", "tmin", "af", "rain", "sun"]:
            df[x] = df[x].str.replace("[^0-9\.-]", "")
            df[x] = pd.to_numeric(df[x], errors='coerce')
        df['tmean'] = df[['tmax', 'tmin']].mean(axis=1)
        for x in ["tmax", "tmin", "af", "rain", "sun", "tmean"]:
            df[x] = df[x].astype('float')
        df['mm'] = df['mm'].astype('int')
        df['season'] = df.apply(self.get_season, axis=1)
        df['date'] = pd.to_datetime(df.apply(
            lambda row: str(int(row.yyyy)) + "-" + str(int(row.mm)), axis=1))
        df.set_index('date', inplace=True)
        return df

    def _createStationDictionary(self):
        return {
            "Aberporth": self._loadStationData('aberporth'),
            "Armagh": self._loadStationData('armagh'),
            "Ballypatrick Forest": self._loadStationData('ballypatrickForest'),
            "Bradford": self._loadStationData('bradford'),
            "Braemar": self._loadStationData('braemar'),
            "Camborne": self._loadStationData('camborne'),
            "Cambridge NIAB": self._loadStationData('cambridgeNIAB'),
            "Cardiff Bute Park": self._loadStationData('cardiffButePark'),
            "Chivenor": self._loadStationData('chivenor'),
            "Cwmystwyth": self._loadStationData('cwmystwyth'),
            "Dunstaffnage": self._loadStationData('dunstaffnage'),
            "Durham": self._loadStationData('durham'),
            "Eastbourne": self._loadStationData('eastbourne'),
            "Eskdalemuir": self._loadStationData('eskdalemuir'),
            "Heathrow": self._loadStationData('heathrow'),
            "Hurn": self._loadStationData('hurn'),
            "Lerwick": self._loadStationData('lerwick'),
            "Leuchars": self._loadStationData('leuchars'),
            "Lowestoft": self._loadStationData('lowestoft'),
            "Manston": self._loadStationData('manston'),
            "Nairn": self._loadStationData('nairn'),
            "Newton Rigg": self._loadStationData('newtonRigg'),
            "Oxford": self._loadStationData('oxford'),
            "Paisley": self._loadStationData('paisley'),
            "Ringway": self._loadStationData('ringway'),
            "Ross-On-Wye": self._loadStationData('rossOnWye'),
            "Shawbury": self._loadStationData('shawbury'),
            "Sheffield": self._loadStationData('sheffield'),
            "Southampton": self._loadStationData('southampton'),
            "Stornoway": self._loadStationData('stornoway'),
            "Sutton Bonington": self._loadStationData('suttonBonington'),
            "Tiree": self._loadStationData('tiree'),
            "Valley": self._loadStationData('valley'),
            "Waddington": self._loadStationData('waddington'),
            "Whitby": self._loadStationData('whitby'),
            "Wick Airport": self._loadStationData('wickAirport'),
            "Yeovilton": self._loadStationData('yeovilton')
        }

    def __init__(self):
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                       "Sep", "Oct", "Nov", "Dec"]
        self.seasons = ["Spring", "Summer", "Autumn", "Winter"]
        self._stations = self._createStationDictionary()
        self._countryStationsMap = {
            "Scotland": ["Braemar", "Dunstaffnage", "Eskdalemuir", "Lerwick",
                         "Leuchars", "Nairn", "Paisley", "Stornoway", "Tiree",
                         "Wick Airport"],
            "England": ["Bradford", "Camborne", "Cambridge NIAB", "Chivenor",
                        "Durham", "Eastbourne", "Heathrow", "Hurn",
                        "Lowestoft", "Manston", "Newton Rigg", "Oxford",
                        "Ringway", "Shawbury", "Sheffield", "Southampton",
                        "Sutton Bonington", "Waddington", "Whitby",
                        "Yeovilton"],
            "Wales": ["Aberporth", "Cardiff Bute Park", "Cwmystwyth",
                      "Ross-On-Wye", "Valley"],
            "Northern Ireland": ["Armagh", "Ballypatrick Forest"]
        }
        self._dataTypes = {
            "Max Temp": "tmax",
            "Min Temp": "tmin",
            "Mean Temp": "tmean",
            "Rainfall": "rain",
            "Air Frost Days": "af",
            "Sun Hours": "sun"
            }
        self._operations = {
            "Highest": max,
            "Lowest": min,
            "Mean Average": nanmean,
            "Standard Deviation": nanstd
            }

    def getAvailableYearsForRegion(self, regionName, data_type):
        if regionName == "UK":
            years = [self.getAvailableYearsForRegion(x, data_type) for x in
                     self._countryStationsMap.keys()]
            return sorted(set([item for sublist in years for item in sublist]))
        elif regionName in self._countryStationsMap.keys():
            years = [self.getAvailableYearsForRegion(x, data_type) for x in
                     self._countryStationsMap.get(regionName)]
            return sorted(set([item for sublist in years for item in sublist]))
        else:
            df = self._stations.get(regionName)
            val = self._dataTypes.get(data_type)
            return sorted(list(set(df[
                df[val].notnull()].loc[:, 'yyyy'].tolist())))

    def values_by_month(self, df, value):
        '''
        Return a Pandas Series
        '''
        return df[value].fillna(method='ffill')

    def values_by_specified_month(self, df, value, month):
        month = self.months.index(month) + 1
        return df[['yyyy', 'mm', value]].loc[df['mm'] == month].fillna(method='ffill').groupby(
            ['yyyy'])[value].apply(list)

    def values_by_annual_month_range(self, df, value, month_range):
        return df.loc[df['mm'].isin(month_range)].fillna(method='ffill').groupby(
            ['yyyy'])[value].apply(list)

    def values_by_season(self, df, value, includeSeasonName=False):
        temp = df.copy()
        temp['date'] = temp.index
        temp['marker'] = (temp['season'] != temp['season'].shift()).cumsum()
        temp = temp.fillna(method='ffill').groupby('marker').agg({'date': 'first',  'season': 'first',
                                           value: lambda x: list(x)})
        if includeSeasonName:
            return temp.set_index('date').iloc[1:-1]
        else:
            return temp.set_index('date').iloc[1:-1][value]

    def values_by_specified_season(self, df, value, season):
        temp = self.values_by_season(df, value, includeSeasonName=True)
        return temp.loc[temp['season'] == season][value]

    def values_by_year(self, df, value):
        return df.fillna(method='ffill').groupby('yyyy')[value].apply(list)

    def values_by_decade(self, df, value):
        return df.fillna(method='ffill').groupby((df.index.year//10)*10)[value].apply(list)

    def get_table_for_country(self, country, value):
        countryStations = pd.concat(
            [self.get_table(x, value) for x in
             self._countryStationsMap.get(country)])[['yyyy',
                                                      'mm', 'season', value]]
        # From - https://stackoverflow.com/questions/17141558/
        # how-to-sort-a-dataframe-in-python-pandas-by-two-or-more-columns
        return countryStations.sort_values(['yyyy', 'mm'],
                                           ascending=[True, True])

    def get_table_for_uk(self, value):
        ukStations = pd.concat([self.get_table(x, value) for x in
                                self._stations.keys()])
        return ukStations.sort_values(['yyyy', 'mm'], ascending=[True, True])

    def get_table(self, region, value):
        if region == "UK":
            return self.get_table_for_uk(value)
        elif region in self._countryStationsMap:
            return self.get_table_for_country(region, value)
        else:
            return self._stations.get(region)[['yyyy', 'mm', 'season', value]]

    def get_values(self, region, datatype, start, end, step, operation,
                   month_range=None):
        data = self._dataTypes.get(datatype)
        df = self.get_table(region, data).loc[start:end]
        op = self._operations.get(operation)
        print "df", df
        if step == "Month":
            return self.values_by_month(df, data)
        elif step == "Season":
            return self.values_by_season(df, data).apply(op)
        elif step == "Full Year":
            return self.values_by_year(df, data).apply(op)
        elif step == "Decade":
            return self.values_by_decade(df, data).apply(op)
        elif step.replace(" Annually", '') in self.months:
            return self.values_by_specified_month(
                df, data, step.replace(" Annually", '')).apply(op)
        elif step.replace(" Annually", '')in self.seasons:
            return self.values_by_specified_season(
                df, data, step.replace(" Annually", '')).apply(op)
        else:  # Custom Month Range
            return self.values_by_annual_month_range(
                df, data, month_range).apply(op)

    def getDataTypes(self):
        return sorted(self._dataTypes.keys())

    def getRegionNames(self):
        regions = [[x] + sorted(self._countryStationsMap.get(x))
                   for x in sorted(self._countryStationsMap.keys())]
        return ['UK'] + [item for sublist in regions for item in sublist]

    def getPossibleOperations(self):
        return sorted(self._operations.keys())
