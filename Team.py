import mysql.connector
import Menu
# import Board
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
        os.system('cls' if os.name == 'nt' else 'clear')
        print("----------teamlist---------")

        sql = "select T.Team_ID, T.Name \
                from Team as T\
                JOIN TeamMember as TM\
                ON T.Team_ID = TM.Team_ID \
                WHERE TM.User_ID = '%d'" % self.user_ID
        self.cursor.execute(sql)
        teams = self.cursor.fetchall()

        for (team_ID, team_name) in teams :
            print(str(team_ID) + " . " + team_name)

        print("---------------------------")
        print("+ : Create Team")
        print("0 : Back to Menu")

        choice = input("Enter Team number : ")
        if(choice == "0"):
            Menu.Menu(self.db, self.cursor , self.user_ID)
        elif(choice == "+"):
            self.createTeam()
        elif(int(choice) <= 2 and int(choice) !=0):
            self.team_ID = choice  
            self.selectTeam()
        else :
            print("Wrong input. Enter again.")
            self.teamlist()
        
        

    def selectTeam(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        sql = "Select Name from Team WHERE Team_ID = '%s'" % self.team_ID
        self.cursor.execute(sql)
        team_name = self.cursor.fetchall()
        
        print("\n-----------Team : %s ------------" % team_name[0][0])
        print("1. Edit team profile")
        print("2. Team's Boards")
        print("3. Team's Members")
        print("4. Delete Team")
        print("5. Back")
        print("---------------------------------------")

        choice = int(input("Enter the number for your choice: "))
        if(choice == 1):
            print("edit profile")
            self.editTeamProfile()
        elif(choice ==2):
            self.teamsBoard()
        elif(choice ==3):
            self.teamsMember()
        elif(choice ==4):
            self.deleteTeam()
        elif(choice ==5):
            self.teamlist()
        else :
            print("잘 못 누르셨습니다.")
            self.selectTeam()

    def editTeamProfile(self):
        os.system('cls' if os.name == 'nt' else 'clear')

        sql = "Select * from Team WHERE Team_ID = '%s'" % self.team_ID
        self.cursor.execute(sql)
        team = self.cursor.fetchall()

        print("------------Team Profile------------")
        print("1. Name : %s" % team[0][1] ) 
        print("2. ShortName : %s" %team[0][2])
        print("3. Website : %s" %team[0][3])
        print("4. Description(optional) : %s" % team[0][4]) 
        print("5. private" )
        print("6. Back")
        print("------------------------------------")
        choice = int(input("Enter Number you want to edit: "))
        if(choice == 1):
            print("name change")
        elif(choice == 2):
            print("description change")
        elif(choice == 3):
            print("private to public")
        elif(choice == 4):
            self.selectTeam()
        else :
            print("wrong choice, Enter the number again")
        self.editTeamProfile()

    def teamsBoard(self):
        # BOARD = Board.Board_Manager(self.user_ID, self.cursor)

        os.system('cls' if os.name == 'nt' else 'clear')
        print("----------Team's Board------------")
        # BOARD.board_list()
        print("----------------------------------")
        print("+ : Create Board")
        print("0 : Back")

        choice = (input("Enter Board number : "))
        if(choice == "0"):
            self.selectTeam()
        elif(choice == "+"):
            # BOARD.board_create()
            print("board_create")
        elif(int(choice) <= 8 and int(choice) !=0):  
            # BOARD.board_specific(int(choice))
            print("board specific")
        else :
            print("Wrong input. Enter again.")
            self.teamsBoard() 

    def teamsMember(self):
        self.teamMemberList()
        print("*******************user가 admin인 경우와 아닌경우")
        user = "admin"
        if(user == "admin"):
            print("user가 admin이면 다른 member remove/ admin 변경 가능")
            self.AdminUser()
        else :
            print("user가 normal이면 Leave만 가능")
            self.NormalUser()

    def teamMemberList(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("-------Members Of Team Boards--------")
        print("UserName @UserID (Normal/Admin)")
        print("HyeWon @hyewon43 (Normal)")
        print("YuJin @yujin128 (Noraml)")
        print("이승윤 @user24339877 (Admin)")
        print("-------------------------------------")

    def AdminUser(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("1. Change Members's Permissions")
        print("2. Remove Other User")
        print("3. Invite Team Members")
        print("4. Search User by name")
        print("5. Back")
        choice = int(input("Enter the number for your choice: "))
        if(choice == 1):
            print("change permissions")
        elif(choice ==2):
            print("remove user")
        elif(choice ==3):
            print("invite user")
        elif(choice ==4):
            self.SearchUser()
        elif(choice ==5):
            self.selectTeam()
        else:
            print("Wrong input. Enter again.")
        self.AdminUser()

    def NormalUser(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("1. Leave Team")
        print("2. Search User by name")
        print("3. Back")
        choice = int(input("Enter the number for your choice: "))
        if(choice == 1):
            print("change permissions")
        elif(choice ==2):
            self.SearchUser()
        elif(choice ==3):
            self.selectTeam()
        else:
            print("Wrong input. Enter again.")
        self.NormalUser()

    def SearchUser(self):
        print("search user")

    
    def createTeam(self):
        # name, description(optional)
        Name = "OSS team"
        Description = "cheers!"
        Visibility = "Y"
        print("\n\n-----------Create Team----------")
        print("Name : %s" % Name)
        print("Description : %s" %Description)
        print("--------------------------------")
        
        sql = "INSERT INTO \
            Team(Name, Description, Visibility)\
            VALUES('%s','%s', '%s')" %(Name, Description, Visibility)
        
        self.cursor.execute(sql)
        self.db.commit()
        self.cursor.execute("SELECT LAST_INSERT_ID()") 
        team_id = cursor.fetchall()
        self.team_id = team_id[0][0]

        sql = "INSERT INTO \
            TeamMember(Team_ID, User_ID, Permission)\
            VALUES('%d', '%d', '%s')" % (self.team_id, self.user_ID, 'Y')
        self.cursor.execute(sql)
        self.db.commit()

        print("*Successfully Create Team into the [Team] TABLE!*")
        input("\n\nPlease Enter to go to NEXT ! :")
        self.selectTeam()

    def deleteTeam(self):
        print("delete Team")
        self.teamlist()

    def start(self):
        self.teamlist()

# Team(db, cursor , user_ID)