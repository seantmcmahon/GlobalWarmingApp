'''
Created on 3 Feb 2018

@author: seantmcmahon
'''
import os
from predictor import Predictor
from newDao import Dao
import kivy
kivy.require('1.9.1')

from kivy.lang import Builder
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, BooleanProperty

Builder.load_file('forecastingScreen.kv')


class ForecastingScreen(Screen):
    data_types = ListProperty()
    month_range_start = BooleanProperty()
    month_range_end = BooleanProperty()
    month_range_start_list = ListProperty()
    month_range_end_list = ListProperty()
    image_source = StringProperty()

    def __init__(self, **kwargs):
        self.dao = Dao()
        self.regions = self.dao.getRegionNames()
        self.predictor = Predictor(self.dao)
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.loading = 'imgs/tenor.gif'
        super(ForecastingScreen, self).__init__()
        self.data_types = self.dao.getDataTypes()
        self.month_range_start = True
        self.month_range_end = True
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self.month_range_start_list = self.months
        self.month_range_end_list = self.months
        self.image_source = ''
        self.error = Popup(title='Error', content=Label(text='Must specify a value for all options.'),
                          size_hint=(0.5, 0.5))

    def timeStepSelected(self, *args):
        if args[1] == "Custom Months Annually":
            self.month_range_start = False
            self.month_range_end = False
        else:
            self.month_range_start = True
            self.month_range_end = True

    def monthStartSelected(self, *args):
        start = self.screen_manager.selection.layout.interval_step_range_start.text
        remaining_months = self.months[self.months.index(start):]
        self.screen_manager.selection.layout.interval_step_range_end.text = '<Month>'
        self.month_range_end_list = remaining_months

    def predict_data(self):
        region = self.screen_manager.selection.layout.region.text
        data_type = self.screen_manager.selection.layout.data_type.text
        prediction_type = self.screen_manager.selection.layout.prediction_type.text
        operation = self.screen_manager.selection.layout.operation.text
        time_step = self.screen_manager.selection.layout.time_step.text
        start = self.screen_manager.selection.layout.interval_step_range_start.text
        end = self.screen_manager.selection.layout.interval_step_range_end.text
        if "<Select>" in [region, data_type, prediction_type, time_step, operation] or\
                (time_step == "Custom Months Annually" and "<Month>" in [start, end]):
            self.error.open()
        else:
            if time_step == "Custom Months Annually":
                months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
                          "Aug", "Sep", "Oct", "Nov", "Dec"]
                month_range = range(int(months.index(start)) + 1,
                                    int(months.index(end)) + 2)
            else:
                month_range = None
            self.predictor.plot_predictions(region, data_type, prediction_type,
                                            time_step, operation, month_range, 500, 250)
            self.image_source = ''
            self.screen_manager.display.display_layout.graph.reload()
            self.image_source = self.path + "/imgs/newModel.png"
            self.screen_manager.display.display_layout.graph.reload()
