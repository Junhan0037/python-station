#!/usr/bin/env python3 
#셀프 주유소 가격 분석

#Selenium
from selenium import webdriver
#크롬 드라이버 접속
driver = webdriver.Chrome('/Users/JunHan/Desktop/Python/Station-Project/driver/chromedriver')
driver.get("http://www.opinet.co.kr/searRgSelect.do")

#구 리스트 Xpath 가져오기
gu_list_raw = driver.find_element_by_xpath("""//*[@id="SIGUNGU_NM0"]""")
#option이라는 태그 안에 속해있다 (element 아닌 elements로 해야 리스트형으로 반환)
gu_list = gu_list_raw.find_elements_by_tag_name("option")

#split 하기
gu_names = [option.get_attribute("value") for option in gu_list]
gu_names.remove('')
print(gu_names)

#time은 sleep 시키기, tqdm은 for문 과정을 시각화
import time
from tqdm import tqdm_notebook

for gu in tqdm_notebook(gu_names):
    #구 선택란에 구 이름 적용
    element = driver.find_element_by_id("SIGUNGU_NM0")
    element.send_keys(gu)
    
    time.sleep(2)
    
    #조회 버튼 클릭
    xpath = """//*[@id="searRgSelect"]/span"""
    element_sel_gu = driver.find_element_by_xpath(xpath).click()
    
    time.sleep(1)
    
    #엑셀저장 버튼
    xpath = """//*[@id="glopopd_excel"]/span"""
    element_get_excel = driver.find_element_by_xpath(xpath).click()
    
    time.sleep(1)

#크롬 드라이버 종료
driver.close()

    
    
    
    
    
    
    
    