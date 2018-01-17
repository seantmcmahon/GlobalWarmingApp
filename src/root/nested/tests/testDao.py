'''
Created on 9 Jan 2018

@author: seantmcmahon
'''
import unittest
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
        
    def testGetRegionNames(self):
        self.assertEquals(len(self.dao.getRegionNames()), 42)
        
    def testGetAvailableYearsForRegion_SingleStation(self):
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth')[0], '1941')
        self.assertEquals(self.dao.getAvailableYearsForRegion('Aberporth')[-1], '2016')
        
    def testGetAvailableYearsForRegion_Country(self):
        pass
        
    def testGetAvailableYearsForRegion_UK(self):
        pass
    
    def testGetAvailableMonthsForRegion_SingleStation(self):
        self.assertEquals(self.dao.getAvailableMonthsForRegion('Aberporth', '1941')[0], 'Jan')
        self.assertEquals(self.dao.getAvailableMonthsForRegion('Aberporth', '1941')[-1], 'Dec')
        
    def testGetAvailableMonthsForRegion_Country(self):
        pass
        
    def testGetAvailableMonthsForRegion_UK(self):
        pass 
    
    def test_create_graph(self):
        self.dao.create_graph({})

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()