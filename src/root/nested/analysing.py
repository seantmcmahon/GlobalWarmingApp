'''
Created on 24 Feb 2018

@author: seantmcmahon
'''
import os
from analyser import Analyser
from newDao import Dao
import kivy
import constants
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty
kivy.require('1.9.1')

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
        self.error = Popup(title=constants.ERROR_LABEL, content=Label(
            text=constants.ERROR_MESSAGE), size_hint=(0.5, 0.5))

    def start_analysis(self):
        region = self.screen_manager.selection.layout.region.text
        data_type = self.screen_manager.selection.layout.data_type.text
        if constants.OPTION_HOLDER in [region, data_type]:
            self.error.open()
        else:
            greatest, smallest, meanRes, stdDevRes =\
                self.analyser.analyse_data(region, data_type, 500, 250)
            self.graphName = ''
            self.screen_manager.display.display_layout.graph.reload()
            self.graphName = self.path + '/imgs/globWarmResults.png'
            self.screen_manager.display.display_layout.graph.reload()
            self.results_text = greatest + "\n\n" + smallest\
                + "\n\n" + meanRes + "\n\n" + stdDevRes
            self.screen_manager.current = "display"
