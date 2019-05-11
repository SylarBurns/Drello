
# coding: utf-8

# In[ ]:
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="gyqls",
  passwd="kj1313",
  database = "Drello"
)

cursor = db.cursor()

import Login

if __name__ == "__main__":
    Login.start(cursor)

