import kivy
kivy.require('1.10.6') # replace with your current kivy version !
import MySQLdb
import time
class DbEngine:
    # connection to the database and queries
    def __init__(self,parent):
        # Connect to the Database
        self.parent = parent
        self.db = MySQLdb.connect(host="localhost",
                            user="pibaruser",
                            passwd="DPSG-Franziskus",
                            db="pibar")
        
        if self.db:
            #print('DbEngine:  db.is_connected') 
            self.cursor = self.db.cursor()
        
    def getProducts(self,UserGroup=0, UserBalance = 0):      
        self.cursor.execute('SELECT * FROM products where drinktype <= {:d} and stock > 0 and price <= {:f}'.format(UserGroup, UserBalance))
        if self.cursor.rowcount:
            result = self.cursor.fetchall() 
        else:
            result = []
        return result     
    
    
    def getUserId(self,cardid):
        
        self.cursor.execute('SELECT * FROM customers where tagid = {}'.format(cardid))
        if not self.cursor.rowcount:
            print('User fuer RFID {} unbekannt'.format(cardid))
            result = []  #customer not found for CardID
        else:
            result = self.cursor.fetchall() 
        return result   
    
    
    def getUserBalance(self,cardnumber):
        result = self.getUserId(cardnumber)
        for user in result:
            return (user[7])
        return -0
        
    def getUserInfo(self,cardnumber):
        result = self.getUserId(cardnumber)
        if result:
            for user in result:
                isCredit = user[6].startswith('CREDIT')
                isAdmin = user[4] > 0
                return [user[0],user[5], isCredit]
        else:
                return [0,0,False]

    def getAdmin(self, cardnumber):
        isAdmin = False
        result = self.getUserId(cardnumber)
        if result:
            for user in result:
                isAdmin = user[4] > 0
                
        return isAdmin
    


    def execute_order(self,price, ean, customer,isCredit):
        #/** update order_list, stock_list and user balance
        #**/
        ispaid = not isCredit
        cursor = self.db.cursor()
        result =cursor.execute('INSERT INTO orders (customerId, productId,isPaid) VALUES({}, {},{})'.format(customer,ean,ispaid))
        if result != 1:     # Error not critical, so log warning and continue
            print ('*********WARNING: could not execute order\n**********\n')
        else:    
            result = cursor.execute('update products set stock = stock - 1 where ean = {:s}'.format(ean))
        if result != 1: # Error not critical, so log warning and continue
            print ('ERROR: could not update stock. check number of items for {:s}'.format(ean))
        else:
            if (price > 0) and not isCredit:
               result = cursor.execute ('update customers set balance = balance - {} where id = {}'.format(price,customer))
        # inform calling widget about the result of the update
        if result != 1: #critical error, rollbacak all transactions and inform customer
            self.db.rollback()
            self.parent.dispatch('on_result','Error','Konnte Guthaben nicht schreiben. \nBestellung nicht nicht berechnet. \n Bitte Getränk zurückstellen !!!!!!!')
        else:
            self.db.commit()  #write updates to database
            cursor.execute('select * from customers where id= {}'.format (customer))
            result= cursor.fetchall()
            User = result[0]
            self.parent.dispatch('on_result','Information','Bestellung durchgeführt.\nDein neues Guthaben ist: {} €'.format(User[7]))
        
        
        cursor.close()
        
    def add_RFID(self,customer):
        cursor = self.db.cursor()
        result = cursor.execute('INSERT INTO customers (tagid,lastName,userCard) VALUES({},{},{})'.format( customer," 'Frei' "," 'Chip xx'"))
        if result !=1: # we have an error
            self.parent.dispatch('on_result','Error', 'Konnte RFID nicht einfügen!\n RFID schon vorhanden?')
        else:
            self.db.commit()  #write updates to database
            cursor.execute('select id from customers where tagid= {}'.format (customer))
            result= cursor.fetchall()
            index= result[0]
            self.parent.dispatch('on_result','Erfolg', 'RFID {} als Karte Nummer\n {} eingefügt'.format(customer,index[0]))
        
    def on_result(*args):
        pass
    
    def on_warning(*args):
        pass
