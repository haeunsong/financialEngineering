import bs4
from urllib.request import urlopen
import datetime as dt 

def date_format(d):
  d = str(d).replace('.','-')
  yyyy = int(d.split('-')[0])
  mm = int(d.split('-')[1])
  dd = int(d.split('-')[2])
  this_date = dt.date(yyyy,mm,dd)
  return this_date

def remove_comma(d):
  this_close = d.replace(',','') # , 제거
  this_close = float(this_close)
  return this_close

historical_prices = dict() # 딕셔너리 선언

# 데이터 추출 기능을 함수로 만들기

def historical_index_naver(index_cd,start_date='',end_date='',page_n=1,last_page=0):
  
  if start_date: # 있으면 # (str 형식)
    start_date = date_format(start_date) # date 포맷으로 변환

  else: # 없으면
    start_date = dt.date.today() # 오늘 날짜 지정
  if end_date: #있으면
    end_date = date_format(end_date)
  else: # 없으면
    end_date = dt.date.toda() 

  naver_index = 'https://finance.naver.com/sise/sise_index_day.nhn?code=' + index_cd + '&page='+str(page_n)

  source = urlopen(naver_index).read() # 지정한 페이지에서 코드 읽기
  source = bs4.BeautifulSoup(source,'lxml') # BeautifulSoup로 태그별로 코드 분류

  dates = source.find_all('td',class_='date')
  prices = source.find_all('td',class_='number_1')

  for n in range(len(dates)): # 6
    if dates[n].text.split('.')[0].isdigit():
      # 날짜 처리
      this_date = dates[n].text 
      this_date = date_format(this_date)

      if this_date <= end_date and this_date >=start_date:
        # 종가 처리
        this_close = prices[n*4].text  # prices 중 종가지수인 0,4,8 ... 데이터만 추출
        this_close = remove_comma(this_close)
        print(n,this_date,this_close)
        # 딕셔너리에 저장
        historical_prices[this_date] = this_close
  
    elif this_date < start_date: # start_date 함수 이전이면 종료
      print('종료')
      return historical_prices

  # 페이지 내비게이션
  if last_page == 0 :
    last_page = source.find('td',class_='pgRR').find('a')['href']
    last_page = int(last_page.split('&')[1].split('=')[1])

  # 다음 페이지 호출
  if page_n < last_page:
    page_n = page_n + 1
    historical_index_naver(index_cd,start_date,end_date,page_n,last_page)
  
  return historical_prices

index_cd = 'KPI200'
res = historical_index_naver(index_cd,'2021-03-01','2021-03-30')
print(res)



