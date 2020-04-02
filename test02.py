#!/usr/bin/env python3 
#Selenium 익히기 (셀프 주유소 가격 분석)
'''
Selenium은 웹 브라우저상의 주소가 바뀌지 않을 시,
접근주소가 없으면 Beautiful Soup에서 처리 할 수 없을 때 사용.
1. 터미널 창 pip install selenium 설치 후,
2. http://chromedriver.chromium.org/downloads 에서 크롬 드라이버 다운 
3. 코드 파일 위치레 driver 폴더 생성 후, 안에 압축 풀기
http://www.opinet.co.kr (주유소)
'''
from selenium import webdriver

#압축 풀어준 크롬 드라이버 접속
driver = webdriver.Chrome('/Users/JunHan/Desktop/Python/Station-Project/driver/chromedriver')
driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com")

#스크린샷 저장
driver.save_screenshot('/Users/JunHan/Desktop/Python/Station-Project/images/001.jpg')

#아이디, 비밀번호 창에 기입
elem_login = driver.find_element_by_id("id")
elem_login.clear()
elem_login.send_keys("wnsgks0037")

elem_login = driver.find_element_by_id("pw")
elem_login.clear()
elem_login.send_keys("173Wnals!!")

#Copy Xpath를 이용하여 로그인 클릭 (앞뒤로 """를 붙여주자)
xpath = """//*[@id="frmNIDLogin"]/fieldset/input"""
driver.find_element_by_xpath(xpath).click()

from bs4 import BeautifulSoup
#네이버 메일
driver.get("http://mail.naver.com")

#현재 Selenium이 접근한 페이지의 소스 받아오기
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

#보낸 사람
raw_list = soup.find_all('div', 'name _ccr(lst.from) ')

#리스트 split하기
send_list = [raw_list[n].find('a').get_text() for n in range(0, len(raw_list))]
print(send_list)

#크롬 드라이버 닫기
driver.close()
