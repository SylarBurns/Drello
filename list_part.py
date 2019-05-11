from Specific_Card import *

def ListofLists(in_board) :
    while(1) :
        print("1. List up all list in board")
        print("2. Search specific list")
        print("3. Add new list")
        print("4. Delete list")
        print("5. Change list's position")
        print("6. Get notice of lists")
        print("7. Move specific list to another board")
        print("8. Copy specific list in this board")
        print("9. Back to board")
        answer = input()

        if answer == "1" :
            # 해당 board id를 가지는 모든 list 가져와서 list에 담고 position 순서대로 sorting 해서 출력하기
            # list에 담았을 때 position 순서대로 솔팅해서 주는 함수 하나 있으면 좋을듯
            print("printing done") # temp

        elif answer == "2" :
            get_list_id = input("Give a list's id")
            # find specific list's information from sql..
            # print out information
            # 지금은 바로 함수 타고 들어가는 건데 이렇게 할지 아니면 정보만 보여주고 다른거 더 만들지 결정
            SpecificList(get_list_id)
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
            # 일단 해당 보드의 리스트 전부 가져오고 포지션보다 큰 애들을 전부 1씩 증가시켜줘야하나..

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


def SpecificList(in_list) :
    while(1) :
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
        answer = input()

        if answer == "1" :
            # list_id 이용해서 information 보여주기
            # 5번 show card랑은 별개로 진짜 그냥 정보만 보여주는건지 확인

            print("printing done") # temp

        elif answer == "2" :
            get_list_id = input("Give a cards's id")
            # find specific list's information from sql..
            # 정보만 보여줄지 바로 함수로 타고 들어갈지 결정
            cursor = ""
            chosen_card = Specific_Card_Manager(get_list_id, cursor) # cursor
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
