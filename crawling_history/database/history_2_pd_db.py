"""

<파일위치> : database 위에 폴더에 위치
사용자가 사이트를 들어오고 검색창을 눌렀을 때, (이 때 동의 버튼을 누르게하면서 기다린다.)

1. 처음 사용자가 사이트를 들어왔을 때는 : 새로 테이블을 만든다.
2. append를 미리 했다면? : 중복 append 없이 그대로 종료
3. append할게 있으면 urls에 visit_count에 count에 더해주고, last_visit_time을 최신화

output : History_user

"""

import pandas as pd
import sqlite3
import os
import getpass
from tensorflow.keras.preprocessing.text import text_to_word_sequence
import glob
import token_word_judge
# print('현재 path : ', os.getcwd())

# user들의 directory list
user_dir_list = os.listdir()
user_only_dir_list = token_word_judge.search(user_dir_list)
# print(user_only_dir_list)
# DB 한 줄씩 읽어들이기
def database_title_token(data_list):
    """
    DB를 한줄씩 sqlite로 불러와서 튜플로 저장된 하나의 원소들을
    for문으로 하나씩 분해 후, title을 token으로 나눈 후,
    token들을 합친 리스트를 return값에 list로 반환
    """

    user_history_update_data_list_titletoken = []

    for i in data_list:    
        
        """
        output : 
        (13567, 'https://www.youtube.com/', 'YouTube', 36, 1420192312848192)
        """
        # output이 tuple이어서 
        Id, url, title, visit_count, last_visit_time = i
        # title의 text를 word로 끊어버리기
        title = text_to_word_sequence(title)
        # title이 빈공간인 건 제외
        if len(title) == 0:
            continue
    
        user_history_update_data_list_titletoken.append((Id, url, title, visit_count, last_visit_time))
    return tuple(user_history_update_data_list_titletoken)

# user dir마다 반복
for user_dir in user_only_dir_list:
    # print('횟수')
    # 1은 History 읽는 conn
    conn1 = sqlite3.connect(user_dir+ "/History")
    conn2 = sqlite3.connect(user_dir+ "/History_" + user_dir +'.db')

    # cursor 생성
    c1 = conn1.cursor()
    c2 = conn2.cursor()

    # update History 데이터 조회
    c1.execute('SELECT id, url, title, visit_count, last_visit_time FROM urls')

    # user_history_update_data_list는 History 에서 가져온 data들
    user_history_update_data_list = c1.fetchall()

    # func.database_title_token 으로 title token화 한 후 이 tuple에 append
    user_history_update_data_list_titletoken = database_title_token(user_history_update_data_list)

    # title token화 한것 DF에 넣기
    user_history_update_df = pd.DataFrame(user_history_update_data_list_titletoken,index = None, columns = ['id', 'url', 'title', 'visit_count', 'last_visit_time'])
    
    # user_history_update_data_list token 진행한 DF output 출력
    # print(user_history_update_df.head())
    # History_user_dir.db 없는 경우 
    c2.execute("CREATE TABLE IF NOT EXISTS urls(id INTEGER, url text, title text, visit_count INTEGER, last_visit_time INTEGER)")
    
    c2.execute('SELECT id, url, title, visit_count, last_visit_time FROM urls')
    
    # final로 합칠 data_list
    user_history_final_data_list = c2.fetchall()

    # print('want : ',tuple(user_history_update_data_list))
    # print('len : ', len(user_history_final_data_list))

    # user_history_final_df 는 final의 list를 DataFrame 화 시킴
    user_history_final_df = pd.DataFrame(user_history_final_data_list, index = None, columns =['id', 'url', 'title', 'visit_count', 'last_visit_time'])

    # update 한 db의 visits를 뽑아옴
    c1.execute('SELECT id, url, visit_time FROM visits')
    # list화 시킴
    user_history_update_visits_list = c1.fetchall()

    # update_visits_DataFrame 에 저장
    user_history_update_visits_df = pd.DataFrame(user_history_update_visits_list, columns = ['id', 'url', 'visit_time'])

    # update 한 db의 urls 뽑아옴
    c1.execute('SELECT id, url, title, visit_count, last_visit_time FROM urls')
    # list화 시킴
    user_history_update_urls_list = c1.fetchall()

    # update_urls_DataFrame 저장
    user_history_update_urls_df = pd.DataFrame(user_history_update_urls_list, columns = ['id', 'url', 'title', 'visit_count', 'last_visit_time'])
    
    # update 정보에서 visits 카테고리 내 visit_time만을 list화
    user_history_update_visits_visit_time_list = list(user_history_update_visits_df.loc[:,'visit_time'])

    # 방금 update한 것이라 빈 table 일 경우, 다더한다.
    if len(user_history_final_data_list) == 0:
        
        # user_history_update_data_list token을 진행한 것이 user_history_update_data_list_titletoken 있다.
        c2.executemany("INSERT INTO urls(id, url, title, visit_count, last_visit_time) VALUES (?,?,?,?,?)", tuple(user_history_update_data_list))
        
        # 정보 입력
        conn2.commit()

    # 이미 똑같은 table이 append 될 경우 종료
    elif max(list(user_history_final_df.loc[:,'last_visit_time'])) == max(user_history_update_visits_visit_time_list):
        pass
    
    # 방금 update 한것이 빈테이블이 아니라면
    else:
        # print('final_max_last_visit_time : ',max(list(user_history_final_df.loc[:,'last_visit_time'])))
        # print('update_max_visit_time : ',max(user_history_update_visits_visit_time_list))
        # print(user_history_update_visits_visit_time_list)
        
        # final_database에서의 가장 최근 방문시간, update 정보에서 visits 카테고리 내 visit_time만을 list 
        # 중에서 같은 시간대를 골라 그 다음 시간부터 append한다.

        # append 할 table row 가 있을 경우
        if max(list(user_history_final_df['last_visit_time'])) in user_history_update_visits_visit_time_list:
            
            # print('final_max_last_visit_time',max(list(user_history_final_df['last_visit_time'])))
            same_visit_time_index = user_history_update_visits_visit_time_list.index(max(list(user_history_final_df['last_visit_time'])))
            # print('same_visit_time_index : ',same_visit_time_index)
            
            # 중복되는 시간들을 다 버리고, 새롭게 추가된 항목만 해서 url을 추출.
            user_history_update_visits_url_list = list(user_history_update_visits_df.loc[same_visit_time_index+1:, 'url'])
            # print('user_history_update_visits_url_list : ', user_history_update_visits_url_list)
            
            # final_database의 id_list
            user_history_final_id_list=list(user_history_final_df.loc[:, 'id'])
            # print('user_history_final_id_list : ',user_history_final_id_list)
            
            # url이 id와 같은지 하나하나 비교
            for url in user_history_update_visits_url_list:
                
                # 만약 url을 겹치는 곳을 들 어갔다면? 
                if url in user_history_final_id_list:
                    # print('final에서 visits의 url과 같은 id의 index : ',user_history_final_id_list.index(url))
                    
                    # 원래 visit_count에 1을 더해준다.
                    # print(user_history_final_df.loc[user_history_final_id_list.index(url),'visit_count'])
                    user_history_final_df.loc[user_history_final_id_list.index(url),'visit_count'] += 1
                    # print(user_history_final_df.loc[user_history_final_id_list.index(url)]['visit_count'])
                    
                    # 원래 last_vist_time을 visits_visit_time으로 바꿔준다.
                    # print('test : ',user_history_update_visits_df.loc[same_visit_time_index,'visit_time'])
                    for value in list(user_history_update_visits_df.loc[same_visit_time_index:,'visit_time']):
                        user_history_final_df.loc[user_history_final_id_list.index(url),'last_visit_time'] = value

                # 만약 url이 겹치지 않는다면.
                else:
                    # update에 urls 에서 id 값을 전체 불러와서 list화
                    user_history_update_urls_id_list = list(user_history_update_urls_df.loc[:,'id'])
                    # print(user_history_update_urls_id_list)
                    # print('i want : ',user_history_update_urls_df.loc[user_history_update_urls_id_list.index(url)])
                    
                    # url을 가지고 있는 list의 index값을 넣어서 그 row행렬을 append한다.
                    user_history_final_df.append(user_history_update_urls_df.loc[user_history_update_urls_id_list.index(url)])
            
            user_history_final_df.to_sql('urls',conn2, if_exists = 'replace', index = False)

    # client History db close
    conn1.close()

    # History_username.db close
    conn2.close()






