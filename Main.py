
# coding: utf-8

# In[ ]:
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="mz0090mz",
  database = "Drello"
)

cursor = db.cursor()

import Login

if __name__ == "__main__":
    Login.start(cursor)

