'''
Created on 26 Dec 2017

@author: seantmcmahon
'''
import kivy
from pygments.lexers import graph
kivy.require('1.9.1')

from kivy.lang import Builder 
from kivy.app import App
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

Builder.load_file('visualisationScreen.kv')

class VisualisationScreen(Screen):  
    
    def __init__(self, **kwargs):
        self.dao = App.get_running_app().DAO 
        self.regions = self.dao.getRegionNames()
        self.unchecked_colour = [0.7, 0, 0, 1]
        self.checked_colour = [0, 0.7, 0, 1]
        super(VisualisationScreen, self).__init__()
      
    def updateStartYearSpinner(self):
        region = self.screen_manager.selection.layout.region.text
        data_type = self.screen_manager.selection.layout.data_type.text
        if region != '<Region>' and data_type != '<Data>':
            self.screen_manager.selection.layout.start_year.text = 'Year'
            self.screen_manager.selection.layout.start_year.disabled = False
            self.screen_manager.selection.layout.start_year.values = self.dao.getAvailableYearsForRegion(region, data_type)
    
    def updateEndYearSpinner(self):
        region = self.screen_manager.selection.layout.region.text
        data_type = self.screen_manager.selection.layout.data_type.text
        self.screen_manager.selection.layout.end_year.text = 'Year'
        self.screen_manager.selection.layout.end_year.disabled = False
        self.screen_manager.selection.layout.end_year.values = self.dao.getAvailableYearsForRegion(region, data_type)
        
    def updatePossibleTimeSteps(self):
        full_selection = ['Month', 'Season', 'Entire Year', 'Jan Annually', 'Feb Annually', 'Mar Annually', 'Apr Annually', 
                          'May Annually', 'Jun Annually', 'Jul Annually', 'Aug Annually', 'Sep Annually', 'Oct Annually', 
                          'Nov Annually', 'Dec Annually', 'Spring (Mar - May) Anually', 'Summer (Jun - Aug) Anually', 
                          'Autumn (Sep - Nov) Anually', 'Winter (Dec - Feb) Anually', 'Custom Months Annually']
        start_year = self.screen_manager.selection.layout.start_year.text
        end_year = self.screen_manager.selection.layout.end_year.text
        self.screen_manager.selection.layout.time_step.disabled = False
        if start_year == end_year:
            self.screen_manager.selection.layout.time_step.values = ["Month", "Season"]
            self.screen_manager.selection.layout.time_step.text = '<Time Step>'
            self.screen_manager.selection.layout.interval_step_range_start.text = '<Month>'
            self.screen_manager.selection.layout.interval_step_range_end.text = '<Month>'
        else:
            self.screen_manager.selection.layout.time_step.values = full_selection
        
    def timeStepSelected(self, *args):
        if args[1] == "Custom Months Annually":
            self.screen_manager.selection.layout.interval_step_range_start.disabled = False
            self.screen_manager.selection.layout.interval_step_range_end.disabled = False
        else:
            self.screen_manager.selection.layout.interval_step_range_start.disabled = True
            self.screen_manager.selection.layout.interval_step_range_end.disabled = True
    
    def second_graph_toggled(self):   
        if self.screen_manager.selection.layout.second_graph.state == 'down':
            self.screen_manager.selection.layout.second_graph.background_color = self.checked_colour
            self.screen_manager.selection.layout.second_graph.text = unichr(8730)
        else:
            self.screen_manager.selection.layout.second_graph.background_color = self.unchecked_colour
            self.screen_manager.selection.layout.second_graph.text = 'x'
            
            
    def create_graph(self):
        details = {}
        graph_type = self.screen_manager.selection.layout.graph_type.text
        details['graph_type'] = graph_type
        if graph_type != "Weather Graph" :
            details['data_type'] = self.screen_manager.selection.layout.data_type.text
        details["region"] = self.screen_manager.selection.layout.region.text
        details["start_year"] = self.screen_manager.selection.layout.start_year.text
        details["end_year"] = self.screen_manager.selection.layout.end_year.text
        details["time_step"] = self.screen_manager.selection.layout.time_step.text
        if self.screen_manager.selection.layout.time_step.text == "Custom Months Annually":
            details["interval_start"] = self.screen_manager.selection.layout.interval_step_range_start.text
            details["interval_end"] = self.screen_manager.selection.layout.interval_step_range_end.text
        
        self.dao.create_graph(details, Window.size[0], Window.size[1])
        self.screen_manager.display.display_layout.graph.source = 'imgs/graph.png'
        self.screen_manager.current = "display"
