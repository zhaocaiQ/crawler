# 필요한 라이브러리를 로딩합니다.
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import os
import sys
import time


class NewsCrawler:
    def __init__(self, menu, headers, sel_header, driver):
        self.menu = menu
        self.headers = headers
        self.driver = driver
        self.sel_header = sel_header

    nos = []
    titles = []
    articles = []
    writers = []
    links = []
    ## 헤드라인 뉴스 ##

    def headline(self):
        global nos
        global titles
        global articles
        global writers
        global links

        # 리스트 비우기
        self.nos.clear()
        self.links.clear()
        self.titles.clear()
        self.articles.clear()
        self.writers.clear()

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        try:
            news = soup.find("div", "hdline_news")
            hdline = news.select("ul > li")
        except AttributeError:
            print("정보가 없습니다.")
            print("="*80)
        else:
            ##헤드라인 뉴스 크롤링##
            # 기사 링크 추출
            for i in hdline:
                try:
                    self.links.append(
                        "https://news.naver.com/"+i.find("a").attrs['href'])
                except AttributeError:
                    self.links.append("해당 기사의 링크가 존재하지 않습니다.")
            num = 1
            # 기사 내용 추출
            for i in range(1, len(self.links)+1):
                try:
                    time.sleep(2)
                    self.driver.find_element_by_xpath(
                        f'//*[@id="today_main_news"]/div[2]/ul/li[{i}]').click()
                    time.sleep(2)
                except:
                    print("추출할 기사가 없습니다.")
                    print("="*80)
                else:
                    # 기사 추출
                    html = self.driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')
                    try:
                        content = soup.find("div", "content")
                    except AttributeError:
                        print(f"{self.headers['%s'%self.menu]}섹션의 기사가 없습니다.")
                    else:
                        try:
                            title = content.find(
                                "h3", "tts_head").get_text().strip()
                        except AttributeError:
                            title = "제목이 없습니다."
                            self.titles.append(title)
                            print("제목:", title)
                        else:
                            self.nos.append(num)
                            print("글번호:", num)
                            self.titles.append(title)
                            print("제목:", title)
                        try:
                            article = content.find(
                                "div", "_article_body_contents").get_text().strip()
                        except AttributeError:
                            article = "내용이 없습니다."
                            self.articles.append(article)
                            print("내용:", article)
                        else:
                            self.articles.append(article)
                            print("내용:", article)
                        try:
                            writer = content.find(
                                "div", "byline").get_text().strip()
                        except AttributeError:
                            writer = "작성자가 없습니다."
                            self.writers.append(writer)
                            print("작성자:", writer)
                        else:
                            self.writers.append(writer)
                            print("작성자:", writer)
                            print("바로가기:", self.links[i-1])
                            num += 1
                    time.sleep(2)
                    self.driver.back()
                    time.sleep(2)
                    print("="*80)

    ## 그외 뉴스들 ##
    def news(self):
        global nos
        global titles
        global articles
        global writers
        global links

        # 리스트 비우기
        self.nos.clear()
        self.links.clear()
        self.titles.clear()
        self.articles.clear()
        self.writers.clear()

        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        try:
            news = soup.select("div[class='main_component droppable']")
        except AttributeError:
            print("정보가 없습니다.")
            print("="*80)
        else:
            num = 1
            for i in range(1, len(news)+1):
                if i == self.menu and self.menu != 1:
                    try:
                        sec = news[i-1].select("ul > li")
                    except AttributeError:
                        print("정보가 없습니다.")
                        print("="*80)
                    for link in sec:
                        try:
                            self.links.append(link.find('a').attrs['href'])
                        except AttributeError:
                            self.links.append("해당 기사의 링크가 존재하지 않습니다.")
                    for j in range(1, len(sec)+1):
                        try:
                            time.sleep(2)
                            self.driver.find_element_by_xpath(
                                f'//*[@id="{self.sel_header["%s" %i][1]}"]/div[2]/div/ul/li[{j}]').click()
                            time.sleep(2)
                        except AttributeError:
                            print("추출할 기사가 없습니다.")
                            print("="*80)
                        else:
                            # 기사 추출
                            html = self.driver.page_source
                            soup = BeautifulSoup(html, 'html.parser')
                            try:
                                content = soup.find("div", "content")
                            except AttributeError:
                                print(
                                    f"{self.headers['%s'%self.menu]}섹션의 기사가 없습니다.")
                            else:
                                try:
                                    title = content.find(
                                        "h3", "tts_head").get_text().strip()
                                except AttributeError:
                                    title = "제목이 없습니다."
                                    self.titles.append(title)
                                    print("제목:", title)
                                else:
                                    self.nos.append(num)
                                    print("글번호:", num)
                                    self.titles.append(title)
                                    print("제목:", title)
                                try:
                                    article = content.find(
                                        "div", "_article_body_contents").get_text().strip()
                                except AttributeError:
                                    article = "내용이 없습니다."
                                    self.articles.append(article)
                                    print("내용:", article)
                                else:
                                    self.articles.append(article)
                                    print("내용:", article)
                                try:
                                    writer = content.find(
                                        "div", "byline").get_text().strip()
                                except AttributeError:
                                    writer = "작성자가 없습니다."
                                    self.writers.append(writer)
                                    print("작성자:", writer)
                                else:
                                    self.writers.append(writer)
                                    print("작성자:", writer)
                                    print("바로가기:", self.links[j-1])
                                    num += 1
                            time.sleep(2)
                            self.driver.back()
                            time.sleep(2)
                            print("="*80)


class Save(NewsCrawler):
    def __init__(self, menu, headers, save_menu):
        self.menu = menu
        self.headers = headers
        self.save_menu = save_menu

    def save_type(self):
        # 정보 리스트 합치기
        sum_list = [self.nos, self.titles,
                    self.articles, self.writers, self.links]
        # 파일저장 메뉴
        file_ext = {"1": "txt", "2": "csv", "3": "xlsx"}

        # 저장에 필요한 시간정보 추출하기
        now = time.localtime()
        ff_name = "%04d-%02d-%02d-%02d-%02d" % (
            now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)

        # 저장명 생성
        save_name = f"{ff_name}-{self.headers['%s' %self.menu]}.{file_ext['%s' %self.save_menu]}"
        # txt 저장
        if self.save_menu == 1:
            f = open(save_name, 'a', encoding='utf-8')
            for i in range(len(sum_list[0])):
                f.write("번호:"+str(sum_list[0][i])+"\n")
                f.write("제목:"+sum_list[1][i]+"\n")
                f.write("내용:"+sum_list[2][i]+"\n")
                f.write("작성자:"+sum_list[3][i]+"\n")
                f.write("링크:"+sum_list[4][i]+"\n")
                f.write("="*80+"\n")
            f.close()
            print(f"{save_name}으로 저장이 완료되었습니다.")
            print("="*80)

        # csv, xlsx 저장
        else:
            data = pd.DataFrame()
            data['번호'] = sum_list[0]
            data['제목'] = sum_list[1]
            data['내용'] = sum_list[2]
            data['작성자'] = sum_list[3]
            data['링크'] = sum_list[4]
            if self.save_menu == 2:
                data.to_csv(save_name, encoding='utf-8-sig')
                print(f"{save_name}으로 저장이 완료되었습니다.")
                print("="*80)
            else:
                data.to_excel(save_name)
                print(f"{save_name}으로 저장이 완료되었습니다.")
                print("="*80)


class Run:
    headers = {}
    sel_header = {}

    def run(self):
        global headers
        global sel_header

        # 크롬으로 네이버 연결
        path = "C:\python_temp\chromedriver_win32\chromedriver.exe"
        driver = webdriver.Chrome(path)
        driver.get("https://www.naver.com")

        # 전체화면으로 변환
        driver.maximize_window()
        time.sleep(1)

        # 네이버에서 뉴스페이지로 이동
        driver.find_element_by_xpath(
            '//*[@id="NM_FAVORITE"]/div[1]/ul[2]/li[2]/a').click()
        time.sleep(1)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        header = soup.find_all("div", "com_header")

        no = 1
        for i in header:
            self.headers[f'{no}'] = i.find("h4").get_text()
            no += 1

        ## 메뉴 만들기 ##
        try:
            header = soup.find_all("div", "com_header")
        except AttributeError:
            print("메뉴 정보가 없습니다.")
        else:
            no = 1
            for i in header:
                head = i.find("h4").get_text()

                # sel_header 사전에 저장 / 뉴스페이지에 들어갈때 xpath에 필요
                if head == "헤드라인 뉴스":
                    self.sel_header[f'{no}'] = [f'{head}', "today_main_news"]
                elif head == "정치":
                    self.sel_header[f'{no}'] = [f'{head}', "section_politics"]
                elif head == "경제":
                    self.sel_header[f'{no}'] = [f'{head}', "section_economy"]
                elif head == "사회":
                    self.sel_header[f'{no}'] = [f'{head}', "section_society"]
                elif head == "생활/문화":
                    self.sel_header[f'{no}'] = [f'{head}', "section_life"]
                elif head == "세계":
                    self.sel_header[f'{no}'] = [f'{head}', "section_world"]
                elif head == "IT/과학":
                    self.sel_header[f'{no}'] = [f'{head}', "section_it"]
                else:
                    pass

                # headers 사전에 저장
                if "/" in head:
                    head = head.replace("/", ',')
                    self.headers[f'{no}'] = head
                else:
                    self.headers[f'{no}'] = head
                no += 1

        # 크롤러 출력시작
        print("="*80)
        print(f'{"네이버 뉴스 크롤러 version 1.0": ^65}')
        print("="*80)
        while True:
            ## 메뉴 출력 ##
            for key, value in self.headers.items():
                print(key+"번: "+value)
            print("0번: 종료")
            print("="*80)
            try:
                menu = int(input("메뉴를 선택해주세요 > "))
            except ValueError:
                print("메뉴를 입력하세요.")
                continue
            else:
                if menu == 0:
                    print("뉴스 크롤러를 종료합니다.")
                    print("웹 브라우저를 종료합니다.")
                    print("="*80)
                    driver.close()
                    break
                else:
                    try:
                        print(f"{menu}번 {self.headers['%s'%menu]} 섹터를 출력합니다.")
                        time.sleep(1)
                    except KeyError:
                        print("메뉴에 있는 숫자만 입력해주세요.")
                    else:
                        new = NewsCrawler(menu, self.headers,
                                          self.sel_header, driver)
                        if menu == 1:
                            new.headline()
                        else:
                            new.news()

                        # 이미지를 저장할 폴더를 생성합니다.
                        while True:
                            try:
                                save_q = input(
                                    "추출된 데이터를 파일로 저장하시겠습니까?(Y/N) > ")
                            except ValueError:
                                print("(Y/N)를 입력해주세요.")
                                print("="*80)
                                continue
                            else:
                                if save_q.upper() == "Y":
                                    while True:
                                        f_dir = input(
                                            "저장할 폴더를 지정하세요:(예: c:\\naver_news\\) > ")
                                        if f_dir == "":
                                            print("저장할 폴더 경로를 입력해주세요.")
                                            continue
                                        elif f_dir[-1] != "\\":
                                            print("저장할 폴더 경로를 정확히 입력해주세요")
                                            continue
                                        else:
                                            if os.path.isdir(f_dir):
                                                os.chdir(f_dir)
                                            else:
                                                os.makedirs(f_dir)
                                                os.chdir(f_dir)
                                            # 저장에 필요한 시간정보 추출하기
                                            now = time.localtime()
                                            f_name = "%04d-%02d-%02d" % (
                                                now.tm_year, now.tm_mon, now.tm_mday)

                                            # 선택한 뉴스 섹션이름으로 폴더 생성하기
                                            ff_dir = f_name+"-" + \
                                                self.headers['%s' % menu]
                                            if os.path.isdir(ff_dir):
                                                os.chdir(ff_dir)
                                            else:
                                                os.makedirs(ff_dir)
                                                os.chdir(ff_dir)
                                            f_result_dir = f_dir+ff_dir
                                            print("저장경로:", f_result_dir)
                                            print("="*80)
                                            # 저장하기
                                            while True:
                                                try:
                                                    save_menu = int(input("[메뉴] 1.txt 2.csv 3.xls (종료: 0)"+"\n"
                                                                          + "메뉴를 선택해 주세요 > "))
                                                except ValueError:
                                                    print("숫자를 입력해주세요.")
                                                    print("="*80)
                                                    continue
                                                if not save_menu in (1, 2, 3, 0):
                                                    print("메뉴만 입력해주세요.")
                                                    print("="*80)
                                                    continue
                                                elif save_menu == 0:
                                                    print("저장 프로그램을 종료합니다.")
                                                    print("="*80)
                                                    break
                                                else:
                                                    save = Save(
                                                        menu, self.headers, save_menu)
                                                    save.save_type()
                                            break
                                    break
                                elif save_q.upper() == "N":
                                    print("저장 프로그램을 종료합니다.")
                                    print("="*80)
                                    break
                                else:
                                    print("(Y/N)만 입력해주세요.")
                                    continue
