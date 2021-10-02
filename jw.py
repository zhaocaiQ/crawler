class JW:
    no2 = []  # 번호들을 담을 리스트
    writers = []  # 작성자들을 담을 리스트
    dates = []  # 날짜들을 담을 리스트
    titles = []  # 제목들을 담을 리스트
    contents = []  # 내용들을 담을 리스트

    def view(self, query_txt, driver):  # 네이버 검색에서 View 섹션 출력 함수
        # 네이버 VIEW - 블로그 주소
        driver.get(
            "https://search.naver.com/search.naver?sm=tab_hty.top&where=blog&query="+query_txt)
        no = 1

        print(f'VIEW-블로그 섹션의 {query_txt}으로 수집된 데이터를 추출합니다.')
        elements = driver.find_elements_by_xpath(
            '/html/body/div[3]/div[2]/div/div[1]/section/html-persist/div/more-contents/div/ul/li')

        for element in elements:
            title = element.find_element_by_css_selector(
                'div > div.total_area > a').text  # 블로그 제목
            content = element.find_element_by_css_selector(
                'div > div > div.total_group > div > a > div').text  # 블로그 요약 내용
            writer = element.find_element_by_css_selector(
                'div > div > div.total_info > div.total_sub > span > span > span.elss.etc_dsc_inner > a').text  # 작성자
            date = element.find_element_by_css_selector(
                'div > div > div.total_info > div.total_sub > span > span > span.etc_dsc_area > span').text  # 날짜

            print(f'번호: {no}')
            self.no2.append(no)
            no += 1
            print("작성자:", writer.strip())
            self.writers.append(writer)
            print("날짜:", date)
            self.dates.append(date)
            print("제목:", title)
            self.titles.append(title)
            print("내용:", content)
            self.contents.append(content)
            print('\n')
