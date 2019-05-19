import mysql.connector

db = mysql.connector.connect(
	host="mydbinstance.cbp3whb5qyie.us-east-2.rds.amazonaws.com",
 	port=3306,
 	user="gyqls",
 	passwd="rnjssmdsoRj1",
 	database = "Drello"
)

cursor = db.cursor()

import Login

if __name__ == "__main__":
    print("main")
    Login.start(db)

