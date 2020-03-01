from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class AdminScreen(Screen):
    Table = BoxLayout(orientation= 'vertical') 
       

    def __init__(self, **kwargs):
        
        super(AdminScreen, self).__init__(**kwargs)
        Button1=(Button(text= 'Willkommen',size_hint= (.5,0.1),pos_hint = {'center_x':1},
                               padding = [10,10]))
        Button2=(Button(text= 'Willkommen2',background_normal = './Themes/Orangejuice/Button1_normal.png', background_down = './Themes/Orangejuice/Button1_pressed.png'))
        self.Table.add_widget(Button1)
        self.Table.add_widget(Button2)
        
        self.add_widget(self.Table)
   
    def on_enter(self):
        self.timeOut=Clock.schedule_once(self.no_input,3)
        
    def on_leave(self):
        self.timeOut.cancel()
        
    def no_input(self,instance):
        self.parent.current ='Welcome'
