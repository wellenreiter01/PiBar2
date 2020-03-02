import MFRC522
import RPi.GPIO as GPIO

class Scanner():
    def __init__(self,parent):
        self.parent= parent
        self.MIFAREReader = MFRC522.MFRC522()
        #self.init_gpio()
        
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

    def scan(self, *args):
       # if self.read:
            #GPIO.output(16, GPIO.HIGH)  #set LED on
            (status,TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
            #GPIO.output(16, GPIO.LOW) #set LED off
            (status,uid) = self.MIFAREReader.MFRC522_Anticoll()
            #print ('\n', status, ' ', uid)
            if status == self.MIFAREReader.MI_OK:
                CardString = str(uid[0]) +str(uid[1]) +str(uid[2]) +str(uid[3]) +str(uid[4])
                self.parent.CardId = CardString
            
                #GPIO.output(12, GPIO.LOW) #LED off
            return True
