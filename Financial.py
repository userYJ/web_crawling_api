import os
from operator import index
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome() 
browser.maximize_window() # window 최대화

# 1. 페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

# 2. 조회 항목 초기화 (체크 리스트 해제)
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected():
        checkbox.click() #체크 해제

# 3. 조회 항목 설정
items_to_select = ["거래량","전일거래량","영업이익","자산총계","매출액"]
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') # 부모 element -> td tag
    label = parent.find_element(By.TAG_NAME, 'label')
    # print(label.text) # 목록 이름 확인
    if label.text in items_to_select:
        checkbox.click()

# 4. Apply
btn_apply = browser.find_element(By.XPATH, '//*[@id="contentarea_left"]/div[2]/form/div/div/div/a[1]')
# btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

for idx in range(1,40): # 1~ 39 페이지까지
    # 페이지 이동
    browser.get(url+str(idx))

# 5. 데이터 추출 // lxml-> 페이지 분석 위해
    df = pd.read_html(browser.page_source)[1]
    df.dropna(axis='index', how='all',inplace=True) # 모두 결측치일때 지우기
    df.dropna(axis='columns', how ='all', inplace=True)
    if len(df) == 0 :
        break 

    # 6. 데이터 파일로 저장
    f_name = 'quote.csv'
    if os.path.exists(f_name): # 파일 있으면 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False) # 앞에 데이터 뒤에다가 append
    else: # 처음으로 파일 만들어지는 과정
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지')

browser.quit() # 브라우저 종료