from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.clock import Clock

import MySQLdb
import time
import MFRC522
import RPi.GPIO as GPIO

from database import DbEngine

class BlackScreen(Screen):
    def __init__(self, **kwargs):
        super(BlackScreen, self).__init__(**kwargs)
        self.register_event_type('on_touch_down')
        
        
    def on_touch_down(self, *args):
        self.manager.current='Welcome'
    
#class HelloScreen(BoxLayout):
class HelloScreen(Screen):
    CardId = StringProperty('0')
    Table= BoxLayout(orientation= 'vertical')
    read = True
    
#    def getUserData(self,cardid):
#        self.engine = DbEngine(self)
#        result = self.engine.getUserId(cardid)
#        for user in result:
#            print (str(user[2]) +" "+str(user [3]))
            
        
    def __init__(self, **kwargs):
       
        super(HelloScreen, self).__init__(**kwargs)
        self.engine= DbEngine(self)
        self.orientation = 'vertical'
        self.padding = (0.5*self.width,30)
        self.Table.add_widget( Label(text= 'Willkommen', 
                               size_hint= (1,0.1),
                               padding_y = 10, 
                               bold=True
                               ))
        self.Table.add_widget( Button(text = '',
                                      background_normal= 'Themes/default/Background.jpg',
                                      background_down= 'Themes/Orangejuice/Background.jpg'))
                                    
        self.Table.add_widget( Label(text = 'Bitte scanne deine Benutzerkarte! ',
                               size_hint= (1,0.1),
                               padding_y = 10, 
                               bold=True
                               ))
        self.add_widget(self.Table)
        self.MIFAREReader = MFRC522.MFRC522()
        self.init_gpio()
        
    def init_gpio(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(15, GPIO.OUT)
        GPIO.output(15, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(15, GPIO.LOW)
        # Pins to control LEDs
        #GPIO.setup(12, GPIO.OUT)
        #GPIO.setup(16, GPIO.OUT)
        #GPIO.setup(18, GPIO.OUT)
 
    def on_enter(self):
        self.read = True
        self.Scan= Clock.schedule_interval(self.scan,.8)
        self.Blank= Clock.schedule_interval(self.blank_screen,180)
    
    def on_leave(self):
        self.read = False
        self.CardId = '0'
        self.Scan.cancel()
        self.Blank.cancel()
        
        GPIO.cleanup()
        
    def on_CardId(self, *args):
        if self.CardId != '0':
            if self.engine.getAdmin(self.CardId):
                self.manager.dispatch('on_isAdmin', self.CardId)
            else:
                self.manager.dispatch('on_set_CardId', self.CardId)
        
    def scan(self, *args):
        if self.read:
            #GPIO.output(16, GPIO.HIGH)  #set LED on
            (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
            #GPIO.output(16, GPIO.LOW) #set LED off
            (status,uid) = self.MIFAREReader.MFRC522_Anticoll()
            if status == self.MIFAREReader.MI_OK:
                CardString = str(uid[0]) +str(uid[1]) +str(uid[2]) +str(uid[3]) +str(uid[4])
                self.CardId = CardString
                self.read = False
            #    if db.open:
                #        who_am_i(cardid)
                #    else:
                #        db.close
                #        cursor = db.cursor()
                #GPIO.output(12, GPIO.LOW) #LED off
                return True

    def blank_screen(self, *args):
            self.manager.current='black'
