import mysql.connector

mydb = mysql.connector.connect(
	host="mydbinstance.cbp3whb5qyie.us-east-2.rds.amazonaws.com",
 	port=3306,
 	user="gyqls",
 	passwd="rnjssmdsoRj1",
 	database = "Drello"
)

mycursor = mydb.cursor()

user = """CREATE TABLE User(
   User_ID int NOT NULL AUTO_INCREMENT,
   Login_ID varchar(32) NOT NULL,
   User_PW varchar(32) NOT NULL,
   User_Email varchar(64) NOT NULL,
   User_Name varchar(16) NOT NULL,
   User_Language varchar(16) NOT NULL,
   User_Profile varchar(1024),
   Is_deleted char(1) DEFAULT 'N',
   PRIMARY KEY(User_ID)
)"""

board = """CREATE TABLE Board (
    Board_ID int NOT NULL AUTO_INCREMENT,
    Team_ID int DEFAULT -1,
    User_ID int DEFAULT NULL,
    Board_Title varchar(128) NOT NULL,
    CommentPerm varchar(128) NOT NULL,
    AddRmPerm varchar(128) NOT NULL,
    IsClosed BOOLEAN DEFAULT false,
    Visibility varchar(128),
    Is_deleted char(1) DEFAULT 'N',
    PRIMARY KEY (Board_ID)
)"""

boardMember= """CREATE TABLE BoardMember(
    Board_ID int NOT NULL,
    User_ID int NOT NULL,
    Permission varchar(16) NOT NULL,
    Is_deleted char(1) DEFAULT 'N',
    CONSTRAINT board_member UNIQUE (Board_ID, User_ID),
    FOREIGN KEY (Board_ID) REFERENCES Board(Board_ID) ON UPDATE CASCADE
)"""

List = """CREATE TABLE List (
   List_ID int NOT NULL AUTO_INCREMENT,
   List_Title varchar(128) NOT NULL,
   Board_ID int NOT NULL,
   Position int NOT NULL,
   Is_deleted char(1) DEFAULT 'N',
   FOREIGN KEY (Board_ID) REFERENCES Board(Board_ID) ON UPDATE CASCADE,
   PRIMARY KEY (List_ID)
)"""

Label="""CREATE TABLE Labels(
   Label_ID int NOT NULL AUTO_INCREMENT,
   Board_ID int NOT NULL,
   Name varchar(16) NOT NULL,
   Color varchar(16) NOT NULL,
   Is_deleted char(1) DEFAULT 'N',
   FOREIGN KEY (Board_ID) REFERENCES Board(Board_ID) ON UPDATE CASCADE,
   PRIMARY KEY (Label_ID)
)"""

Card="""CREATE TABLE Card(
   Card_ID int NOT NULL AUTO_INCREMENT,
   List_ID int NOT NULL,
   Label_ID varchar(128),
   Card_Title varchar(32) NOT NULL,
   Position int NOT NULL,
   Description varchar(256),
   Due_Date TIMESTAMP,
   Members varchar(128) NOT NULL,
   Is_deleted char(1) DEFAULT 'N',
   FOREIGN KEY (List_ID) REFERENCES List(List_ID) ON UPDATE CASCADE,
   PRIMARY KEY (Card_ID)
)"""

Activity="""CREATE TABLE Activity(
   Activity_ID int NOT NULL AUTO_INCREMENT,
   Board_ID int NOT NULL,
   List_ID int DEFAULT NULL,
   Card_ID int DEFAULT NULL,
   User_ID int NOT NULL,
   Action varchar(256) NOT NULL,
   DateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (Board_ID) REFERENCES Board(Board_ID) ON UPDATE CASCADE,
   FOREIGN KEY (List_ID) REFERENCES List(List_ID) ON UPDATE CASCADE,
   FOREIGN KEY (Card_ID) REFERENCES Card(Card_ID) ON UPDATE CASCADE,
   FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON UPDATE CASCADE,
   PRIMARY KEY (Activity_ID)
)"""

Notice="""CREATE TABLE Notice (
   User_ID int NOT NULL,
   Activity_ID int NOT NULL,
   Is_read char(1) DEFAULT 'N',
   CONSTRAINT Notice_Link UNIQUE (Activity_ID, User_ID),
   FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON UPDATE CASCADE
)"""

Watch="""CREATE TABLE Watch(
   User_ID int NOT NULL,
   ID_type varchar(10) NOT NULL,
   ID int NOT NULL,
   FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON UPDATE CASCADE
)"""

CheckList="""CREATE TABLE Checklist(
   Checklist_ID int NOT NULL AUTO_INCREMENT,
   Card_ID int NOT NULL,
   Checklist_Name varchar(64),
   Check_Item varchar(1024),
   Is_deleted char(1) DEFAULT 'N',
   FOREIGN KEY (Card_ID) REFERENCES Card(Card_ID) ON UPDATE CASCADE,
   PRIMARY KEY (Checklist_ID)
)"""

Comment="""CREATE TABLE Comment(
   Comment_ID int NOT NULL AUTO_INCREMENT,
   User_ID int NOT NULL,
   Card_ID int NOT NULL,
   Content varchar(256) NOT NULL,
   DateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   Is_edited char(1) DEFAULT 'N',
   Is_deleted char(1) DEFAULT 'N',
   FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON UPDATE CASCADE,
   FOREIGN KEY (Card_ID) REFERENCES Card(Card_ID) ON UPDATE CASCADE,
   PRIMARY KEY (Comment_ID)
)"""

Attachment="""CREATE TABLE Attachment(
   Attachment_ID int NOT NULL AUTO_INCREMENT,
   Card_ID int NOT NULL,
   User_ID int NOT NULL,
   Type varchar(16) NOT NULL,
   Name varchar(64) NOT NULL,
   DateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   Is_deleted char(1) DEFAULT 'N',
   FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON UPDATE CASCADE,
   FOREIGN KEY (Card_ID) REFERENCES Card(Card_ID) ON UPDATE CASCADE,
   PRIMARY KEY (Attachment_ID)
)"""

Team ="""CREATE TABLE Team(
   Team_ID int NOT NULL AUTO_INCREMENT,
   Name varchar(64) NOT NULL,
   ShortName varchar(64),
   Website varchar(64),
   Description varchar(512),
   Visibility varchar(128),
   Is_deleted char(1) DEFAULT 'N',
   PRIMARY KEY (Team_ID)
)"""

TeamMember = """CREATE TABLE TeamMember(
   Team_ID int NOT NULL,
   User_ID int NOT NULL,
   Permission varchar(16) NOT NULL,
   Is_deleted varchar(1) DEFAULT 'N',
   CONSTRAINT board_member UNIQUE (Team_ID, User_ID),
   FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID) ON UPDATE CASCADE,
   FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON UPDATE CASCADE
)"""

sql_list = [user, board, boardMember, List, Card, Activity, Label, Notice, Watch, CheckList, Comment, Attachment, Team, TeamMember]
for sql in sql_list:
    mycursor.execute(sql)

mycursor = mydb.cursor()

sqlFormula = "INSERT INTO User (Login_ID, User_PW, User_Email, User_Name, User_Language, User_Profile) VALUES (%s, %s, %s, %s, %s, %s)"
users =[("Handong","1111", "JC@handong.edu",  "JC", "Korean", "Hi"),
        ("hyeon-62", "123123", "21700646@handong.edu", "hyewon", "Korean", "Hi! I'm hyewon"),
        ("first-id", "12345", "hi@handong.edu", "CRA", "Korean", "Hi! I'm hello"),
        ("english_id", "abcde", "hello@naver.com", "곽효빈", "English", "Hello world"),
        ("math", "xyz123", "mathlove@naver.com", "Sun", "Korean", "Hi! i love math"),
        ("cs_love", "helloworld", "cs@handong.edu", "Jiyun", "Korean", "hello, world"),
        ("gyqls","1005", "HB@handong.edu",  "HyoBin", "Korean" , ""),
        ("yujineee","1006", "yujin@handong.edu",  "yujin", "Korean", "I'm yujin"),
        ("user24339877","1007", "user24339877@handong.edu",  "이승윤", "Korean", "Drello lover"),
        ("hyewon43","1008", "hyewon43@handong.edu",  "Hyewon", "Korean", "best developer"),
        ("love_Drumer", "1111", "love@handong.edu","drummer" ,"Korean", "hello~"),
        ("Drumer_123", "2222", "handonge@naver.com", "Drummer", "Korean", "my name is drumer"),
        ("Drumer_love_Drum", "3333", "kakao@handong.edu", "drummer", "English", "hello baby들")]
mycursor.executemany(sqlFormula, users)

sqlFormula = "INSERT INTO Team(Name, ShortName, Website, Description, Visibility) VALUES(%s, %s, %s, %s, %s)"
Team = [("Team Avengers", "Avengers", "https://www.github.com/avengers", "This is team avengers", "Y"),
         ("Team handong for DB", "Handong", "https://www.github.com/handong", "This is team handong!", "Y"),
         ("super cool drello", "Drello", "https://drello.github.io", "super super coooooooooooool team drello", "N"),
         ("universal cool CRA", "CRA", "https://www.github.com/CRA16", "super cool in universe CRA", "Y"),
         ("Database Team", "DB", "https://www.drive.google.com/database", "database class in handong 2019-1", "Y"),]
mycursor.executemany(sqlFormula, Team)
mydb.commit()

sqlFormula = "INSERT INTO TeamMember(Team_ID, User_ID, Permission) VALUES(%s, %s, %s)"
teamMembers = [(1, 1, 'Y'),
               (1, 2, 'N'),
               (1, 3, 'Y'),
               (1, 4, 'N'),
               (1, 5, 'N'),
               (2, 6, 'N'),
               (2, 1, 'Y'),
               (2, 2, 'N'),
               (2, 3, 'N'),
               (3, 1, 'N'),
               (3, 4, 'N'),
               (3, 5, 'N'),
               (3, 6, 'Y'),
               (4, 1, 'N'),
               (5, 1, 'N')]
mycursor.executemany(sqlFormula, teamMembers)
mydb.commit()

sqlFormula = "INSERT INTO Board (Team_ID, User_ID, Board_Title, CommentPerm, AddRmPerm, IsClosed, Visibility) VALUES (%s, %s, %s, %s, %s, %s)"
boards =[(-1 , 1, "First Board", "Member", "Member", True, "Private"),
         (-1, 2, "Second Board", "Disabled", "Member", False, "Public"),
         (-1, 3, "last Board", "Member", "Admin", False, "Public"),
         (1, -1, "OSS study", "Member", "Admin", False, "Public"),
         (1, -1, "DB Meeting", "Member", "Admin", False, "Public")]

# sqlFormula = "INSERT INTO List (List_Title, Board_ID, Position) VALUES (%s, %s, %s)"
# lists = [("Avengers", 1, 1),
#          ("Captain America", 1, 2),
#          ("Iron Man", 1, 3),
#          ("Thor", 1, 4),
#          ("Hulk", 1, 5),
#          ("black widow", 1, 6),
#          ("Hawkeye", 1, 7),
#          ("First list", 2, 1),
#          ("Second List", 2, 2),
#          ("Third List", 2, 3),]
# mycursor.executemany(sqlFormula, lists)

sqlFormula = "INSERT INTO BoardMember(Board_ID, User_ID, Permission) VALUES(%s, %s, %s)"
BoardMember = [(1, 1, "Admin"),
         (2, 2, "Admin"),
         (3, 3, "Admin"),
         (2, 7, "Member"),
         (2, 1, "Member"),
         (3, 2, "Member"),]
mycursor.executemany(sqlFormula, BoardMember)

sqlFormula = "INSERT INTO Labels(Board_ID, Name, Color) VALUES(%s, %s, %s)"
Labels = [(1, "Black Label", "Black"),
         (2, "Pink Label", "Black"),
         (3, "BlackPink Label", "Yellow"),
         (1, "Iron legion", "Red"),
         (1, "Asgard", "Blue"),
         (1, "Sheild", "Magenta"),
         (2, "Sanctum", "Red"),
         (2, "Wakanda", "Cyan"),
         (3, "Guardians", "Green"),
         (3, "Loki", "Dark Green"),]
mycursor.executemany(sqlFormula, Labels)
mydb.commit()

# sqlFormula = "INSERT INTO Card(List_ID, Card_Title, Position, Description) VALUES(%s, %s, %s, %s)"
# Card = [(1, "First card", "1", "hihihi "),
#          (2, "Card A",  "1","Hello I'm Card A"),
#          (1, "Second Card", "2", "hihi second card from first list"),
#          (1, "Third Card", "3", "33333333 card"),
#          (1, "Fourth Card", "4", "4_4_4_4_4-4-4-4-4-4"),
#          (1, "Fifth Card", "5", "Oh! 5 is perfect number"),
#          (2, "Card B", "2", "card b from 2"),
#          (2, "Card C", "3", "today's schedule..."),
#          (3, "11111", "1", "i'm hungry."),
#          (3, "22222", "2", "i'm tired."),]
# # mycursor.executemany(sqlFormula, Card)
# # mydb.commit()

# sqlFormula = "INSERT INTO CheckList (Card_ID, Checklist_Name) VALUES(%s, %s)"
# checklists = [(1, "Captain America"),
#               (1, "Iron Man"),
#               (2, "Thor"),
#               (2, "Hulk"),
#               (3, "black widow")]
# mycursor.executemany(sqlFormula, checklists)

# sqlFormula = "INSERT INTO Comment(User_ID, Card_ID, Content) VALUES (%s, %s, %s)"
# Comment = [(1, 1, "my comment.."),
#           (2, 2, "very good project!"),
#           (3, 3, "sleeeeep....zzz"),
#           (7, 4, "comment for test.."),
#           (7, 5, "Database team project"),
#           (4, 6, "we use python for project."),
#           (6, 7, "and mysql!"),
#           (2, 8, "we love computer ~!"),
#           (1, 9, "hello, world!"),]
# mycursor.executemany(sqlFormula, Comment)
# mydb.commit()

# sqlFormula = "INSERT INTO Attachment(Card_ID, User_ID, Type, Name) VALUES(%s, %s, %s, %s)"
# Attachment = [(1, 1, "pptx", "final"),
#           (1, 2, "docx", "first_commit"),
#           (3, 3, "txt", "my_txt"),
#           (4, 4, "jpg", "favorite_picture"),
#           (4, 5, "pptx", "presentation"),
#           (4, 6, "docx", "midterm"),
#           (6, 7, "jpg", "my_pick"),
#           (2, 8, "jpg", "hungry_TT"),
#           (5, 9, "docx", "message"),]
# mycursor.executemany(sqlFormula, Attachment)
# mydb.commit()

