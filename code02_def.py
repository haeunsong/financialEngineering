import bs4
from urllib.request import urlopen
import datetime as dt
import pandas as pd
import time
import requests

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

def getClosingPrice(index_cd,start_date='',end_date='',page_n=0,last_page=0):

  # 문자열 형식 날짜 => data 포맷으로 변환
  start_date = dt.datetime.strptime(start_date, "%Y.%m.%d").date()
  end_date = dt.datetime.strptime(end_date, "%Y.%m.%d").date()

  while(True):
    page_n += 1
    
    url = 'https://finance.naver.com/sise/sise_index_day.nhn?code='+index_cd+'&page='+str(page_n)
    source = urlopen(url).read()  # 지정한 페이지에서 코드 읽기
    source = bs4.BeautifulSoup(source, 'lxml')

    dates = source.find_all('td', class_='date')
    prices = source.find_all('td', class_='number_1')

    for i in range(0,len(dates)):
      this_date = dates[i].text 
      this_date = dt.datetime.strptime(this_date,"%Y.%m.%d").date()

      if this_date >= start_date and this_date <= end_date:
        # 종가 구하기
        this_close =  prices[i*4].text 
        print(this_date,this_close)


getClosingPrice('KPI200','2020.04.01','2021.05.01')

