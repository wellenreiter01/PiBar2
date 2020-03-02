#!/usr/bin/python3
from kivy.core.window import Window
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager,  SlideTransition
from welcome import HelloScreen, BlackScreen
from selection import *
from admin import AdminScreen

class BarScreenManager(ScreenManager):
    
    Theme = StringProperty('Themes/default')
    
    def __init__(self, **kwargs):
        self.register_event_type('on_set_CardId')
        self.register_event_type('on_isAdmin')
        self.register_event_type('on_no_input')
        self.register_event_type('on_drink_selected')
        super(BarScreenManager, self).__init__(**kwargs)
        
    def on_set_CardId(self, *args):
        #print ('Screenmanager:on_set_CardId')
        self.transition.direction = 'left'
        self.current='DrinkList'
        self.dispatch_children('on_set_CardId',*args)
        
    def on_isAdmin(self, *args):
        self.current='Admin'
        
    def on_drink_selected(self,*args):
       self.dispatch_children('on_drink_selected',*args)
    
    def on_no_input(self,*args):
       # print ('Screenmanager:on_no_input')
        self.current='Welcome'
    
            
            
        
class PiBarApp(App):
    
    def build_config(self,config):
        config.setdefaults('Themes', {
            'active': 'default'
        })
       
    def build(self):
        config=self.config

        AppTheme=config.get('Themes', 'active'),
       
        Window.fullscreen = 'auto'
        Window.show_cursor = False
        sm = BarScreenManager(transition = SlideTransition(), Theme = AppTheme[0])
        sm.Theme = AppTheme[0]
        sm.add_widget(HelloScreen(AppTheme[0],name='Welcome'))
        sm.add_widget(SelectionScreen(AppTheme[0],name='DrinkList'))
        sm.add_widget(AdminScreen(AppTheme[0], name='Admin'))
        sm.add_widget(BlackScreen(name='black'))
        sm.current='Welcome'
        
        return sm
    
        
if __name__ == '__main__':
    PiBarApp().run()
