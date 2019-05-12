# Board.py
# import mysql.connector
import Board_Specific
import Menu
import os
# mydb = mysql.connector.connect(
#     host ='localhost',
#     user='root',
#     passwd='mz0090mz',
#     database="testdb"
# )
# mycursor = mydb.cursor()

class Board_Manager:
    def __init__(self, new_user_ID, new_cursor):
        self.user_ID = new_user_ID
        self.count = 5
        self.mycursor = new_cursor
        self.Board_list={}
    def board_list(self):
        # board_sql = "SELECT Board_Title, Board_ID FROM Board INNER JOIN BoardMember ON Board.User_ID = BoardMember.User_ID WHERE BoardMember.User_ID = %s"
        # self.mycursor.execute(board_sql, (self.user_ID))
        # myresult = self.mycursor.fetchall()
        # #list up the boards after the 1. create board, 2. delete board, 3. search
        # for (title, ID) in myresult:
        #     print(self.count+". "+title)
        #     self.Board_list[self.count] = ID #form a dictionary {count:Board_ID}
        #     self.count += 1
        myresult = [('first', 1), ('second', 2), ('third', 3)]
        for (title, ID) in myresult:
            print(self.count, title)
            self.Board_list[self.count] = ID #form a dictionary {count:Board_ID}
            self.count += 1
            self.Max_Count = self.count
        self.count = 5
    def board_create(self):
        print("Creating a new Board. Please enter the information required below\n")
        Title = input("Title: ")
        Visibility = input("\nVisibility. You can choose from 1.Disabled 2.Members. ")
        Email_CSV = input("\nE-mails of the members. Seperated by comma \nex) first@gmail.com,second@gamil.com,third@gamil.com\nEnter 'no' if you wnat to skip\nenter here: ")
        Com_Perm = input("\nComment permission\nYou can choose from 1.Disabled 2.Members. \nEnter the number of your choice: ")
        Members_Email = Email_CSV.split(',')
        
        # for email in Members_Email:
        #     if email == "no":
        #         pass
        #     else:
        #         print(mem)#search the User_ID with the email address and add them to the BoardMemeber table.
        #         sql = "SELECT User_ID FROM User WHERE Email = %s"
        #         self.mycursor.execute(sql, email)
        #         Member_ID = mycursor.fetchone()
        #         if Member_ID is None:
        #             pass
        #         else:
        #             sql ="INSERT board (Board_ID, User_ID) VALUES (%s, %s)"
        #             self.mycursor.execute(sql,(Member_ID, Board_ID))
    def board_delete(self):
        delete_target = input("Enter the number of the board you'd like to delete")
        print("The Board_ID of the board you want to delete is"+self.Board_list[delete_target])
    def board_search(self):
        search_target = input("Enter the title of the board: ") 
    def board_specific(self, choice):
        #choice가 board_ID 인건가요  ? ?  ?
        print("You selected",self.Board_list[choice])
        chosen_board = Board_Specific.Specific_Board_Manager(self.Board_list[choice],self.mycursor)
    def start(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Let's get this party started!")
        choice = 0
        while(choice != 4):
            print("1 Search\n2 Create Board\n3 Delete Board\n4 Go Back\n-----------\nYour Boards\n-----------")
            self.board_list()
            choice = input("Enter the number for your choice: ")
            choice = int(choice)
            if choice == 1:
                self.board_search()
            elif choice == 2:
                self.board_create()
            elif choice == 3:
                self.board_delete()
            elif choice == 4:
                print("return to previous view")
                Menu.Menu(self.mycursor , self.user_ID)
            elif choice >= 5 and choice <= self.Max_Count:
                self.board_specific(choice)

            os.system('cls' if os.name == 'nt' else 'clear')
# mycursor = ""                
# a =Board_Manager(55, mycursor)
# a.start()
