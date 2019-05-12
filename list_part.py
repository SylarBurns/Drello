import mysql.connector
from Specific_Card import *
import os

def ListofLists(in_board, curr_user, my_db) :
    while(1) :
        curr_cursor = my_db.cursor()
        os.system('cls' if os.name == 'nt' else 'clear')
        print("========================================")
        print("1. List up all list in board")
        print("2. Search specific list")
        print("3. Add new list")
        print("4. Delete list")
        print("5. Change list's position")
        print("6. Get notice of lists")
        print("7. Move specific list to another board")
        print("8. Copy specific list in this board")
        print("9. Back to board")
        print("========================================")
        answer = input()

        if answer == "1" :
            sql_query = "SELECT * FROM List WHERE Board_id = %d ORDER BY Position" % in_board
            curr_cursor.execute(sql_query)
            my_result = curr_cursor.fetchall()
                
            for row in my_result :
                print("%2d | List ID : %5d, List Title : %s"%(row[3], row[0], row[1]))

        elif answer == "2" :
            get_list_id = input("Give a list's id")
            # find specific list's information from sql..
            # print out information
            # 없으면 어떻게 할지
            #sql_query = "SELECT * FROM List WHERE Board_id = %d ORDER BY Position" % in_board
            #curr_cursor.execute(sql_query)
            #my_result = curr_cursor.fetchall()

            SpecificList(get_list_id, curr_user, my_db)
            print("printing done") # temp

        elif answer == "3" :
            get_list_name = input("Give a new list's name")
            # add new list to sql
            # position 어떡하지...

            print("printing done") # temp

        elif answer == "4" :
            get_list_id = input("Give a list's id you want to delete")
            # delete query..
            print("printing done") # temp

        elif answer == "5" :
            get_list_id = input("Give a list's id you want change position")
            get_list_position = input("Give a list's position")
            # 변경하기.. 근데 어떻게 변경하지
            # 쿼리에서 가져올때 특정 포지션보다 큰 애들만 가져오자

            print("printing done") # temp

        elif answer == "6" :
            #해당 보드에서 리스트 아이디 전부 뽑아오기
            # 유저랑 리스트 아이디랑 매칭해서 맞는거만 다 가져와서 프린트

            print("printing done") # temp

        elif answer == "7" :
            get_board_id = input("Give a board id")
            # list에서 보드 아이디 바꿔끼우기
            # 추가적으로 할꺼 없는지 확인하자 consistency..!

            print("printing done") # temp

        elif answer == "8" :
            get_list_id = input("Give a list id")
            # 해당 리스트 정보 가져와서 cp해서 또 넣기
            print("printing done") # temp

        elif answer == "9" :
            print("return to board....") # temp
            break

        else :
            print("Invalid answer.")


def SpecificList(in_list, curr_user, my_db) :
    while(1) :
        curr_cursor =  my_db.cursor() 
        os.system('cls' if os.name == 'nt' else 'clear')
        print("========================================")
        print("1. Show list's information.")
        print("2. Search cards")
        print("3. Watch the list / Disable the watch")
        print("4. Notifications")
        print("5. Show cards.")
        print("6. Sorting the card.")
        print("7. Add Card")
        print("8. Delete the card")
        print("9. Move specific card to another list")
        print("10. Copy specific card in this list")
        print("11. Back to list")
        print("========================================")
        answer = input()

        if answer == "1" :
            # list_id 이용해서 information 보여주기
            # 5번 show card랑은 별개로 진짜 그냥 정보만 보여주는건지 확인

            print("printing done") # temp

        elif answer == "2" :
            get_list_id = input("Give a cards's id")
            # find specific list's information from sql..
            # 정보만 보여줄지 바로 함수로 타고 들어갈지 결정
            chosen_card = Specific_Card_Manager(get_list_id, curr_user, my_db) # cursor
            print("printing done") # temp

        elif answer == "3" :
            # 정보 가져와서 만약에 watch하고 있으면 disable 시키고 안하고 있으면 watch 시키기
            print("printing done") # temp

        elif answer == "4" :
            # list id 이용해서 nofi 가져와서 보여주기 
            print("printing done") # temp

        elif answer == "5" :
            # card 내용 가져와서 보여주기

            print("printing done") # temp

        elif answer == "6" :
            # order by

            print("printing done") # temp

        elif answer == "7" :
            get_board_id = input("Give a card name")
            # 기타 필요한 정보 다 받아서 insert하기
            print("printing done") # temp

        elif answer == "8" :
            get_card_id = input("Give card's id")
            # 지우기
            print("printing done") # temp

        elif answer == "9" :
            get_card_id = input("Give a card id")
            # card에서 list 아이디 바꿔끼우기
            # 추가적으로 할꺼 없는지 확인하자 consistency..!
            print("printing done") # temp

        elif answer == "10" :
            get_card_id = input("Give a card id")
            # 해당 card 정보 가져와서 cp해서 또 넣기
            print("printing done") # temp

        elif answer == "11" :
            print("return to list of lists....") # temp
            break

        else :
            print("Invalid answer.")
