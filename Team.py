import mysql.connector
import Menu
import Board
import Board_Specific
import os

db = mysql.connector.connect(
  host="mydbinstance.cbp3whb5qyie.us-east-2.rds.amazonaws.com",
  port=3306,
  user="gyqls",
  passwd="rnjssmdsoRj1",
  database = "Drello"
)
cursor = db.cursor()
user_ID = 1

class Team:
    def __init__(self, db, cursor , user_ID):
        self.db = db
        self.cursor = cursor   
        self.user_ID = user_ID
        self.team_ID = 0
        self.start()   
        
    def teamlist(self):
        # 속한 팀 보여주기
        self.clear()
        # print("-----------------------------")
        print("----------Your Team----------")
        # print("-----------------------------")
        sql = "select T.Team_ID, T.Name \
                from Team as T\
                JOIN TeamMember as TM\
                ON T.Team_ID = TM.Team_ID \
                WHERE TM.User_ID = '%d' AND TM.Is_deleted = 'N' AND T.Is_deleted = 'N'" % self.user_ID
                
        self.cursor.execute(sql)
        teams = self.cursor.fetchall()

        for (team_ID, team_name) in teams :
            print( " " +str(team_ID) + " : " + team_name)

        print("-----------------------------")
        print(" + : Create Team")
        print(" 0 : Back to Menu")
        print("-----------------------------")
        choice = input(" Enter Team number : ")
        if(choice == "0"):
            Menu.Menu(self.db, self.cursor , self.user_ID)
        elif(choice == "+"):
            self.createTeam()
        elif(choice != "0"):
            # 팀 넘버 존재 체크
            self.team_ID = int(choice)  
            self.selectTeam()
        else :
            print("Wrong input. Enter again.")
            self.teamlist()
        
        

    def selectTeam(self):
        self.clear()

        sql = "Select Name from Team WHERE Team_ID = '%s'" % self.team_ID
        self.cursor.execute(sql)
        team_name = self.cursor.fetchall()
        print("--------Team : %s ---------" % team_name[0][0])
        print(" 1. Edit team profile")
        print(" 2. Team's Boards")
        print(" 3. Team's Members")
        print(" 4. Delete Team")
        print(" 5. Back")
        print("---------------------------------")

        choice = int(input(" Enter the number for your choice: "))
        if(choice == 1):
            print("edit profile")
            self.editTeamProfile()
        elif(choice ==2):
            self.teamsBoard()
        elif(choice ==3):
            self.clear()
            self.teamsMember()
        elif(choice ==4):
            self.deleteTeam()
        elif(choice ==5):
            self.teamlist()
        else :
            print("잘 못 누르셨습니다.")
            self.selectTeam()

    def editTeamProfile(self):
        self.clear()
        while(True):
            sql = "Select * from Team WHERE Team_ID = '%s'" % self.team_ID
            self.cursor.execute(sql)
            team = self.cursor.fetchall()
            YesOrNo = team[0][5] 
            if(YesOrNo == "Y") :
                private_public = "public"
                changed = "private"
                YesOrNo = "N"
            else :
                private_public = "private"
                changed = "public"
                YesOrNo = "Y"

            print("------------Team Profile------------")
            print(" 1. Name : %s" % team[0][1] ) 
            print(" 2. ShortName : %s" %team[0][2])
            print(" 3. Website : %s" %team[0][3])
            print(" 4. Description(optional) : %s" % team[0][4]) 
            print(" 5. %s" %private_public )
            print("------------------------------------")
            print(" 6. Back")
            choice = int(input("\nEnter Number you want to edit: "))
            if(choice == 1):
                name = input("\nName : ")
                sql = "Update Team Set Name = '%s' WHERE Team_ID = '%d'" % (name, self.team_ID)
                print("Team Name is changed\n")
            elif(choice == 2):
                Shortname = input("\nShortName : ")
                sql = "Update Team Set ShortName = '%s' WHERE Team_ID = '%d'" % (Shortname, self.team_ID)
                print("Team ShortName is changed\n")
            elif(choice == 3):
                website = input("Website : ")
                sql = "Update Team Set Website = '%s' WHERE Team_ID ='%d' " % (website, self.team_ID)
                print("Team Website is changed\n")
            elif(choice == 4):
                Description = input("Description : ")
                sql = "Update Team Description = '%s' WHERE Team_ID = '%d'" % (Description, self.team_ID)
                print("Team Description is changed\n")
            elif(choice == 5) :
                sql = "Update Team Set Visibility = '%s' WHERE Team_ID = '%d'" % (YesOrNo , self.team_ID)
                print("%s to %s\n" % (private_public , changed))
            elif(choice == 6):
                self.selectTeam()
            else :
                print("wrong choice, Enter the number again\n")
                
            self.cursor.execute(sql)
            self.db.commit()


    def teamsBoard(self):
        BOARD = Board.Board_Manager(self.team_ID,self.db, self.user_ID)
        self.clear()
        print("----------Team's Board------------")
        sql = "select Board_ID, Board_Title from Board \
            Where Team_ID = '%s'" % self.team_ID
        self.cursor.execute(sql)
        boards = self.cursor.fetchall()
        i = 1
        for board in boards :
            print("\n ● %d. %s\n" % (i, board[1]))
            i = i+1
        print("----------------------------------")
        print(" + : Create Board")
        print(" 0 : Back")

        choice = (input("Enter Board number : "))
        if(choice == "0"):
            self.selectTeam()
        elif(choice == "+"):
            BOARD.board_create()
            print("board_create")
        elif(int(choice) <= len(boards) and int(choice) !=0): 
            #  new_Team_ID, new_Board_ID, db, new_User_ID) 
            c = int(choice)
            Board_Specific.Specific_Board_Manager(self.team_ID, boards[c-1][0], self.db, self.user_ID)
            print("board specific")
        else :
            print("Wrong input. Enter again.")
            self.teamsBoard() 

    def teamsMember(self):
        self.clear()
        sql = "SELECT U.User_Name, U.Login_ID, TM.Permission, TM.User_ID \
            FROM Team as T, TeamMember as TM, User as U \
            WHERE T.Team_ID = TM.Team_ID AND TM.User_ID = U.User_ID \
                AND TM.Is_deleted = 'N' AND TM.Team_ID = '%d'" %(self.team_ID)
        self.cursor.execute(sql)
        users = self.cursor.fetchall()
        i = 1
        print("-------------Team Members(%d)------------" % len(users))
        for (username, userid, permission, u_id) in users :
            if(permission == "Y") :
                Normal_or_Admin = "Admin"
            else :
                Normal_or_Admin = "Normal"
            print(" ● %d. %s @%s (%s)" % (i, username, userid, Normal_or_Admin))
            i = i + 1
        print("------------------------------------------")

        sql = "Select Permission From TeamMember Where User_ID = '%s'" % (self.user_ID)
        self.cursor.execute(sql)
        Normal_or_Admin = self.cursor.fetchall()

        if(Normal_or_Admin[0][0] == "Y"):
            self.AdminUser(users)
        else :
            self.NormalUser(users)
        self.AdminUser(users)

    def AdminUser(self, users) :
        # self.teamsMember()
        print("------------------------------------------")        
        print(" 1 : Change Members's Permissions")
        print(" 2 : Remove Other User")
        print(" 3 : Invite Team Members")
        print(" 4 : Search User by name")
        print(" 5 : Leave Team")
        print(" 6 : Back")
        print("------------------------------------------")
        choice = input("( Admin ) Order : ")
        # print(users)
        if(choice == "1"):
            if(len(users) == 1) :
                print("\n You are the only member.\n" )
                input("\n\nEnter : ")
                self.teamsMember()
            for i in range(len(users)):
                if (users[i][3] == self.user_ID) :
                    hisNumber = i
                    break
            while(True) :
                c = int(input("Enter Member Number for changing permission : "))

                if(c <= len(users) and c != hisNumber+1) :
                    if(users[c-1][2] == "Y") :
                        permission = "Normal"
                        changed = "N"
                    else :
                        permission = "Admin"
                        changed = "Y"

                    sql = "Update TeamMember Set Permission = '%s'\
                        WHERE Team_ID ='%s' AND User_ID = '%s'\
                            " %(changed, self.team_ID, users[c-1][3])
                    self.cursor.execute(sql)
                    self.db.commit()

                    print("\n Update %s permission to %s\n" % (users[c-1][0], permission))
                    input("\nEnter : ")
                    self.teamsMember()
                elif(c == hisNumber+1) :
                    print("\n you can not change your permission.\n")
                    input("\nEnter : ")
                    self.teamsMember()
                else :
                    print("wrong number. select again\n")
        elif(choice =="2"):
            if(len(users) == 1) :
                print("\n You are the only member.\n" )
                input("\nEnter : ")
                self.teamsMember()
            for i in range(len(users)):
                if (users[i][3] == self.user_ID) :
                    hisNumber = i
                    break
            while(True) :
                c = int(input("Enter Member Number for removing : "))
                if(c <= len(users) and c != hisNumber+1) :
                    sql = "Update TeamMember Set Is_deleted = 'Y'\
                        WHERE Team_ID = %s AND User_ID = '%s'" % (self.team_ID, users[c-1][3])
                    self.cursor.execute(sql)
                    self.db.commit()
                    print("\n Delete '%s' member\n" % users[c-1][0])
                    input("\nEnter : ")
                    self.teamsMember()
                elif (c ==hisNumber+1):
                    print("\n You can not remove yourself.\n")
                    input("\nEnter : ")
                    self.teamsMember()
                else :
                    print("\n wrong number. select again\n")
        elif(choice =="3"):
            self.InviteUser(users)
        elif(choice =="4"):
            self.SearchUser(users)
            input("\n\nEnter : ")
            self.teamsMember()
        elif(choice == "5") :
            while(True):
                answer = input("Do you want to leave this team? (Y/N) ")
                if(answer.lower() == "y") :
                    self.leaveTeam()
                    break
                elif(answer.lower() == "n") :
                    input("\n\nEnter : ")
                    self.teamsMember()  
                    break
                else :
                    print("wrong input") 
        elif(choice =="6"):
            self.selectTeam()
        else:
            print("Wrong input. Enter again.")

        input("\n\n Enter : ")
        self.clear()
        self.teamsMember()

    def leaveTeam(self):
        sql = "UPDATE TeamMember Set Is_deleted = 'Y'\
        WHERE Team_ID = '%d' AND User_ID = '%d'" % (self.team_ID, self.user_ID)
        self.cursor.execute(sql)
        self.db.commit() 
        self.teamlist()

    def NormalUser(self, users):
        # self.clear()
        # self.teamsMember
        print("------------------------------------------")  
        print(" 1. Leave Team")
        print(" 2. Search User by name")
        print(" 3. Back")
        print("------------------------------------------")
        choice = (input(" ( Normal )  Order : "))
        if(choice == "1"):
            answer = input("Do you want to leave this team? (Y/N) ")
            if(answer.lower() == "y") :
                self.leaveTeam()
            else :
                input("\n\nEnter : ")
                self.teamsMember()              
        elif(choice =="2"):
            self.SearchUser(users)
            input("\nEnter : ")
            self.teamsMember()
        elif(choice =="3"):
            self.selectTeam()
        else:
            print("Wrong input. Enter again.")
            input("\nEnter : ")
            self.teamsMember()

    def InviteUser(self, users) :
        Email_Or_Name = input(" Enter Email Address or Name (yujin/이승윤/HyoBin/hyewon) : ")
        
        # sql = "Select U.User_ID, U.Login_ID, U.User_Name from User as U , TeamMember as TM\
        #     WHERE (U.User_Name = '%s' or U.User_Email = '%s') AND U.Is_deleted = 'N' AND TM.Team_ID != '%d' AND TM.Is_deleted = 'N'\
        #         " %(Email_Or_Name, Email_Or_Name, self.team_ID)

        # self.cursor.execute("drop view Findusers")
        # self.db.commit()

        sql = "Create view Findusers AS Select User_ID, Login_ID, User_Name from User\
            Where (User_Name = '%s' or User_Email = '%s') AND Is_deleted = 'N'\
                " %(Email_Or_Name, Email_Or_Name)

        self.cursor.execute(sql)
        self.db.commit()

        sql = "select * from Findusers"
        self.cursor.execute(sql)
        allfinduser = self.cursor.fetchall()   
        # print(allfinduser)

        if (allfinduser == []):
            print("\n no results \n")
        else :
            sql = "select U.user_ID from Findusers as U\
                left join TeamMember as TM ON U.User_ID = TM.User_ID\
                WHERE TM.Team_ID = '%s' AND TM.Is_deleted = 'N' \
                    " % self.team_ID

            self.cursor.execute(sql)
            teamusers = self.cursor.fetchall()

            # print(teamusers)

            for teamuser in teamusers :
                for user in allfinduser :
                    if user[0] == teamuser[0] :
                        allfinduser.remove(user)

            i = 1
            print("\n")
            if(allfinduser == []) :
                print("\n No results \n")
            else :
                for user in allfinduser :
                    print(" ● %d. %s @%s" % (i, user[2], user[1]))
                    i = i+1

                c = int(input("\nSelect User Number you want to invite : "))
                if(c<=len(user)) :
                    while(True):
                        answer = input("Do you want to invite? '%s' (Y/N) : " % allfinduser[c-1][2])
                        if(answer.lower() == "y") :
                            # print("\nDrello send Invite E-Mail to %s\n" % (allfinduser[c-1][2]))
                            sql = "Insert INTO TeamMember VALUES ('%d', '%d', '%s', '%s')" % (self.team_ID, allfinduser[c-1][0], 'N', 'N')
                            self.cursor.execute(sql)
                            self.db.commit()
                            break
                        elif(answer.lower() == "n") :
                            print("\nNo invitation\n")
                            break
                        else :
                            continue
                else :
                    print("\nWrong Number.\n")
        
        self.cursor.execute("drop view Findusers")
        self.db.commit()

        input("\nEnter : ")
        self.teamsMember()

    def SearchUser(self, users):
        name = input(" Filter by name : ")
        sql = "Select U.Login_ID, U.User_Name FROM User as U \
            JOIN TeamMember as TM ON TM.User_ID = U.User_ID\
            WHERE User_Name = '%s' AND TM.Team_ID = '%d'" % (name, self.team_ID)

        self.cursor.execute(sql)
        user = self.cursor.fetchall()
        
        if(user != []) :
            print("\n ● %s @%s \n" % (user[0][1], user[0][0]))
        else :
            print("\n No User \n")

        
    
    def createTeam(self):
        # name, description(optional)
        self.clear()
        Name = "OSS team"
        Description = "cheers!"
        Visibility = "Y"
        print("-----------Create Team----------")
        Name = input(" Name : ")
        Description = input(" Description : ")
        # print(" Name : %s" % Name)
        # print(" Description : %s" %Description)
        print("--------------------------------")
        
        sql = "INSERT INTO \
            Team(Name, Description, Visibility)\
            VALUES('%s','%s', '%s')" %(Name, Description, Visibility)
        
        self.cursor.execute(sql)
        self.db.commit()

        # self.cursor.execute("SELECT LAST_INSERT_ID()") 
        # team_id = cursor.fetchall()
        # self.team_id = team_id[0][0]

        sql = "INSERT INTO \
            TeamMember(Team_ID, User_ID, Permission)\
            VALUES(LAST_INSERT_ID(), '%d', '%s')" % ( self.user_ID, 'Y')
        self.cursor.execute(sql)
        self.db.commit()

        print(" Successfully Create Team")
        input("\n\nPlease Enter to go to NEXT ! :")
        

        # self.cursor.execute(sql) 
        # team_id = cursor.fetchall()
        # self.team_ID = team_id[0][0]
        self.teamlist()

    def deleteTeam(self):
        sql = "update Team set Is_deleted = 'Y' where Team_ID = '%d'" % self.team_ID
        self.cursor.execute(sql)
        self.db.commit()
        self.teamlist()

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def start(self):
        self.teamlist()

# Team(db, cursor , user_ID)q
