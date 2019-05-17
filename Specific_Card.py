import Thanos
import random
import string
import Lists
import os


class Specific_Card_Manager:
    def __init__(self, card_ID, user_ID, DB):
        self.Attachment_list = Lists.Attachment_List_Manager(card_ID, user_ID, DB)
        self.Checklist_list = Lists.Checklist_List_Manager(card_ID, user_ID, DB)
        self.Activity_list = Lists.Activity_List_Manager(card_ID, DB.cursor())
        self.Comment_list = Lists.Comment_List_Manager(card_ID, user_ID, DB)
        self.Activity_manager = Lists.Activity_Manager(card_ID, user_ID, DB)
        self.Label_list = Lists.Label_List_Manager(card_ID, user_ID, DB)
        self.cursor = DB.cursor()
        self.card_ID = card_ID
        self.user_ID = user_ID
        self.db = DB
        self.init_ids()
        self.start()
    def init_ids(self):
        # init list_id and board_id
        sql = "SELECT List_ID FROM Card WHERE Card_ID = %d" % self.card_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        self.list_ID = result[0]
        sql = "SELECT Board_ID FROM List WHERE List_ID = %d" % self.list_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        self.board_ID = result[0]
    def start(self):
        choice = 0
        while choice != '7':
            os.system('cls' if os.name == 'nt' else 'clear')
            self.card_info()
            print("\n1. Edit Card\n2. Checklists\n3. Comments\n4. Attachments\n5. Activity\n6. Share\n7. Back to List")
            choice = input("\nEnter the number for your choice : ")
            if choice == '1':
                self.edit_card()
            elif choice == '2':
                self.checklists()
            elif choice == '3':
                self.comments()
            elif choice == '4':
                self.attachments()
            elif choice == '5':
                self.activity()
            elif choice == '6':
                self.share()
            elif choice == '7':
                break
            else:
                input("Wrong choice! Please enter again >>")
    def card_info(self):
        # card information
        try:
            sql1 = "SELECT Card_Title, Description, Members, Label_ID, DATE_FORMAT(Due_Date, '%%Y %%b %%d (%%a)') FROM Card WHERE Card_ID = %d" % self.card_ID
            sql2 = "SELECT * FROM Watch WHERE ID_type = 'CARD' AND ID = %d AND User_ID = %d" % (self.card_ID, self.user_ID)
            self.cursor.execute(sql1)
            result1 = self.cursor.fetchone()
            self.cursor.execute(sql2)
            result2 = self.cursor.fetchone()
            Title = result1[0]
            Due_date = result1[4]
            Member = result1[2]
            Label = self.Label_list.setting_labels(result1[3])
            Description = result1[1]
            if not result2:
                print("Title : " + Title + " ⁎ᵕᴗᵕ⁎")
            else:
                print("Title : " + Title + " ⁎⊙ᴗ⊙⁎")
            if Due_date:
                print("Due Date :", Due_date)
            if Label:
                self.Label_list.print_labels()
            print("Member : " + Member)
            if Description:
                print("Description : " + Description)
        except:
            print("Card info errors")
    def edit_card(self):
        print("\n1. Edit Title\n2. Edit Description\n3. Toggle Watch\n4. Add/Remove Label\n5. Add/Remove/Edit Due Date\n6. Go Back")        
        while True:
            choice = input("\nEnter the number for your choice : ")
            if choice == '1':
                self.edit_title()
                break
            elif choice == '2':
                self.edit_description()
                break
            elif choice == '3':
                self.toggle_watch()
                break
            elif choice == '4':
                self.label()
                break
            elif choice == '5':
                self.due_date()
                break
            elif choice == '6':
                break
            else:
                print("Wrong choice! Please enter again")
    def edit_title(self):
        # 현재 카드의 title을 HELLO로 변경
        try:
            modified = "HELLO"
            sql = "UPDATE Card SET Card_Title = '%s' WHERE Card_ID = %d" % (modified, self.card_ID)
            self.cursor.execute(sql)
            self.db.commit()

            c_name, b_title, l_title = self.Activity_manager.for_activity()
            act_str = "Edited title of card '%s' to '%s' in list '%s' on '%s'" % (c_name, modified, l_title, b_title)
            Thanos.Activity_notice("CARD", self.card_ID, self.user_ID, self.db, act_str)
        except:
            print("Edit Title error")
    def edit_description(self):
        # 현재 카드의 Description을 HELLO, WORD로 변경
        try:
            modified = "HELLO, WORD"
            sql = "UPDATE Card SET Description = '%s' WHERE Card_ID = %d" % (modified, self.card_ID)
            self.cursor.execute(sql)
            self.db.commit()

            c_name, b_title, l_title = self.Activity_manager.for_activity()
            act_str = "Edited description of card '%s' in list '%s' on '%s'" % (c_name, l_title, b_title)
            Thanos.Activity_notice("CARD", self.card_ID, self.user_ID, self.db, act_str)
        except:
            print("Edit Description error")
    def toggle_watch(self):
        try:
            sql = "SELECT * FROM Watch WHERE ID_type = 'CARD' AND ID = %d AND User_ID = %d" % (self.card_ID, self.user_ID)
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            if result:
                sql = "DELETE FROM Watch WHERE ID_type = 'CARD' AND ID = %d AND User_ID = %d" % (self.card_ID, self.user_ID)
                self.cursor.execute(sql)
                self.db.commit()
            else:
                sql = "INSERT INTO Watch (User_ID, ID_type, ID) VALUES (%d, 'CARD', %d)" % (self.user_ID, self.card_ID)    
                self.cursor.execute(sql)
                self.db.commit()
            os.system('cls' if os.name == 'nt' else 'clear')                
            print("Toggling the watch info\n")
        except:
            print("Card toggle watch error")
    def label(self):
        sql = "SELECT Label_ID FROM Card WHERE CARD_ID = %d" % self.card_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        Label = self.Label_list.setting_labels(result[0])
        if not Label:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Label : Empty")
                choice = input("\n(1) Add Label  (q : Go back) >> ")
                if choice == 'q':
                    break
                elif choice == '1':
                    self.Label_list.add_label()
                    break
                else:
                    input("Wrong choice! Please enter again >>")
        else:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                self.Label_list.print_labels()
                choice = input("\n(1) Add Label  (2) Remove Label  (q : Go back) >> ")
                if choice == 'q':
                    input("return to previous view >> ")
                    break
                elif choice == '1':
                    self.Label_list.add_label()
                    break
                elif choice == '2':
                    # 1번 라벨 삭제
                    r_label = 1
                    self.Label_list.remove_label(r_label)
                    break
                else:
                    input("Wrong choice! Please enter again >>")
    def due_date(self):
        sql = "SELECT DATE_FORMAT(Due_Date , '%%Y %%b %%d (%%a)') FROM Card WHERE Card_ID = %d" % self.card_ID
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if not result[0]:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Due Date : Empty")
                choice = input("\n(1)Add Due Date  (q : Go back) >> ")
                if choice == 'q':
                    break
                elif choice == '1':
                    # Due_Date를 May 19 (Sun)으로 생성
                    Due_Date = "2019-05-19"
                    sql = "UPDATE Card SET Due_Date = TIMESTAMP('%s') WHERE Card_ID = %d" % (Due_Date, self.card_ID)
                    self.cursor.execute(sql)
                    self.db.commit()

                    c_name, b_title, l_title = self.Activity_manager.for_activity()
                    act_str = "Created Due date of card '%s' in list '%s' on '%s'" % (c_name, l_title, b_title)
                    Thanos.Activity_notice("CARD", self.card_ID, self.user_ID, self.db, act_str)
                    break
                else:
                    input("Wrong choice! Please enter again >>")
        else:
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Due Date:", result[0])
                choice = input("\n(1)Edit Due Date  (2)Remove Due Date  (q : Go back) >> ")
                if choice == 'q':
                    break
                elif choice == '1':
                    # Due_Date를 May 20 (Mon)으로 변경
                    Due_Date = "2019-05-20"
                    sql = "UPDATE Card SET Due_Date = TIMESTAMP('%s') WHERE Card_ID = %d" % (Due_Date, self.card_ID)
                    self.cursor.execute(sql)                    
                    self.db.commit()

                    c_name, b_title, l_title = self.Activity_manager.for_activity()
                    act_str = "Edited Due date of card '%s' in list '%s' on '%s'" % (c_name, l_title, b_title)
                    Thanos.Activity_notice("CARD", self.card_ID, self.user_ID, self.db, act_str)
                    break
                elif choice == '2':
                    sql = "UPDATE Card SET Due_Date = NULL WHERE Card_ID = %d" % self.card_ID
                    self.cursor.execute(sql)
                    self.db.commit()

                    c_name, b_title, l_title = self.Activity_manager.for_activity()
                    act_str = "Deleted Due date of card '%s' in list '%s' on '%s'" % (c_name, l_title, b_title)
                    Thanos.Activity_notice("CARD", self.card_ID, self.user_ID, self.db, act_str)
                    break
                else:
                    input("Wrong choice! Please enter again >>")
    def checklists(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            is_checklists = self.Checklist_list.setting()
            print("-----------------\n    Checklist\n-----------------")
            if is_checklists:
                self.Checklist_list.print_checklist_list()
                Lists.Checklist_List_Manager.checklist_menu()
                choice = 0
                while True:
                    choice = input("\nEnter the number for your choice : ")
                    if choice == '1':
                        self.Checklist_list.create()
                        break
                    elif choice == '2':
                        self.Checklist_list.delete()
                        break
                    elif choice == '3':
                        self.Checklist_list.print_checklist()
                        break
                    elif choice == '4':
                        self.Checklist_list.edit()
                        break
                    elif choice == '5':
                        return
                    else:
                        print("Wrong choice! Please enter again")
            else:
                print("Empty")
                while True:
                    answer = input("\nDo you want to create a new checklist?(y/n) : ")
                    if answer == 'y':
                        self.Checklist_list.create()
                        break
                    elif answer == 'n':
                        input("return to previous view >>")
                        return
                    else:
                        print("Wrong character! please enter again")
    def comments(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            is_comments = self.Comment_list.setting()
            print("-----------------------------------\n              Comment\n-----------------------------------")
            if is_comments:
                self.Comment_list.print_comments()
                Lists.Comment_List_Manager.comment_menu()
                choice = 0
                while True:
                    choice = input("\nEnter the number for your choice : ")
                    if choice == '1':
                        self.Comment_list.add()
                        break
                    elif choice == '2':
                        self.Comment_list.delete()
                        break
                    elif choice == '3':
                        self.Comment_list.edit()
                        break
                    elif choice == '4':
                        return
                    else:
                        print("Wrong choice! Please enter again")
            else:
                print("Empty")
                while True:
                    answer = input("\nAdd Comment?(y/n) : ")
                    if answer == 'y':
                        self.Comment_list.add()
                        break
                    elif answer == 'n':
                        input("return to previous view >>")
                        return
                    else:
                        print("Wrong character! please enter again")
    def attachments(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("-----------------------------------\n            Attachment\n-----------------------------------")
            is_attachment = self.Attachment_list.setting()
            self.Attachment_list.print_attachments()
            if is_attachment:
                Lists.Attachment_List_Manager.attachment_menu()
                choice = 0
                while True:
                    choice = input("\nEnter the number for your choice : ")
                    if choice == '1':
                        self.Attachment_list.add()
                        break
                    elif choice == '2':
                        self.Attachment_list.delete()
                        break
                    elif choice == '3':
                        self.Attachment_list.edit()
                        break
                    elif choice == '4':
                        return
                    else:
                        print("Wrong choice! Please enter again")
            else:
                print("Empty")
                while True:
                    answer = input("\nAdd an Attachment?(y/n) : ")
                    if answer == 'y':
                        self.Attachment_list.add()
                        break
                    elif answer == 'n':
                        input("return to previous view >>")
                        return
                    else:
                        print("Wrong character! please enter again")
    def activity(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("----------------------------------------------------------------------------------------------------------------\n                                                 Activity\n----------------------------------------------------------------------------------------------------------------")
        if self.Activity_list.setting():
            self.Activity_list.print_acticities()
            input("\nreturn to previous view >>")
        else:
            print("Empty")
            input("\nreturn to previous view >>")
    def share(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        url = "https://bit.ly/"
        url = url + random.choice(string.digits)
        for i in range(6):
            url = url + random.choice(string.ascii_letters)
        print("----------------------------------------")
        print("Sharing URL : " + url)
        print("----------------------------------------")
        input("\nreturn to previous view >>")

