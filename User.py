
# coding: utf-8

# In[ ]:

import Menu

def user():
    print("1. Show user info")
    print("2. Edit user info")
    print("3. Leave drello")
    print("4. Back to Menu")
    choice = int(input("Enter the number for your choice: "))

    if(choice == 1) :
        showinfo()
    elif(choice ==2):
        editinfo()
    elif(choice ==3):
        leaving()
    elif(choice ==4):
        Menu.menu()
    else :
        "잘못 누르셨습니다."
        user()
        
        
def showinfo():
    print("showinfo")
    
def editinfo():
    print("editinfo")
    
def leaving():
    print("leaving")

