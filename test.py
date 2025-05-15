import random 
import sqlite3
conn = sqlite3.connect("Lotusbank.db")
cursor = conn.cursor()

emmanuel = cursor.execute("""
  SELECT * FROM customers
  WHERE username=?              
                 """,("emma",)).fetchall()   
print(emmanuel) 











# acc_no_gen=[str(num) for num in range(10)]
# acc_no=""
# random.shuffle(acc_no_gen)
# for i in acc_no_gen[:8]:
#     acc_no += i
# print(acc_no)   

# full_name=input("Enter your full name : ")
# chk_length= len(full_name) >=4 and len(full_name) <= 255
# if not full_name.replace(" ","").isalpha():
#     print("full name must be alphabet only")
# if not chk_length:
#     print("Full name must be at least min of 4 characters and max of 255 characters ")
# else :    
#   print(full_name)    

