'''
Created on 13 Mar 2018

@author: seantmcmahon
'''
import unittest
from newDao import Dao
from predictor import Predictor


class Test(unittest.TestCase):

    def setUp(self):
        dao = Dao()
        self.predictor = Predictor(dao)

    def tearDown(self):
        self.predictor = None

    def testARIMA(self):
        pass

    def testGetBestFitModel(self):
        pass

    def testPredict(self):
        pass

    def testGetForecast(self):
        pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
