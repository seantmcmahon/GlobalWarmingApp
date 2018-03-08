'''
Created on 24 Feb 2018

@author: seantmcmahon
'''
import os
from analyser import Analyser
from newDao import Dao
import kivy
kivy.require('1.9.1')

from kivy.properties import StringProperty, ListProperty
from kivy.lang import Builder 
from kivy.app import App
from kivy.uix.screenmanager import Screen

Builder.load_file('analysingScreen.kv')


class AnalysingScreen(Screen):
    graphName = StringProperty()
    results_text = StringProperty()
    data_types = ListProperty()

    def __init__(self, **kwargs):
        self.dao = Dao()
        self.regions = self.dao.getRegionNames()
        self.analyser = Analyser(self.dao)
        self.path = os.path.abspath(os.path.dirname(__file__))
        super(AnalysingScreen, self).__init__()
        self.graphName = ''
        self.results_text = ''
        self.data_types = self.dao.getDataTypes()

    def start_analysis(self):
        greatest, smallest, meanRes, stdDevRes = self.analyser.analyse_data(
            self.screen_manager.selection.layout.region.text,
            self.screen_manager.selection.layout.data_type.text, 500, 250)
        self.graphName = ''
        self.screen_manager.display.display_layout.graph.reload()
        self.graphName = self.path + '/imgs/globWarmResults.png'
        self.screen_manager.display.display_layout.graph.reload()
        self.results_text =\
            "\n\n" + greatest + "\n\n" + smallest + "\n\n" + meanRes + "\n\n" + stdDevRes
        self.screen_manager.current = "display"
