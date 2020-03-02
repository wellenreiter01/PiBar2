from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.image import Image

from database import DbEngine
from scanner import Scanner

class AdminScreen(Screen):
    
    
    Table = BoxLayout(orientation= 'vertical') 
       

    def __init__(self, Theme, **kwargs):
        
        super(AdminScreen, self).__init__(**kwargs)
        self.Theme = Theme
        self.add_widget(Image(source='Themes/{}/Background.jpg'.format(Theme),
                        size_hint = (1,1)),
                        index=1
                        ) 
        self.Table.add_widget( Label(text= 'Administration', 
                               size_hint= (1,0.1),
                               padding_y = 10, 
                               bold=True
                               ))
        
        self.Table.add_widget(AdminSelection(Theme= self.Theme))
        self.add_widget(self.Table)
        
        
   
    def on_enter(self):
        
        self.timeOut=Clock.schedule_once(self.no_input,5)
        
        
    def on_leave(self):
        self.timeOut.cancel()
        
        
    def no_input(self,instance):
        self.parent.current ='Welcome'
        
        

class AdminPopup(Popup):
    
    def __init__(self, **kwargs):
        super(AdminPopup,self).__init__(**kwargs)
    
class AdminButton(Button):
    id = NumericProperty(0)
    def __init__(self,Id, Theme, **kwargs):
        self.id = Id
        self.Theme= Theme
        super(AdminButton,self).__init__(**kwargs)
        self.halign = 'center'
        self.background_normal = 'Themes/{}/Button1_normal.png'.format(self.Theme)
        self.background_down = 'Themes/{}/Button1_pressed.png'.format(self.Theme)
        self.background_color = [.6,.5,.9,1] 
        self.text_size = (150,None)
        self.shorten_from = 'right'
        
        
class AdminSelection(GridLayout):

    CardId = StringProperty('0') #used to add new RFID cards to DB
    def __init__(self,Theme, **kwargs):
        self.register_event_type('on_result')
        
        super(AdminSelection, self).__init__(**kwargs)
        self.Theme=Theme
        self.scanner= Scanner(self)
        self.engine= DbEngine(self)
        self.spacing = 10
        self.cols = 4
        self.padding = (60, 10,0,0)
        self.size_hint_x = (.9)
        self.row_default_height=40
        self.row_force_default=True
        self. Buttons = []
        self.engine= DbEngine(self)
        self.UserGroup = 0
        
        self. Buttons = []
        self.Buttons.append(AdminButton(Id= 0,Theme= self.Theme,text= 'RFID Chip anlernen'))
        self.Buttons[0].bind(on_release=self.scanMe)
        self.add_widget(self.Buttons[0])
       
    def scanMe(self,instance):
        self.Scan= Clock.schedule_interval(self.scanner.scan,.8)
       
       
        
    def on_CardId(self, *args):
        #print ('selection:on_card_id',args[0])
        self.parent.parent.timeOut.cancel()
        if self.CardId != '0':
            print ('Card ', self.CardId, ' found')
            self.engine.add_RFID(self.CardId)
            self.CardId = '0'
            
            
    def on_result(self,*args):
        
        popup = AdminPopup(title = args[0], content=Label(text= args[1], size_hint_x = .9, halign='center'),
            size_hint = (None, None), 
            size=(300, 200))
       
              
        popup.open()
        #Close_me= Clock.schedule_once(popup.dismiss,2)
        
        
