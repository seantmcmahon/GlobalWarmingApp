'''
Created on 3 Feb 2018

@author: seantmcmahon
'''
import os
from predictor import Predictor
from newDao import Dao
import kivy
import constants
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, BooleanProperty
kivy.require('1.9.1')

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
        self.month_range_start_list = constants.MONTH_LIST
        self.month_range_end_list = constants.MONTH_LIST
        self.image_source = ''
        self.error = Popup(title=constants.ERROR_LABEL, content=Label(
            text=constants.ERROR_MESSAGE), size_hint=(0.5, 0.5))

    def timeStepSelected(self, *args):
        if args[1] == constants.CUSTOM_MONTHS:
            self.month_range_start = False
            self.month_range_end = False
        else:
            self.month_range_start = True
            self.month_range_end = True

    def monthStartSelected(self, *args):
        start = self.screen_manager.selection.layout.\
            interval_step_range_start.text
        remaining_months = constants.MONTH_LIST[constants.MONTH_LIST.index(start):]
        self.screen_manager.selection.layout.interval_step_range_end.text =\
            constants.MONTH
        self.month_range_end_list = remaining_months

    def predict_data(self):
        region = self.screen_manager.selection.layout.region.text
        data_type = self.screen_manager.selection.layout.data_type.text
        prediction_type = self.screen_manager.selection.layout.\
            prediction_type.text
        operation = self.screen_manager.selection.layout.operation.text
        time_step = self.screen_manager.selection.layout.time_step.text
        start = self.screen_manager.selection.layout.\
            interval_step_range_start.text
        end = self.screen_manager.selection.layout.interval_step_range_end.text
        if constants.OPTION_HOLDER in [region, data_type, prediction_type,
                                       time_step, operation] or\
                (time_step == constants.CUSTOM_MONTHS and constants.MONTH in
                 [start, end]):
            self.error.open()
        else:
            if time_step == constants.CUSTOM_MONTHS:
                month_range = range(int(constants.MONTH_LIST.index(start)) + 1,
                                    int(constants.MONTH_LIST.index(end)) + 2)
            else:
                month_range = None
            self.predictor.plot_predictions(region, data_type, prediction_type,
                                            time_step, operation, month_range,
                                            500, 250)
            self.image_source = ''
            self.screen_manager.display.display_layout.graph.reload()
            self.image_source = self.path + "/imgs/newModel.png"
            self.screen_manager.display.display_layout.graph.reload()
            self.screen_manager.current = "display"
