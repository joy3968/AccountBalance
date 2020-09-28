from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_data(symbol):
    url = 'https://finance.naver.com/item/sise.nhn?code={}'.format(symbol)
    with urlopen(url) as doc:
        soup = BeautifulSoup(doc, "lxml", from_encoding="euc-kr")
        cur_price = soup.find('strong', id='_nowVal') # id가 _nowVal인 <strong>태그를 찾는다.
        cur_rate = soup.find('strong', id= '_rate') # id가 _rate인 <strong> 태그를 찾는다.
        stock = soup.find('title') # <title> 태그를 찾는다.
        stock_name = stock.text.split(':')[0].strip() # <title>태그에서 ':' 문자를 기준으로 분리
        return cur_price.text, cur_rate.text.strip(), stock_name

def main_view(request):

    querydict = request.GET.copy()
    mylist = querydict.lists() # get 방식으로 넘어온 QueryDict을 리스트 형태로 변환
    rows = []
    total = 0

    for x in mylist:
        cur_price, cur_rate, stock_name = get_data(x[0]) # 현재가, 등락률, 종목명을 구한다.
        price = cur_price.replace(',', '')
        stock_count = format(int(x[1][0]), ',') # 종목수를 int 형으로 변환 뒤 천 단위에 ','를 포함
        sum = int(price) * int(x[1][0])
        stock_sum = format(sum, ',')
        rows.append([stock_name, x[0], cur_price, stock_count, cur_rate,
                     stock_sum]) # 종목명, 종목코드, 현재가, 주식수, 등락률, 평가금액을 추가
        total = total + int(price) * int(x[1][0]) # 평가금액 * 주식수

    # 천 단위로 ',' 를 표시
    total_amount = format(total, ',')
    values = {'rows' : rows, 'total' : total_amount, 'request' : request, 'mylist':mylist, 'querydict':querydict} # balance.html 에 전달할 값 저장

    # # balance.html에 values를 넘겨줌.
    return render(request, 'balance.html', values) # balance.html을 표시하도록 값을 전달
#
def main_info(request):
    querydict = request.GET.copy()
    mylist = querydict.lists()
    rows = []
    total = 0

    values = {'rows': rows, 'code': '005930'}  # balance.html 에 전달할 값 저장

    # # balance.html에 values를 넘겨줌.
    return render(request, 'info.html', values)

# 주식명, 보유 수 등을 받음
def main_view2(request):
    querydict = request.GET.copy()
    asset_info = list(querydict.values())


    asset = asset_info[0]
    stock_code = asset_info[1]
    quantity = asset_info[2]
    first_price = asset_info[3]
    # 타입을 정수형을 바꾸어 준 후 천 단위마다 쉼표를 표시
    first_price = int(first_price)
    # 주식코드를 입력하면 (현재가, 등락률, 주식명)을 가져온다.
    cur_price, cur_rate, stock_name = get_data(stock_code)
    # ','를 없애준다 -> 자료형을 정수형으로 변환시키기 위해
    cur_price = cur_price.replace(',', '')
    # 자료형을 정수형으로 변환(매입가와 현재가의 계산을 위해-> 등락률)
    cur_price = int(cur_price)
    # 등락률 계산
    revenue = (cur_price - first_price) / first_price * 100
    revenue = round(revenue, 2)

    asset_sum = cur_price * int(quantity)

    # 천단위 쉼표 표시하기
    cur_price = format(cur_price, ',')
    first_price = format(first_price, ',')
    asset_sum = format(asset_sum, ',')

    values = {'asset' : asset, 'stock_code':stock_code, 'quantity':quantity,
              'cur_price': cur_price, 'first_price':first_price, 'revenue' : revenue, 'asset_sum':asset_sum}


    return render(request, 'balance.html', values)

def info(request):

    return render(request, 'index.html')


# 로그인 페이지로 이동
def login(request):

    return render(request, 'login.html')

def sign_in(request):
    return render(request, 'sign.html')

def insert_info(request):
    querydict = request.POST.copy()
    member_info = list(querydict.values())

    id = member_info[0]
    pw = member_info[1]

    # 디비 연동
    from django.db import connection, transaction

    cursor = connection.cursor()

    sql = "insert into balance_user(user_id, password) values('{}', '{}')".format(id,pw)
    cursor.execute(sql)
    transaction.commit_unless_managed()
    return redirect('../../../')


# Create your views here.
