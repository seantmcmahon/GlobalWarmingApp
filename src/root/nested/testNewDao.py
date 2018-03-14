'''
Created on 26 Feb 2018

@author: seantmcmahon
'''
import unittest
from newDao import Dao


class Test(unittest.TestCase):

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

    def testGetAvailableYearsForRegion_SingleStation(self):
        vals = [('Aberporth', "Max Temp", 0, '1942'),
                ('Aberporth', "Max Temp", -1, '2016'),
                ('Aberporth', "Min Temp", 0, '1942'),
                ('Aberporth', "Min Temp", -1, '2016'),
                ('Aberporth', "Mean Temp", 0, '1942'),
                ('Aberporth', "Mean Temp", -1, '2016'),
                ('Aberporth', "Air Frost Days", 0, '1957'),
                ('Aberporth', "Air Frost Days", -1, '2016'),
                ('Aberporth', "Rainfall", 0, '1941'),
                ('Aberporth', "Rainfall", -1, '2016'),
                ('Aberporth', "Sun Hours", 0, '1942'),
                ('Aberporth', "Sun Hours", -1, '2016'),
                ('Scotland', "Max Temp", 0, '1873'),
                ('Scotland', "Max Temp", -1, '2016'),
                ('England', "Min Temp", 0, '1853'),
                ('England', "Min Temp", -1, '2016'),
                ('England', "Mean Temp", 0, '1853'),
                ('England', "Mean Temp", -1, '2016'),
                ('Wales', "Air Frost Days", 0, '1930'),
                ('Wales', "Air Frost Days", -1, '2016'),
                ('Northern Ireland', "Rainfall", 0, '1853'),
                ('Northern Ireland', "Rainfall", -1, '2016'),
                ('Northern Ireland', "Sun Hours", 0, '1929'),
                ('Northern Ireland', "Sun Hours", -1, '2016'),
                ('UK', "Max Temp", 0, '1853'),
                ('UK', "Max Temp", -1, '2016'),
                ('UK', "Min Temp", 0, '1853'),
                ('UK', "Min Temp", -1, '2016'),
                ('UK', "Mean Temp", 0, '1853'),
                ('UK', "Mean Temp", -1, '2016'),
                ('UK', "Air Frost Days", 0, '1853'),
                ('UK', "Air Frost Days", -1, '2016'),
                ('UK', "Rainfall", 0, '1853'),
                ('UK', "Rainfall", -1, '2016'),
                ('UK', "Sun Hours", 0, '1890'),
                ('UK', "Sun Hours", -1, '2016')]
        for x in vals:
            self.assertEquals(self.dao.getAvailableYearsForRegion(
                x[0], x[1])[x[2]], x[3])

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

    def test_get_table_for_country(self):
        testAndExpectedValues = [("Northern Ireland", "rain", 0, 57.3),
                                 ("Northern Ireland", "rain", -1, 131.4)]
        for x in testAndExpectedValues:
            self.assertAlmostEquals(self.dao.get_table_for_country(
                x[0], x[1])[x[1]].tolist()[x[2]], x[3])

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


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
