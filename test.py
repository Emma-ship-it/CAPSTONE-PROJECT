import random 
import sqlite3
from datetime import datetime
from myclasses import *

conn = sqlite3.connect("Lotusbank.db")
cursor = conn.cursor()

# now=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# print(type(now))

emmanuel = cursor.execute("""
  SELECT * FROM transactions
  WHERE user_id = ?             
                 """,(1,)).fetchall()   
print(emmanuel) 
for i in emmanuel:
      print(f"transaction:{i[1]}/{i[2]} alert\nDate: {i[3]}\nAmount: ${i[4]}  ")
stevo=60985374
# acc=AccountOwner("toby",400)
# acc.insert_transaction("Alice","emm",40)
# trans=cursor.execute("""
#    SELECT * FROM transactions                  
#                      """).fetchall()
# print(trans)








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

