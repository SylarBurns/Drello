import Lists
import os

class Specific_Card_Manager:
    def __init__(self, card_ID, user_ID, DB):
        self.db = DB
        self.cursor = self.db.cursor()
        self.Attachment_list = Lists.Attachment_List_Manager(card_ID, self.cursor)
        self.Checklist_list = Lists.Checklist_List_Manager(card_ID, self.cursor)
        self.Activity_list = Lists.Activity_List_Manager(card_ID, self.cursor)
        self.Comment_list = Lists.Comment_List_Manager(card_ID, self.cursor)
        self.Label_list = Lists.Label_List_Manager(card_ID, self.cursor)
        self.card_ID = card_ID
        self.user_ID = user_ID
        self.start()
    def start(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Specific Card start!")
        choice = 0

        while choice != '7':
            self.card_info()
            Specific_Card_Manager.menu()
            # print("1. Edit Card\n2. Checklists\n3. Comments\n4. Attachments\n5. Activity\n6. Share\n7. Go Back")
            choice = input("Enter the number for your choice : ")
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
                print("return to previous view")
                break
            else:
                print("Wrong choice! Please enter again")
    @staticmethod
    def menu():
        print("1. Edit Card")
        print("2. Checklists")
        print("3. Comments")
        print("4. Attachments")
        print("5. Activity")
        print("6. Share")
        print("7. Go Back")
    @staticmethod
    def card_menu():
        print("1. Edit Title")
        print("2. Edit Description")
        print("3. Toggle Watch")
        print("4. Add/Remove Label")
        print("5. Add/Remove/Edit Due Date")
        print("6. Go Back")
    def card_info(self):
        # get card information by using sql
        sql1 = "SELECT Card_Title, Description, Members, Label_ID, Due_Date FROM Card WHERE CARD_ID = %d" % self.card_ID
        sql2 = "SELECT Mark FROM Watch WHERE ID_type = 'CARD' AND ID = %d AND User_ID = %d" % (self.card_ID, self.user_ID)
        self.cursor.execute(sql1)
        result1 = self.cursor.fetchone()
        self.cursor.execute(sql2)
        result2 = self.cursor.fetchone()
        if result1 is not None and result2 is not None:
            Title = result1[0]
            Due_date = result1[4]
            Member = result1[2]
            Label = self.Label_list.setting_labels(result1[3])
            Description = result1[1]
            Watch = result2[0]
            if Watch:
                print("Title : " + Title + "*")
            else:
                print("Title : " + Title)
            print("Due Date : " + Due_date)
            if Label:
                self.Label_list.print_labels()
            print("Member : " + Member)
            print("Description : " + Description)
        else :
            print("No Card")
    def edit_card(self):
        while True:
            Specific_Card_Manager.card_menu()
            # print("1. Edit Title\n2. Edit Description\n3. Toggle Watch\n4. Add/Remove Label\n5. Add/Remove/Edit Due Date\n6. Go Back")
            choice = 0
            while True:
                choice = input("Enter the number for your choice : ")
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
                elif choice == '5':
                    self.due_date()
                    break
                elif choice == '6':
                    print("return to previous view")
                    break
                else:
                    print("Wrong choice! Please enter again")
    def edit_title(self):
        # 현재 카드의 title을 HELLO로 변경
        edit_title = "HELLO"
        sql = "UPDATE Card SET Card_Title = %s WHERE Card_ID = %d" % (edit_title, self.card_ID)
        self.db.commit()
    def edit_description(self):
        print("Edit Description")
    def toggle_watch(self):
        print("Toggling the watch info")
        # Update the watch state
    def due_date(self):
        while True:
            # due date 가져오기
            dd = ""
            if dd == "null":
                choice = input("(1)Add Due Date  (q : Go back)")
                if choice == 'q':
                    print("return to previous view")
                    break
                elif choice == '1':
                    print("Add Due Date")
                else:
                    print("Wrong choice! Please enter again")
            else:
                choice = input("(1)Edit Due Date  (2)Remove Due Date  (q : Go back)")
                if choice == 'q':
                    print("return to previous view")
                    break
                elif choice == '1':
                    print("Edit Due Date")
                elif choice == '2':
                    print("Remove Due Date")
                else:
                    print("Wrong choice! Please enter again")
    def label(self):
        while True:
            # label 가져오기
            l = ""
            if l == "null":
                choice = input("(1)Add Label  (q : Go back)")
                if choice == 'q':
                    print("return to previous view")
                    break
                elif choice == '1':
                    print("Add Label")
                else:
                    print("Wrong choice! Please enter again")
            else:
                choice = input("(1)Add Label  (2)Remove Label  (q : Go back)")
                if choice == 'q':
                    print("return to previous view")
                    break
                elif choice == '1':
                    print("Add Label")
                elif choice == '2':
                    print("Remove Label")
                else:
                    print("Wrong choice! Please enter again")
    def checklists(self):
        while True:
            is_checklists = self.Checklist_list.setting()
            self.Checklist_list.print_checklist_list()
            if is_checklists:
                Lists.Checklist_List_Manager.checklist_menu()
                choice = 0
                while True:
                    choice = input("Enter the number for your choice : ")
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
                        print("return to previous view")
                        return
                    else:
                        print("Wrong choice! Please enter again")
            else:
                while True:
                    answer = input("Do you want to create a new checklist?(y/n) : ")
                    if answer == 'y':
                        self.Checklist_list.create()
                        break
                    elif answer == 'n':
                        print("return to previous view")
                        return
                    else:
                        print("Wrong character! please enter again")
    def comments(self):
        while True:
            is_comments = self.Comment_list.setting()
            self.Comment_list.print_comments()
            if is_comments:
                Lists.Comment_List_Manager.comment_menu()
                choice = 0
                while True:
                    choice = input("Enter the number for your choice : ")
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
                        print("return to previous view")
                        return
                    else:
                        print("Wrong choice! Please enter again")
            else:
                while True:
                    answer = input("Add Comment?(y/n) : ")
                    if answer == 'y':
                        self.Comment_list.add()
                        break
                    elif answer == 'n':
                        print("return to previous view")
                        return
                    else:
                        print("Wrong character! please enter again")
    def attachments(self):
        while True:
            is_attachment = self.Attachment_list.setting()
            self.Attachment_list.print_attachments()
            if is_attachment:
                Lists.Attachment_List_Manager.attachment_menu()
                choice = 0
                while True:
                    choice = input("Enter the number for your choice : ")
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
                        print("return to previous view")
                        return
                    else:
                        print("Wrong choice! Please enter again")
            else:
                while True:
                    answer = input("Add an Attachment?(y/n) : ")
                    if answer == 'y':
                        self.Attachment_list.add()
                        break
                    elif answer == 'n':
                        print("return to previous view")
                        return
                    else:
                        print("Wrong character! please enter again")
    def activity(self):
        self.Activity_list.setting()
        self.Activity_list.print_acticities()
    def share(self):
        url = ""
        print("Sharing URL : " + url)
