# Section06-4
# Selenium
# Selenium 사용 실습(4) - 실습 프로젝트(3)
import sys
import time
# 이미지 다운
import urllib.request as req

# 엑셀 처리 임포트
import xlsxwriter
# bs4 임포트
from bs4 import BeautifulSoup
# selenium 임포트
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from krwordrank.word import KRWordRank 

chrome_options = Options()
chrome_options.add_argument("--headless")

# webdriver 설정(Chrome, Firefox 등) - Headless 모드 (일반보드는 처음 잘 실행되는지에 쓰임.)
# browser = webdriver.Chrome('./크롤링기초_코드/webdriver/chrome/chromedriver.exe', options=chrome_options)
browser = webdriver.Chrome('../webdriver/chrome/chromedriver.exe')

# 엑셀 처리 선언
workbook = xlsxwriter.Workbook("C:/wordcount/google_history_intermediate.xlsx")

# 워크 시트(엑셀의 시트를 만드는 메소드.)
worksheet = workbook.add_worksheet()

# 크롬 브라우저 내부 대기
browser.implicitly_wait(5)

# 브라우저 사이즈
browser.set_window_size(1920, 1028)  # maximize_window(), minimize_window()

# 페이지 이동
browser.get('https://myactivity.google.com/myactivity?restrict=waa&utm_source=udc&utm_medium=r&min=1572188400000000&max=1572879599999999&product=19%2C6')

# 1차 페이지 내용
# print('Before Page Contents : {}'.format(browser.page_source))

# ID 입력란
user_id = sys.argv[1]
user_password = sys.argv[2]

# 로그인 클릭
# Explicitly wait
WebDriverWait(browser, 5) \
    .until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div/div[3]/div/a'))).click()

# ID 입력
elem = browser.find_element_by_id("identifierId")
elem.send_keys(user_id)
elem.send_keys(Keys.RETURN)

# password 입력
elem = browser.find_element_by_name("password")
elem.send_keys(user_password)
elem.send_keys(Keys.RETURN)

# 2초 대기
time.sleep(2)


# 번들보기 -> 항목보기로 마우스 클릭
WebDriverWait(browser, 5) \
    .until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="gb"]/div[4]/div[2]/div/c-wiz/div/div/nav/a[2]'))).click()


# 밑으로 스크롤 내리기
while True:
    time.sleep(1)
    final_word = browser.find_elements_by_class_name('hV1B3e')
    # final_word[-1]이 끝까지 스크롤 할때의 element 부분
    if final_word[-1].text == '더 이상 표시할 콘텐츠가 없습니다.':
        print(final_word[0].text)
        break
    browser.find_element_by_tag_name('body').send_keys(Keys.END)

# html parsing 들어가기
soup = BeautifulSoup(browser.page_source, "html.parser")

# 추출할 word를 모아두는 장소
word_list = []

# word 추출
for line in soup.select('div >div >div >div >div.QTGV3c > a'):
    word_list.append(line.string)

# word_list 출력
print(word_list)

print('Crawling Succeed.')


# excel 행
ins_cnt = 1

# excel에 입력하기
for i in word_list:
    worksheet.write('A%s' % ins_cnt, i)
    ins_cnt += 1

# BeautifulSoup 인스턴스 삭제
del soup

# 4초간 대기
time.sleep(4)

# 브라우저 종료
browser.quit()

# 엑셀 파일 닫기 (close를 해야 엑셀에 저장이 된다.)
workbook.close()


min_count = 5   # 단어의 최소 출현 빈도수 (그래프 생성 시)
max_length = 15 # 단어의 최대 길이
verbose = True
wordrank_extractor = KRWordRank(min_count, max_length, verbose = True)
beta = 0.85    # PageRank의 decaying factor beta
max_iter = 10

keywords, rank, graph = wordrank_extractor.extract(word_list, beta, max_iter)

for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
    print()
    print('%8s:\t%.4f' % (word, r))