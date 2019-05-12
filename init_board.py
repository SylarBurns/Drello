import mysql.connector

mydb = mysql.connector.connect(
    host ='localhost',
    user='root',
    passwd='mz0090mz',
    database='Drello'
)

mycursor = mydb.cursor()
create_database = "CREATE DATABASE Drello"
#mycursor.execute(create_database)

user = """CREATE TABLE User(
	User_ID int NOT NULL AUTO_INCREMENT,
	User_PW varchar(32) NOT NULL,
	User_Email varchar(64) NOT NULL,
	User_Name varchar(16) NOT NULL,
	User_Language varchar(16) NOT NULL,
	User_Profile varchar(1024),
	PRIMARY KEY(User_ID)
)"""

board = """CREATE TABLE Board (
    Board_ID int NOT NULL AUTO_INCREMENT,
    Team_ID int DEFAULT -1,
    User_ID int DEFAULT -1,
    Board_Title varchar(128) NOT NULL,
    CommentPerm varchar(128) NOT NULL,
    AddRmPerm varchar(128) NOT NULL,
    IsClosed BOOLEAN DEFAULT false,
    Visibility varchar(128),
    PRIMARY KEY (Board_ID)
)"""

boardMember= """CREATE TABLE BoardMember(
    Board_ID int NOT NULL,
    User_ID int NOT NULL,
    CONSTRAINT board_member UNIQUE (Board_ID, User_ID),
    FOREIGN KEY (Board_ID) REFERENCES Board(Board_ID) ON UPDATE CASCADE
)"""
List = """CREATE TABLE List (
   List_ID int NOT NULL AUTO_INCREMENT,
   List_Title varchar(128) NOT NULL,
   Board_ID int NOT NULL,
   Position int NOT NULL,
   FOREIGN KEY (Board_ID) REFERENCES Board(Board_ID) ON UPDATE CASCADE,
   PRIMARY KEY (List_ID)
)"""
Label="""CREATE TABLE Labels(
   Label_ID int NOT NULL AUTO_INCREMENT,
   Board_ID int NOT NULL,
   Name varchar(16) NOT NULL,
   Color varchar(16) NOT NULL,
   FOREIGN KEY (Board_ID) REFERENCES Board(Board_ID) ON UPDATE CASCADE,
   PRIMARY KEY (Label_ID)
)"""
Card="""CREATE TABLE Card(
   Card_ID int NOT NULL AUTO_INCREMENT,
   List_ID int NOT NULL,
   Label_ID varchar(128),
   Card_Title varchar(32) NOT NULL,
   Position int Not NULL,
   Description varchar(256),
   Due_Date varchar(16),
   Members varchar(128),
   FOREIGN KEY (List_ID) REFERENCES List(List_ID) ON UPDATE CASCADE,
   PRIMARY KEY (Card_ID)
)"""
Activity="""CREATE TABLE Activity(
   Activity_ID int NOT NULL AUTO_INCREMENT,
   Board_ID int NOT NULL,
   List_ID int DEFAULT -1,
   Card_ID int DEFAULT -1,
   User_ID int NOT NULL,
   Action varchar(256) NOT NULL,
   DateTime TIMESTAMP,
   FOREIGN KEY (Board_ID) REFERENCES Board(Board_ID) ON UPDATE CASCADE,
   FOREIGN KEY (List_ID) REFERENCES List(List_ID) ON UPDATE CASCADE,
   FOREIGN KEY (Card_ID) REFERENCES Card(Card_ID) ON UPDATE CASCADE,
   FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON UPDATE CASCADE,
   PRIMARY KEY (Activity_ID)
)"""
Notice="""CREATE TABLE Notice (
   User_ID int NOT NULL,
   Activity_ID int NOT NULL,
   ID int NOT NULL,
   CONSTRAINT Notice_Link UNIQUE (Activity_ID, User_ID),
   FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON UPDATE CASCADE
)"""
Watch="""CREATE TABLE Watch(
   User_ID int NOT NULL,
   ID_type varchar(10) NOT NULL,
   ID int NOT NULL,
   Mark BOOLEAN DEFAULT false,
   FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON UPDATE CASCADE
)"""
CheckList="""CREATE TABLE Checklist(
   Checklist_ID int NOT NULL AUTO_INCREMENT,
   Card_ID int NOT NULL,
   Checklist_Name varchar(64),
   Check_Item varchar(32),
   FOREIGN KEY (Card_ID) REFERENCES Card(Card_ID) ON UPDATE CASCADE,
   PRIMARY KEY (Checklist_ID)
)"""
Comment="""CREATE TABLE Comment(
   Comment_ID int NOT NULL AUTO_INCREMENT,
   User_ID int NOT NULL,
   Card_ID int NOT NULL,
   Content varchar(256) NOT NULL,
   DateTime TIMESTAMP,
   Is_edited BOOLEAN DEFAULT false,
   Is_deleted BOOLEAN DEFAULT false,
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
   Is_deleted BOOLEAN DEFAULT false,
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
   Is_deleted BOOLEAN DEFAULT false,
   PRIMARY KEY (Team_ID)
)"""

TeamMember = """CREATE TABLE TeamMember(
   Team_ID int NOT NULL,
   User_ID int NOT NULL,
   Permission varchar(16) NOT NULL,
   CONSTRAINT board_member UNIQUE (Team_ID, User_ID),
   FOREIGN KEY (Team_ID) REFERENCES Team(Team_ID) ON UPDATE CASCADE,
   FOREIGN KEY (User_ID) REFERENCES User(User_ID) ON UPDATE CASCADE
)"""

sql_list = [user, board, boardMember, List, Card, Activity, Label, Notice, Watch, CheckList, Comment, Attachment, Team, TeamMember]
for sql in sql_list:
    mycursor.execute(sql)
