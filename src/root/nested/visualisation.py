'''
Created on 26 Dec 2017

@author: seantmcmahon
'''
from plotter import plotGraph
import kivy
kivy.require('1.9.1')
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, BooleanProperty

Builder.load_file('visualisationScreen.kv')


class VisualisationScreen(Screen):
    data_types = ListProperty()
    month_range_start = BooleanProperty()
    month_range_end = BooleanProperty()
    image_source = StringProperty()

    def __init__(self, **kwargs):
        self.dao = App.get_running_app().DAO
        self.regions = self.dao.getRegionNames()
        self.unchecked_colour = [0.7, 0, 0, 1]
        self.checked_colour = [0, 0.7, 0, 1]
        super(VisualisationScreen, self).__init__()
        self.error = Popup(title='Error', content=Label(text='Must specify a value for all options.'),
                          size_hint=(0.5, 0.5))
        self.loading = Popup(title='Loading...', content=Label(text='Performing Action...'),
                          size_hint=(0.5, 0.5), auto_dismiss=False)

    def updateStartYearSpinner(self):
        region = self.screen_manager.selection.layout.region.text
        data_type = self.screen_manager.selection.layout.data_type.text
        if "<Select>" not in [region, data_type]:
            self.screen_manager.selection.layout.start_year.text = 'Year'
            self.screen_manager.selection.layout.start_year.disabled = False
            self.screen_manager.selection.layout.start_year.values = self\
                .dao.getAvailableYearsForRegion(region, data_type)

    def updateEndYearSpinner(self):
        region = self.screen_manager.selection.layout.region.text
        data_type = self.screen_manager.selection.layout.data_type.text
        self.screen_manager.selection.layout.end_year.text = 'Year'
        self.screen_manager.selection.layout.end_year.disabled = False
        self.screen_manager.selection.layout.end_year.values = self\
            .dao.getAvailableYearsForRegion(region, data_type)

    def updatePossibleTimeSteps(self):
        full_selection = ['Month', 'Season', 'Full Year', 'Jan Annually',
                          'Feb Annually', 'Mar Annually', 'Apr Annually',
                          'May Annually', 'Jun Annually', 'Jul Annually',
                          'Aug Annually', 'Sep Annually', 'Oct Annually',
                          'Nov Annually', 'Dec Annually', 'Spring Annually',
                          'Summer Annually', 'Autumn Annually',
                          'Winter Annually', 'Custom Months Annually']
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
        if "<Select>" in [region, data_type, start_year, end_year, time_step, operation] or\
                (time_step == "Custom Months Annually" and "<Month>" in [start, end]):
            self.error.open()
        else:
            self.loading.open()
            if self.screen_manager.selection.layout.time_step.text == "Custom Months Annually":
                start = self.screen_manager.selection.layout.interval_step_range_start.text
                end = self.screen_manager.selection.layout.interval_step_range_end.text
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
                          "Aug", "Sep", "Oct", "Nov", "Dec"]
                month_range = range(int(months.index(start))+1,
                                               int(months.index(end))+2)

            series = self.dao.get_values(region, data_type, start_year, end_year,
                                         time_step, operation, month_range)
            plotGraph("graph", operation + " " + data_type + " By " + time_step + " For " + region, "Time", data_type, [series])
            self.screen_manager.display.display_layout.graph.source = ''
            self.screen_manager.display.display_layout.graph.reload()
            self.screen_manager.display.display_layout.graph.source = 'imgs/graph.png'
            self.screen_manager.display.display_layout.graph.reload()
            self.loading.dismiss()
            self.screen_manager.current = "display"
