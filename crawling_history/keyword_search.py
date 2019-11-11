# keyword 입력받게 함
# keyword 추출
# clients_chrome_history.db

import sqlite3
from googletrans import Translator
from tensorflow.keras.preprocessing.text import text_to_word_sequence

# user가 input한 word일 때
user_input_word = input()

user_token_word_list = text_to_word_sequence(user_input_word)

# # Translator function
# def kor_2_en(input_word_list):
#     word_list_result = []
#     translator = Translator()
#     for input_word in input_word_list:
#         print(translator.detect(input_word))
#         if translator.detect(input_word) == 'ko':
#             word_list_result.append(change_word)
#         elif change_word.src == 'en':
#             word_list_result.append(input_word)
#         else:
#             pass
    
#     return word_list_result



conn = sqlite3.connect('./database/clients_chrome_history.db')

c = conn.cursor()

# 테이블생성(Data Type : TEXT, NUMERIC(소수자리까지) INTEGER(정수) REAL(실수) BLOB(파일저장))
c.execute("SELECT url, title, visit_count FROM users")

# client_chrome_history_list 에 내용 담기
client_chrome_history_list = c.fetchall()

# token 한 결과 list
result = []

# DB 한 줄씩 읽어들이기
for i in client_chrome_history_list:    
    
    """
    output : 
    ('https://www.youtube.com/', 'YouTube', 36)
    """
    # output이 tuple이어서 
    url, title, visit_count = i
    # title의 text를 word로 끊어버리기
    title = text_to_word_sequence(title)
    # title이 빈공간인 건 제외
    if len(title) == 0:
        continue
    # change_title = kor_2_en(title)
    result.append([url, title, visit_count])

