"""
<파일 위치> : ./database

<파일 목적> :

History_all_users db 파일에서 History_all_users_title_token.db 을 생성

History_all_users_title_token.db는 title을 token_word_judge에서 함수를 적용
title을 한글, 영어, 한글+영어 붙어있는 부분을 RegexTokenizer로 token
영어인 부분은 lower로 소문자화
한글인 부분은 OKT로 명사화

"""


import sqlite3
from soynlp.tokenizer import RegexTokenizer
import token_word_judge

# title token으로 나누기 전 db
conn = sqlite3.connect('../crawling_history/database/History_all_users.db')
# title token으로 나눈 후 db
conn2 = sqlite3.connect('../crawling_history/database/History_all_users_title_token.db')

# cursor 생성
c = conn.cursor()
c2 = conn2.cursor()

# 테이블생성
c.execute("SELECT url, title, visit_count, user_count FROM urls")

# client_chrome_history_list 에 내용 담기
database_history_all_users_data_list = c.fetchall()

# token 한 결과 list
result = token_word_judge.db_sentence_2_token_list(database_history_all_users_data_list)

c2.execute("CREATE TABLE IF NOT EXISTS urls(title_token text, url text, visit_count INTEGER, user_count INTEGER)")
c2.executemany("INSERT INTO urls(title_token, url, visit_count, user_count) VALUES (?,?,?,?)", tuple(result))
conn2.commit()

# database 파일에 sorted한 거 추가하기
c2.execute("CREATE TABLE IF NOT EXISTS sorted_urls(title_token text, url text, visit_count INTEGER, user_count INTEGER)")
c2.execute('SELECT * From urls order by title_token')
database_history_all_users_sorted_data_list = c2.fetchall()
# print(database_history_all_users_data_list[-30:-1])
c2.executemany("INSERT INTO sorted_urls(title_token, url, visit_count, user_count) VALUES (?,?,?,?)", tuple(database_history_all_users_sorted_data_list))
conn2.commit()
conn.close()
conn2.close()