import bs4
from urllib.request import urlopen
import datetime as dt 

# 1. 크롤링할 페이지 주소 분석
# https://finance.naver.com/sise/sise_index_day.nhn?code=KPI200&page=1
# https://finance.naver.com/sise/sise_index_day.nhn?code=종목코드&page=페이지번호
index_cd = 'KPI200'
page_n = 1
naver_index = 'https://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page='+str(page_n)

source = urlopen(naver_index).read()
print(source)
print('------------------------------')
source = bs4.BeautifulSoup(source,'lxml') # ** 이 과정 꼭 있어야한다!!! ** (html.parser 보다는 lxml 사용하기!)
print(source)


# 2. 날짜 가져오기

# 오늘: /html/body/div/table[1]/tbody/tr[3]/td[1] => /html/body/div/table[0]/tbody/tr[2]/td[0]
# 어제: /html/body/div/table[1]/tbody/tr[4]/td[1] => 
print(source.find_all('table')[0].find_all('tr')[2].find_all('td')[0]) # <td class="date">2021.04.30</td>
d = source.find_all('td',class_='date')[0].text # class 이름을 이용해서 뽑아냄. td앞에 붙은 태그 생략 가능!
print(d)

# 2.1. 날짜 형식 바꾸기
def date_format(d):
  yyyy = int(d.split('.')[0])
  mm = int(d.split('.')[1])
  dd = int(d.split('.')[2])
  this_date = dt.date(yyyy,mm,dd)
  this_date = str(this_date).replace('-','.')
  return this_date


# 3. 해당일의 종가지수 가져오기

# 3.1. Xpath이용해서 copy 
# 오늘: /html/body/div/table[1]/tbody/tr[3]/td[2] => /html/body/div/table[0]/tbody/tr[2]/td[1]
# 어제: /html/body/div/table[1]/tbody/tr[4]/td[2] => 

this_close = source.find_all('td',class_='number_1')[0].text

# 3.2. 받아온 데이터를 숫자로 인식하기 위해 숫자에서 천의 자리를 표시하는 쉼표제거하는 작업
def remove_comma(d):
  this_close = d.replace(',','') # , 제거
  this_close = float(this_close)
  return this_close

# 3.3. 페이지에 있는 모든 날짜와 가격을 불러옴.
dates = source.find_all('td',class_='date')
prices = source.find_all('td',class_='number_1')

for n in range(len(dates)):
  this_date = dates[n].text
  this_date = date_format(this_date)
  
  # 검사를 보면 number_1 태그를 체결가, 등락률, 거래량, 거래대금 칼럼이 모두 사용하고 있는데, 
  # 4개 값 중 0번째만 필요하기 때문에, 4를 곱해주어서 0,4,.. 등 4의 배수로 나타나는 값들만 추출하기
  this_close = prices[n*4].text 
  this_close = remove_comma(this_close)
  print(this_date,this_close)

# 4. 전체 페이지에서 데이터 가져오기
# 4.1. 마지막 페이지 주소를 가리키는 하이퍼링크 주소 뽑아오기
paging = source.find('td',class_='pgRR').find('a')['href']
# 4.1.1 페이지 번호만 뽑아오기
last_page = (int(paging.split('&')[1].split('=')[1]))
