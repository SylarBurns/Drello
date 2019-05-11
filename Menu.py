
# coding: utf-8
import mysql.connector
import User
import Login
import Team
# import Board

class Menu :
    def __init__(self, cursor, user_ID ):
        self.cursor = cursor
        self.user_ID = user_ID
        self.start()

    def menu(self):
        print("1. USER")
        print("2. TEAM")
        print("3. BOARD")
        print("4. NOTICE(NOT YET)")
        print("5. LOGOUT")
            
    def user(self):
        print("SQL about user")
        User.User(self.cursor , self.user_ID)
        
    def team(self):
        print("SQL about team")
        Team.Team(self.cursor , self.user_ID)
        
    def board(self):
        print("SQL about board")
        
        
    def notice(self):
        print("SQL about notice")
        
    def logout(self):
        print("logout")
        Login.start(self.cursor)
    
    def start(self):
        self.menu()
        choice = int(input("Enter the number for your choice: "))

        if(choice == 1) :
            self.user()
        elif(choice ==2):
            self.team()
        elif(choice ==3):
            self.board()
        elif(choice==4):
            self.notice()
        elif(choice==5):
            self.logout()
        else:
            print("잘못 누르셨습니다.")
            self.start()
    
    

