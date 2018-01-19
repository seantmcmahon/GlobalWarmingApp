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
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Air Frost")[0], '1957')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Air Frost")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Total Rainfall")[0], '1941')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Total Rainfall")[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Sun hours")[0], '1942')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth', "Sun hours")[-1], '2016')
        
    """def testGetAvailableYearsForRegion_Country(self):
        self.assertEquals(self.dao.getAvailableYearsForRegion('Scotland')[0], '1873')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Scotland')[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('England')[0], '1853')
        self.assertEquals(self.dao.getAvailableYearsForRegion('England')[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Wales')[0], '1930')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Wales')[-1], '2016')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Northern Ireland')[0], '1853')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Northern Ireland')[-1], '2016')
        
    def testGetAvailableYearsForRegion_UK(self):
        self.assertEquals(self.dao.getAvailableYearsForRegion('UK')[0], '1853')
        self.assertEquals(self.dao.getAvailableYearsForRegion('UK')[-1], '2016')
    
    def test_create_graph(self):
        #self.dao.create_graph({}, 500, 250)
        pass"""

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()