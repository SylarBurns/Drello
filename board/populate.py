insert_user = """INSERT
into user (User_PW, User_Email, User_Name, User_Language, User_Profile) 
Values ("1234", "2140054485@handong.edu", "SeungYunLee", "Korean", "Student of HGU")"""

insert_board = """INSERT
into board (User_ID, Board_Title, CommentPerm, AddRmPerm, Visibility) 
Values ("1", "Drello", "Members", "Members", "private")"""

alter_table ="""ALTER TABLE BoardMember
ADD Permission varchar(16) NOT NULL"""