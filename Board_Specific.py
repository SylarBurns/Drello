from list_part import *

class Specific_Board_Manager:
    def __init__(self, new_Board_ID, new_cursor):
        self.Board_ID = new_Board_ID
        self.mycursor = new_cursor
        self.count = 5
        self.Notice_list={}
        self.start()
    def board_info(self):
        print("Title: ")
        print("Team: ")
        print("Member: ")
        print("Watch: ")
        print("Label: ")
    def board_toggle_watch(self):
        print("Toggling the watch info")
    def board_edit(self):
        print("Start editing")
    def lists(self):
        print("Entering the list of lists")
        dummy_list = 1
        ListofLists(dummy_list)
    def board_notice(self):
        myresult = [('firstNotice', 1), ('secondNotice', 2), ('thirdNotice', 3)]
        for (content, ID) in myresult:
            print(self.count, content)
            self.Notice_list[self.count] = ID #form a dictionary {count:Board_ID}
            self.count += 1
            self.Max_Count = self.count
        self.count = 5
    def board_notice_check(self, choice):
        print("Marking notice",self.Notice_list[choice],"as checked")
    def start(self):
        print("Let's get this party started!")
        choice = 0
        while(choice != 4):
            self.board_info()
            print("1 View Lists\n2 Toggle Watch\n3 Edit Board Information\n4 Go Back\n------------\nYour Notices\n------------")
            self.board_notice();
            choice = input("Enter the number for your choice: ")
            choice = int(choice)
            if choice == 1:
                self.lists()
            elif choice == 2:
                self.board_toggle_watch()
            elif choice == 3:
                self.board_edit()
            elif choice == 4:
                print("return to previous view")
            elif choice >= 5 and choice <= self.Max_Count:
                self.board_notice_check(choice)
            else:
                print("Wrong choice! please enter again")

