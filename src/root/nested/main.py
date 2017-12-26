'''
Created on 7 Dec 2017

@author: seantmcmahon
'''
import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown


class Screen1(Screen):
    pass

class Screen2(Screen):
    pass

class Screen3(Screen):
    pass

class Menu(NavigationDrawer):
    def __init__(self):
        super(Menu, self).__init__()
        
    def toggle_screen(self, next_screen):
        self.screen_manager.current = next_screen
        self.anim_to_state('closed')


class WeatherApp(App):
    
    def build(self):
        return Menu()
        
if __name__ == '__main__':
    WeatherApp().run()