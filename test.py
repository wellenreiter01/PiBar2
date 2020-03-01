from kivy.app import App
#from kivy.config import Config,ConfigParser
 

 

class TestApp(App):
    
     def build_config(self, config):
        config.setdefaults('section1', {
            'key1': 'value1',
            'key2': '42'
        })                     

   
     
if __name__ == '__main__':
    TestApp().run()
