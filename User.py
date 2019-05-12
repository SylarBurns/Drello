
# coding: utf-8
import mysql.connector
import Menu

class User:
    def __init__(self, cursor , user_ID):
        self.cursor = cursor   
        self.user_ID = user_ID
        self.start()         
    
    def usermenu(self):
        print("1. Show user info")
        print("2. Edit user info")
        print("3. Leave drello")
        print("4. Back to Menu")

    def showinfo(self):
        print("showinfo")
        
    def editinfo(self):
        print("editinfo")
        
    def leaving(self):
        print("leaving")

    def start(self):
        self.usermenu()
        choice = int(input("Enter the number for your choice: "))

        if(choice == 1) :
            self.showinfo()
        elif(choice ==2):
            self.editinfo()
        elif(choice ==3):
            self.leaving()
        elif(choice ==4):
            Menu.Menu(self.cursor , self.user_ID)
        else :
            "잘못 누르셨습니다."
        self.start()

