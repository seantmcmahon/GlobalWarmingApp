'''
Created on 24 Feb 2018

@author: seantmcmahon
'''
import os
import kivy
kivy.require('1.9.1')

from kivy.lang import Builder 
from kivy.app import App
from kivy.uix.screenmanager import Screen

from analyser import Analyser

Builder.load_file('analysingScreen.kv')

class AnalysingScreen(Screen):  
    
    def __init__(self, **kwargs):
        self.dao = App.get_running_app().DAO 
        self.regions = self.dao.getRegionNames()
        self.analyser = Analyser(self.dao)
        self.path = os.path.abspath(os.path.dirname(__file__))
        super(AnalysingScreen, self).__init__()  
        
    def start_analysis(self): 
        params = {"region" : self.screen_manager.selection.layout.region.text, "data_type": self.screen_manager.selection.layout.data_type.text}
        self.analyser.analyse_data(params, 500, 250)