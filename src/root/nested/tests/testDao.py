'''
Created on 9 Jan 2018

@author: seantmcmahon
'''
import unittest
import itertools
import sys
import numpy as np
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
           
    def test_average_two_columns(self):
        col1 = ['5.0','7.3','6.2','8.6','15.8','17.7','18.9','17.5','16.3','14.6','9.6','5.8']
        col2 = ['-1.4','1.9','0.3','2.1','7.7','8.7','11.0','9.7','8.4','8.0','3.4','0.0']
        expectedResults = [1.8, 4.6, 3.25, 5.35, 11.75, 13.2, 14.95, 13.6, 12.35, 11.3, 6.5, 2.9]
        actualResults = self.dao.average_two_columns(col1, col2)
        for x in range(len(expectedResults)):
            self.assertAlmostEquals(expectedResults[x], actualResults[x])

    def test_total_values_by_year(self):
        self.assertEquals(self.dao.total_values_by_year(self.dao._stations.get("Aberporth").head(36), "rain", sum)["rain"].tolist(), [786.9, 962.0, 992.5])
     
    def test_get_combined_table_for_country(self):
        self.assertAlmostEquals(self.dao.get_combined_table_for_country("Northern Ireland", "rain", sum)["rain"].tolist()[0], 57.3)
        self.assertAlmostEquals(self.dao.get_combined_table_for_country("Northern Ireland", "rain", sum)["rain"].tolist()[-1], 131.4)
        
    def test_get_combined_table_for_uk(self):
        self.assertAlmostEquals(self.dao.get_combined_table_for_uk("rain", sum)["rain"].tolist()[0], 120.1)
        self.assertAlmostEquals(self.dao.get_combined_table_for_uk("rain", sum)["rain"].tolist()[-1], 1950)
      
    def test_total_values_by_month(self):
        values = ["tmax", "tmin", "af", "rain", "sun"]
        for station in self.dao._stations.keys():
            for v in values:
                table = self.dao.get_table(station, v, None)
                for row in table[v].tolist():
                    try:
                        self.assertTrue(isinstance(row, float))
                    except AssertionError:
                        self.assertEquals(row, "---")
    
    def test_get_combined_table_for_country_all_float_or_NaN(self):
        values = ["tmax", "tmin", "af", "rain", "sun"]
        for country in self.dao._countryStationsMap.keys():
            for v in values:
                table = self.dao.get_table(country, v, max)
                for row in table[v].tolist():
                    try:
                        self.assertTrue(isinstance(row, float))
                    except AssertionError:
                        self.assertTrue(row in ["---", np.NaN])
    
    def test_get_combined_table_for_uk_all_float_or_NaN(self):
        values = ["tmax", "tmin", "af", "rain", "sun"]
        for v in values:
            table = self.dao.get_table("UK", v, max)
            for row in table[v].tolist():
                try:
                    self.assertTrue(isinstance(row, float))
                except AssertionError:
                    self.assertTrue(row in ["---", np.NaN])
                    
    def test_all_possible_graph_combinations(self):
        regions = self.dao.getRegionNames()
        data_types = ['Max Temp', 'Min Temp', 'Avg Max Temp', 'Avg Min Temp', 'Avg Temp', 'Total Rainfall', 'Avg Rainfall', 'Air Frost Days', 'Total Sun Hours', 'Avg Sun Hours']
        time_steps = ['Month', 'Season', 'Year', 'Jan Annually', 'Feb Annually', 'Mar Annually', 'Apr Annually', 
                          'May Annually', 'Jun Annually', 'Jul Annually', 'Aug Annually', 'Sep Annually', 'Oct Annually', 
                          'Nov Annually', 'Dec Annually', 'Spring (Mar - May) Annually', 'Summer (Jun - Aug) Annually', 
                          'Autumn (Sep - Nov) Annually', 'Winter (Dec - Feb) Annually', 'Custom Months Annually']
        numGraphs = 1
        for region in regions:
            for data_type in data_types:
                years = self.dao.getAvailableYearsForRegion(region, data_type)
                for i in years:
                    for j in years[years.index(i):]:
                        if i == j:
                            for time in ['Month', 'Season']:
                                try:
                                    details = {"data_type": data_type, "region": region, "start_year": i, "end_year": j, "time_step": time}
                                    self.dao.create_graph(details, 500, 250) 
                                    print numGraphs, "graphs made"
                                    numGraphs = numGraphs +1
                                except Exception as e:
                                    print e
                                    print region, data_type, i, j, time
                                    self.fail("Error raised unexpectedly")  
                        else:
                            for time in time_steps:
                                if time == 'Custom Months Annually':
                                    for a in range(0, 12):
                                        for b in range(a, 13):
                                            try:
                                                details = {"data_type": data_type, "region": region, "start_year": i, "end_year": j, "time_step": time, "month_range": range(a+1, b+2)}
                                                self.dao.create_graph(details, 500, 250)
                                                print numGraphs, "graphs made"
                                                numGraphs = numGraphs +1
                                            except Exception as e:
                                                print e
                                                print region, data_type, i, j, time, a, b
                                                self.fail("Error raised unexpectedly")
                                else:
                                    try:
                                        details = {"data_type": data_type, "region": region, "start_year": i, "end_year": j, "time_step": time}
                                        self.dao.create_graph(details, 500, 250)
                                        print numGraphs, "graphs made"
                                        numGraphs = numGraphs +1 
                                    except Exception as e:
                                        print e
                                        print region, data_type, i, j, time
                                        self.fail("Error raised unexpectedly")
            
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()