import mysql.connector
import Menu
import os

def Notice(db, cursor, user_ID):
    os.system('cls' if os.name == 'nt' else 'clear')

    sql = "select A.Action, A.DateTime \
        From Activity as A , Notice as N\
        WHERE N.User_ID = '%d' and N.Activity_ID = A.Activity_ID and N.Is_read = 'N'" % user_ID

    # sql = "select A.Action, A.DateTime from Activity as A, Notice as N"

    cursor.execute(sql)
    notices = cursor.fetchall()

    print("-----------------------Your Notice --------------------")
    for notice in notices :
        print ( " ● %s | %s " % (notice[1] ,  notice[0]))
    print("-------------------------------------------------------")
    

    input("\n\nEnter to go to Menu ")
    Menu.Menu(db, cursor , user_ID)
