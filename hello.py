import mysql.connector

mydb = mysql.connector.connect(
    host ='localhost',
    user='root',
    passwd='sylar475869*',
    database="Drello"
)

mycursor = mydb.cursor()

# sql = """CREATE TABLE Board (
#     Board_ID int AUTO_INCREMENT,
#     Board_Title varchar(128) NOT NULL,
#     Visibility varchar(128),
#     PRIMARY KEY (Board_ID)
# )"""
# sql = "DROP TABLE Board"
# mycursor.execute(sql)

sqlFormula = "INSERT INTO board (Board_Title, Visibility) VALUES (%s, %s)"
# titles =[("KAS", "public"),
#         ("HAS", "public"),
#         ("SAS", "private"),]
# bt1 = input("title")
# bv1 = input("Visibility")
# bt2 = input("title")
# bv2 = input("Visibility")
# bt3 = input("title")
# bv3 = input("Visibility")
# t1 =(bt1,bv1)
# t2 =(bt2,bv2)
# t3 =(bt3,bv3)
# titles =[]
# titles.append(t1)
# titles.append(t2)
# titles.append(t3)
# mycursor.executemany(sqlFormula, titles)
# mydb.commit()
sql = "SELECT Board_Title, Board_ID FROM Board"
mycursor.execute(sql)
myresult = mycursor.fetchall()

for (title, ID) in myresult:
    print("Title: "+title+" ID", ID)