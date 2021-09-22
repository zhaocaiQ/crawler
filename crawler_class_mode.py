#네이버 크롤러 Version 1.0

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys
from selenium.webdriver.common.keys import Keys
import pandas as pd

#검색어 입력 받은 후 검색화면까지 이동하는 클래스
class Searcher:
    def __init__(self):
        self.search = input("크롤링할 키워드는 무엇입니까?: ")
        #크롬으로 네이버 연결
        path = "C:\python_temp\chromedriver_win32\chromedriver.exe"
        self.driver = webdriver.Chrome(path)
        self.driver.get("https://www.naver.com")

        #전체화면으로 변환
        self.driver.maximize_window()
        time.sleep(1)

        #검색어 입력 후 검색버튼 클릭
        element = self.driver.find_element_by_class_name("input_text")
        element.send_keys(self.search)
        self.driver.find_element_by_class_name("btn_submit").click()
        time.sleep(1)

#크롤링 클래스 - Searcher 클래스 상속받음
class Crawler(Searcher):
    #동일 저장리스트
    no2 = []
    title2= []
    content2 = []
    #카페와 블로그만 동일
    writer2 = []
    dates2 = []
    #다른 저장리스트들
    sources=[]
    s_title2=[]
    dic2=[]
    dic_more2=[]
    
    #블로그
    def blog(self):
        pass

    #뉴스
    def news(self):
        pass

    #카페
    def cafe(self):
        pass

    #백과사전
    def know(self):
        pass
    
    #어학사전
    def lan_dic(self):
        pass

    
#저장하기 클래스
class SaveMenu():

    def save_txt(self):
        pass
    
    def save_csv(self):
        pass
    
    def save_xls(self):
        pass