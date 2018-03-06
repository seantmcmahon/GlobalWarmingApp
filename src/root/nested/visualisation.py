'''
Created on 26 Dec 2017

@author: seantmcmahon
'''
import kivy
kivy.require('1.9.1')

from kivy.lang import Builder 
from kivy.app import App
from kivy.uix.screenmanager import Screen

Builder.load_file('visualisationScreen.kv')


class VisualisationScreen(Screen):

    def __init__(self, **kwargs):
        self.dao = App.get_running_app().DAO
        self.regions = self.dao.getRegionNames()
        self.unchecked_colour = [0.7, 0, 0, 1]
        self.checked_colour = [0, 0.7, 0, 1]
        super(VisualisationScreen, self).__init__()
        self.screenlayout = self.screen_manager.selection.layout
        self.display = self.screen_manager.display.display_layout

    def updateStartYearSpinner(self):
        region = self.screenlayout.region.text
        data_type = self.screenlayout.data_type.text
        if region != '<Region>' and data_type != '<Data>':
            self.screenlayout.start_year.text = 'Year'
            self.screenlayout.start_year.disabled = False
            self.screenlayout.start_year.values = self\
                .dao.getAvailableYearsForRegion(region, data_type)

    def updateEndYearSpinner(self):
        region = self.screenlayout.region.text
        data_type = self.screenlayout.data_type.text
        self.screenlayout.end_year.text = 'Year'
        self.screenlayout.end_year.disabled = False
        self.screenlayout.end_year.values = self\
            .dao.getAvailableYearsForRegion(region, data_type)

    def updatePossibleTimeSteps(self):
        full_selection = ['Month', 'Season', 'Year', 'Jan Annually',
                          'Feb Annually', 'Mar Annually', 'Apr Annually',
                          'May Annually', 'Jun Annually', 'Jul Annually',
                          'Aug Annually', 'Sep Annually', 'Oct Annually',
                          'Nov Annually', 'Dec Annually', 'Spring Annually',
                          'Summer Annually', 'Autumn Annually',
                          'Winter Annually', 'Custom Months Annually']
        start_year = self.screenlayout.start_year.text
        end_year = self.screenlayout.end_year.text
        self.screenlayout.time_step.disabled = False
        if start_year == end_year:
            self.screenlayout.time_step.values = ["Month", "Season"]
            self.screenlayout.time_step.text = '<Time Step>'
            self.screenlayout.interval_step_range_start.text = '<Month>'
            self.screenlayout.interval_step_range_end.text = '<Month>'
        else:
            self.screenlayout.time_step.values = full_selection

    def timeStepSelected(self, *args):
        if args[1] == "Custom Months Annually":
            self.screenlayout.interval_step_range_start.disabled = False
            self.screenlayout.interval_step_range_end.disabled = False
        else:
            self.screenlayout.interval_step_range_start.disabled = True
            self.screenlayout.interval_step_range_end.disabled = True

    def second_graph_toggled(self):
        if self.screenlayout.second_graph.state == 'down':
            self.screenlayout.second_graph.background_color = self.checked_colour
            self.screenlayout.second_graph.text = unichr(8730)
        else:
            self.screenlayout.second_graph.background_color = self.unchecked_colour
            self.screenlayout.second_graph.text = 'x'

    def create_graph(self):
        details = {}
        # graph_type = self.screen_manager.selection.layout.graph_type.text
        # details['graph_type'] = graph_type
        # if graph_type != "Weather Graph" :
        details['data_type'] = self.screenlayout.data_type.text
        details["region"] = self.screenlayout.region.text
        details["start_year"] = self.screenlayout.start_year.text
        details["end_year"] = self.screenlayout.end_year.text
        details["time_step"] = self.screenlayout.time_step.text
        if self.screenlayout.time_step.text == "Custom Months Annually":
            start = self.screenlayout.interval_step_range_start.text
            end = self.screenlayout.interval_step_range_end.text
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
                      "Aug", "Sep", "Oct", "Nov", "Dec"]
            details["month_range"] = range(int(months.index(start))+1,
                                           int(months.index(end))+2)

        self.dao.create_graph(details, 500, 250)
        self.display.graph.source = ''
        self.display.graph.reload()
        self.display.graph.source = 'imgs/graph.png'
        self.display.graph.reload()
        self.screen_manager.current = "display"
