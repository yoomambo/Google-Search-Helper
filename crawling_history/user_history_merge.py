"""
<파일 위치> : database 위 폴더


"""

import sqlite3
import pandas as pd
import os
import getpass
import shutil

# user들의 directory list
# user_dir_list = os.listdir()
user_dir_list = ['yoohj']

# user dir마다 반복
for user_dir in user_dir_list:
    
    # history_user_dir_address
    history_user_dir_address = "./database/" +user_dir+ "/History_" + user_dir

    # 1은 모든 user의 History 읽는 conn / 2는 각각의 user의 history 읽는 conn
    conn1 = sqlite3.connect("./database/History_all_users")
    conn2 = sqlite3.connect(history_user_dir_address)
    
    # cursor 생성
    c1 = conn1.cursor()
    c2 = conn2.cursor()

    # table이 없다면 새로 생성
    c1.execute("CREATE TABLE IF NOT EXISTS urls(url text, title text, visit_count INTEGER, user_count INTEGER DEFAULT 1)") 
    c1.execute('select url, title, visit_count from urls')
    # 경량화를 위해 url, title, visit_count만 추출
    c2.execute('select url, title, visit_count from urls')

    # History_all_users_history의 data ->list로 fetch
    history_all_users_history_data_list = c1.fetchall()

    # 개인의 user들의 data
    history_div_user_history_data_list = c2.fetchall()
    
    # 처음 만들어지는 table 이라면?
    if len(history_all_users_history_data_list) == 0:
        print(1)
        # 개인의 user들의 data 입력
        c1.executemany("INSERT INTO urls(url, title, visit_count) VALUES (?,?,?)", tuple(history_div_user_history_data_list))
        conn1.commit()
        conn1.close()
        conn2.close()
        continue
    
    # 그 다음부턴, append 될 때
    else:
        # 모두 url만 추출 후 비교
        c1.execute('SELECT url FROM urls')
        c2.execute('SELECT url FROM urls')

        # url 추출 후, list 에 저장
        history_all_users_history_url_list = c1.fetchall()
        history_div_user_history_url_list = c2.fetchall()

        # user url list 를 하나씩
        for urls in history_div_user_history_url_list:
            # 개인의 url이 모든 user에 있다면
            if urls in history_all_users_history_url_list:
                c1.execute("update urls SET user_count = user_count + 1 where url = '" + urls[0] + "'")


        conn1.commit()
        conn1.close()
        conn2.close()
