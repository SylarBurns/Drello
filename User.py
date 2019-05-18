
# coding: utf-8
import mysql.connector
import Menu
import os
import Login

class User:
    def __init__(self, db, cursor , user_ID):
        self.db = db
        self.cursor = cursor  
        self.user_ID = user_ID
        self.clear()
        self.start()     
    
    def usermenu(self):
        print("-----------USER SQL----------")
        print("1. Show user info")
        print("2. Edit user info")
        print("3. Leave drello")
        print("4. Back to Menu")
        print("-----------------------------")

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')    

    def showinfo(self):
        self.clear()
        sql = "SELECT * from User WHERE User_ID = '%d'" % self.user_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        print("\n           <USER INFO>     ")
        print(" ● ID : " + result[0][1])
        print(" ● PW : " + result[0][2])
        print(" ● Email : " + result[0][3])
        print(" ● Name : " + result[0][4])
        print(" ● Language : " + result[0][5])
        print(" ● profile : " + result[0][6])
        print("\n")
        self.clear()
        
    def editinfo(self):
        Email = "JC@handong.edu"
        Name = "JC"
        self.clear()
        print("----------Edit User------------")
        print("1. Change Password ")
        print("2. Change others ")
        print("-------------------------------")
        c = int(input("Enter you want to change : "))

        if(c==1) : 
            self.clear()
            print("\n<SECURITY> EDIT PASSWORD \n")
            print("ENTER YOUR Email and Name to verify\n")
            print(" ● Email : " + Email)
            print(" ● Name : " + Name)
            # print("CHECK DataBase ...")

            sql = "SELECT User_Email, User_Name From User \
                WHERE User_ID = '%d' AND Is_deleted='N'" \
                    % (self.user_ID)
            self.cursor.execute(sql)
            users = self.cursor.fetchall()
        
            if(users[0][0] == Email and users[0][1] == Name ) : 
                PW = "1004"
                print("Verified. You can change your password.")
                print("Change password to %s\n\n" % PW)

                sql = "UPDATE User Set User_PW = '%s' \
                    WHERE User_ID = '%d'" % (PW , self.user_ID)
                self.cursor.execute(sql)
                self.db.commit()
            else :
                print("\nNOT Verified. \nYou can not change your password.")
            # self.clear()

        elif (c==2) :   
            self.clear()
            print("\n<NORMAL>")

            Email = "JJCC@handong.edu"
            Language = "English"
            Profile = "Happy handong life :)"
            Name = "JC"

            print("ENTER YOUR INFO to want to change\n")
            print(" ● Email : %s" %Email)
            print(" ● Name : %s" %Name)
            print(" ● Language :%s" %Language)
            print(" ● Profile : %s" %Profile)

            sql = "UPDATE User \
                SET User_Language = '%s' ,User_Profile = '%s' \
                    ,User_Name = '%s' ,user_Email = '%s'\
                WHERE User_ID = '%d'" % (Language , Profile, Name, Email, self.user_ID )
            self.cursor.execute(sql)
            self.db.commit()

            print("\nSuccessfully edited User info\n\n")
            
            # self.clear()
        else :
            print("wrong number\n")
        input("\nEnter to next : ")
        self.clear()
        
    def leaving(self):
        # user뿐 아니라 다른 table에서도 다 지워야 함
        # is_Delete 값 변경
        sql = "UPDATE User SET Is_deleted = 'Y' WHERE User_ID = '%d'" % self.user_ID
        self.cursor.execute(sql)
        self.db.commit()
        print("\nSUCCESS : DELETE Your ID")
        print("Leaving Drello. JOIN AGAIN.")
        
        input("\n\nPlease Enter to go to NEXT ! :")
        Login.start(self.db)
        

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
            Menu.Menu(self.db, self.cursor , self.user_ID)
        else :
            "잘못 누르셨습니다."

        # input("\n\nPlease Enter to go to NEXT ! :")
        self.start()

