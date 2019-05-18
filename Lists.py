import Thanos
import Color
import os

class Activity_Manager:
    def __init__(self, card_ID, user_ID, DB):
        self.cursor = DB.cursor()
        self.card_ID = card_ID
        self.user_ID = user_ID
        self.db = DB
        sql = "SELECT List_ID FROM Card WHERE Card_ID = %d" % self.card_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        self.list_ID = result[0]
        sql = "SELECT Board_ID FROM List WHERE List_ID = %d" % self.list_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        self.board_ID = result[0]
    def for_activity(self):
        sql = "SELECT Card_Title FROM Card WHERE Card_ID = %d" % self.card_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        Card_Name = result[0]
        sql = "SELECT Board_Title FROM Board WHERE Board_ID = %d" % self.board_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        Board_Title = result[0]
        sql = "SELECT List_Title FROM List WHERE List_ID = %d" % self.list_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        List_Title = result[0]
        return Card_Name, Board_Title, List_Title

class Label_List_Manager:
    def __init__(self, card_ID, user_ID, DB):
        self.Activity_manager = Activity_Manager(card_ID, user_ID, DB)
        self.cursor = DB.cursor()
        self.card_ID = card_ID
        self.user_ID = user_ID
        self.db = DB
        self.list = {}
    def setting_labels(self, label_IDs):
        self.list = {}
        if label_IDs:
            label_ids = label_IDs.split(",")
            i = 1
            for l_id in label_ids:
                l_id = int(l_id)
                sql = "SELECT Name, Color FROM Labels WHERE Label_ID = %d AND Is_deleted = 'N'" % l_id
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                if result:
                    name = result[0]
                    color = result[1]
                    self.list[i] = (l_id, name, color)
                    i += 1
                else:
                    print("No Label")
            return True
        else:
            return False
    def print_labels(self):
        print("Label : ", end = "")
        for i in range(len(self.list)):
            Color.Color_Manager.FgPrint(self.list[i + 1][1], self.list[i + 1][2])
        print()
    def add_label(self):
        sql = "SELECT Label_ID, Name, Color FROM Labels WHERE Board_ID = %d" % self.Activity_manager.board_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if result:
            while True:
                try:
                    label_list = {}
                    i = 1
                    print()
                    for l_id, name, color in result:
                        label_list[i] = (l_id, name)
                        print(str(i) + ".", end = " ")
                        Color.Color_Manager.FgPrint(name, color)
                        print()
                        i += 1
                    label_num = input("\nWhich Label? (q : Go back) >> ")
                    if label_num == 'q':
                        break
                    label_num = int(label_num)
                    if label_num <= len(label_list):
                        dup = False
                        for i in range(len(self.list)):
                            if self.list[i + 1][0] == label_list[label_num][0]:
                                dup = True
                                break
                        if dup:
                            input("Already Exist! please enter again >> ")
                            os.system('cls' if os.name == 'nt' else 'clear')
                        else:
                            label_ids = ""
                            for i in range(len(self.list)):
                                label_ids = label_ids + str(self.list[i + 1][0]) + ","
                            label_ids = label_ids + str(label_list[label_num][0])
                            sql = "UPDATE Card SET Label_ID = '%s' WHERE Card_ID = %d" % (label_ids, self.card_ID)
                            self.cursor.execute(sql)
                            self.db.commit()

                            c_name, b_title, l_title = self.Activity_manager.for_activity()
                            act_str = "Add '%s' label to card '%s' in list '%s' on '%s'" % (label_list[label_num][1], c_name, l_title, b_title)
                            Thanos.Activity_notice("CARD", self.card_ID, self.user_ID, self.db, act_str)
                            break
                    else:
                        input("Wrong number! please enter again >>")
                except:
                    input("Wrong number! please enter again >>")
        else:
            input("No label in this Board (Go back) >> ")
    def remove_label(self, r_label):
        label_ids = ""
        for i in range(len(self.list)):
            if i + 1 != r_label:
                label_ids = label_ids + "," + str(self.list[i + 1][0])
        label_ids = label_ids.lstrip(',')
        sql = "UPDATE Card SET Label_ID = '%s' WHERE Card_ID = %d" % (label_ids, self.card_ID)
        self.cursor.execute(sql)
        self.db.commit()

        c_name, b_title, l_title = self.Activity_manager.for_activity()
        act_str = "Remove '%s' label from card '%s' in list '%s' on '%s'" % (self.list[r_label][1], c_name, l_title, b_title)
        Thanos.Activity_notice("CARD", self.card_ID, self.user_ID, self.db, act_str)
class Checklist_List_Manager:
    def __init__(self, Card_ID, User_ID, DB):
        self.Activity_manager = Activity_Manager(Card_ID, User_ID, DB)
        self.cursor = DB.cursor()
        self.Card_ID = Card_ID
        self.User_ID = User_ID
        self.db = DB
        self.list = {}
    @staticmethod
    def checklist_menu():
        print("\n1. Create new Checklist")
        print("2. Delete Checklist")
        print("3. View Checklist")
        print("4. Edit Checklist")
        print("5. Go Back")
    @staticmethod
    def checkitem_menu():
        print("\n1. Edit Checklist title")
        print("2. Add new item")
        print("3. Delete a item")
        print("4. Edit item")
        print("5. Toggle a item")
        print("6. Go Back")
    def setting(self):
        self.list = {}
        sql = "SELECT Checklist_ID, Checklist_Name FROM Checklist WHERE Card_ID = %d AND Is_deleted = 'N'" % self.Card_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if not result:
            return False
        else :
            i = 1
            for ch_id, ch_name in result:
                self.list[i] = (ch_id, ch_name)
                i += 1
            return True
    def print_checklist_list(self):
        for i in range(len(self.list)):
            print(str(i + 1) + ". " + self.list[i + 1][1])
    def create(self):
        # To do list 라는 이름의 checklist 생성
        # name = "To do list"
        name = input("Checklist name : ")
        sql = "INSERT INTO Checklist (Card_ID, Checklist_Name) VALUES(%d, '%s')" % (self.Card_ID, name)
        self.cursor.execute(sql)
        self.db.commit()

        c_name, b_title, l_title = self.Activity_manager.for_activity()
        act_str = "Created Checklist '%s' to card '%s' in list '%s' on '%s'" % (name, c_name, l_title, b_title)
        Thanos.Activity_notice("CARD", self.Card_ID, self.User_ID, self.db, act_str)
    def delete(self):
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("-----------------\n    Checklist\n-----------------")
                self.print_checklist_list()
                checklist_num = input("\nWhich Checklist? (q : go back) >> ")
                if checklist_num == 'q':
                    input("return to previous view >>")
                    break
                checklist_num = int(checklist_num)
                if checklist_num in self.list:
                    sql = "UPDATE Checklist SET Is_deleted = 'Y' WHERE Checklist_ID = %d" % self.list[checklist_num][0]
                    self.cursor.execute(sql)
                    self.db.commit()
                    name = self.list[checklist_num][1]

                    c_name, b_title, l_title = self.Activity_manager.for_activity()
                    act_str = "Deleted Checklist '%s' from card '%s' in list '%s' on '%s'" % (name, c_name, l_title, b_title)
                    Thanos.Activity_notice("CARD", self.Card_ID, self.User_ID, self.db, act_str)
                    break
                else:
                    print("Wrong number! please enter again")
            except:
                print("Wrong number! please enter again")
    def print_checklist(self):
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("-----------------\n    Checklist\n-----------------")
                self.print_checklist_list()
                checklist_num = input("\nWhich Checklist? (q : go back) >> ")
                if checklist_num == 'q':
                    print("return to previous view")
                    break
                checklist_num = int(checklist_num)
                if checklist_num in self.list:
                    os.system('cls' if os.name == 'nt' else 'clear')                        
                    sql = "SELECT Check_Item FROM Checklist WHERE Checklist_ID = %d" % self.list[checklist_num][0]
                    self.cursor.execute(sql)
                    result = self.cursor.fetchone()
                    print("------------------\n" + self.list[checklist_num][1].center(18) + "\n------------------")
                    if result[0]:
                        item_list = result[0].split(",")
                        items = []
                        for item in item_list:
                            item = item.split(":")
                            items.append((item[0], item[1]))
                        for item, check in items:
                            if check == 'T':
                                print("☑ " + item)
                            elif check == 'F':
                                print("☐ " + item)
                        input("\nGo Back >>")
                    else:
                        print("Empty")
                        input("\nGo Back >>")
                    break
                else:
                    print("Wrong number! please enter again")
            except:
                print("Wrong number! please enter again")
    def edit(self):
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("-----------------\n    Checklist\n-----------------")
                self.print_checklist_list()
                checklist_num = input("\nWhich Checklist? (q : go back) >> ")
                if checklist_num == 'q':
                    print("return to previous view")
                    break
                checklist_num = int(checklist_num)
                if checklist_num in self.list:
                    choice = 0
                    while True:
                        sql = "SELECT Check_Item, Checklist_Name FROM Checklist WHERE Checklist_ID = %d" % self.list[checklist_num][0]
                        self.cursor.execute(sql)
                        result = self.cursor.fetchone()
                        items = {}
                        os.system('cls' if os.name == 'nt' else 'clear')
                        print("------------------\n" + result[1].center(18) + "\n------------------")
                        if result[0]:
                            item_list = result[0].split(",")
                            i = 1
                            for item in item_list:
                                item = item.split(":")
                                items[i] = (item[0], item[1])
                                if item[1] == 'T':
                                    print(str(i) + ". ☑ " + item[0])
                                elif item[1] == 'F':
                                    print(str(i) + ". ☐ " + item[0])
                                i += 1
                            while True:
                                self.setting()
                                Checklist_List_Manager.checkitem_menu()
                                choice = input("\nEnter the number for your choice : ")
                                if choice == '1':
                                    self.edit_checkname(checklist_num)
                                    break
                                elif choice == '2':
                                    self.add_checkitem(checklist_num, result[0])
                                    break
                                elif choice == '3':
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                    print("------------------\n" + result[1].center(18) + "\n------------------")
                                    self.del_checkitem(checklist_num, items)
                                    break
                                elif choice == '4':
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                    print("------------------\n" + result[1].center(18) + "\n------------------")
                                    self.edit_checkitem(checklist_num, items)
                                    break
                                elif choice == '5':
                                    os.system('cls' if os.name == 'nt' else 'clear')
                                    print("------------------\n" + result[1].center(18) + "\n------------------")
                                    self.toggle_checkitem(checklist_num, items)
                                    break
                                elif choice == '6':
                                    return
                                else:
                                    input("Wrong choice! Please enter again >>")
                        else:
                            print("Empty")
                            while True:
                                choice = input("\n(1) Edit Checklist title  (2) Add new item  (q : Go back) >> ")
                                if choice == 'q':
                                    print("return to previous view")
                                    return
                                elif choice == '1':
                                    self.edit_checkname(checklist_num)
                                    break
                                elif choice == '2':
                                    self.add_checkitem(checklist_num, result[0])
                                    break
                                else:
                                    print("Wrong choice! Please enter again")
            except:
                print("Wrong choice! Please enter again")         
    def edit_checkname(self, list_num):
        # checklist name을 Avengers로 수정
        name = "AAA"
        sql = "UPDATE Checklist SET Checklist_Name = '%s' WHERE Checklist_ID = %d" % (name, self.list[list_num][0])
        self.cursor.execute(sql)
        self.db.commit()

        c_name, b_title, l_title = self.Activity_manager.for_activity()
        act_str = "Edited title of Checklist '%s' to '%s' included with card '%s' in list '%s' on '%s'" % (self.list[list_num][1], name, c_name, l_title, b_title)
        Thanos.Activity_notice("CARD", self.Card_ID, self.User_ID, self.db, act_str)      
    def add_checkitem(self, list_num, items):
        # Captain America 추가
        # item = "Make database schema"
        item = input("new item : ")
        if items:
            items = items + "," + item + ":F"
        else:
            items = item + ":F"
        sql = "UPDATE Checklist SET Check_Item = '%s' WHERE Checklist_ID = %d" % (items, self.list[list_num][0])
        self.cursor.execute(sql)
        self.db.commit()

        c_name, b_title, l_title = self.Activity_manager.for_activity()
        act_str = "Add item '%s' to Checklist '%s' included with card '%s' in list '%s' on '%s'" % (item, self.list[list_num][1], c_name, l_title, b_title)
        Thanos.Activity_notice("CARD", self.Card_ID, self.User_ID, self.db, act_str)
    def del_checkitem(self, list_num, items):
        while True:
            try:
                for i in range(len(items)):
                    if items[i + 1][1] == 'T':
                        print(str(i + 1) + ". ☑ " + items[i + 1][0])
                    elif items[i + 1][1] == 'F':
                        print(str(i + 1) + ". ☐ " + items[i + 1][0])
                item_num = input("\nWhich Item? (q : go back) >> ")
                if item_num == 'q':
                    print("return to previous view")
                    break
                item_num = int(item_num)
                if item_num in items:
                    item_list = ""
                    for i in range(len(items)):
                        if item_num != i + 1:
                            item_list = item_list + items[i + 1][0] + ":" + items[i + 1][1] + ","
                    if item_list == "":
                        sql = "UPDATE Checklist SET Check_Item = %s WHERE Checklist_ID = %d" % ("NULL", self.list[list_num][0])
                    else:
                        item_list = item_list.rstrip(",")
                        sql = "UPDATE Checklist SET Check_Item = '%s' WHERE Checklist_ID = %d" % (item_list, self.list[list_num][0])
                    self.cursor.execute(sql)
                    self.db.commit()

                    c_name, b_title, l_title = self.Activity_manager.for_activity()
                    act_str = "Deleted item '%s' from Checklist '%s' included with card '%s' in list '%s' on '%s'" % (items[item_num][0], self.list[list_num][1], c_name, l_title, b_title)
                    Thanos.Activity_notice("CARD", self.Card_ID, self.User_ID, self.db, act_str)
                    break
                else:
                    print("Wrong number! please enter again")
            except:
                print("Wrong number! please enter again")
    def edit_checkitem(self, list_num, items):
        while True:
            try:
                for i in range(len(items)):
                    if items[i + 1][1] == 'T':
                        print(str(i + 1) + ". ☑ " + items[i + 1][0])
                    elif items[i + 1][1] == 'F':
                        print(str(i + 1) + ". ☐ " + items[i + 1][0])
                item_num = input("\nWhich Item? (q : go back) >> ")
                if item_num == 'q':
                    print("return to previous view")
                    break
                item_num = int(item_num)
                if item_num in items:
                    # check item을 "make ER- diagram" 수정
                    item = "Make ER-Diagram"
                    item_list = ""
                    for i in range(len(items)):
                        if item_num != i + 1:
                            item_list = item_list + items[i + 1][0] + ":" + items[i + 1][1] + ","
                        else:
                            item_list = item_list + item + ":" + items[i + 1][1] + ","
                    item_list = item_list.rstrip(",")
                    sql = "UPDATE Checklist SET Check_Item = '%s' WHERE Checklist_ID = %d" % (item_list, self.list[list_num][0])
                    self.cursor.execute(sql)
                    self.db.commit()

                    c_name, b_title, l_title = self.Activity_manager.for_activity()
                    act_str = "Edit Checklist item '%s' to '%s' from Checklist '%s' included with card '%s' in list '%s' on '%s'" % (items[item_num][0], item, self.list[list_num][1], c_name, l_title, b_title)
                    Thanos.Activity_notice("CARD", self.Card_ID, self.User_ID, self.db, act_str)
                    break
                else:
                    print("Wrong number! please enter again")
            except:
                print("Wrong number! please enter again")
    def toggle_checkitem(self, list_num, items):
        while True:
            try:
                for i in range(len(items)):
                    if items[i + 1][1] == 'T':
                        print(str(i + 1) + ". ☑ " + items[i + 1][0])
                    elif items[i + 1][1] == 'F':
                        print(str(i + 1) + ". ☐ " + items[i + 1][0])
                item_num = input("\nWhich Item? (q : go back) >> ")
                if item_num == 'q':
                    print("return to previous view")
                    break
                item_num = int(item_num)
                if item_num in items:
                    item_list = ""
                    c_name, b_title, l_title = self.Activity_manager.for_activity()
                    for i in range(len(items)):
                        if item_num == i + 1:
                            if items[i + 1][1] == 'F':
                                act_str = "Completed item '%s' in Checklist '%s' included with card '%s' in list '%s' on '%s'" % (items[item_num][0], self.list[list_num][1], c_name, l_title, b_title)
                                item_list = item_list + items[i + 1][0] + ":T,"
                            else:
                                act_str = "Unmarked item '%s' in Checklist '%s' included with card '%s' in list '%s' on '%s'" % (items[item_num][0], self.list[list_num][1], c_name, l_title, b_title)
                                item_list = item_list + items[i + 1][0] + ":F,"
                        else:
                            item_list = item_list + items[i + 1][0] + ":" + items[i + 1][1] + ","                            
                    item_list = item_list.rstrip(",")
                    sql = "UPDATE Checklist SET Check_Item = '%s' WHERE Checklist_ID = %d" % (item_list, self.list[list_num][0])
                    self.cursor.execute(sql)
                    self.db.commit()

                    Thanos.Activity_notice("CARD", self.Card_ID, self.User_ID, self.db, act_str)
                    break
                else:
                    print("Wrong number! please enter again")
            except:
                print("Wrong number! please enter again")
class Comment_List_Manager:
    def __init__(self, Card_ID, User_ID, DB):
        self.Activity_manager = Activity_Manager(Card_ID, User_ID, DB)
        self.cursor = DB.cursor()
        self.Card_ID = Card_ID
        self.User_ID = User_ID
        self.db = DB
        self.list = {}
    @staticmethod
    def comment_menu():
        print("\n1. Add Comment")
        print("2. Delete Comment")
        print("3. Edit Comment")
        print("4. Go Back")
    def setting(self):
        self.list = {}
        sql = "SELECT Comment_ID, User_ID, Content, DateTime, Is_edited FROM Comment WHERE Card_ID = %d AND Is_deleted = 'N'" % self.Card_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if not result:
            return False
        else :
            i = 1
            for cm_id, user_id, text, time, edit in result:
                sql = "SELECT User_Name, Is_deleted FROM User WHERE User_ID = %d" % user_id
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                u_name = result[0]
                del_user = result[1]
                if del_user == 'Y':
                    u_name = "Withdraw_User"
                self.list[i] = (cm_id, user_id, u_name, text, time, edit)
                i += 1
            return True
    def print_comments(self):
        for i in range(len(self.list)):
            if self.list[i + 1][5] == 'Y':
                print(str(i + 1) + ".", self.list[i + 1][2], self.list[i + 1][4], "(edited)")
            else:
                print(str(i + 1) + ".", self.list[i + 1][2], self.list[i + 1][4])
            if self.list[i + 1][1] == self.User_ID:
                print("   " + self.list[i + 1][3] + " ✐ ✄")
            else:
                print("   " + self.list[i + 1][3])
    def add(self):
        # Lovely JC 라는 comment 작성
        # comment = "Lovely JC"
        comment = input("new comment : ")
        sql = "INSERT INTO Comment (User_ID, Card_ID, Content) VALUES(%d, %d, '%s')" % (self.User_ID, self.Card_ID, comment)
        self.cursor.execute(sql)
        self.db.commit()

        c_name, b_title, l_title = self.Activity_manager.for_activity()
        act_str = "Add Comment to card '%s' in list '%s' on '%s'" % (c_name, l_title, b_title)
        Thanos.Activity_notice("CARD", self.Card_ID, self.User_ID, self.db, act_str)
    def delete(self):
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("-----------------------------------\n              Comment\n-----------------------------------")
                self.print_comments()
                comment_num = input("\nWhich Comment? (q : go back) >> ")
                if comment_num == 'q':
                    print("return to previous view")
                    break
                comment_num = int(comment_num)
                if comment_num in self.list:
                    if self.list[comment_num][1] == self.User_ID:
                        sql = "UPDATE Comment SET Is_deleted = 'Y' WHERE Comment_ID = %d" % self.list[comment_num][0]
                        self.cursor.execute(sql)
                        self.db.commit()
                        break
                    else:
                        print("It's not your comment!")
                        break
                else:
                    print("Wrong number! please enter again")
            except:
                print("Wrong number! please enter again")
    def edit(self):
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("-----------------------------------\n              Comment\n-----------------------------------")
                self.print_comments()
                comment_num = input("\nWhich Comment? (q : go back) >> ")
                if comment_num == 'q':
                    print("return to previous view")
                    break
                comment_num = int(comment_num)
                if comment_num in self.list:
                    if self.list[comment_num][1] == self.User_ID:
                        # Lovely JH 라는 comment로 수정
                        # modified = "Lovely JH"
                        modified = input("comment : ")
                        sql = "UPDATE Comment SET Content = '%s', DateTime = CURRENT_TIMESTAMP, Is_edited = 'Y' WHERE Comment_ID = %d" % (modified, self.list[comment_num][0])
                        self.cursor.execute(sql)
                        self.db.commit()
                        print("Edit Comment")
                        break
                    else:
                        print("It's not your comment!")
                        break
                else:
                    print("Wrong number! please enter again")
            except:
                print("Wrong number! please enter again")
class Attachment_List_Manager:
    def __init__(self, Card_ID, User_ID, DB):
        self.Activity_manager = Activity_Manager(Card_ID, User_ID, DB)
        self.cursor = DB.cursor()
        self.Card_ID = Card_ID
        self.User_ID = User_ID
        self.db = DB
        self.list = {}
    @staticmethod
    def attachment_menu():
        print("\n1. Add an Attachment")
        print("2. Delete an Attachment")
        print("3. Edit an Attachment")
        print("4. Go Back")
    def setting(self):
        self.list = {}
        sql = "SELECT Attachment_ID, User_ID, Type, Name, DATE_FORMAT(DateTime, '%%Y %%b %%d %%T') FROM Attachment WHERE Card_ID = %d AND Is_deleted = 'N'" % self.Card_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if not result:
            return False
        else :
            i = 1
            for am_id, user_id, type_, name, time in result:
                self.list[i] = (am_id, user_id, name, type_, time)
                i += 1
            return True
    def print_attachments(self):
        for i in range(len(self.list)):
            print(str(i + 1) + ". " + self.list[i + 1][2] + "." + self.list[i + 1][3])
            print("   Added", self.list[i + 1][4])
    def add(self):
        # DB_Query라는 이름의 docx 파일 첨부
        Type = "docx"
        Name = "DB_Query"
        sql = "INSERT INTO Attachment(Card_ID, User_ID, Type, Name) VALUES(%d, %d, '%s', '%s')" % (self.Card_ID, self.User_ID, Type, Name)
        self.cursor.execute(sql)
        self.db.commit()

        c_name, b_title, l_title = self.Activity_manager.for_activity()
        act_str = "Add Attachment '%s' to card '%s' in list '%s' on '%s'" % (Name + "." + Type, c_name, l_title, b_title)
        Thanos.Activity_notice("CARD", self.Card_ID, self.User_ID, self.db, act_str)
    def delete(self):
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("-----------------------------------\n            Attachment\n-----------------------------------")
                self.print_attachments()              
                attach_num = input("\nWhich Attachment? (q : go back) >> ")
                if attach_num == 'q':
                    print("return to previous view")
                    break
                attach_num = int(attach_num)
                if attach_num in self.list:
                    sql = "UPDATE Attachment SET Is_deleted = 'Y' WHERE Attachment_ID = %d" % self.list[attach_num][0]
                    self.cursor.execute(sql)
                    self.db.commit()

                    c_name, b_title, l_title = self.Activity_manager.for_activity()
                    act_str = "Deleted Attachment '%s' from card '%s' in list '%s' on '%s'" % (self.list[attach_num][2] + "." + self.list[attach_num][3], c_name, l_title, b_title)
                    Thanos.Activity_notice("CARD", self.Card_ID, self.User_ID, self.db, act_str)
                    break
                else:
                    input("Wrong number! please enter again >>")
            except:
                print("Wrong number! please enter again")
    def edit(self):
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("-----------------------------------\n            Attachment\n-----------------------------------")
                self.print_attachments() 
                attach_num = input("\nWhich Attachment? (q : go back) >> ")
                if attach_num == 'q':
                    print("return to previous view")
                    break
                attach_num = int(attach_num)
                if attach_num in self.list:
                    # DB_ER-Diagram으로 name 변경
                    Name = "DB_ER-Diagram"
                    sql = "UPDATE Attachment SET Name = '%s' WHERE Attachment_ID = %d" % (Name, self.list[attach_num][0])
                    self.cursor.execute(sql)
                    self.db.commit()

                    c_name, b_title, l_title = self.Activity_manager.for_activity()
                    act_str = "Edited name of Attachment '%s' to '%s' included with card '%s' in list '%s' on '%s'" % (self.list[attach_num][2] + "." + self.list[attach_num][3], Name + "." + self.list[attach_num][3], c_name, l_title, b_title)
                    Thanos.Activity_notice("CARD", self.Card_ID, self.User_ID, self.db, act_str)
                    break
                else:
                    print("Wrong number! please enter again")
            except:
                print("Wrong number! please enter again")
class Activity_List_Manager:
    def __init__(self, Card_ID, cursor):
        self.Card_ID = Card_ID
        self.cursor = cursor
        self.list = {}
    def setting(self):
        self.list = {}
        sql = "SELECT Activity_ID, User_ID, Action, DateTime FROM Activity WHERE Card_ID = %d" % self.Card_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        if not result:
            return False
        else :
            i = 1
            for av_id, user_id, action, time in result:
                sql = "SELECT User_Name, Is_deleted FROM User WHERE User_ID = %d" % user_id
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                u_name = result[0]
                del_user = result[1]
                if del_user == 'Y':
                    u_name = "Withdraw_User"
                idx = action.find(' in list')
                if idx == -1:
                    idx = len(action)
                action = action[0:idx]
                self.list[i] = (av_id, user_id, u_name, action, time)
                i += 1
            return True
    def print_acticities(self):
        for i in range(len(self.list)):
            print(self.list[i + 1][2], self.list[i + 1][3], "(",self.list[i + 1][4],")")
