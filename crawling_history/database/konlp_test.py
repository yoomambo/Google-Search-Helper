# import google_history
# from konlpy.tag import Okt
# from tensorflow.keras.preprocessing.text import text_to_word_sequence
# from sklearn.feature_extraction.text import CountVectorizer
# from nltk.tokenize import word_tokenize
# from soynlp.tokenizer import RegexTokenizer
# import sqlite3
# import token_word_judge
# import bisect
# from threading import Thread

# result = list()
# th1 = Thread(target=token_word_judge.word_bisect, args=([1,2,3,4,5,6,7,10], 9))

# th1.start()
# th1.join()s

# print(f"Result: {sum(result)}")

# print(token_word_judge.word_bisect([1,2,3,4,5,6,7,10], 9))
user_name = 'jihoon'
print(('./database/{}/History_{}').format(user_name, user_name))
charu = 'strong'
print(charu[-3:])
import os
def search(dirname):
    result = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        print(full_filename[-3:])
        if full_filename[-3:] == '.py' or full_filename[-3:] =='.db':
            pass
        else:
            result.append(full_filename)
    return result
# user들의 directory list
user_dir_list = search(os.getcwd())
print(user_dir_list)
# # data는 오름차순으로 정렬된 리스트
# def binary_search_recursion(target, start, end, data):
#     if start > end:
#         return None

#     mid = (start + end) // 2

#     if data[mid] == target:
#         return mid
#     elif data[mid] > target:
#         end = mid - 1
#     else:
#         start = mid + 1        

#     return binary_search_recursion(target, start, end, data)

# # 테스트용 코드
# if __name__ == '__main__':
#     li = [i*3 for i in range(11)]
#     target = 6
#     idx = binary_search_recursion(target, 0, 10, li)

#     print(li)
#     print(idx)

# # 가독성 좋게 중간결과물 txt 파일 저장
# with open('../read_intermediate_result.txt', 'w', encoding='UTF-8') as f:
#     for i in google_history.word_list:
#         word = text_to_word_sequence(i)
#         if len(word) != 0:
#             for j in word:
#                 j = j +' '
#                 f.writelines(j)
#             f.write('\n')
#         else:
#             pass

# # input 중간결과물 txt 파일 저장
# with open('../input_intermediate_result.txt', 'w', encoding='UTF-8') as f:
#     for i in google_history.word_list:
#         word = text_to_word_sequence(i)
#         # 파싱중에 0인것도 존재
#         if len(word) != 0:
#             # MapReduce split ' ' 을 위해!
#             for j in word:
#                 j = j +' '
#                 f.writelines(j)
#         else:
#             pass

# okt=Okt()  
# print(okt.nouns("한국과학기술연구원"))

# tokenizer = RegexTokenizer()
# print(tokenizer.tokenize("computer의 Youtube채널 확인하기"))

# # # print(str(['혁준']))
# # database_history_all_users_data_list = [['https://www.youtube.com/', 'computer의 Youtube채널 확인하기', 36, 3]]
# result = token_word_judge.db_sentence_2_token_list(database_history_all_users_data_list)
# print('result : ', result)
# # print(ord('가'))
# # print(ord('p'))

# # from googletrans import Translator

# # t = Translator()

# # print(t.translate('google', dest = 'ko', src = 'en').text)

# # from nltk.corpus import stopwords 
# # from nltk.tokenize import word_tokenize 

# # example = "Family is not an important thing. It's everything."
# # stop_words = set(stopwords.words('english')) 

# # word_tokens = word_tokenize(example)

# # result = []
# # for w in word_tokens: 
# #     if w not in stop_words: 
# #         result.append(w) 

# # print(word_tokens) 
# # print(result) 

# print(('혁준').lower())