
# coding: utf-8
import mysql.connector
import Menu
import os

def start(db):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-------- Welcome Drello!! -----------")
    print("1. LOGIN")
    print("2. JOIN")
    print("-------------------------------------")
    choice = int(input("Enter the number for your choice: "))

    if choice == 1:
        login(db)
        
    elif choice == 2:
        join(db)
    else :
        print("다시 입력해주세요.")
        start(db)

def login(db):
    cursor = db.cursor()
    print("\n\n---------DRELLO LOGIN--------")
    print("ID : Handong")
    print("PW : 1004")
    print("-----------------------------")
    print("...CHECK DATABASE .. ")
    user_ID = 'Handong'
    sql = "SELECT EXISTS (select * from User where User_ID = 'Hanong' AND User_PW = '1004') as success"
    # sql = "select User_ID FROM User WHERE EXISTS (select * from User where User_ID = 'Handong' AND User_PW = '1004')"
    # sql = "select User_ID FROM User where User_ID = 'Handong' AND User_PW = '1004'"
    cursor.execute(sql)
    success = cursor.fetchall()
    if(success[0][0] == 1): 
        print("LOGIN SUCCESS")
    else :
        print("LOGIN FAIL")
        input("\n\nPlease Enter to go to NEXT ! :")
        start(db)

    input("\n\nPlease Enter to go to NEXT ! :")
    Menu.Menu(db, cursor , user_ID)

def join(db):
    cursor = db.cursor()
    cursor.execute("delete from User where User_ID='Handong'")

    print("\n\n----------DRELLO JOIN---------")
    print("ID : Handong")
    print("PW : 1004")
    print("Email : JC@handong.edu")
    print("Name : JC")
    print("Language : Korean")
    print("profile : Hi")
    print("-------------------------------")
    print("...INSERT INTO User TABLE...")

    sql = """INSERT INTO User 
            (User_ID, User_Email, User_PW, User_Name, User_Language, User_profile)
            VALUES(%s, %s, %s, %s, %s, %s )
    """

    users = [
        ("Handong","JC@handong,edu", "1004", "JC", "Korean", "Hi")
    ]

    cursor.executemany(sql, users)

    print("*Successfully Inserted User inforamtion into the [User] TABLE!*")
    
    sql = "SELECT User_ID FROM User Where User_ID = 'Handong'"
    cursor.execute(sql)
    user_ID = cursor.fetchall()
    db.commit()
    print("...AUTO LOGIN ...\n\n")
    print("Your user ID : " , user_ID[0][0])
    input("\n\nPlease Enter to go to NEXT ! :")
    Menu.Menu(db, cursor , user_ID)

