"""
<파일위치> : ./database

1. 사용자가 input값을 입력. -> RegexTokenizer로 token화
2. 영어면, lower로 통일해서 받기
3. 한글이면 okt로 명사화 시켜서 input 받기
4. token으로 나눠놓은 것들을 google translator로 넣기.
5. token_list로 저장

6. History_all_users_title_token.db 에서 title_token, url, user_count, visit_count를 각각의 list로 받기
7. 입력한 user의 folder에서 History 파일 불러와서 url_list 세팅
8. user_url_list가 
"""
from konlpy.tag import Okt
from soynlp.tokenizer import RegexTokenizer
import sqlite3
import token_word_judge
import os
import sys
import json
user_name = sys.argv[1]

# user가 word input
user_input_word = input('여기에 단어를 입력하세요 : ')

# RegexTokenizer's object 생성
tokenizer = RegexTokenizer()

# input한 word token화
new_token_list = tokenizer.tokenize(user_input_word)
"""
이 부분은 상의해보고 결정

# token_list를 영어버젼도!
# trans_token_list = token_word_judge.google_translator(token_list)

# trans전, 후 단어들 list화
# new_token_list = token_list + trans_token_list
"""
# 0.1초 이거만하면
# print(new_token_list)

final_token_list = []

# 명사만 추출하는 code
for new_token in new_token_list:
    # str인 것은 모두 영어이거나, 한글 단독 명사다.
    if type(token_word_judge.token_judge_en_lower_ko_noun(new_token)) == str:
        final_token_list.append(token_word_judge.token_judge_en_lower_ko_noun(new_token))
    # list 인 것은 명사가 여러개인 것이 list로 묶인다.
    elif type(token_word_judge.token_judge_en_lower_ko_noun(new_token)) == list:
        for i in token_word_judge.token_judge_en_lower_ko_noun(new_token):
            final_token_list.append(i)
    # 글자가 아닌것은 None 처리
    elif token_word_judge.token_judge_en_lower_ko_noun(new_token) == None:
        pass

# 한글도 명사만 존재하는 list
print(final_token_list)

conn1 = sqlite3.connect('./History_all_users_title_token.db')

c1 = conn1.cursor()

# 비교할 username의 최근 History를 모든 user들의 history와 비교하기 위해 임시로 attach
c1.execute("ATTACH '" + os.getcwd()+ "/" + user_name+"/History' as History_"+user_name+"_temp;")
c1.execute("ATTACH '" + os.getcwd()+ "/History_all_users.db' as History_all_users_temp;")

# username의 history가 있다면 이를 제거한 모든 user들의 history data들의 결과
result = []
# token마다 진행
for token in final_token_list:    
    c1.execute("CREATE TABLE IF NOT EXISTS extract_urls(title text, url text, user_count INTEGER, visit_count INTEGER)")
    c1.execute("SELECT title, url, user_count, visit_count from History_all_users_temp.urls WHERE url in (SELECT url from sorted_urls where title_token = '"+token+"' EXCEPT SELECT url from History_"+user_name+"_temp.urls) ORDER by user_count DESC")
    result.extend(c1.fetchall())

# 결과를 extract_urls table에 저장
c1.executemany("INSERT INTO extract_urls(title, url, user_count ,visit_count) VALUES (?,?,?,?)", result)
# 우선 token이 두 개 이상 겹치는 단어를 보여준다.
c1.execute("select title, url , user_count, visit_count FROM extract_urls GROUP BY url having count(url) > 2")
# c1.execute("select * from extract_urls order by url")
# token이 2개 이상 겹친 것을 보여준다.
result_token_2 = c1.fetchall()

# list를 json으로 출력해주는 함수
def print_json(result):
    columns = ['title', 'url', 'user_count', 'visit_count']
    change_dict= []
    for result_line in result:
        change_dict = dict(zip(columns, result_line))

# 2개이상이 있는 경우 json으로 출력
if len(result_token_2)!= 0:
    print_json(result_token_2)
# 2개이상 없는 경우 1개이상으로 선택
elif len(result_token_2) == 0:
    c1.execute("select title, url , user_count, visit_count FROM extract_urls GROUP BY url having count(url) > 1")

result_token_1 = c1.fetchall()

# 1개이상 있는 경우 json으로 출력
if len(result_token_1) != 0:
    c1.execute("select title, url , user_count, visit_count FROM extract_urls GROUP BY url having count(url) > 1")
    print_json(result_token_1)
# 1개이상 없는 경우 구글을 보여줌
else:
    data = [{'title':"I'm very sorry.....", "url":"www.google.com", "요청하신 단어에 관한 유사 검색 결과가 존재하지 않습니다."}]
    print(json.dump(data))

"""

"""