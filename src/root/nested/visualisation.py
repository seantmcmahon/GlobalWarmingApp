'''
Created on 26 Dec 2017

@author: seantmcmahon
'''
import kivy
kivy.require('1.9.1')

from kivy.lang import Builder 
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

Builder.load_file('visualisationScreen.kv')

class DataSelectScreen(Screen):
    
    def __init__(self, **kwargs):
        self.dao = App.get_running_app().DAO 
        self.regions = self.dao.getRegionNames()
        self.unchecked_colour = [0.7, 0, 0, 1]
        self.checked_colour = [0, 0.7, 0, 1]
        super(DataSelectScreen, self).__init__()
        
    def updateStartYearSpinner(self, *args):
        self.layout.start_year.text = 'Year'
        self.layout.start_year.disabled = False
        self.layout.start_year.values = self.dao.getAvailableYearsForRegion(args[1])
        
    def updateStartMonthSpinner(self, *args):
        self.layout.start_month.text = 'Month'
        self.layout.start_month.disabled = False
        self.layout.start_month.values = self.dao.getAvailableMonthsForRegion(self.layout.region.text, args[1])
        
    def updateEndYearSpinner(self):
        self.layout.end_year.text = 'Year'
        self.layout.end_year.disabled = False
        self.layout.end_year.values = self.dao.getAvailableYearsForRegion(self.layout.region.text)
        
    def updateEndMonthSpinner(self, *args):
        self.layout.end_month.text = 'Month'
        self.layout.end_month.disabled = False
        self.layout.end_month.values = self.dao.getAvailableMonthsForRegion(self.layout.region.text, args[1])
        
    def timeStepSelected(self, *args):
        if args[1] == "Custom Months Annually":
            self.layout.interval_step_range_start.disabled = False
            self.layout.interval_step_range_end.disabled = False
        else:
            self.layout.interval_step_range_start.disabled = True
            self.layout.interval_step_range_end.disabled = True
    
    def second_graph_toggled(self):   
        if self.layout.second_graph.state == 'down':
            self.layout.second_graph.background_color = self.checked_colour
            self.layout.second_graph.text = unichr(8730)
        else:
            self.layout.second_graph.background_color = self.unchecked_colour
            self.layout.second_graph.text = 'x'
            
    def create_graph(self):
        print("here")
        #details = { "graph_type" : self.layout.graph_type.text,
         #           "region" : self.layout.region.text,    
          #          "start_year" : self.layout.start_year.text,
           #         "start_month" : self.layout.start_month.text,
            #        "end_year" :self.layout.end_year.text,
             #       "end_month" : self.layout.end_month.text,
              #      "time_step" : self.layout.time_step.text,
               #     "interval_start" : self.layout.interval_step_range_start.text,
                #    "interval_end" : self.layout.interval_step_range_end.text
        #}
        self.dao.create_graph({}, Window.size[0], Window.size[1])

class DataViewScreen(Screen):
    pass

class VisualisationScreen(Screen):
    def create_graph(self):
        print("click")
        self.screen_manager.selection.create_graph()
        self.screen_manager.display.layout.graph.source = 'imgs/graph.png'
        self.screen_manager.current = "display"

