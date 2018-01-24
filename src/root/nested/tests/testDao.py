'''
Created on 9 Jan 2018

@author: seantmcmahon
'''
import unittest
import itertools
import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('../')
from dao import Dao

class TestDao(unittest.TestCase):

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
        self.assertEquals(len(list(itertools.chain.from_iterable([self.dao._countryStationsMap.get(x) for x in ["Scotland", "England", "Wales", "Northern Ireland"]]))), 37)
          
    def testGetRegionNames(self):
        self.assertEquals(len(self.dao.getRegionNames()), 42)
        
    def testGetAvailableYearsForRegion_SingleStation(self):
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Max Temp")[0], '1942')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Max Temp")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Min Temp")[0], '1942')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Min Temp")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Air Frost Days")[0], '1957')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Air Frost Days")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Total Rainfall")[0], '1941')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Total Rainfall")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Sun hours")[0], '1942')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Sun hours")[-1], '2016')
        
    def testGetAvailableYearsForRegion_Country(self):
        self.assertEquals(self.dao.getAvailableYearsForRegion('Scotland', "Max Temp")[0], '1873')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Scotland', "Max Temp")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('England', "Min Temp")[0], '1853')
        self.assertEquals(self.dao.getAvailableYearsForRegion('England', "Min Temp")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Wales', "Air Frost Days")[0], '1930')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Wales', "Air Frost Days")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Northern Ireland', "Sun Hours")[0], '1929')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Northern Ireland', "Sun Hours")[-1], '2016')
        
    def testGetAvailableYearsForRegion_UK(self):
        self.assertEquals(self.dao.getAvailableYearsForRegion('UK', "Max Temp")[0], '1853')
        self.assertEquals(self.dao.getAvailableYearsForRegion('UK', "Max Temp")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('UK', "Min Temp")[0], '1853')
        self.assertEquals(self.dao.getAvailableYearsForRegion('UK', "Min Temp")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('UK', "Air Frost Days")[0], '1853')
        self.assertEquals(self.dao.getAvailableYearsForRegion('UK', "Air Frost Days")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('UK', "Total Rainfall")[0], '1853')
        self.assertEquals(self.dao.getAvailableYearsForRegion('UK', "Total Rainfall")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('UK', "Sun hours")[0], '1890')
        self.assertEquals(self.dao.getAvailableYearsForRegion('UK', "Sun hours")[-1], '2016')
        
    def test_prepare_values_for_display(self):
        self.assertEquals(self.dao.prepare_values_for_display(["118.6*", "173.8"]), [118.6, 173.8])
        
    def test_get_avg_temps(self):
        temps = [('5.0', '-1.4'),('7.3', '1.9'),('6.2', '0.3'),('8.6', '2.1'),('15.8', '7.7'),
                 ('17.7', '8.7'),('18.9', '11.0'),('17.5', '9.7'),('16.3', '8.4'),
                 ('14.6', '8.0'),('9.6', '3.4'),('5.8', '0.0')]
        self.assertEquals(self.dao.get_avg_temps(temps), [1.8, 4.6, 3.25, 5.35, 11.75, 13.2, 14.95, 13.6, 12.35, 11.3, 6.5, 2.9])

    def test_total_values_by_year(self):
        self.assertEquals(self.dao.total_values_by_year(self.dao._stations.get("Aberporth").head(36), "rain")["rain"].tolist(), [786.9, 962.0, 992.5])
     
    def test_get_combined_table_for_country(self):
        self.assertAlmostEquals(self.dao.get_combined_table_for_country("Northern Ireland", "rain")["rain"].tolist()[0], 57.3)
        self.assertAlmostEquals(self.dao.get_combined_table_for_country("Northern Ireland", "rain")["rain"].tolist()[-1], 131.4)
        
    def test_get_combined_table_for_uk(self):
        self.assertAlmostEquals(self.dao.get_combined_table_for_uk("rain")["rain"].tolist()[0], 120.1)
        self.assertAlmostEquals(self.dao.get_combined_table_for_uk("rain")["rain"].tolist()[-1], 1950)
      
    #def test_group_values_by_season(self):
    #    self.assertEquals(self.dao.group_values_by_season(self.dao._stations.get("Aberporth")[['yyyy', 'mm', 'rain']], 'rain'), [("1941-Winter", 71.9), ("1941-Spring", 53.7333333), ("1941-Summer", 57.1333333), ("1941-Autumn", 74.6666667)])

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()