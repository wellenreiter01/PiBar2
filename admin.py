from subprocess import call
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.clock import Clock

from database import DbEngine
from scanner import Scanner

#/* popup windows */
class AdminPopup(Popup):
    def __init__(self,Parent,Title, Message, **kwargs):
        super(AdminPopup,self).__init__(**kwargs)
        self.Parent=Parent
        self.title=Title
        # outerLayout contains headline, list and buttons
        self.outerLayout=BoxLayout(orientation= 'vertical',spacing=1 ) 
        self.innerLayout=GridLayout(cols=3,size_hint_y=None,spacing=1)
        self.innerLayout.bind(minimum_height=self.innerLayout.setter('height'))
        self.innerLayout.row_default_height=20
        self.innerLayout.row_force_default=True
        if Message =='':
        
            # list is a list of items do be displayed, tha actual content
            self.itemList=ScrollView( size_hint=(1,.8))
            self.itemList.add_widget(self.innerLayout)

            
            #create a group with 2 buttons
            self.buttonGroup= BoxLayout(orientation='horizontal',height=40,size_hint_y=.15, spacing=8)
            self.okButton= AdminButton(0,Parent.Theme,text= 'Ok')
            self.buttonGroup.add_widget(self.okButton)
            self.okButton.bind(on_release=self.dismiss)
            self.cancelButton= AdminButton(0,Parent.Theme,text= 'Cancel')
            self.buttonGroup.add_widget(self.cancelButton)
            self.cancelButton.bind(on_release=self.dismiss)
            
            #add content 
            self.outerLayout.add_widget(self.itemList)
            
            # add buttongroup to the popup
            self.outerLayout.add_widget(self.buttonGroup)
            # finaly add the layout to the popup
            self.content=self.outerLayout
        else:
            self.content=Label(text=Message)
        
        
        
        
    
    def on_open(self):
        self.Parent.timeOut.cancel()
        self.timeOut=Clock.schedule_once(self.dismiss,3)
    
    def on_dismiss(self):
        self.Parent.timeOut()
        
        
class StockPopup(AdminPopup):
    CardId = StringProperty('0') #used to add new RFID cards to DB
    
    def __init__(self,Parent,Theme, Title, Message, **kwargs):
        super(StockPopup,self).__init__(Parent, Title, Message, **kwargs)
        self.Parent=Parent
        self.Theme= Theme
        self.engine = DbEngine(self)
        self.okButton.text='fertig'
        self.cancelButton.disabled = True
        
    def getStock(self, *args):
        label=Label(text='[b]Ean[/b]',halign='left', markup=True,size_hint_x=None, width=120)
        label.text_size=(label.width,None)
        self.innerLayout.add_widget(label)
        label=Label(text='[b]Getränk[/b]',halign='left', markup=True,size_hint_x=None, width=220)
        label.text_size=(label.width,None)
        self.innerLayout.add_widget(label)
        label=Label(text='[b]Bestand[/b]',halign='left', markup=True)
        label.text_size=(label.width,None)
        self.innerLayout.add_widget(label)
         
        dbResult= self.engine.getProducts(100,100,True)
        for Product in dbResult:      
            label=Label(text=Product[0],halign='left',size_hint_x=None, width=120)
            label.text_size=(label.width,None)
            self.innerLayout.add_widget(label)
            label=Label(text=Product[1],halign='left',size_hint_x=None, width=220)
            label.text_size=(label.width,None)
            self.innerLayout.add_widget(label)
            label=Label(text='{:5d}'.format(Product[2]),halign='right')
            label.text_size=(.5*label.width,None)
            self.innerLayout.add_widget(label)
            
                                                           

    # event handlers       
    def on_open(self,*args):
        #stop timeout of Admin screen
        self.Parent.timeOut.cancel()
        self.getStock()
        
        
    def on_dismiss(self,*args):
        #trigger timout on Adminscreen
        self.Parent.timeOut()
        
class ScanPopup(AdminPopup):
    CardId = StringProperty('0') #used to add new RFID cards to DB
    
    def __init__(self,Parent,Theme, Title, Message, **kwargs):
        super(ScanPopup,self).__init__(Parent, Title, Message, **kwargs)
        self.register_event_type('on_result')
        self.Parent=Parent
        self.Theme= Theme
        self.scanner= Scanner(self)
        self.okButton.text='fertig'
        self.cancelButton.disabled = True
        
    
        

    def on_open(self,*args):
        #stop timeout of Admin screen
        self.engine=  DbEngine(self)
        self.Parent.timeOut.cancel()
        #Start Scanner
        self.Scan= Clock.schedule_interval(self.scanner.scan,.8)
        #set timeout
        self.timeOut= Clock.schedule_interval(self.no_input,10)
        
    def on_dismiss(self,*args):
        #stop scanner
        self.Scan.cancel()
        #trigger timout on Adminscreen
        self.Parent.timeOut()
        
    
    def no_input(self,*args):
        self.dismiss()

    def on_CardId(self, *args):
        if self.CardId != '0':
            #print ('Card ', self.CardId, ' found')
            self.engine.add_RFID(self.CardId)
            self.CardId = '0'
                    
    def on_result(self,*args):
        if args[0] != 'Erfolg':
            popup = AdminPopup(self,args[0], '', 
                size_hint = (None, None), 
            size=(400, 300)
                )
            popup.innerLayout.add_widget(Label(text='\n\n{}'.format(args[1]), valign='bottom' ))
            popup.open()
        else:
            self.innerLayout.add_widget(Label(text='Chip {:15} index {:5} eingefügt'.format(args[1],args[2])))

class UserPopup(AdminPopup):
    CardId = StringProperty('0') #used to add new RFID cards to DB
    
    def __init__(self,Parent,Theme, Title, Message, **kwargs):
        super(UserPopup,self).__init__(Parent, Title, Message, **kwargs)
        self.Parent=Parent
        self.Theme= Theme
        self.engine = DbEngine(self)
        self.okButton.text='fertig'
        self.cancelButton.disabled = True
        
    def getUserList(self, *args):
        label=Label(text='[b]Chip-Nr.[/b]',halign='left', markup=True,size_hint_x=None, width=100)
        label.text_size=(label.width,None)
        self.innerLayout.add_widget(label)
        label=Label(text='[b]Name[/b]',halign='left', markup=True,size_hint_x=None, width=100)
        label.text_size=(label.width,None)
        self.innerLayout.add_widget(label)
        label=Label(text='[b]Vorname[/b]',halign='left', markup=True)
        label.text_size=(label.width,None)
        self.innerLayout.add_widget(label)
         
        dbResult= self.engine.getUserList()
        for User in dbResult:      
            label=Label(text=U'{:5d}'.format(User[0]),halign='left',size_hint_x=None, width=120)
            label.text_size=(label.width,None)
            self.innerLayout.add_widget(label)
            label=Label(text=User[1],halign='left',size_hint_x=None, width=100)
            label.text_size=(label.width,None)
            self.innerLayout.add_widget(label)
            label=Label(text=User[2],halign='left')
            label.text_size=(label.width,None)
            self.innerLayout.add_widget(label)
            
    def on_open(self,*args):
        #stop timeout of Admin screen
        self.Parent.timeOut.cancel()
        self.getUserList()
        
        
    def on_dismiss(self,*args):
        #trigger timout on Adminscreen
        self.Parent.timeOut()

#/* Buttons for Adminscreens*/            
class AdminButton(Button):
    id = NumericProperty(0)
    def __init__(self,Id, Theme, **kwargs):
        self.id = Id
        self.Theme= Theme
        super(AdminButton,self).__init__(**kwargs)
        self.halign = 'center'
        self.background_disabled_normal = 'Themes/{}/Button1_disabled_normal.png'.format(self.Theme)
        self.background_normal = 'Themes/{}/Button1_normal.png'.format(self.Theme)
        self.background_down = 'Themes/{}/Button1_pressed.png'.format(self.Theme)
        self.background_color = [0,0,1,.8] 
        self.text_size = (150,None)
        self.shorten_from = 'right'

#/*main Adminscreen and children 
class AdminScreen(Screen):
    Table = BoxLayout(orientation= 'vertical') 
    AdminCardId= 0
       

    def __init__(self, Theme, **kwargs):
        
        self.register_event_type('on_set_CardId')
        super(AdminScreen, self).__init__(**kwargs)
        self.Theme = Theme
        self.engine= DbEngine(self)
        #set idle timeout
        self.timeOut=Clock.create_trigger(self.no_input,5)
        #add content
        self.add_widget(Image(source='Themes/{}/Background.jpg'.format(Theme),
                        size_hint = (1,1),
                        opacity=.5),
                        index=1
                        ) 
        self.Table.add_widget( Label(text= 'Administration', 
                               size_hint= (1,0.1),
                               padding_y = 10, 
                               bold=True
                               ))
        self.selection=AdminSelection(Theme= self.Theme)
        self.Table.add_widget(self.selection)
        self.add_widget(self.Table)
        
        
   
    def on_enter(self):
        
        self.timeOut()
        
        
    def on_leave(self):
        self.AdminCardId = 0
        self.timeOut.cancel()
        
    def on_set_CardId(self, *args):
        if self.AdminCardId == 0:
          self.AdminCardId=args[0]
        
    def no_input(self,instance):
        self.parent.current ='Welcome'
        
class AdminSelection(GridLayout):
    CardId = StringProperty('0') #used to add new RFID cards to DB
    def __init__(self,Theme, **kwargs):
        
        super(AdminSelection, self).__init__(**kwargs)
        self.Theme=Theme
        self.engine= DbEngine(self)
        self.spacing = 10
        self.cols = 2
        self.padding = (60, 10,0,0)
        self.size_hint_x = (.9)
        self.row_default_height=40
        self.row_force_default=True
        self. Buttons = []
        self.UserGroup = 0
        
        self. Buttons = []
        self.Buttons.append(AdminButton(Id= 0,Theme= self.Theme,text= 'RFID Chip anlernen'))
        self.Buttons.append(AdminButton(Id= 1,Theme= self.Theme,text= 'Getränkebestand'))
        self.Buttons.append(AdminButton(Id= 2,Theme= self.Theme,text= 'Benutzerliste'))
        self.Buttons.append(AdminButton(Id= 3,Theme= self.Theme,text= 'Freie RFID chips'))
        self.Buttons.append(AdminButton(Id= 4,Theme= self.Theme,text= 'Zu den Getränken'))
        self.Buttons.append(AdminButton(Id= 5,Theme= self.Theme,text= ''))
        self.Buttons.append(AdminButton(Id= 6,Theme= self.Theme,text= 'Programm beenden'))
        self.Buttons.append(AdminButton(Id= 7,Theme= self.Theme,text= 'Pi herunterfahren'))
        self.Buttons[0].bind(on_release=self.scanMe)
        self.Buttons[1].bind(on_release=self.get_Stock)
        self.Buttons[2].bind(on_release=self.get_Users)
        self.Buttons[3].bind(on_release=self.get_freeChips)
        self.Buttons[4].bind(on_release=self.to_drinkSelection)
        
        self.Buttons[6].bind(on_release=self.app_exit)
        self.Buttons[7].bind(on_release=self.popup_poweroff)
        
        self.Buttons[5].background_color=[0,0,0,0]  #invisible button as spacer
        self.Buttons[6].background_color=[1,.3,0,1]
        self.Buttons[7].background_color=[1,.3,0,1]
        self.add_widget(self.Buttons[0])
        self.add_widget(self.Buttons[1])
        self.add_widget(self.Buttons[2])
        self.add_widget(self.Buttons[3])
        self.add_widget(self.Buttons[4])
        self.add_widget(self.Buttons[5])
        self.add_widget(self.Buttons[6])
        self.add_widget(self.Buttons[7])
        
    def scanMe(self,instance):
        popup = ScanPopup(self.parent.parent,self.Theme,'RFID anlernen', '',
            size_hint = (.3, .6), 
            )
        popup.open()
        
    def get_Stock(self,instance):
        popup = StockPopup(self.parent.parent,self.Theme,'Getränkebestand','',
        size_hint = (.6, .7)
        )
        popup.open()
    
    def get_Users(self,instance):
        popup = UserPopup(self.parent.parent,self.Theme,'Benutzerliste','',
        size_hint = (.6, .7)
        )
        popup.open()
    
    def get_freeChips(self,instance):
        dbresult=self.engine.getFreeChips()
        for item in dbresult:
            popup=AdminPopup(self.parent.parent,'Anzahl freier RFID Chips','Es sind {:3d} Chips unbenutzt'.format(item[0]),
            size_hint=(.4,.4))
            popup.open()
        
       
    def to_drinkSelection(self,instance):
        # tel manager to make drinklist current and set card for selection to the Admin's card
        self.parent.parent.manager.dispatch('on_set_CardId', self.parent.parent.AdminCardId)
       
    def app_exit(self,instance):
        call(['sudo', 'systemctl' ,'stop','pibar2'])
    
    def popup_poweroff(self,instance): 
        popup=AdminPopup(self.parent.parent,'System Shutdown', '',
                         size_hint=(.7,.7))
        popup.innerLayout.add_widget(Label(text='\n\n\nDer Pi wird Heruntergefahren'))
        popup.okButton.bind(on_release=self.poweroff_pi)
        popup.open()
        
    def poweroff_pi(self,instance):
        call(['sudo', 'poweroff'])
    
        #Close_me= Clock.schedule_once(popup.dismiss,2)
        
        
