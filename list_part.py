import mysql.connector
from Specific_Card import *
from Thanos import *
import os

def ListofLists(in_board, my_db, curr_user) :
    while True :
        curr_cursor = my_db.cursor(buffered=True)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("============= List of Lists ============")
        print("1. List up all list in board")
        print("2. Enter a specific list")
        print("3. Create new list")
        print("4. Delete list")
        print("5. Change list's position")
        print("6. Move specific list to another board")
        print("7. Copy specific list in this board")
        print("========================================")
        print("[0] to back to Board")
        answer = input("Give a number. : ")
        my_db.commit()

        if answer == "1" :
            sql_query = "SELECT * FROM List WHERE Board_id = %d ORDER BY Position" % in_board
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchall()
                            
            for row in my_result :
                if row[4] == 'N' :
                    print("%2d | List ID : %-3d   List Title : %s"%(row[3], row[0], row[1]))

            input("Enter to continue ...")

        elif answer == "2" :
            get_list_id = int(input("Give a list's id : "))
            sql_query = "SELECT * FROM List WHERE Board_id = %d and List_ID = %d" % (in_board, get_list_id)
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()

            if not my_result :
                print("The list can not be found.")
            elif my_result[4]=='Y' :
                print("The list has been deleted.") # 
            else :
                SpecificList(get_list_id, my_db, curr_user)

            input("Enter to continue ...")

        elif answer == "3" :
            curr_name = input("Give a new list's name : ")
            sql_query = "SELECT * FROM List WHERE Board_id = %d AND Is_deleted = 'N' ORDER BY Position DESC" % in_board
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()

            if not my_result :
                curr_position = 1
            else :
                curr_position = my_result[3]+1 

            sql_query = "INSERT INTO List (List_Title, Board_ID, Position) VALUES (%s, %s, %s)"
            input_query = [(curr_name, in_board, curr_position),]
            curr_cursor.executemany(sql_query, input_query)
            my_db.commit()
            
            curr_cursor.execute("SELECT LAST_INSERT_ID()")
            my_result = curr_cursor.fetchone()
            sql_query = "SELECT Board_Title FROM Board WHERE Board_ID = %d" % in_board
            curr_cursor.execute(sql_query)
            my_result2 = curr_cursor.fetchone()

            activity_str = "Created list '%s' on board '%s'" % (curr_name, my_result2[0])
            Activity_notice("LIST", my_result[0], curr_user, my_db, activity_str)
            input("Sucessfully saved.")

        elif answer == "4" :
            get_list_id = input("Give a list's id you want to delete : ")
            sql_query = "SELECT * FROM List WHERE Board_id = %s AND List_ID = %s" % (in_board, get_list_id)
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()

            if not my_result :
                print("The list can not be found.")
                input("Enter to continue ...")
            elif my_result[4]=='Y' :
                print("The list has already been deleted.") 
                input("Enter to continue ...")
            else :
                sql_query = "UPDATE List SET Is_deleted = 'Y' WHERE List_id = %s" % get_list_id
                curr_cursor.execute(sql_query)
                sql_query = "UPDATE LIST SET Position=Position-1 WHERE Board_ID=%d AND Position>%d" % (in_board, my_result[3])
                curr_cursor.execute(sql_query)
                my_db.commit()

                sql_query = "SELECT Board_Title FROM Board WHERE Board_ID = %d" % in_board
                curr_cursor.execute(sql_query)
                my_result2 = curr_cursor.fetchone()
                activity_str = "Deleted list '%s' from board '%s'" % (my_result[1], my_result2[0])
                Activity_notice("LIST", int(get_list_id), curr_user, my_db, activity_str)
                input("Sucessfully deleted.")

        elif answer == "5" :
            get_list_id = input("Give a list's id you want change position : ")
            get_list_position = int(input("Give a list's position : "))

            sql_query = "SELECT * FROM List WHERE List_ID = %s" % get_list_id
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()

            if not my_result :
                print("The list can not be found.")
                continue
            elif my_result[4]=='Y' :
                print("The list has been deleted.")
                continue
            elif my_result[3] > get_list_position : # 리스트를 뒤로 민다
                sql_query = "UPDATE List SET Position = Position+1 WHERE Board_ID = %d AND Position>=%d AND Position<%d AND Is_deleted = 'N'" % (in_board, get_list_position, my_result[3])
                curr_cursor.execute(sql_query)
                sql_query = "UPDATE List SET Position = %s WHERE List_ID = %s" % (get_list_position, get_list_id)
                curr_cursor.execute(sql_query)
            elif my_result[3] < get_list_position : # 리스트를 앞으로 당긴다
                sql_query = "UPDATE List SET Position=Position-1 WHERE Board_ID = %d AND Position<=%d AND Position>%d AND Is_deleted = 'N'" % (in_board, get_list_position, my_result[3])
                curr_cursor.execute(sql_query)
                sql_query = "UPDATE List SET Position = %s WHERE List_ID = %s" % (get_list_position, get_list_id)
                curr_cursor.execute(sql_query)
            else :
                print("Nothing Changed.")
                
            my_db.commit()
            activity_str = "Changed list '%s' position to %d" % (my_result[1], int(get_list_position))
            Activity_notice("LIST", int(get_list_id), curr_user, my_db, activity_str)
            input("Enter to continue ...")

        elif answer == "6" :
            get_list_id = input("Move list ID : ")
            get_board_id = input("Move to board ID : ")

            sql_query = "SELECT * FROM List WHERE Board_id = %s" % (get_board_id)
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()

            sql_query = "SELECT * FROM List WHERE Board_id = %d AND List_ID = %s ORDER BY Position DESC" % (in_board, get_list_id)
            curr_cursor.execute(sql_query)
            my_result2 = curr_cursor.fetchone()

            if not my_result :
                print("Invalid Board ID.")
            elif not my_result2 :
                print("Invalid List ID.")
            else :
                act_list_title = my_result2[1]
                sql_query = "UPDATE List SET Board_ID = %s WHERE List_ID = %s" % (get_board_id, get_list_id)
                curr_cursor.execute(sql_query)
                
                sql_query = "SELECT * FROM List WHERE Board_ID = %s ORDER BY Position DESC" % get_board_id
                curr_cursor.execute(sql_query)
                my_result = curr_cursor.fetchone()
                sql_query = "UPDATE List SET Position = %d WHERE List_ID = %s" % (my_result[3]+1, get_list_id)
                curr_cursor.execute(sql_query)
                
                sql_query = "UPDATE List SET Position = Position-1 WHERE Board_ID = %s AND Position>%d" % (in_board, my_result2[3])
                curr_cursor.execute(sql_query)
                
                my_db.commit()
                sql_query = "SELECT Board_Title FROM Board WHERE Board_ID=%d" % in_board
                curr_cursor.execute(sql_query)
                my_result = curr_cursor.fetchone()
                old_board_title = my_result[0]

                sql_query = "SELECT Board_Title FROM Board WHERE Board_ID=%s" % get_board_id
                curr_cursor.execute(sql_query)
                my_result = curr_cursor.fetchone()
                new_board_title = my_result[0]

                activity_str = "Moved list '%s' from '%s' to '%s'" % (act_list_title, old_board_title, new_board_title)
                Activity_notice("LIST", int(get_list_id), curr_user, my_db, activity_str)
            
            input("Enter to continue ...")

        elif answer == "7" :
            get_list_id = input("Give a list id : ")

            sql_query = "SELECT * FROM List WHERE Board_ID = %s AND List_ID = %s" % (in_board, get_list_id)
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchall()
            if not my_result :
                print("The list can not be found.")
                input("Enter to continue ...")
            else :
                token = my_result[0][1][-1]
                if token.isdigit() :
                    new_list_title = my_result[0][1][:-1] + str(int(token)+1)
                else :
                    new_list_title = my_result[0][1] + " 2"

                sql_query = "SELECT * FROM List WHERE Board_ID = %s ORDER BY Position DESC" % in_board
                curr_cursor.execute(sql_query)
                result = curr_cursor.fetchone()
                curr_position = result[3]+1

                sql_query = "INSERT INTO List (List_Title, Board_ID, Position) VALUES (%s, %s, %s)"
                input_query = [(new_list_title, in_board, curr_position),]
                curr_cursor.executemany(sql_query, input_query)
                my_db.commit()

                sql_query = "SELECT Board_Title FROM Board WHERE Board_ID=%d" % in_board
                curr_cursor.execute(sql_query)
                result = curr_cursor.fetchone()
                board_title = result[0]

                activity_str = "Copied list '%s' on board '%s'" % (my_result[0][1], board_title)
                Activity_notice("LIST", int(get_list_id), curr_user, my_db, activity_str)

                input("Sucessfully saved.")

        elif answer == "0" :
            break

        else :
            print("Invalid answer.")


def SpecificList(in_list, my_db, curr_user) :
    while True :
        curr_cursor =  my_db.cursor(buffered=True) 
        os.system('cls' if os.name == 'nt' else 'clear')
        print("================= List =================")
        print("1. Show list's information.")
        print("2. Enter a specific cards")
        print("3. Watch the list / Disable the watch")
        print("4. Notifications")
        print("5. Edit list's information")
        print("6. Show cards.")
        print("7. Sorting the card by title.")
        print("8. Add Card")
        print("9. Delete the card")
        print("10. Change positions of cards")
        print("11. Move specific card to another list")
        print("12. Copy specific card in this list")
        print("========================================")
        print("[0] Back to lists of list.")
        answer = input("Give the number. : ")
        my_db.commit()

        if answer == "1" :
            sql_query = """SELECT List.List_Title, Board.Board_Title FROM List, Board 
                            WHERE List.List_ID = %s AND List.Board_ID=Board.Board_ID AND List.Is_deleted='N'""" % in_list
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()
            print("List ID : %d  | Title : %s From board '%s'" % (in_list, my_result[0], my_result[1]))
            input("Enter to continue ...")

        elif answer == "2" :
            get_card_id = int(input("Give a cards's id : "))
            sql_query = "SELECT * FROM Card WHERE Card_ID = %d" % get_card_id
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()

            if not my_result :
                print("The card can not be found.")
            elif my_result[8] == 'Y' :
                print("The card has been deleted.")
            else :
                chosen_card = Specific_Card_Manager(get_card_id, curr_user, my_db) # cursor

        elif answer == "3" :
            sql_query = "SELECT * FROM Watch WHERE User_ID=%d AND ID_Type='LIST' AND ID=%d" % (curr_user, in_list)
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()

            sql_query = "SELECT * FROM List WHERE List_ID=%d" % in_list
            curr_cursor.execute(sql_query)
            input_result = curr_cursor.fetchone()

            if not my_result :
                sql_query = "INSERT INTO Watch (User_ID, ID_Type, ID) VALUES (%s, %s, %s)"
                input_query = [(curr_user, "LIST", in_list),]
                curr_cursor.executemany(sql_query, input_query)
                
                activity_str = "Watched the list '%s'" % (input_result[1])
                Activity_notice("LIST", in_list, curr_user, my_db, activity_str)
                input(activity_str)
            elif input_result[4] == 'Y' :
                print("The list has been deleted.")
            else :
                sql_query = "DELETE FROM Watch WHERE User_ID=%s AND ID_Type='LIST' AND ID=%d" % (curr_user, in_list)
                curr_cursor.execute(sql_query)

                activity_str = "Disabled watch list '%s'" % (input_result[1])
                Activity_notice("LIST", in_list, curr_user, my_db, activity_str)
                input(activity_str)

            my_db.commit()

        elif answer == "4" :
            my_db.commit()
            sql_query = """SELECT Activity.DateTime, Activity.Action FROM Activity, Notice 
                            WHERE Activity.User_ID=Notice.User_ID AND Activity.Activity_ID=Notice.Activity_ID
                            AND Activity.List_ID=%d AND Notice.Is_read='N' ORDER BY Activity.DateTime DESC""" % in_list
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchall()
            if not my_result :
                print("There is no new nofitications.")
                
            for row in my_result :
                print("%s | %s" % (row[0], row[1]))
            
            sql_query = "UPDATE Notice SET Is_read='Y' WHERE User_ID=%d AND Is_read='N'" % curr_user
            curr_cursor.execute(sql_query)

            input("Enter to continue ...")

        elif answer == "5" : 
            new_list_title = input("Give new list title : ")
            sql_query = "UPDATE List SET List_Title='%s' WHERE List_ID=%d" % (new_list_title, in_list)            
            curr_cursor.execute(sql_query)
            
            activity_str = "Edited list '%s' title" % (new_list_title)
            Activity_notice("LIST", in_list, curr_user, my_db, activity_str)
            input("Enter to continue ...")
        
        elif answer == "6" :
            order = input("1 for increasing / 2 for decreasing : ")
            if order == "1" :
                sql_query = "SELECT * FROM Card WHERE List_ID = %d ORDER BY Position" % in_list
            elif order == "2" :
                sql_query = "SELECT * FROM Card WHERE List_ID = %d ORDER BY Position DESC" % in_list
            else : 
                continue
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchall()

            for row in my_result :
                print("Card ID : %2d | Title : %s" % (row[0], row[3]))
                print("Description : %s" % row[5])
                if row[6] :
                    print("Due Date : %s" % row[6])
                print("Member : %s\n" % row[7])

            input("\nEnter to continue ...")

        elif answer == "7" :
            order = input("1 for increasing / 2 for decreasing : ")
            if order == "1" :
                sql_query = "SELECT * FROM Card WHERE List_ID = %d ORDER BY Description" % in_list
            elif order == "2" :
                sql_query = "SELECT * FROM Card WHERE List_ID = %d ORDER BY Description DESC" % in_list
            else :
                continue
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchall()

            for row in my_result :
                print("Card ID : %2d | Title : %s" % (row[0], row[3]))
                print("Description : %s" % row[5])
                if row[6] :
                    print("Due Date : %s" % row[6])
                print("Member : %s\n" % row[7])

            input("\nEnter to continue ...")

        elif answer == "8" :
            card_title = input("Give a card name : ")
            card_description = input("Give a card description : ")
            
            sql_query = """SELECT Board.Board_ID, Board.Team_ID FROM Board, List 
                            WHERE List.List_ID=%d AND List.Board_ID=Board.Board_ID""" % (in_list)
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()
            board_id = my_result[0]

            if my_result[1] == -1 : # a user owes board
                sql_query = "SELECT User_Name from User, BoardMember WHERE Board_ID = %d \
                            AND BoardMember.User_ID=User.User_ID ;" % board_id
                curr_cursor.execute(sql_query)

            else : # team owes board
                sql_query = "SELECT User.User_Name, Team_ID FROM User, TeamMember \
                            WHERE User.User_ID=TeamMember.User_ID AND Team_ID=%d \
                            AND User.Is_deleted='N' AND TeamMember.Is_deleted='N'" % my_result[1]
                curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchall()
            tmp = [row[0] for row in my_result]
            member_str = ",".join(tmp)
            
            sql_query = "SELECT Position FROM Card WHERE List_ID=%d AND Is_deleted='N' ORDER BY Position DESC" % in_list
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()
            if not my_result :
                curr_position = 1
            else :
                curr_position = my_result[0]+1
            sql_query = "INSERT INTO Card(List_ID, Card_Title, Position, Description, Members) VALUES (%s, %s, %s, %s, %s)"
            input_query = [(in_list, card_title, curr_position ,card_description, member_str),]
            curr_cursor.executemany(sql_query, input_query)
            my_db.commit()

            curr_cursor.execute("SELECT LAST_INSERT_ID()")
            my_result = curr_cursor.fetchone()
            card_id = my_result[0]

            sql_query = "SELECT List_Title FROM List WHERE List_ID=%d" % in_list
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()
            activity_str = "Created card %s on list %s" % (card_title, my_result[0])
            Activity_notice("CARD", card_id, curr_user, my_db, activity_str)
            
            input("Enter to continue ...")

        elif answer == "9" :
            get_card_id = input("Give card's id that you want to delete. : ")
            sql_query = "SELECT * FROM Card WHERE Card_id = %s AND List_ID = %d ORDER BY Position DESC" % (get_card_id, in_list)
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()

            if not my_result :
                print("The card can not be found.")
            elif my_result[4]=='Y' :
                print("The card has already been deleted.") #
            else :
                card_title = my_result[3]
                sql_query = "UPDATE Card SET Is_deleted = 'Y' WHERE Card_id = %s" % get_card_id
                curr_cursor.execute(sql_query)
                sql_query = "UPDATE Card SET Position=Position-1 WHERE List_ID=%d AND Position>%d" % (in_list, my_result[4])
                curr_cursor.execute(sql_query)
                my_db.commit()

                sql_query = "SELECT List_Title FROM List WHERE List_ID=%d" % in_list
                curr_cursor.execute(sql_query)
                my_result = curr_cursor.fetchone()
                activity_str = "Deleted card %s from list %s" % (card_title, my_result[0])
                Activity_notice("CARD", int(get_card_id), curr_user, my_db, activity_str)

                input("Sucessfully deleted.")
            input("Enter to continue ...")

        elif answer == "10" : # change positions
            get_card_id = input("Give a card's id you want change position : ")
            get_card_position = int(input("Give a card's position : "))

            sql_query = "SELECT * FROM Card WHERE List_ID = %s" % get_card_id
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()

            if not my_result :
                print("The card can not be found.")
                continue
            elif my_result[8]=='Y' :
                print("The card has been deleted.")
                continue
            elif my_result[4] > get_card_position : # push the card
                sql_query = "UPDATE Card SET Position = Position+1 WHERE List_ID = %d AND Position>=%d AND Position<%d AND Is_deleted = 'N'" % (in_list, get_card_position, my_result[4])
                curr_cursor.execute(sql_query)
                sql_query = "UPDATE Card SET Position=%s WHERE Card_ID=%s" % (get_card_position, get_card_id)
                curr_cursor.execute(sql_query)

            elif my_result[4] < get_card_position : # pull the card
                sql_query = "UPDATE Card SET Position=Position-1 WHERE List_ID = %d AND Position<=%d AND Position>%d AND Is_deleted = 'N'" % (in_list, get_card_position, my_result[4])
                curr_cursor.execute(sql_query)
                sql_query = "UPDATE Card SET Position=%s WHERE Card_ID=%s" % (get_card_position, get_card_id)
                curr_cursor.execute(sql_query)
            else :
                print("Nothing Changed.")
                
            my_db.commit()
            activity_str = "Changed card %s's position to %d" % (my_result[1], get_card_position)
            Activity_notice("CARD", int(get_card_id), curr_user, my_db, activity_str)
            input("Enter to continue ...")


        elif answer == "11" :
            get_card_id = input("Move a card ID : ")
            get_list_id = input("Move to list ID : ")

            sql_query = "SELECT * FROM Card WHERE Card_id = %s AND List_ID = %s ORDER BY Position DESC" % (get_card_id, in_list)
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()

            if not my_result :
                print("Invalid Card ID.")
            else :
                card_title = my_result[3]
                sql_query = "UPDATE Card SET List_ID = %s WHERE Card_ID = %s" % (get_list_id, get_card_id)
                curr_cursor.execute(sql_query)
                sql_query = "SELECT * FROM Card WHERE List_ID = %s ORDER BY Position DESC" % get_list_id
                curr_cursor.execute(sql_query)
                my_result = curr_cursor.fetchone()

                sql_query = "UPDATE Card SET Position = %d WHERE Card_ID = %s" % (my_result[4]+1, get_card_id)
                curr_cursor.execute(sql_query)
                sql_query = "UPDATE Card SET Position=Position-1 WHERE List_ID = %s AND Position>%d" % (in_list, my_result[4]) 
                curr_cursor.execute(sql_query)

                my_db.commit()

                sql_query = "SELECT List_Title FROM List WHERE List_ID=%d" % in_list
                curr_cursor.execute(sql_query)
                my_result = curr_cursor.fetchone()
                old_list_title = my_result[0]

                sql_query = "SELECT List_Title FROM List WHERE List_ID=%s" % get_list_id
                curr_cursor.execute(sql_query)
                my_result = curr_cursor.fetchone()
                new_list_title = my_result[0]

                activity_str = "Moved card %s from %s to %s" % (card_title, old_list_title, new_list_title)
                Activity_notice("CARD", int(get_card_id), curr_user, my_db, activity_str)

            input("Enter to continue ...")

        elif answer == "12" :
            get_card_id = input("Give a card id : ")

            sql_query = "SELECT * FROM Card WHERE Card_ID = %s AND List_ID = %s" % (get_card_id, in_list)
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchone()

            if not my_result :
                print("The card can not be found.")
            else :
                token = my_result[3][-1]
                if token.isdigit() :
                    new_card_title = my_result[3][:-1] + str(int(token)+1)
                else :
                    new_card_title = my_result[3] + " 2"
                sql_query = "SELECT * FROM Card WHERE List_ID = %s ORDER BY Position DESC" % in_list
                curr_cursor.execute(sql_query)
                result = curr_cursor.fetchone()
                curr_position = result[4]+1

                sql_query = "INSERT INTO Card(List_ID, Label_ID, Card_Title, Position, Description, Due_Date, Members) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                input_query = [(in_list, my_result[2], new_card_title, curr_position, my_result[5], my_result[6], my_result[7]),]
                curr_cursor.executemany(sql_query, input_query)
                my_db.commit()

                sql_query = "SELECT List_Title FROM List WHERE List_ID=%d" % in_list
                curr_cursor.execute(sql_query)
                result = curr_cursor.fetchone()
                list_title = result[0]

                activity_str = "Copied card %s on %s" % (my_result[3], list_title)
                Activity_notice("LIST", int(get_card_id), curr_user, my_db, activity_str)

                input("Sucessfully saved.")

        elif answer == "0" :
            break

        else :
            print("Invalid answer.")
