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
from kivy.properties import ListProperty
from kivy.core.text import LabelBase

Builder.load_file('visualisationScreen.kv')

class DataSelectScreen(Screen):
    
    def __init__(self, **kwargs):
        self.unchecked_colour = [0.7, 0, 0, 1]
        self.checked_colour = [0, 0.7, 0, 1]
        super(DataSelectScreen, self).__init__()
    
    def second_graph_toggled(self):   
        if self.layout.second_graph.state == 'down':
            self.layout.second_graph.background_color = self.checked_colour
            self.layout.second_graph.text = unichr(8730)
        else:
            self.layout.second_graph.background_color = self.unchecked_colour
            self.layout.second_graph.text = 'x'

class DataViewScreen(Screen):
    pass

class VisualisationScreen(Screen):
    pass


