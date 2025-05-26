import re
import sqlite3
import hashlib
import random 
import time
from datetime import datetime
from getpass import getpass
from myclasses import *


# 1. Build sign up feature
# 2. Build log in feature
# 3. Protect the main menu so that only logged in users can access it
# 4. Input validation

conn = sqlite3.connect("Lotusbank.db")

cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON")
now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def acc_no_generator():
    acc_no_gen=[str(num) for num in range(10)]
    acc_no=""
    random.shuffle(acc_no_gen)
    for i in acc_no_gen[:8]:
        acc_no += i
    return  acc_no  

def trans_id_generator():
    trans_id_gen=[str(num) for num in range(10)]
    trans_id=""
    random.shuffle(trans_id_gen)
    for i in trans_id_gen:
        trans_id += i
    return trans_id
def main():
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        full_name TEXT NOT NULL,
        password TEXT NOT NULL,
        Acc_no TEXT NOT NULL UNIQUE,
        Account_balance INTEGER DEFAULT 0
        
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        trans_id INTEGER PRIMARY KEY AUTOINCREMENT,
        transac TEXT,
        transaction_type TEXT,
        date_time_stamp TEXT,
        Amount INTEGER,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES customers(id)
        
    )
    """)
    
    
    
    
    
   

    def sign_up():
        Account_number=acc_no_generator()
        while True:
            full_name = input("Enter your full name: ").strip()
            chk_length= len(full_name) >=4 and len(full_name) <= 255
            if not full_name:
                print("First name cannot be blank")
                continue
            if not full_name.replace(" ","").isalpha():
                print("Input field must contain only alpahabet")
                continue
            if not chk_length:
                print("Input field must have a min of 4 to 255 characters")
                continue
            break


        while True:
            username = input("Enter your username: ").strip()
            chk_username_length=len(username)>=3 and len(username)<=20
            if not username:
                print("Username cannot be blank")
                continue
            if not chk_username_length:
                print("Username must have at least 3 to 20 characters")
                continue
            
            exists = cursor.execute("SELECT 1 FROM customers WHERE username = ?", (username,)).fetchone() == (1, )
            if exists:
                print("User with that Username already exists")
                continue
            break



        while True:
            password = getpass("Enter your password: ").strip()
            chk_password_length= len(password) >= 3 and len(password)<=20 
            pattern=r"[A-Za-z0-9 %$#_@?]"
            match=re.match(pattern,password)
            if not password:
                print("Password cannot be blank")
                continue
            if not match:
                print("Passowrd must contain at least one uppercase,lowercase and special character")
                continue
            if not chk_password_length:
                print("Password must be at 3 to 20 characters")
                continue
            confirm_password = getpass("Confirm your password: ").strip()

            if not confirm_password:
                print("Confirm Password field cannot be blank")
                continue

            if password != confirm_password:
                print("Passwords don't match")
                continue
            break


        hashed_password = hashlib.sha256(password.encode()).hexdigest()



        try:
            cursor.execute("""
                INSERT INTO customers (username, full_name, password, Acc_no) VALUES 
                (?, ?, ?, ?)
            """, ( username, full_name, hashed_password,Account_number))
        except sqlite3.IntegrityError as e:
            print(f"User with that username already exists: {e}")
        else:
            conn.commit()
            print("Account created successfully.")
            log_in()


    def log_in():
        print("\n\n**********************Log In**********************")

        while True:
            username = input("Enter your username: ").strip()
            if not username:
                print("Username field is required.")
                continue
            break

        while True:
            password = getpass("Enter your password: ").strip()
            if not password:
                print("Password field is required.")
                continue
            break
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        user = cursor.execute("SELECT * FROM customers WHERE username = ? AND password = ?", (username, hashed_password)).fetchone()
        if user is not None:
            time.sleep(3)
            print("Logged in successfully")
            time.sleep(2)
            Lotusbank(user)
        else:    
           time.sleep(1)
           print("Invalid username or password")
            

    main_menu = """
    1. Make deposit.
    2. Withdraw.
    3. Transfer.
    4. Transaction History.
    5. Exit.
    """

    

    
    def Lotusbank(user):
        id, username, full_name, password, Acc_no,Account_balance = user
        acc= AccountOwner(username,Account_balance)
        print("\n\n**********************Lotusbank plc **********************")
        print(f"Welcome, {username}")
        time.sleep(3)
        
        while True:
            
            print(main_menu)   
                     
            choice = input("Choose an option from the menu above: ").strip()
            if choice == "5":
                break
            if choice == "1":
               while True:
                    try:
                        deposit=int(input("Enter amount to be deposited : "))
                        print("Processing",end='')
                        for _ in range(5):
                            time.sleep(2) 
                            print('.',end="",flush=True)
                        print(f"\n{acc.deposit(deposit)}\n")
                        
                   
                    except ValueError as e:
                            print(e) 
                            continue    


                    except InsuficientFunds as e:
                        print(e)
                        continue
                    except Exception as e:
                        print(f"Something went wrong : {e}")
                    else:
                        
                        acc.update_balance()
                        acc.insert_transaction("Deposit","Credit",now,deposit,id)
                    break
            
            elif choice == "2":
                while True:
                    try:
                        amount_withdrawn=int(input("Enter amount to be deposited : "))
                        print("Processing",end='')
                        for _ in range(5):
                            time.sleep(2) 
                            print('.',end='',flush=True)
                        
                        print(f"\n{acc.withdraw(amount_withdrawn)}")
                        
                   
                    except ValueError as e:
                            print(e) 
                            continue    
                    except NegativeValues as e:
                            print(e)    
                            continue
                    except Exception as e:
                        print(f"Something went wrong : {e}")        
                    else:
                        acc.update_balance() 
                        acc.insert_transaction("Withdrawal","debit",now,amount_withdrawn,id)   
                    break
            
            
            elif choice == "3":
                recepient= input("Enter receipient account number : ")
                recepient_details=cursor.execute("""
                SELECT username,Acc_no,Account_balance
                FROM customers
                WHERE Acc_no = ? 
                                                 """,(recepient,)).fetchone()
                if recepient_details is not None:
                    print(recepient_details)
                    username,Ac_no,Acc_bal=recepient_details
                    print(f"{username} : {Ac_no}")
                    rec=Recepient(username,Acc_bal)
                    print(rec.username)
                    while True: 
                        try:
                            transferred_amount=int(input("Enter the amount you want to transfer : "))
                            print(acc.transfer(transferred_amount))
                            print(rec.deposit(transferred_amount))
                        except ValueError as e:
                            print(e)  
                            continue  
                        except InsuficientFunds as e:
                            print(e)
                            continue
                        except Exception as e:
                            print(f"Something went wrong : {e}")
                        else: 
                          acc.update_balance()  
                          rec.update_balance()
                          acc.insert_transaction("Transfer","debit",now,transferred_amount,id)
                        break  
            elif choice == "4":
                trans_history=acc.chk_transaction_history(id)
                print("Processing",end='')
                for _ in range(3):
                    time.sleep(2) 
                    print('.',end="",flush=True)
                for i in trans_history:
                    time.sleep(2)
                    print(f"transaction :{i[1]}/{i[2]}alert\nDate:{i[3]}\nAmount :${i[4]}\n")
            
                
    
    auth_menu = """
    1. Sign Up.
    2. Log In.
    3. Quit
    """



    while True:
        print("\n\n*******************Sign up Page*************************")
        print("Welcome to Lotusbank.")
        print(auth_menu)
        choice = input("Choose an option from the menu above to perform transactions: ").strip()
        
        if choice == "1":
            print(sign_up())
        elif choice == "2":
            log_in()
        elif choice == "3":
            print("Bye!...It's nice banking with you 👋.")
            break
        else:
            print("Invalid choice.")
            continue
            


try:
    main()
except sqlite3.IntegrityError as e:
    print(e)
except sqlite3.OperationalError as e:
    print(e)
except Exception as e:
    print(f"Something went wrong: {e}")
finally:
    conn.close()
    
 

        
  
     
        
         
        
        