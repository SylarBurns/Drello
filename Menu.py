
# coding: utf-8
import mysql.connector
import User
import Login
import Team
import Board
import os

class Menu :
    def __init__(self, db, cursor, user_ID):
        self.cursor = cursor
        self.user_ID = user_ID
        self.db = db
        self.start()

    def menu(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("----------MENU----------")
        print("1. USER")
        print("2. TEAM")
        print("3. BOARD")
        print("4. NOTICE(NOT YET)")
        print("5. LOGOUT")
        print("------------------------")
            
    def user(self):
        print("SQL about user")
        User.User(self.db, self.cursor , self.user_ID)
        
    def team(self):
        print("SQL about team")
        Team.Team(self.db, self.cursor , self.user_ID)
        
    def board(self):
        print("SQL about board")
        BOARD = Board.Board_Manager(-1, self.db, self.user_ID)
        BOARD.start()
        
    def notice(self):
        print("SQL about notice")
        
    def logout(self):
        print("\nLOGOUT , Go to start page.")
        input("\n\nPlease Enter to go to NEXT ! :")
        Login.start(self.db)
    
    def start(self):
        self.menu()
        choice = int(input("Enter the number of SQL content you want to see : "))

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
    
    

