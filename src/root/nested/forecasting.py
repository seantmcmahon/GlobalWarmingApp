'''
Created on 3 Feb 2018

@author: seantmcmahon
'''
import os
from predictor import Predictor
import kivy
kivy.require('1.9.1')

from kivy.lang import Builder 
from kivy.app import App
from kivy.uix.screenmanager import Screen

Builder.load_file('forecastingScreen.kv')


class ForecastingScreen(Screen):

    def __init__(self, **kwargs):
        self.dao = App.get_running_app().DAO
        self.regions = self.dao.getRegionNames()
        self.predictor = Predictor(self.dao)
        self.path = os.path.abspath(os.path.dirname(__file__))
        super(ForecastingScreen, self).__init__()
        self.layout = self.screen_manager.selection.layout
        self.display = self.screen_manager.display.display_layout

    def timeStepSelected(self, *args):
        if args[1] == "Custom Months Annually":
            self.layout.interval_step_range_start.disabled = False
            self.layout.interval_step_range_end.disabled = False
        else:
            self.layout.interval_step_range_start.disabled = True
            self.layout.interval_step_range_end.disabled = True

    def predict_data(self):
        details = {}
        # graph_type = self.screen_manager.selection.layout.graph_type.text
        # details['graph_type'] = graph_type
        # if graph_type != "Weather Graph" :
        details['data_type'] = self.layout.data_type.text
        details["region"] = self.layout.region.text
        details["prediction_type"] = self.layout.prediction_type.text
        details["time_step"] = self.layout.time_step.text
        if self.layout.time_step.text == "Custom Months Annually":
            start = self.layout.interval_step_range_start.text
            end = self.layout.interval_step_range_end.text
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
                      "Aug", "Sep", "Oct", "Nov", "Dec"]
            details["month_range"] = range(int(months.index(start))+1,
                                           int(months.index(end))+2)
        self.predictor.plot_predictions(details, 500, 250)
        self.display.graph.source = ''
        self.display.graph.reload()
        self.display.graph.source = self.path + "/imgs/newModel.png"
        self.display.graph.reload()
        self.screen_manager.current = "display"
