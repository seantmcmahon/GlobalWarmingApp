'''
Created on 23 Mar 2018

@author: seantmcmahon
'''

getYearsForRegionAndDataTypeMap = {
    "AberporthMaxTempStart": ('Aberporth', "Max Temp", 0, '1942'),
    "AberporthMaxTempEnd": ('Aberporth', "Max Temp", -1, '2016'),
    "AberporthMinTempStart": ('Aberporth', "Min Temp", 0, '1942'),
    "AberporthMinTempEnd": ('Aberporth', "Min Temp", -1, '2016'),
    "AberporthMeanTempStart": ('Aberporth', "Mean Temp", 0, '1942'),
    "AberporthMeanTempEnd": ('Aberporth', "Mean Temp", -1, '2016'),
    "AberporthAirFrostStart": ('Aberporth', "Air Frost Days", 0, '1957'),
    "AberporthAirFrostEnd": ('Aberporth', "Air Frost Days", -1, '2016'),
    "AberporthRainfallStart": ('Aberporth', "Rainfall", 0, '1941'),
    "AberporthRainfallEnd": ('Aberporth', "Rainfall", -1, '2016'),
    "AberporthSunStart": ('Aberporth', "Sun Hours", 0, '1942'),
    "AberporthSunEnd": ('Aberporth', "Sun Hours", -1, '2016'),
    "ScotlandMaxTempStart": ('Scotland', "Max Temp", 0, '1873'),
    "ScotlandMaxTempEnd": ('Scotland', "Max Temp", -1, '2016'),
    "EnglandMinTempStart": ('England', "Min Temp", 0, '1853'),
    "EnglandMinTempEnd": ('England', "Min Temp", -1, '2016'),
    "EnglandMeanTempStart": ('England', "Mean Temp", 0, '1853'),
    "EnglandMeanTempEnd": ('England', "Mean Temp", -1, '2016'),
    "WalesAirFrostStart": ('Wales', "Air Frost Days", 0, '1930'),
    "WalesAirFrostEnd": ('Wales', "Air Frost Days", -1, '2016'),
    "NorthernIrelendRainfallStart": ('Northern Ireland', "Rainfall", 0, '1853'),
    "NorthernIrelendRainfallEnd": ('Northern Ireland', "Rainfall", -1, '2016'),
    "NorthernIrelendSunStart": ('Northern Ireland', "Sun Hours", 0, '1929'),
    "NorthernIrelendSunEnd": ('Northern Ireland', "Sun Hours", -1, '2016'),
    "UKMaxTempStart": ('UK', "Max Temp", 0, '1853'),
    "UKMaxTempEnd": ('UK', "Max Temp", -1, '2016'),
    "UKMinTempStart": ('UK', "Min Temp", 0, '1853'),
    "UKMinTempEnd": ('UK', "Min Temp", -1, '2016'),
    "UKMeanTempStart": ('UK', "Mean Temp", 0, '1853'),
    "UKMeanTempEnd": ('UK', "Mean Temp", -1, '2016'),
    "UKAirFrostStart": ('UK', "Air Frost Days", 0, '1853'),
    "UKAirFrostEnd": ('UK', "Air Frost Days", -1, '2016'),
    "UKRainfallStart": ('UK', "Rainfall", 0, '1853'),
    "UKRainfallEnd": ('UK', "Rainfall", -1, '2016'),
    "UKSunStart": ('UK', "Sun Hours", 0, '1890'),
    "UKMaxSunEnd": ('UK', "Sun Hours", -1, '2016')
    }

getTableForCountryMap = {
    "NorthernIrelandRainStart": ("Northern Ireland", "rain", 0, [57.3]),
    "NorthernIrelandRainEnd": ("Northern Ireland", "rain", -1, [51.4, 80.0])
    }

getSeasonMap = {
    "January": (1, "Winter"),
    "February": (2, "Winter"),
    "March": (3, "Spring"),
    "April": (4, "Spring"),
    "May": (5, "Spring"),
    "June": (6, "Summer"),
    "July": (7, "Summer"),
    "August": (8, "Summer"),
    "September": (9, "Autumn"),
    "October": (10, "Autumn"),
    "November": (11, "Autumn"),
    "December": (12, "Winter")
    }
