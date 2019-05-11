
# coding: utf-8

# In[ ]:

import Menu

def start():
    print("--------- Welcom Drello -----------")
    print("1. LOGIN")
    print("2. JOIN")
    print("-----------------------------------")
    choice = int(input("Enter the number for your choice: "))

    if choice == 1:
        login()
        Menu.menu()
    elif choice == 2:
        join()
        Menu.menu()
    else :
        print("다시 입력해주세요.")
        start()

def login():
    print("login")
def join():
    print("join")
    print("auto login")

