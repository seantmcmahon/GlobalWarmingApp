'''
Created on 26 Dec 2017

@author: seantmcmahon
'''
import kivy
kivy.require('1.9.1')

from kivy.lang import Builder 
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window

Builder.load_file('visualisationScreen.kv')

class DataSelectScreen(Screen):
    def __init__(self, **kwargs):
        self.dropdown_height = Window.size[1] * 0.1
        super(DataSelectScreen, self).__init__()
    pass

class DataViewScreen(Screen):
    pass

class VisualisationScreen(Screen):
    pass


