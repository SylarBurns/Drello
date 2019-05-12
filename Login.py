
# coding: utf-8
import mysql.connector
import Menu
import os

# usersql = """CREATE TABLE User(
# 	User_ID int NOT NULL,
# 	User_PW varchar(32) NOT NULL,
# 	User_Email varchar(64) NOT NULL,
# 	User_Name varchar(16) NOT NULL,
# 	User_Language varchar(16) NOT NULL,
# 	User_Profile varchar(1024),
# 	PRIMARY KEY(User_ID)
# )"""

def start(cursor):
    # cursor.execute(usersql)

    print("--------- Welcome Drello -----------")
    print("1. LOGIN")
    print("2. JOIN")
    print("-----------------------------------")
    choice = int(input("Enter the number for your choice: "))

    if choice == 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        login(cursor)
        
    elif choice == 2:
        os.system('cls' if os.name == 'nt' else 'clear')
        join(cursor)
    else :
        print("다시 입력해주세요.")
        os.system('cls' if os.name == 'nt' else 'clear')
        start(cursor)

def login(cursor):
    print("login")
    user_ID = 000
    Menu.Menu(cursor , user_ID)

def join(cursor):
    print("join")
    print("auto login")
    user_ID = 111
    Menu.Menu(cursor , user_ID)

