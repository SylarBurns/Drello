import mysql.connector
import mysql_auth

login = mysql_auth.info

db = mysql.connector.connect(
	host=login['host'],
 	port=login['port'],
 	user=login['user'],
 	passwd=login['passwd'],
 	database =login['database'],
)

cursor = db.cursor()

import Login

if __name__ == "__main__":
    print("main")
    Login.start(db)

