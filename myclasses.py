import sqlite3

conn = sqlite3.connect("Lotusbank.db")
cursor = conn.cursor()
class NegativeValues(Exception):
    def __init__(self,message):
        self.message=message
        super().__init__(self.message)


class InsuficientFunds(Exception):
    def __init__(self,message):
        self.message=message
        super().__init__(self.message)     


class AccountOwner:
       def __init__(self,username,balance):
           self.username=username
           self._balance=balance

    
       def update_balance(self):
        #    print(f"Updating balance of {self.username} to {self._balance}")
           cursor.execute("""
            UPDATE customers
            SET Account_balance=?
            WHERE username = ?              
            
                        """,(self._balance,self.username))
           conn.commit()
       def deposit(self,amount) :
            if amount <= 0:
                raise NegativeValues("Amount cannot be less than zero")
            self._balance+=amount
            # print(self._balance)
        
       def withdraw(self,amount):
            if amount > self._balance:
                raise InsuficientFunds(f"Insufficient funds")
            self._balance-=amount
            return "Withdrawal Accepted"   
       def transfer(self,amount):
           
           if amount > self._balance:
               raise InsuficientFunds(f"Funds unavailable") 
           self._balance-=amount
           return "Transfer successful"
       def insert_transaction(self,trans,trans_type,date,amt,user_id,rept=None):
           cursor.execute("""
              INSERT INTO transactions(transac,transaction_type,date_time_stamp,Amount,user_id,recepient) VALUES
              (?,?,?,?,?,?)         
          
               """,(trans,trans_type,date,amt,user_id,rept))
           conn.commit()
       def chk_transaction_history(self,user_id):
           owner=cursor.execute("""
             SELECT * FROM transactions
             WHERE user_id = ?             
                          """,(user_id,)).fetchall()
        
           return owner
           
             

class Recepient(AccountOwner):
    def __init__(self,name,balance):
        super().__init__(name,balance)     
        

                     