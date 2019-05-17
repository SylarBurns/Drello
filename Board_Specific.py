# from list_part import *
import os
import Thanos
from list_part import *
import mysql.connector
class Specific_Board_Manager:
    def __init__(self, new_Team_ID, new_Board_ID, db, new_User_ID):
        self.Board_ID = new_Board_ID
        self.Team_ID = new_Team_ID
        self.User_ID = new_User_ID
        self.db = db
        self.mycursor = self.db.cursor()
        self.count = 0
        self.Max_Count = 0;
        self.Notice_list={}
        
        if self.Team_ID == -1: #if team information is not given.
            sql = "SELECT Permission FROM BoardMember where Board_Id = %d AND User_ID = %d" % (self.Board_ID, self.User_ID)
            self.mycursor.execute(sql)
            result = self.mycursor.fetchone();
            self.User_Perm = result[0]
        else:# if the board belongs to a team.
            sql = "SELECT Permission FROM TeamMember where Team_Id = %d AND User_ID = %d" % (self.Team_ID, self.User_ID)
            self.mycursor.execute(sql)
            result = self.mycursor.fetchone();
            if result[0] == 'Y':
                self.User_Perm = "Admin"
            else:
                self.User_Perm = "Member"
        
        sql = "SELECT Board_title From Board Where Board_ID = %d" % self.Board_ID
        self.mycursor.execute(sql)
        self.board_title = self.mycursor.fetchone()[0]
        self.start()

    def board_info(self):
        print("{0:-^30}".format("Board Information"))
        sql = "SELECT Board.Board_title From Board Where Board.Board_ID = %d" % self.Board_ID
        self.mycursor.execute(sql)
        Title = self.mycursor.fetchone()
        print("Title: "+Title[0])

        if self.Team_ID != -1: #if the board belongs to a team
            sql = "SELECT Team.Name From Team, Board Where Board.Board_ID = %d AND Board.Team_ID = Team.Team_ID" % self.Board_ID
            self.mycursor.execute(sql)
            Title = self.mycursor.fetchone()
            if Title is None:
                pass
            else:
                print("Team: "+title[0])
        else:#if the board belongs to a User
            sql = "SELECT User.Login_ID From BoardMember, User Where BoardMember.Board_ID = %d AND BoardMember.Is_deleted='N' AND BoardMember.User_Id = User.User_ID" % self.Board_ID
            self.mycursor.execute(sql)
            Members = self.mycursor.fetchall()
            print("Members:")
            for Login_ID in Members:
                print("\t-"+Login_ID[0])

        sql = "SELECT * FROM Watch Where Watch.User_ID = %d AND Watch.ID_type = 'BOARD' AND Watch.ID = %d" % (self.User_ID, self.Board_ID)
        self.mycursor.execute(sql)
        Watch = self.mycursor.fetchone()
        if Watch is None:
            print("Watch: X")
        else:
            print("Watch: O")

        sql = "SELECT Labels.Name, Labels.Color FROM Labels where Labels.Board_ID = %d" % self.Board_ID
        self.mycursor.execute(sql)
        Labels = self.mycursor.fetchall()
        print("Labels: ")
        for (Name, Color) in Labels:
            print("\t-"+Name+" "+Color)
        print("{0:-^30}".format(""))
    def board_toggle_watch(self):
        print("Toggling the watch info")
        sql = "SELECT * From Watch where Watch.ID_type = 'BOARD' AND Watch.ID = %d AND Watch.User_ID = %d" % (self.Board_ID, self.User_ID)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchone()
        
        if result is None: #if there is no watch information
            sql = "INSERT into watch (User_ID, ID_type, ID) VALUES (%d, 'BOARD', %d)" % (self.User_ID, self.Board_ID)
            self.mycursor.execute(sql)
            Action = "Checked Watch for Board %s" % self.board_title
            Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
        else:
            sql = "DELETE From Watch WHERE Watch.ID = %d AND Watch.User_ID = %d AND Watch.ID_type ='BOARD'" % (self.Board_ID, self.User_ID)
            self.mycursor.execute(sql)
            Action = "Unchecked Watch for Board %s" % self.board_title
            Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
        self.db.commit()
    def board_edit(self):    
        choice = 0
        while(choice != 8):
            os.system('cls' if os.name == 'nt' else 'clear')
            print("{0:-^30}".format("Start editing"))
            print("1 Board Title\n2 Comment Permission \n3 Add Remove Permission\n4 Visibility\n5 Members\n6 Team\n7 Labels\n8 Go Back")
            Ans = input("Enter your choice: ")
            choice = int(Ans)
            if choice == 1:#Board Title
                new_title = input("Enter the new title: ")
                sql = "UPDATE Board SET Board_title = %s WHERE Board_ID = %s"
                self.mycursor.execute(sql, (new_title, self.Board_ID))
                print("Board title has been changed to '%s'" % new_title)
                Action = "Changed Board title from '%s' to '%s'" % (self.board_title, new_title)
                Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                self.db.commit()
            elif choice == 2:#Comment Permission
                if self.User_Perm == "Admin":#Permission Check
                    Ans = input("Choose from Below: \n1 Disabled(No one can add Comments)\n2 Member(Members can add Comments)\n:")
                    new_perm = int(Ans)
                    if new_perm == 1:
                        sql = "UPDATE Board SET CommentPerm = 'Disabled' WHERE Board_ID = %d" % self.Board_ID
                        self.mycursor.execute(sql)
                        Action = "changed Comment Permission of '%s' to 'Disabled' " % self.board_title
                        Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                  
                    elif new_perm == 2:
                        sql = "UPDATE Board SET CommentPerm = 'Member' WHERE Board_ID = %d" % self.Board_ID
                        self.mycursor.execute(sql)
                        Action = "changed Comment Permission of '%s' to 'Member' " % self.board_title
                        Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                    else:
                        print("Wrong input! Try Again")
                    print("Change has been made")
                    self.db.commit()
                else:
                    print("You can't change comment permission of this Board. Only the admin User can.")

            elif choice == 3:#Add Remove Permission
                if self.User_Perm == "Admin":#Permission Check
                    Ans = input("Choose from Below: \n1 Admin(Only Admin User can add new members)\n2 Member(Members can also add new members)\n:")
                    new_perm = int(Ans)
                    if new_perm == 1:
                        sql = "UPDATE Board SET AddRmPerm = 'Admin' WHERE Board_ID = %d" % self.Board_ID
                        self.mycursor.execute(sql)
                        Action = "changed Add/Remove Permission of '%s' to 'Admin' " % self.board_title
                        Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                    elif new_perm == 2:
                        sql = "UPDATE Board SET AddRmPerm = 'Member' WHERE Board_ID = %d" % self.Board_ID
                        self.mycursor.execute(sql)
                        Action = "changed Add/Remove Permission of '%s' to 'Member' " % self.board_title
                        Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                    else:
                        print("Wrong input! Try Again")
                    print("Change has been made")
                    self.db.commit()
                else:
                    print("You can't change comment permission of this Board. Only the admin User can.")

            elif choice == 4:#Visibility
                if self.User_Perm == "Admin":#Permission Check
                    Ans = input("Choose from Below: \n1 Public \n2 Private\n:")
                    new_perm = int(Ans)
                    if new_perm == 1:
                        sql = "UPDATE Board SET Visibility = 'Public' WHERE Board_ID = %d" % self.Board_ID
                        self.mycursor.execute(sql)
                        Action = "changed Visibility of '%s' to 'Public' " % self.board_title
                        Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                    elif new_perm == 2:
                        sql = "UPDATE Board SET Visibility = 'Private' WHERE Board_ID = %d" % self.Board_ID
                        self.mycursor.execute(sql)
                        Action = "changed Visibility of '%s' to 'Private' " % self.board_title
                        Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                    else:
                        print("Wrong input! Try Again")
                    print("Change has been made")
                    self.db.commit()
                else:
                    print("You can't change visibility of this Board. Only the admin User can.")
            elif choice == 5: # Members
                sql = "SELECT AddRmPerm FROM Board where Board_Id = %d" % self.Board_ID
                self.mycursor.execute(sql)
                result = self.mycursor.fetchone();
                Board_AddRmPerm = result[0]
        
                Current_Perm = 'N'
                if Board_AddRmPerm == 'Admin': # When the AddRmPerm of Board is Admin, we want only the admin user can add new members
                    if self.User_Perm == 'Admin':
                        Current_Perm = 'Y'
                    else:
                        Current_Perm = 'N'
                        print("You can't add or delete new Members to this Board Only the admin User can.")
                else:# if the AddRmPerm is not Admin, then any member can add new members
                    Current_Perm = 'Y'

                if Current_Perm == 'Y':
                    Ans = input("1 Add new User\n2 Delete a User\n:")
                    Add_or_Delete = int(Ans)
                    if Add_or_Delete == 1:
                        # ID_CSV = "cs_love,math,gyqls,Handong,PerfectGuy"
                        ID_CSV = input("Enter the Login ID of new Members. Separate them by comma ex)ID,ID2,ID3\n:")
                        Members_ID = ID_CSV.split(',')
                        for Login_ID in Members_ID:
                            #search the User with the User_ID and add them to the BoardMemeber table.
                            sql = "SELECT User_ID FROM User WHERE Login_ID= %s AND is_deleted ='N'" 
                            self.mycursor.execute(sql, (Login_ID))
                            result = self.mycursor.fetchone()
                            if result is None:
                                print("We can't find any user with "+ Login_ID)# When the User is not on our database
                                pass
                            else:# When the User exists on our database
                                new_Member_ID = result[0]#integer value
                                if self.Team_ID == -1: #when the board belongs to a user
                                    try:
                                        sql ="SELECT User_ID, Is_deleted From BoardMember WHERE Board_ID = %d AND User_ID = %d" % (self.Board_ID, new_Member_ID)
                                        self.mycursor.execute(sql)
                                        result = self.mycursor.fetchone()
                                        if result is None:
                                            sql ="INSERT into BoardMember(Board_ID, User_ID, Permission) VALUES(%d, %d, 'Member')" % (self.Board_ID, new_Member_ID)
                                            self.mycursor.execute(sql)
                                            print("adding a new User to the board with ID "+ Login_ID)
                                            Action = "invited %s to the board %s" % (Login_ID, self.board_title)
                                            Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                                        elif result[1] == 'N':#if the user is already on the board
                                            print(Login_ID+" is already a member of this board")
                                        elif result[1] == 'Y':#if the user is already on our database but also deleted
                                            sql = "UPDATE BoardMember SET Is_deleted = 'N' WHERE Board_ID = %d AND User_ID = %d" % (self.Board_ID, new_Member_ID)
                                            self.mycursor.execute(sql)
                                            print("Old member "+Login_ID+" has rejoined on this board.")
                                            Action = "reinvited %s to the board %s" % (Login_ID, self.board_title)
                                            Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                                    except:
                                        print("Error occured on Adding a new User")
                                else:#When the board belongs to a team
                                    try:
                                        sql ="SELECT User_ID, Is_deleted From TeamMember WHERE Team_ID = %d AND User_ID = %d" % (self.Team_ID, new_Member_ID)
                                        self.mycursor.execute(sql)
                                        result = self.mycursor.fetchone()
                                        if result is None:
                                            sql ="INSERT into TeamMember(Team_ID, User_ID, Permission) VALUES(%d, %d, 'Member')" % (self.Team_ID, new_Member_ID)
                                            self.mycursor.execute(sql)
                                            print("adding a new User to the team/board with ID "+ Login_ID)
                                            Action = "invited %s to the team that board %s belongs to" % (Login_ID, self.board_title)
                                            Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                                        elif result[1] == 'N':#if the user is already on the board
                                            print(Login_ID+" is already a member of this Team")
                                        elif result[1] == 'Y':#if the user is already on our database but also deleted
                                            sql = "UPDATE TeamMember SET Is_deleted = 'N' WHERE Team_ID = %d AND User_ID = %d" % (self.Team_ID, new_Member_ID)
                                            self.mycursor.execute(sql)
                                            print("Old member "+Login_ID+" has rejoined on this team/board.")
                                            Action = "reinvited %s to the team that board %s belongs to" % (Login_ID, self.board_title)
                                            Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                                    except:
                                        print("Error occured on Adding a new User")
                                    
                    elif Add_or_Delete == 2:
                        ID_CSV = input("Enter the ID of Members you wish to delete. Separate them by comma ex)ID,ID2,ID3\n:")
                        Members_ID = ID_CSV.split(',')
                        for Login_ID in Members_ID:
                            #search the User_ID with the ID and set Is_deleted to 'Y' on the BoardMemeber table.
                            if self.Team_ID == -1:#delete from BoardMember
                                sql = "SELECT BoardMember.User_ID FROM BoardMember, User \
                                    WHERE BoardMember.User_ID = User.User_ID AND User.Login_ID = %s \
                                    AND BoardMember.Board_ID = %s AND BoardMember.Is_deleted = 'N'"
                                self.mycursor.execute(sql, (Login_ID, self.Board_ID))
                                result = self.mycursor.fetchone()
                                if result is None:
                                    print("We can't find any user with "+ Login_ID +" from this Board")
                                    pass
                                else:
                                    old_Member_ID = result[0]#integer value
                                    try:
                                        sql = "UPDATE BoardMember SET Is_deleted = 'Y' WHERE Board_ID = %d AND User_ID = %d" % (self.Board_ID, old_Member_ID)
                                        self.mycursor.execute(sql)
                                        print("Deleting "+ Login_ID+" from this board")
                                        Action = "deleted %s from board %s" % (Login_ID, self.board_title)
                                        Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                                    except:
                                        print("error occured on deleting a user")
                            else:#delete from TeamMember
                                sql = "SELECT TeamMember.User_ID FROM TeamMember, User \
                                    WHERE TeamMember.User_ID= User.User_ID AND User.Login_ID = %s\
                                    AND TeamMember.Team_ID = %s AND TeamMember.Is_deleted = 'N'" 
                                self.mycursor.execute(sql, (Login_ID, self.Team_ID))
                                result = self.mycursor.fetchone()
                                if result is None:
                                    print("We can't find any user with "+ Login_ID +" from this Team")
                                    pass
                                else:
                                    old_Member_ID = result[0]#integer value
                                    try:
                                        sql = "UPDATE TeamMember SET Is_deleted = 'Y' WHERE Team_ID = %d AND User_ID = %d" % (self.Team_ID, old_Member_ID)
                                        self.mycursor.execute(sql)
                                        print("Deleting "+ Login_ID+" from this Team")
                                        Action = "deleted %s from team that board %s belongs to" % (Login_ID, self.board_title)
                                        Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                                    except:
                                        print("error occured on deleting a user")
                    else:
                        print("Wrong input! Tray again.")
                self.db.commit()

            elif choice == 6: # add new Team
                
                sql = "SELECT AddRmPerm FROM Board where Board_Id = %d" % self.Board_ID
                self.mycursor.execute(sql)
                result = self.mycursor.fetchone();
                Board_AddRmPerm = result[0]
                Current_Perm = 'N'
                if Board_AddRmPerm == 'Admin': # When the AddRmPerm is Admin, we want only the admin user can add new members or team
                    if self.User_Perm == 'Admin':
                        Current_Perm = 'Y'
                    else:
                        Current_Perm = 'N'
                        print("You can't add or delete new Members to this Board Only the admin User can.")
                else:# if the AddRmPerm is not Admin, then any member can add new members
                    Current_Perm = 'Y'

                if Current_Perm == 'Y':
                    sql = """SELECT Board.Team_ID, Team.Name 
                    From Board, Team 
                    Where Board.Board_ID = %d AND Team.Team_ID = Board.Team_ID """ % (self.Board_ID)
                    self.mycursor.execute(sql)
                    existing_team = self.mycursor.fetchone()

                    if existing_team is not None:#if the board already has a team
                        print("Your Board already has a team Named "+ existing_team[1])
                        Ans = input("Do you want to change the team?\n1 Yes\n2 No")
                        choice = int(Ans)
                        if choice == 1:
                            Ans = input("Enter the Name of the new team: ")
                            sql = "SELECT Team.Team_ID, Team.Name From Team, TeamMember Where Team.Name = '%s' AND Team.Team_ID = TeamMember.Team_ID AND TeamMember.User_ID = %d "% (Ans, self.User_ID)
                            # find the team that the user is a member of and has the name that the user entered
                            self.mycursor.execute(sql)
                            new_Team = self.mycursor.fetchone()
                            if new_Team is None:
                                print("Cannot find a team with Name "+ Ans)
                            else:
                                sql = "UPDATE Board SET Team_ID = %d WHERE Board_ID = %d" % (new_Team[0], self.Board_ID)
                                Action = "changed The Team of the Board %s to %s" % (self.board_title, new_Team[0])
                                Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                        elif choice == 2:
                            pass
                        else:
                            print("Wrong input! Try again")
                    else: #When there is no Team
                        print("You must create a board on the team menu in order to add a board to a team")
                        # Ans = input("Enter the Name of the new team: ")
                        # sql = "SELECT Team.Team_ID Name From Team, TeamMember Where Team.Name = '%s' AND Team.Team_ID = TeamMember.Team_ID AND TeamMember.User_ID = %d "% (Ans, self.User_ID)
                        # # find the team that the user is a member and has the name that the user entered
                        # self.mycursor.execute(sql)
                        # new_Team = self.mycursor.fetchone()
                        # if new_Team is None:
                        #     print("Cannot find a team with Name "+ Ans)
                        # else:
                        #     sql = "UPDATE Board SET Team_ID = %d WHERE Board_ID = %d" % (new_Team[0], self.Board_ID)
                self.db.commit()

            elif choice == 7: #Labels
                Ans = input("1 Add new label\n2 Delete label\n:")
                Add_or_Delete = int(Ans)
                if Add_or_Delete == 1:
                    label_name = input("Label Name: ")
                    Label_color = input("Label Color: ")
                    sql = "INSERT into Labels(Board_ID, Name, Color) Values (%s, %s, %s)"
                    self.mycursor.execute(sql, (self.Board_ID, label_name, Label_color))
                    Action = "added new label %s to %s" % (label_name, self.board_title)
                    Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                elif Add_or_Delete == 2:
                    sql = "SELECT Labels.Label_ID, Labels.Name, Labels.Color FROM Labels where Labels.Board_ID = %d" % self.Board_ID
                    self.mycursor.execute(sql)
                    Labels = self.mycursor.fetchall()
                    print("Labels: ")
                    for (ID, Name, Color) in Labels:
                        print("\t-",ID,Name+Color)
                    Ans = input("Enter the number of the label you want to delete")
                    delete_target = int(Ans)
                    sql = "DELETE from Labels WHERE Labels.Label_ID = %d" % delete_target
                    try:
                        self.mycursor.execute(sql)
                        Action = "deleted label %s to %s" % (label_name, self.board_title)
                        Thanos.Activity_notice("BOARD", self.Board_ID, self.User_ID, self.db, Action)
                    except:
                        print("Failed to delelte the label you selected.")
                else:
                    print("Wrong input! Try Again")
                self.db.commit()
            elif choice == 8:
                print("{0:-^30}".format("Finish editing"))
            else:
                print("Wrong input! Try again")
            pause = input("Enter to continue")
        
    def lists(self):
        print("Entering the list of lists")
        ListofLists(self.Board_ID, self.db, self.User_ID)
    def board_notice(self):
        print("{0:-^30}".format("Your Notices"))
        sql = """SELECT Activity.Activity_ID, User.Login_ID, Activity.Action 
        From Activity, Notice, User
        Where Activity.Board_ID = %d AND Notice.User_ID = %d AND Notice.User_ID = User.User_ID
        AND Activity.Activity_ID = Notice.Activity_ID AND Notice.Is_read = 'N'""" % (self.Board_ID, self.User_ID)
        self.mycursor.execute(sql)
        myresult = self.mycursor.fetchall()
        #select all notices with in this Board.
        # myresult = [('firstNotice', 1), ('secondNotice', 2), ('thirdNotice', 3)]
        if myresult is not None:
            self.count = 5
            for (Activity_ID, Login_ID, Action) in myresult:
                print(self.count, Login_ID+" "+Action)
                self.Notice_list[self.count] = Activity_ID #form a dictionary {count:Board_ID}
                self.Max_Count = self.count
                self.count += 1
        else:
            self.count = 0
            self.Max_Count = 0
        print("{0:-^30}".format(""))
    def board_notice_check(self, choice):
        sql = "UPDATE Notice SET Is_read = 'Y' WHERE Notice.User_ID = %d AND Notice.Activity_ID = %d "% (self.User_ID, self.Notice_list[choice])
        self.mycursor.execute(sql)
        self.db.commit()
        print("Marked notice",self.Notice_list[choice],"as read")
    def start(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        sql = "SELECT IsClosed From Board Where Board_ID = %d" % self.Board_ID
        self.mycursor.execute(sql)
        result = self.mycursor.fetchone()
        Is_Closed = result[0]

        if Is_Closed == 0 or self.User_Perm == "Admin":
            choice = 0
            while(choice != 4):
                self.board_info()
                print("1 View Lists\n2 Toggle Watch\n3 Edit Board Information\n4 Go Back")
                self.board_notice();
                if self.User_Perm == "Admin":
                    print("**You have the Admin Permission for this Board")
                Ans = input("Enter the number for your choice: ")
                choice = int(Ans)
                if choice == 1:
                    self.lists()
                elif choice == 2:
                    self.board_toggle_watch()
                elif choice == 3:
                    self.board_edit()
                elif choice == 4:
                    print("return to previous view")
                elif self.count >= 5 and choice <= self.Max_Count:
                    self.board_notice_check(choice)
                else:
                    print("Wrong input! Try Again")
                    pause = input("Enter to continue")
                    os.system('cls' if os.name == 'nt' else 'clear')
        elif Is_Closed == 1 and self.User_Perm == 'Member':
            print("**This Board is currently closed. Only admin User can gain access to this board")
            pause = input("Enter to continue")
        else:
            print("error occured on opening the Board.")
            pause = input("Enter to continue")
        

