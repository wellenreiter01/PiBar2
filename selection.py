import kivy
kivy.require('1.10.6') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.properties import StringProperty

import MySQLdb
import signal
import time

from welcome import HelloScreen 
from database import DbEngine

    
class InfoLine(Button):
    def __init__(self,**kwargs):
        super(InfoLine,self).__init__(**kwargs)
        self.background_color = [0,0,0,.4]
        
    
    
    
class DrinkButton(Button):
    
    ean = 0000
    isCredit = False
    
    

    def __init__(self,Name, ean,UserId,price,backgroundImage='',**kwargs):
        super(DrinkButton, self).__init__(**kwargs)
        self.ean=ean
        self.UserId = UserId
        self.price = price
        self.text = Name
        self.halign = 'center'
        self.background_normal = '{}_normal.png'.format(backgroundImage)
        self.background_down = '{}_pressed.png'.format(backgroundImage)
        self.background_color = [.6,.5,.9,.8] 
        self.text_size = (150,None)
        self.shorten_from = 'right'
        

        
        
    def callback(self,instance): 
        #Trigger selection_widget to update database
        self.parent.parent.parent.dispatch('on_drink_selected',instance.price, instance.ean, instance.UserId,self.parent.isCredit) 
        print   ('on_drink_selected',instance.price, instance.ean, instance.UserId,self.parent.isCredit)
        

        

        
    
class Selection(GridLayout):
    # Widget containing the list of drinks 
    
    
    UserGroup = 0
    UserBalance = 0
    
    
    def __init__(self,CardId,parent, **kwargs):
        
        super(Selection, self).__init__(**kwargs)
        self.spacing = 10
        self.cols = 4
        self.padding = (60, 10,0,0)
        self.size_hint_x = (.9)
        self.row_default_height=40
        self.row_force_default=True
        self. Buttons = []
        self.engine= DbEngine(self)
        self.CardId = CardId
        self.UserGroup = 0
        
    def get_product_list(self):
        #get Productlist based the user's group
        self.UserId,self.UserGroup, self.isCredit = self.engine.getUserInfo(self.CardId)
        if self.UserId:
            self.UserBalance = self.engine.getUserBalance(self.CardId)
        else:
            popup = Popup(title = 'Warnung', content=Label(text= 'Benutzer für RFID\n {} \nnicht gefunden'.format(self.CardId), size_hint_x = .9, halign='center'),
            size_hint = (None, None), 
            size=(300, 200))
              
            popup.open()
            Close_me= Clock.schedule_once(popup.dismiss,3)
         
        if self.UserGroup:
            if self.isCredit:
                dbResult= self.engine.getProducts(self.UserGroup,100)
            else:
                dbResult= self.engine.getProducts(self.UserGroup,self.UserBalance)
            
            #display results
            j= 0
            for Product in dbResult:
    
                Productlist = self.Buttons.append(DrinkButton(Product[2],Product[1],self.UserId,Product[3],'Themes/default/Button1'))
                self.add_widget(self.Buttons[j])
                self.Buttons[j].bind(on_release=self.Buttons[j].callback)
                self.add_widget( Label(text='{:.2f}'.format(Product[3])+' €',
                                            bold = True,
                                            
                                            ))
                j = j+1
                
            if (j == 0):
                self.add_widget(InfoLine(text='Keine passenden Produkte gefunden'))
            
    def on_enter(self):
        timeOut=Clock.schedule_once(self.no_input,TIMEOUT)
        
    def on_leave(self):
        timeOut.cancel()
        
    def no_input(self,instance):
        self.parent.parent.no_input(instance.parent)
    
    
    
    
class SelectionScreen(Screen):
    # provides a screen with headline, list of drinks and bottom line
    # handles the interface to the customer and informs customer about 
    # orders and value of his card
    
    Buttons = []
    UserId = ''
    CardId = StringProperty('-1')
    
    
    
        
        
    def __init__(self, **kwargs):
        self.register_event_type('on_set_CardId')
        self.register_event_type('on_drink_selected')
        self.register_event_type('on_result')
        super(SelectionScreen, self).__init__(**kwargs)
        self.tableLayout = BoxLayout(orientation= 'vertical')  
        
       
        #self.tableLayout.add_widget(self.selection)

        self.add_widget(Image(source="Themes/default/Background.jpg",size_hint = (1,1)),
                        index=1
                        ) 
        
        self.add_widget(self.tableLayout)
        
       
    def on_enter(self):
        self.timeout = Clock.create_trigger(self.no_input,10)
        self.timeout()
        
    def on_leave(self):
        self.timeout.cancel()
                
    def on_set_CardId(self, *args):
        #print ('selection:on_card_id',args[0])
        self.CardId=args[0]
        self.tableLayout.clear_widgets()
        # the card is known, so show list of productss allowed
        self.selection = Selection(self.CardId,self)
        #self.selection.parent = self
        self.selection.get_product_list()
        self.tableLayout.add_widget( InfoLine(text='Bitte wähle ein Getränk:', 
                        size_hint= (1,0.2),
                        bold = True
                        ))
        self.tableLayout.add_widget(self.selection)
    
        if not self.selection.isCredit:
            self.BalanceInfo= InfoLine(text='Du hast noch {:.2f} € auf Deiner Karte'.format(self.get_userbalance()) ,
                                        size_hint= (1,.2),
                                        bold=True)
        else:
            self.BalanceInfo= InfoLine(text='Gästekarte mit Rechnung' ,size_hint= (1,.2), bold=True)
            
        self.tableLayout.add_widget(self.BalanceInfo)
    
        
    def on_result(self,*args):
        self.tableLayout.remove_widget(self.BalanceInfo)
        
        popup = Popup(title = args[0], content=Label(text= args[1], size_hint_x = .9, halign='center'),
            auto_dismiss = False,
            size_hint = (None, None), 
            size=(300, 200))
        if self.selection.isCredit:
            popup.content.text = 'Dein Getränk wurde erfasst'
              
        popup.open()
        Close_me= Clock.schedule_once(popup.dismiss,2)
        # trigger update for list of drinks
        self.on_set_CardId(self.CardId)
        #self.BalanceInfo.text='Du hast noch {:.2f} € auf Deiner Karte'.format(self.get_userbalance())
        #reset timeout so user can select more drinks
        self.timeout.cancel()
        self.timeout()
        
        

    
    def get_userbalance(self):
        db = DbEngine(self)
        if db:
            UserBalance = db.getUserBalance(self.CardId)
            del db
        return UserBalance
        
    def on_drink_selected(self,*args):
        db = DbEngine(self)
        if db:
            db.execute_order(args[0],args[1],args[2],args[3])
            del db
        
    def no_input(self,instance):
        try:
            self.manager.transition.direction='right'
            self.manager.current='Welcome'
        except:    
             print ('not found.', self.manager.screens,'.....\n')
        
        #return False   
    
   
    
        
