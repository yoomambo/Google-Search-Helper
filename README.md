# SW-Festival (Google History 분석)
<br>
<br>

## Theme

이 프로젝트는 client의 Google의 검색엔진, chrome history 를 분석, 다른 client의 history를 비교해서<br>
client가 <strong>입력한 keyword에 대하여 검색하지 못한 url을 보여주는 웹 페이지</strong>입니다.<br>
<br>
우리는 현재 지금 집단지성을 추구하는 사회를 살아가고 있기 때문에<br>
같은 keyword에 대하여 <strong>내가 보지 못했던 정보를 아는 것</strong>은 굉장히 중요한 부분입니다.<br>
따라서 이러한 부분에서 우리가 만든 웹 페이지는 실제로 많은 benefit을 제공할 것이라 생각합니다.<br>
<br>
<br>

## Why Google Chrome?

구글은 검색엔진으로써 <strong>78.78%</strong> 의 시장점유율을 보이고 있습니다. <br>
이는 7% 로 두번째 점유율을 가지고 있는 bing 과 비교하여 보면 10 배라는 놀라운 차이를 보입니다 . <br>
이로써 우리는 이용자가 많은 Google 의 검색엔진을 기본으로 사용하고있는 웹 브라우저 , Chrome 의 history를<br>
분석에 사용한다면 보편적인 데이터를 얻기에 충분하다고 생각하였습니다. <br>
<br>
<br>

## settings

~~~
pip install konlpy
pip install sonlpy
pip install pandas
pip install tensorflow
pip install JPype1 == 0.6.3
~~~

위와 같은 code를 terminal, cmd 창에서 실행합니다. JPype1이 0.7.0을 0.6.3로 downgrade 해야 오류가 발생하지 않습니다.<br>

~~~
pip install -r requirements.txt
pip install JPype1 == 0.6.3
~~~

위의 과정이 어려운 경우, requirements.txt를 실행한 후, 똑같이 JPype1을 0.6.3으로 downgrade 시켜줍니다.<br>
<br>
npm과 nodejs는 항상 최신 버젼을 유지합니다.<br>
nodejs == 6.0.0
npm == 3.8.6

<br>
<br>

## How to use

~~~
cd festival/w500
npm start
~~~

1. 홈페이지에 Info 를 눌러 주의사항을 확인
2. 홈페이지에 start 부분을 클릭
3. 구글 로그인 창으로 연결되면, 보여진 아이디 창을 클릭한 후, 연결
4. OS에 따라 주어진 경로에서 chrome의 History 데이터베이스 파일을 send
5. 검색어 창에 내가 입력하고 싶은 keyword 입력
6. 출력된 결과 확인

<br>
<br>

## benefit
이러한 웹페이지를 제공함으로써, 여러 방면으로 쓰일 수 있습니다.

- 같은 목적을 지닌 집단에서 사용 : 비슷한 keyword 입력으로 서로의 정보를 공유할 수 있습니다. <br>
- 같은 chorme 검색엔진을 사용함으로써, 비슷한 keword로 다른 사람의 정보가 궁금할 때 정보를 찾을 수 있습니다.<br>
