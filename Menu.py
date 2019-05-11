
# coding: utf-8
import User
import Login
import Team

def menu():
    # while(True):
    print("--------------------------")
    print("1. USER")
    print("2. TEAM")
    print("3. BOARD")
    print("4. NOTICE")
    print("5. LOGOUT")
    print("--------------------------")
    choice = int(input("Enter the number for your choice: "))

    if(choice == 1) :
        user()
    elif(choice ==2):
        team()
    elif(choice ==3):
        board()
    elif(choice==4):
        notice()
    elif(choice==5):
        logout()
    else:
        print("잘못 누르셨습니다.")
        menu()
        
def user():
    print("SQL about user")
    User.user()
    
def team():
    print("SQL about team")
    Team.team()
    
def board():
    print("SQL about board")
    
def notice():
    print("SQL about notice")
    
def logout():
    print("logout")
    Login.start()
    
    

