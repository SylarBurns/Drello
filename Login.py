
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
    Login_ID = "Handong"
    User_PW = "1004"

    print("\n\n---------DRELLO LOGIN--------")
    print("ID : %s" %Login_ID)
    print("PW : %s" %User_PW)
    print("-----------------------------")
    print("...CHECK DATABASE .. ")

    sql = "SELECT EXISTS (select * from User \
         where Login_ID = '%s' AND User_PW = '%s' AND Is_deleted = 'N')\
              as success" % (Login_ID , User_PW)
    cursor.execute(sql)
    success = cursor.fetchall()
    if(success[0][0] == 1): 
        print("LOGIN SUCCESS")
    else :
        print("LOGIN FAIL")
        input("\n\nPlease Enter to go to NEXT ! :")
        start(db)

    sql = "SELECT User_ID, Login_ID FROM User\
        Where Login_ID = '%s' AND User_PW = '%s' AND Is_deleted = 'N'" \
            % (Login_ID , User_PW)
    cursor.execute(sql)
    Users = cursor.fetchall()
    input("\n\nPlease Enter to go to NEXT ! :")
    Menu.Menu(db, cursor , Users[0][0])

def join(db):
    cursor = db.cursor()
    # cursor.execute("delete from User where User_ID='Handong'")

    print("\n\n----------DRELLO JOIN---------")
    print("ID : Handong")
    print("PW : 1004")
    print("Email : JC@handong.edu")
    print("Name : JC")
    print("Language : Korean")
    print("profile : Hi")
    print("-------------------------------")
    
    ID = "Handong"
    PW = "1004"
    Email = "JC@handong.edu"
    Name = "JC"
    Language = "Korean"
    profile = "Hi"

    # ID Exist CHECK
    sql = "SELECT EXISTS (select * from User \
        where Login_ID = '%s' AND Is_deleted = 'N') \
            as success" % (ID)

    cursor.execute(sql)
    success = cursor.fetchall()
    # 1 = Exists
    if(success[0][0] == 1): 
        print("ID already exists. Enter another ID")
        input("\n\nPlease Enter to go to NEXT ! :")
        start(db)
    else :
        print("...INSERT INTO User TABLE...")
        sql = "INSERT INTO User \
                (Login_ID, User_Email, User_PW, User_Name, User_Language, User_profile)\
                VALUES('%s','%s', '%s', '%s','%s', '%s' )" % (ID, Email, PW, Name, Language,profile )
            

        cursor.execute(sql)
        print("*Successfully Create User into the [User] TABLE!*")
        
        sql = "SELECT User_ID, Login_ID FROM User\
             Where Login_ID = '%s' AND User_PW = '%s' AND Is_deleted = 'N'" \
                 % (ID,PW)
        cursor.execute(sql)

        Users = cursor.fetchall()
        db.commit()
        print("...AUTO LOGIN ...\n\n")
        print("Your ID : " , Users[0][1])
        input("\n\nPlease Enter to go to NEXT ! :")
        Menu.Menu(db, cursor , Users[0][0])



