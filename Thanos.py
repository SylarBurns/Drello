def Activity_notice(Type, ID, User_ID, db, Action) :
    my_cursor = db.cursor()
    if Type == 'BOARD' :
        sql_query = "INSERT INTO Activity(Board_ID, User_ID, Action) VALUES (%s, %s, %s)"
        input_query = [(ID, User_ID, Action),]
        my_cursor.executemany(sql_query, input_query)
        
    elif Type == 'LIST' :
        sql_query = "SELECT Board_ID FROM List WHERE List_ID=%d" % ID
        my_cursor.execute(sql_query)
        my_result = my_cursor.fetchone()
        
        sql_query = "INSERT INTO Activity(Board_ID, List_ID, User_ID, Action) VALUES (%s, %s, %s, %s)"
        board_id = my_result[0]
        input_query = [(board_id, ID, User_ID, Action),]
        my_cursor.executemany(sql_query, input_query)
        
    elif Type == 'CARD' :
        sql_query = "SELECT List_ID FROM Card WHERE Card_ID=%d" % ID
        my_cursor.execute(sql_query)
        my_result = my_cursor.fetchone()
        list_id = my_result[0]
        
        sql_query = "SELECT Board_ID FROM List WHERE List_ID=%d" % list_id
        my_cursor.execute(sql_query)
        my_result = my_cursor.fetchone()
        board_id = my_result[0]
        
        sql_query = "INSERT INTO Activity(Board_ID, List_ID, Card_ID, User_ID, Action) \
                    VALUES (%s, %s, %s, %s, %s)"
        input_query = [(board_id, list_id, ID, User_ID, Action),]
        my_cursor.executemany(sql_query, input_query)
    else :
        print("Error. Type Check.")
        return
    
    db.commit()
    
    my_cursor.execute("SELECT LAST_INSERT_ID()")
    my_result = my_cursor.fetchone()
    activity_id = my_result[0]
    
    if Type == "BOARD" :
        Give_notice("BOARD", ID, activity_id, my_cursor, db)
        
    elif Type  == "LIST" :
        Give_notice("LIST", ID, activity_id, my_cursor, db)
        Give_notice("BOARD", board_id, activity_id, my_cursor, db)
        
    elif Type == "CARD" :
        Give_notice("CARD", ID, activity_id, my_cursor, db)
        Give_notice("LIST", list_id, activity_id, my_cursor, db)
        Give_notice("BOARD", board_id, activity_id, my_cursor, db)

    db.commit()


def Give_notice(Type, ID, activity_id, my_cursor, db) :
    sql_query = "SELECT User_ID FROM Watch WHERE ID_type='%s' AND ID=%d" % (Type, ID)
    my_cursor.execute(sql_query)
    my_result = my_cursor.fetchall()
    input_query = [(activity_id, row[0]) for row in my_result]

    sql_query = "INSERT IGNORE INTO Notice(Activity_ID, User_ID) VALUES (%s, %s)"
    my_cursor.executemany(sql_query, input_query)
    db.commit()
