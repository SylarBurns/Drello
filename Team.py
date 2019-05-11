
import mysql.connector
import Menu

class Team:
    def __init__(self, cursor , user_ID):
        self.cursor = cursor   
        self.user_ID = user_ID
        self.team_ID = 0
        self.start()   
        
    def teamlist(self):
        # 속한 팀 보여주기
        # avengers
        # drello
        # DB
        print("----------teamlist---------")
        print("1. avengers")
        print("2. Drello")
        print("---------------------------")
        print("+ : Create Team")
        print("0 : Back to Menu")

        choice = input("Enter Team number : ")
        if(choice == "0"):
            Menu.Menu(self.cursor , self.user_ID)
        elif(choice == "+"):
            self.createTeam()
        elif(int(choice) <= 2 and int(choice) !=0):
            self.team_ID = choice  
            self.selectTeam()
        else :
            print("Wrong input. Enter again.")
            self.teamlist()
        
        

    def selectTeam(self):
        print("-----------Team : avengers ------------")
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
        print("------------Team Profile------------")
        print("1. Name : Avengers")
        print("2. Description(optional) : ~~~~~")
        print("3. private")
        print("4. Back")
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
        print("----------Team's Board------------")
        print("1. OS meeting")
        print("2. DB meeting")
        print("----------------------------------")
        print("+ : Create Board")
        print("0 : Back")

        choice = (input("Enter Board number : "))
        if(choice == "0"):
            self.selectTeam()
        elif(choice == "+"):
            print("********************createBoard")
        elif(int(choice) <= 2 and int(choice) !=0):  
            print("***********************speicific board")
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
        print("-------Members Of Team Boards--------")
        print("UserName @UserID (Normal/Admin)")
        print("HyeWon @hyewon43 (Normal)")
        print("YuJin @yujin128 (Noraml)")
        print("이승윤 @user24339877 (Admin)")
        print("-------------------------------------")

    def AdminUser(self):
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
        print("createTeam (만들었다 가정하고 team specific으로 이동)")
        team_id = 1
        self.selectTeam()

    def deleteTeam(self):
        print("delete Team")
        self.teamlist()

    def start(self):
        self.teamlist()

