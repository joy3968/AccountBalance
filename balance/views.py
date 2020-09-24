from django.shortcuts import render
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

    total_amount = format(total, ',')
    values = {'rows' : rows, 'total' : total_amount, 'request' : request} # balance.html 에 전달할 값 저장

    # # balance.html에 values를 넘겨줌.
    return render(request, 'balance.html', values) # balance.html을 표시하도록 값을 전달


# Create your views here.
