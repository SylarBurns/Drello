class Label_List_Manager:
    def __init__(self, Card_ID, cursor):
        self.Card_ID = Card_ID
        self.cursor = cursor
        self.list = {}
    def setting_labels(self):
        # get data qry
        # label id 가져와서 label table에서 name, color 받아오기
        label_id = 1234
        name = "name"
        color = "color"
        i = 1
        self.list[i] = (label_id, name, color)
    def print_labels(self):
        print("Label : ", end = "")
        for i in range(len(self.list)):
            print(self.list[i + 1][1], end = " ")
        print()

class Checklist_List_Manager:
    def __init__(self, Card_ID, cursor):
        self.Card_ID = Card_ID
        self.cursor = cursor
        self.list = {}
    @staticmethod
    def checklist_menu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("1. Create new Checklist")
        print("2. Delete Checklist")
        print("3. View Checklist")
        print("4. Edit Checklist")
        print("5. Go Back")
    def setting(self):
        # get data qry
        # checklist id 가져와서 table에서 id, name 받아오기
        L = []
        if len(L) == 0:
            return False
        else :
            i = 1
            for ID, name in L:
                self.list[i] = (ID, name)
                i += 1
            return True
    def print_checklist_list(self):
        print("-----------\n   Checklist   \n-----------")
        if len(self.list) == 0:
            print("Empty")
        else :
            for i in range(len(self.list)):
                print(str(i + 1) + " " + self.list[i][1])
    def create(self):
        # update data qry
        name = ""
        print("Create checklist '" + name + "'")
    def delete(self):
        while True:
            try:
                checklist_num = int(input("Which Checklist?(0 : go back) >> "))
                if checklist_num == 0:
                    print("return to previous view")
                    break
                elif checklist_num in self.list:
                    # update data qry
                    name = ""
                    print("Delete checklist '" + name + "'")
                    break
                else:
                    print("Wrong number! please enter again")
            except:
                print("Wrong number! please enter again")
    def print_checklist(self):
        while True:
            try:
                checklist_num = int(input("Which Checklist?(0 : go back) >> "))
                if checklist_num == 0:
                    print("return to previous view")
                    break
                elif checklist_num in self.list:
                    ID = self.list[checklist_num][0]
                    name = self.list[checklist_num][1]
                    print("Checklist '" + name + "'")
                    items = [] # get data qry
                    if len(items) == 0:
                        print("Empty")
                    else:
                        for item in items:
                            to_do = ""
                            checked = False
                            print("☑ ☐" + to_do)
                    break
                else:
                    print("Wrong number! please enter again")
            except:
                print("Wrong number! please enter again")
    def edit(self):
        while True:
            try:
                checklist_num = int(input("Which Checklist?(0 : go back) >> "))
                if checklist_num == 0:
                    print("return to previous view")
                    break
                elif checklist_num in self.list:
                    # update data qry
                    name = ""
                    print("Edit checklist '" + name + "'")
                    break
                else:
                    print("Wrong number! please enter again")
            except:
                print("Wrong number! please enter again")

class Comment_List_Manager:
    def __init__(self, Card_ID, cursor):
        self.Card_ID = Card_ID
        self.cursor = cursor
        self.list = {}
    @staticmethod
    def comment_menu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("1. Add Comment")
        print("2. Delete Comment")
        print("3. Edit Comment")
        print("4. Go Back")
    def setting(self):
        # get data qry
        # comments id 가져와서 table에서 is_Deleted == False 인 id, userid, comment, time 받아오기
        L = []
        if len(L) == 0:
            return False
        else :
            i = 1
            for ID, u_id, comment, time in L:
                self.list[i] = (ID, u_id, comment, time)
                i += 1
            return True
    def print_comments(self):
        print("-----------\n    Comment    \n-----------")
        if len(self.list) == 0:
            print("Empty")
        else :
            for i in range(len(self.list)):
                print(str(i + 1) + " writer : " + self.list[i][1])
                print(self.list[i][2] + "(time : " + self.list[i][3] + ")")
    def add(self):
        # update data qry
        print("Add Comment")
    def delete(self):
        # update data qry
        print("Delete Comment")
    def edit(self):
        # update data qry
        print("Edit Comment")

class Attachment_List_Manager:
    def __init__(self, Card_ID, cursor):
        self.Card_ID = Card_ID
        self.cursor = cursor
        self.list = {}
    @staticmethod
    def attachment_menu():
        os.system('cls' if os.name == 'nt' else 'clear')
        print("1. Add an Attachment")
        print("2. Delete an Attachment")
        print("3. Edit an Attachment")
        print("4. Go Back")
    def setting(self):
        # get data qry
        # attachment id 가져와서 table에서 is_Deleted == False 인 id, type, name, time 받아오기
        L = []
        if len(L) == 0:
            return False
        else :
            i = 1
            for ID, type_, name, time in L:
                self.list[i] = (ID, type_, name, time)
                i += 1
            return True
    def print_attachments(self):
        print("-----------\n  Attachment  \n-----------")
        if len(self.list) == 0:
            print("Empty")
        else :
            for i in range(len(self.list)):
                print(str(i + 1) + self.list[i][2] + "(time : " + self.list[i][3] + ")")
    def add(self):
        # update data qry
        print("Add Attachment")
    def delete(self):
        # update data qry
        print("Delete Attachment")
    def edit(self):
        # update data qry
        print("Edit Attachment")

class Activity_List_Manager:
    def __init__(self, Card_ID, cursor):
        self.Card_ID = Card_ID
        self.cursor = cursor
        self.list = {}
    def setting(self):
        # get data qry
        # activity id 가져와서 table에서 id, userid, action, time 받아오기 (time이 옛날~최신 순이 되게)
        L = []
        if len(L) == 0:
            return False
        else :
            i = 1
            for ID, u_id, action, time in L:
                self.list[i] = (ID, u_id, action, time)
                i += 1
            return True
    def print_acticities(self):
        print("-----------\n  Activity  \n-----------")
        if len(self.list) == 0:
            print("Empty")
        else :
            for i in range(len(self.list)):
                print(self.list[i][1], self.list[i][2] + "(time : " + self.list[i][3] + ")")
