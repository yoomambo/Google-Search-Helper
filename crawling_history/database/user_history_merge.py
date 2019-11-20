"""
<파일 위치> : database 위 폴더

<목적> : user들의 history를 받아서 겹치는 url에 user_count를 1을 추가한다.

"""

import sqlite3
import pandas as pd
import os
import getpass
import shutil
import token_word_judge
# user들의 directory list
user_dir_list = os.listdir()
user_only_dir_list = token_word_judge.search(user_dir_list)
# print(user_only_dir_list)
# user dir마다 반복
for user_dir in user_only_dir_list:
    # print(user_dir)
    # history_user_dir_address
    history_user_dir_address = user_dir+ "/History_" + user_dir + '.db'

    # 1은 모든 user의 History 읽는 conn / 2는 각각의 user의 history 읽는 conn
    conn1 = sqlite3.connect("./History_all_users.db")
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
        c2.execute('SELECT url, title, visit_count FROM urls')

        # url 추출 후, list 에 저장
        history_all_users_history_url_list = c1.fetchall()
        history_div_user_history_all_list = c2.fetchall()

        # 이 과정은 (url, )이렇게 빈칸으로 되어있어 제거하기 위함.
        history_all_users_history_url_list_change = []
        for i in history_all_users_history_url_list:
            history_all_users_history_url_list_change.append(i[0])

        # user url list 를 하나씩
        for urls in history_div_user_history_all_list:
            # 개인의 url이 모든 user에 있다면
            # print(history_all_users_history_url_list[:])
            if urls[0] in history_all_users_history_url_list_change:
                c1.execute("update urls SET user_count = user_count + 1 where url = '" + urls[0] + "'")
            else:
                c1.execute("INSERT INTO urls(url, title, visit_count) VALUES (?,?,?)", tuple(urls))


        conn1.commit()
        conn1.close()
        conn2.close()
