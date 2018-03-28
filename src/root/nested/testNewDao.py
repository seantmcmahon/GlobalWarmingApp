'''
Created on 26 Feb 2018

@author: seantmcmahon
'''
import unittest
import pandas as pd
from newDao import Dao
import testConstants


class TestsDao(unittest.TestCase):
    longMessage = True

    def setUp(self):
        self.dao = Dao()

    def tearDown(self):
        self.dao = None

    def testLoadStation_Valid(self):
        self.assertIsNotNone(self.dao._loadStationData("aberporth"))

    def testLoadStation_Invalid(self):
        with self.assertRaises(IOError):
            self.dao._loadStationData("tireeeee")

    def testCreateStationDictionary(self):
        self.assertEquals(len(self.dao._createStationDictionary().keys()), 37)

    def testCountriesDictionaryStationAmount(self):
        countries = ["Scotland", "England", "Wales", "Northern Ireland"]
        stationslist = [self.dao._countryStationsMap.get(x) for x in countries]
        self.assertEquals(len(
            [item for sublist in stationslist for item in sublist]), 37)

    def testGetRegionNames(self):
        self.assertEquals(len(self.dao.getRegionNames()), 42)

    def test_values_by_month(self):
        expectedValues = [("Aberporth", "rain", [74.7])]
        for x in expectedValues:
            self.assertEqual(self.dao.values_by_month(self.dao._stations.get(
                x[0]).head(30), x[1]).iloc[0], x[2])

    def test_values_by_specified_month(self):
        self.assertEqual(self.dao.values_by_specified_month(
            self.dao._stations.get("Aberporth").head(30),
            "rain", "Mar").iloc[0], [76.2])

    def test_values_by_annual_month_range(self):
        self.assertEquals(self.dao.values_by_annual_month_range(
            self.dao._stations.get("Aberporth").head(30),
            "rain", [3, 4, 5, 6]).iloc[0], [76.2, 33.7, 51.3, 25.7])

    def test_values_by_season(self):
        self.assertEquals(self.dao.values_by_season(
            self.dao._stations.get("Aberporth"),
            "rain").iloc[0], [76.2, 33.7, 51.3])

    def test_values_by_specified_season(self):
        self.assertEqual(self.dao.values_by_specified_season(
            self.dao._stations.get("Aberporth"),
            "rain", "Summer").iloc[0], [25.7, 53.9, 91.8])

    def test_values_by_year(self):
        self.assertEquals(self.dao.values_by_year(
            self.dao._stations.get("Aberporth").head(36),
            "rain").iloc[0], [74.7, 69.1, 76.2, 33.7, 51.3, 25.7,
                              53.9, 91.8, 25.5, 106.2, 92.3, 86.5])

    def get_table_for_uk(self):
        self.assertAlmostEquals(
            self.dao.get_table_for_uk(
                "rain", sum)["rain"].tolist()[0], 120.1)
        self.assertAlmostEquals(
            self.dao.get_table_for_uk(
                "rain", sum)["rain"].tolist()[-1], 1950)

    def test_get_values(self):
        self.assertEqual(self.dao.get_values(
            "Aberporth", "Rainfall", '1941', '1942', "Full Year", "Highest",
            month_range=None).iloc[0], 106.2)

    def test_get_data_types(self):
        self.assertEqual(sorted(self.dao.getDataTypes()),
                         sorted(["Max Temp", "Min Temp", "Mean Temp", "Rainfall", "Air Frost Days", "Sun Hours"]))

    def test_get_operations(self):
        self.assertEqual(sorted(self.dao.getPossibleOperations()),
                         sorted(["Highest", "Lowest", "Mean Average", "Standard Deviation"]))


"""Following code is adated from tutorial on https://
eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases"""


def make_test_years_for_region_and_data(description, region, data, index, expectedValue):
    def test(self):
        years = self.dao.getAvailableYearsForRegion(region, data)
        self.assertEquals(years[index], expectedValue, description)
    return test


def make_test_get_table_for_country(description, region, data, index, expectedValue):
    def test(self):
        df = self.dao.get_table_for_country(region, data)
        groupedResults = df.groupby(df.index)[data].apply(list)
        self.assertEquals(sorted(groupedResults.iloc[index]), sorted(expectedValue))
    return test


def make_test_get_season(description, month, expectedValue):
    def test(self):
        series = pd.Series([month], index=['mm'])
        self.assertEquals(self.dao.get_season(series), expectedValue)
    return test


testYearsMap = testConstants.getYearsForRegionAndDataTypeMap
for name, params in testYearsMap.iteritems():
    test_func = make_test_years_for_region_and_data(name, params[0], params[1], params[2], params[3])
    setattr(TestsDao, 'testGetAvailableYearsForRegion_{0}'.format(name), test_func)


testTableForCountryMap = testConstants.getTableForCountryMap
for name, params in testTableForCountryMap.iteritems():
    test_func = make_test_get_table_for_country(name, params[0], params[1], params[2], params[3])
    setattr(TestsDao, 'test_get_table_for_country_{0}'.format(name), test_func)


testGetSeasonMap = testConstants.getSeasonMap
for name, params in testGetSeasonMap.iteritems():
    test_func = make_test_get_season(name, params[0], params[1])
    setattr(TestsDao, 'test_get_season_{0}'.format(name), test_func)
