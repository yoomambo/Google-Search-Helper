"""
db_title을 다루는 함수들 모음

"""
# 한글 명사화
from konlpy.tag import Okt
# 엉어+한글 붙어있는 경우 + Tens - orflow로 나뉨
# sentence_to_word 보다 되게 세분화 되서 나뉨.
from soynlp.tokenizer import RegexTokenizer
from googletrans import Translator

# sentence tokenizing
# tokenizer 생성 (abc에 를 abc, 에 로 나눠줌)

def search(dirname):
    """
    <설명> : 현재 실행되는 파일의 dir에서 dir만 출력, -> .py, .db 파일제외

    input : os.listdir

    output : dir만 출력

    """
    result = []
    for filename in dirname:
        if filename[-3:] == '.py' or filename[-3:] =='.db' or filename[-3:] =='e__' or filename[-3:] =='.sh':
            pass
        else:
            result.append(filename)
    return result


def db_sentence_2_token_list(database_history_all_users_data_list):
    """
    설명 : 긴 sentence를 RegexTokenizer로 token으로 나눠서 title에 있던 자리에 다시 담는다.

    input : Sentence들을 모아둔 list
    ex)
    input : [['computer', '의', 'Youtube', '채널', '확인하기'], ----]
    return : result (type = list)
    result : 
    [['computer', 'https://www.youtube.com/', 36, 3], 
    ['의', 'https://www.youtube.com/', 36, 3], 
    ['youtube', 'https://www.youtube.com/', 36, 3], 
    ['채널', 'https://www.youtube.com/', 36, 3], 
    ['확인', 'https://www.youtube.com/', 36,3]
    ------
    ]

    """
    # token
    tokenizer = RegexTokenizer()

    result = []
    # DB 한 줄씩 읽어들이기
    for line in database_history_all_users_data_list:    
        
        """
        output : 
        ('https://www.youtube.com/', 'YouTube', 36)
        """
        # output이 tuple이어서 
        url, title, visit_count , user_count = line
        # title의 text를 word로 끊어버리기
        title_list = tokenizer.tokenize(title)
        # title이 빈공간인 건 제외
        if len(title_list) == 0:
            continue
       
        else:
            for word in title_list:
                judgement = kor_or_eng_judge(word)
                # judgement 가 영어 한글이 아닐 경우
                if judgement == 0:
                    pass
                # judgement가 영어 경우 : 영어인 경우 lower한 단어 입력
                elif judgement == 'en':    
                    result.append([token_judge_en_lower_ko_noun(word), url, visit_count, user_count])
                # judgement가 영어 경우 : 한글인 경우 lower한 단어 입력
                elif judgement == 'ko':
                    if len(token_judge_en_lower_ko_noun(word)) == 1:
                        result.append([token_judge_en_lower_ko_noun(word)[0], url, visit_count, user_count])
                    elif len(token_judge_en_lower_ko_noun(word)) == 0:
                        pass
                    else:
                        for token_noun in token_judge_en_lower_ko_noun(word):
                            result.append([token_noun, url, visit_count, user_count])

    
    return result

def token_judge_en_lower_ko_noun(token):
    """
    설명 : RegexTokenizer로 나눈 token을 받으면 영어, 한글을 파악해서 영어면, lower로 , 한글이면 noun으로 return

    input : 단어, token
    output : 
    영어면 lower해서 단어 return
    한글이면 noun으로 나눠서 return
    """
    # 한글 명사화 객체
    okt=Okt()
    
    judgement = kor_or_eng_judge(token)
    # judgement가 영어, 한글일 경우 : 영어인 경우 lower한 단어 입력
    if judgement == 'en':
        return token.lower()
    elif judgement == 'ko':
        return okt.nouns(token)
    # judgement 가 영어 한글이 아닐 경우
    elif judgement == 0:
        return None
    



def kor_or_eng_judge(token_word):
    """
    설명 : token_word를 param으로 받는다.

    input : token된 word

    output : 
    1. token_word 대문자, 소문자 영어면, en를 return
    2. token_word 한글이면 , ko를 return
    3. token_word 다른 글자면, 0 return
    """
    kor_start_asci = ord('가')
    kor_finish_asci = ord('힣')
    # word가 영어라면, capitalize로 대문자로 만들예정
    eng_start_asci_upper = ord('A')
    eng_finish_asci_upper = ord('Z')
    eng_start_asci_lower = ord('a')
    eng_finish_asci_lower = ord('z')
    
    token_word_list = list(token_word)
    
    # 영어 대문자라면
    if eng_start_asci_upper <= ord(token_word_list[0]) <= eng_finish_asci_upper:
        return 'en'
    # 영어 소문자라면
    elif eng_start_asci_lower <= ord(token_word_list[0]) <= eng_finish_asci_lower:
        return 'en'
    # 한글이라면
    elif kor_start_asci <= ord(token_word_list[0]) <= kor_finish_asci:
        return 'ko'
    # 영어, 한글 둘다 아니면,
    else:
        return 0

# Translator function
def google_translator(input_word_list):
    word_list_result = []
    t = Translator()
    for input_word in input_word_list:
        if kor_or_eng_judge(input_word) == 'en':
            word_list_result.append(t.translate(input_word, dest = 'ko', src = 'en').text)
        elif kor_or_eng_judge(input_word) == 'ko':
            word_list_result.append(t.translate(input_word).text)
        else:
            pass
    word_list_result.extend(input_word_list)

    return word_list_result

def word_bisect(a, x, lo=0, hi=None):
    """
    <설명> : word에 관한 이진 검색

    input : a -> 찾고자 하는 단어의 검색 list
            x -> 찾고자 하는 단어

    output : 
    1. 단어가 없으면 None return
    2. 단어가 가지는 index return
    """

    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi is None:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid] < x: lo = mid+1
        else: hi = mid
    if a[lo] != x:
        return None
    else:
        return lo