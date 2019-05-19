# Board.py
import mysql.connector
import Board_Specific
import Menu
import os

class Board_Manager:
    def __init__(self, new_team_ID, db, new_user_ID):
        self.user_ID = new_user_ID
        self.count = 0
        self.mycursor = db.cursor()
        self.db = db
        self.Board_list={}
        self.team_ID = new_team_ID
    def board_list(self):
        self.db.commit()
        board_sql = "SELECT Board.Board_Title, Board.Board_ID FROM Board INNER JOIN BoardMember ON Board.Board_ID = BoardMember.Board_ID WHERE BoardMember.User_ID = '%s' AND Board.Is_deleted = 'N' " % self.user_ID
        self.mycursor.execute(board_sql)
        myresult = self.mycursor.fetchall()
        #list up the boards after the 1. create board, 2. delete board, 3. search 4. Go Back
        if myresult is not None:
            self.count = 5
            for (title, ID) in myresult:
                print(self.count, title)
                self.Board_list[self.count] = ID #form a dictionary {count:Board_ID}
                self.Max_Count = self.count
                self.count += 1
        # myresult = [('first', 1), ('second', 2), ('third', 3)]
        else:
            self.count = 0
            self.Max_Count = 0
    def board_create(self):
        self.db.commit()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Creating a new Board.\n")
        # Title = input("Title: ")
        # Visibility = input("\nVisibility. You can choose from 1.Disabled 2.Members. ")
        # Email_CSV = input("\nE-mails of the members. Seperated by comma \nex) first@gmail.com,second@gamil.com,third@gamil.com\nEnter 'no' if you wnat to skip\nenter here: ")
        # Com_Perm = input("\nComment permission\nYou can choose from 1.Disabled 2.Members. \nEnter the number of your choice: ")
        if self.team_ID == -1: #Board is created by a User, not a team.
            new_board = """INSERT into Board (User_ID, Board_Title, CommentPerm, AddRmPerm, Visibility)
                        Values ('%s', "AwesomeBoard3", "Members", "Members", "private")""" % self.user_ID
            self.mycursor.execute(new_board) #insert new tuple to the board table

            board_member_admin = """INSERT into BoardMember (Board_ID, User_ID, Permission)
                                    Values (LAST_INSERT_ID(), '%s', 'Admin')""" % self.user_ID
            self.mycursor.execute(board_member_admin)##insert new tuple to the boardmember table 

            # Email_CSV = "yujin@handong.edu,hyewon43@handong.edu"
            # Members_Email = Email_CSV.split(',')
            # for email in Members_Email:
            #     if email == "no":
            #         pass
            #     else:
            #         #search the User_ID with the email address and add them to the BoardMemeber table.
            #         sql = "SELECT User_ID FROM User WHERE User_Email = '%s'" % email
            #         self.mycursor.execute(sql)
            #         result = mycursor.fetchone()
            #         if result is None:
            #             pass
            #         else:
            #             Member_ID = result[0]
            #             board_member ="INSERT into boardmember (Board_ID, User_ID, Permission) VALUES (LAST_INSERT_ID(), %d, 'Member')" % Member_ID
            #             self.mycursor.execute(board_member)
            #             print("adding a new User to the board with email "+email, Member_ID)
        else:#Board is created by a team.
            new_board = """INSERT into Board (Team_ID, Board_Title, CommentPerm, AddRmPerm, Visibility)
                    Values (%d, "AwesomeBoard", "Members", "Members", "private")""" % self.team_ID
            self.mycursor.execute(new_board) #insert new tuple to the board table

        self.db.commit()
    def board_delete_close(self):
        self.db.commit()
        os.system('cls' if os.name == 'nt' else 'clear')
        option = input("1 Close\n2 Delete\nEnter your option:")
        if option == "1":
            close_or_open = input("1 Close\n2 Reopen\nEnter your option:")
            delete_target = input("Enter the number of the board you'd like to close or reopen: ")
            delete_target = int(delete_target)
            permission_sql = "SELECT Permission FROM BoardMember where Board_Id = %d AND User_ID = %d" % (self.Board_list[delete_target], self.user_ID)
            self.mycursor.execute(permission_sql)
            result = self.mycursor.fetchone();
            user_permission = result[0]
            if user_permission == "Admin":
                if close_or_open == "1":
                    sql = "UPDATE Board SET IsClosed = true WHERE Board_ID = %s"
                elif close_or_open == "2":
                    sql = "UPDATE Board SET IsClosed = false WHERE Board_ID = %s"
                try:
                    self.mycursor.execute(sql, (self.Board_list[delete_target],))
                except:
                    print("Wrong input! Try again")
            else:
                print("**You cannot close or reopen this Board. Only Admin User can.")

        elif option == "2":
            delete_target = input("Enter the number of the board you'd like to delete: ")
            delete_target = int(delete_target)
            permission_sql = "SELECT Permission FROM BoardMember where Board_Id = %d AND User_ID = %d" % (self.Board_list[delete_target], self.user_ID)
            self.mycursor.execute(permission_sql)
            result = self.mycursor.fetchone();
            user_permission = result[0]
            if user_permission == "Admin":
                sql = "UPDATE Board SET Is_deleted = 'Y' WHERE Board_ID = %d" % self.Board_list[delete_target]
                try:
                    self.mycursor.execute(sql)
                except:
                    print("Wrong input! Try again")
            else:
                print("**You cannot delete this Board. Only Admin User can.")
        else:
            print("Wrong input! Try again")
        self.db.commit()
        pause = input("Enter to continue")
        
    def board_search(self):
        self.db.commit()
        os.system('cls' if os.name == 'nt' else 'clear')
        search_target = input("Enter the title of the board: ")
        search_sql = """SELECT Board.Board_Title, Board.Board_ID FROM Board
        INNER JOIN BoardMember ON Board.Board_ID = BoardMember.Board_ID 
        WHERE BoardMember.User_ID = %s AND Board.Board_title = %s""" 
        self.mycursor.execute(search_sql,(self.user_ID, search_target))
        result = self.mycursor.fetchall()
        for (title, ID) in result:
            print(ID, title)
        
        Ans = input("Enter the number for the Board we want to access or 'no' to go back to previous page: ")
        try:
            Board_id = int(Ans)
        except:
            pass
        
        if Ans != "no":
            try:
                chosen_board = Board_Specific.Specific_Board_Manager(-1, Board_id, self.db, self.user_ID)
            except:
                print("Wrong input! Search again")
                pause = input("Enter to continue")
          
    def board_specific(self, choice):
        self.db.commit()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("You selected",self.Board_list[choice])
        chosen_board = Board_Specific.Specific_Board_Manager(-1,self.Board_list[choice], self.db, self.user_ID)
    def start(self):
        self.db.commit()
        os.system('cls' if os.name == 'nt' else 'clear')
        choice = 0
        while(choice != 4):
            print("1 Search\n2 Create Board\n3 Delete or Close Board\n4 Go Back\n-----------\nYour Boards\n-----------")
            self.board_list()
            choice = input("Enter the number for your choice: ")
            choice = int(choice)
            if choice == 1:
                self.board_search()
            elif choice == 2:
                self.board_create()
            elif choice == 3:
                self.board_delete_close()
            elif choice == 4:
                print("return to previous view")
                Menu.Menu(self.db, self.mycursor, self.user_ID)
            elif choice >= 5 and choice <= self.Max_Count:
                self.board_specific(choice)
            else:
                print("Wrong input! Tray again")
                pause= input("Enter to continue")
            os.system('cls' if os.name == 'nt' else 'clear')
# mycursor = ""                
# a =Board_Manager(-1, mydb, 1)
# a.start()
# print(mydb.cursor())
# chosen_board = Board_Specific.Specific_Board_Manager(2, mydb, "Handong")
