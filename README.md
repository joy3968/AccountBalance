# AccountBalance
장고를 통한 주식계좌 잔고조회

***
+ 네이버 주식 시세 정보(현재가)를 크롤링 하여 현재 나의 잔고를 나타내는 웹페이지

![stock_balance](https://user-images.githubusercontent.com/69666784/94119733-47193e00-fe8a-11ea-94f2-4fbcb171beeb.PNG)
***
### django 환경설정
1. 장고 웹 프레임 워크 설치
> pip install django

2. 서버 구동
> python manage.py runserver

3. (구동 취소 > ctrl + c)

4. http://127.0.0.1:8000/balance/ 로 접속

5. url : http://127.0.0.1:8000/balance/?{종목코드}={보유주식수량}&{종목코드}={보유주식수량} ...
ex) http://127.0.0.1:8000/balance/?035420=50000&005930=100&068270=50&035720=14040&305080=2200&045340=11
***
