'''
Created on 26 Dec 2017

@author: seantmcmahon
'''
import constants
from plotter import plotGraph
import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, BooleanProperty
from sklearn.gaussian_process.regression_models import constant
kivy.require('1.9.1')

Builder.load_file('visualisationScreen.kv')


class VisualisationScreen(Screen):
    data_types = ListProperty()
    start_year = ListProperty()
    end_year = ListProperty()
    month_range_start = ListProperty()
    month_range_end = ListProperty()
    image_source = StringProperty()

    def __init__(self, **kwargs):
        self.dao = App.get_running_app().DAO
        self.regions = self.dao.getRegionNames()
        self.unchecked_colour = [0.7, 0, 0, 1]
        self.checked_colour = [0, 0.7, 0, 1]
        super(VisualisationScreen, self).__init__()
        self.data_types = self.dao.getDataTypes()
        self.start_year = []
        self.end_year = []
        self.month_range_start = constants.MONTH_LIST
        self.month_range_end = constants.MONTH_LIST
        self.error = Popup(title=constants.ERROR_LABEL, content=Label(text=constants.ERROR_MESSAGE),
                          size_hint=(0.5, 0.5))

    def updateStartYearSpinner(self):
        region = self.screen_manager.selection.layout.region.text
        data_type = self.screen_manager.selection.layout.data_type.text
        if constants.OPTION_HOLDER not in [region, data_type]:
            self.screen_manager.selection.layout.start_year.text = constants.YEAR
            self.screen_manager.selection.layout.start_year.disabled = False
            self.start_year = self.dao.getAvailableYearsForRegion(region, data_type)

    def updateEndYearSpinner(self):
        try:
            region = self.screen_manager.selection.layout.region.text
            data_type = self.screen_manager.selection.layout.data_type.text
            self.screen_manager.selection.layout.end_year.text = constants.YEAR
            self.screen_manager.selection.layout.end_year.disabled = False
            start = self.screen_manager.selection.layout.start_year.text
            years = list(self.start_year)
            self.end_year = years[years.index(start):]
        except:
            self.end_year = years

    def updatePossibleTimeSteps(self):
        full_selection = constants.FULL_TIME_STEP_SELECTION
        start_year = self.screen_manager.selection.layout.start_year.text
        end_year = self.screen_manager.selection.layout.end_year.text
        self.screen_manager.selection.layout.time_step.disabled = False
        if start_year == end_year:
            self.screen_manager.selection.layout.time_step.values = constants.MONTH_SEASON_TIME_STEP_SELECTION
            self.screen_manager.selection.layout.time_step.text = constants.OPTION_HOLDER
            self.screen_manager.selection.layout.interval_step_range_start.text = constants.MONTH
            self.screen_manager.selection.layout.interval_step_range_end.text = constants.MONTH
        else:
            self.screen_manager.selection.layout.time_step.values = full_selection

    def timeStepSelected(self, *args):
        if args[1] == constants.CUSTOM_MONTHS:
            self.screen_manager.selection.layout.interval_step_range_start.disabled = False
            self.screen_manager.selection.layout.interval_step_range_end.disabled = False
        else:
            self.screen_manager.selection.layout.interval_step_range_start.disabled = True
            self.screen_manager.selection.layout.interval_step_range_end.disabled = True

    def monthStartSelected(self, *args):
        start = self.screen_manager.selection.layout.interval_step_range_start.text
        self.screen_manager.selection.layout.interval_step_range_end.text = constants.MONTH
        try:
            remaining_months = constants.MONTH_LIST[constants.MONTH_LIST.index(start):]
            self.month_range_end = remaining_months
        except:
            self.month_range_end = constants.MONTH_LIST

    def create_graph(self):
        details = {}
        data_type = self.screen_manager.selection.layout.data_type.text
        region = self.screen_manager.selection.layout.region.text
        start_year = self.screen_manager.selection.layout.start_year.text
        end_year = self.screen_manager.selection.layout.end_year.text
        time_step = self.screen_manager.selection.layout.time_step.text
        operation = self.screen_manager.selection.layout.operation.text
        start = self.screen_manager.selection.layout.interval_step_range_start.text
        end = self.screen_manager.selection.layout.interval_step_range_end.text
        month_range = None
        if constants.OPTION_HOLDER in [region, data_type, start_year, end_year, time_step, operation] or\
                (time_step == constants.CUSTOM_MONTHS and constants.MONTH in [start, end]) or\
                constants.YEAR in [start_year, end_year]:
            self.error.open()
        else:
            if self.screen_manager.selection.layout.time_step.text == constants.CUSTOM_MONTHS:
                start = self.screen_manager.selection.layout.interval_step_range_start.text
                end = self.screen_manager.selection.layout.interval_step_range_end.text
                month_range = range(int(constants.MONTH_LIST.index(start))+1,
                                               int(constants.MONTH_LIST.index(end))+2)

            series = (self.dao.get_values(region, data_type, start_year, end_year,
                                         time_step, operation, month_range), "Data Series")
            plotGraph("graph", operation + " " + data_type + " By " + time_step + " For " + region, "Time", data_type, [series])
            self.screen_manager.display.display_layout.graph.source = ''
            self.screen_manager.display.display_layout.graph.reload()
            self.screen_manager.display.display_layout.graph.source = 'imgs/graph.png'
            self.screen_manager.display.display_layout.graph.reload()
            self.screen_manager.current = "display"
