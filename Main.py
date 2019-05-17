
# coding: utf-8

# In[ ]:
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="sylar475869*",
  database="Drello"
)

cursor = db.cursor()

import Login

if __name__ == "__main__":
    print("main")
    Login.start(db)

