'''
Created on 26 Dec 2017

@author: seantmcmahon
'''
import kivy
kivy.require('1.9.1')

from kivy.lang import Builder 
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_file('visualisationScreen.kv')

class DataSelectScreen(Screen):
    pass

class DataViewScreen(Screen):
    pass

class VisualisationScreen(Screen):
    pass


