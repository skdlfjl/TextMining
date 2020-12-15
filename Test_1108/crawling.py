import requests
from bs4 import BeautifulSoup
import re


# [BeautifulSoup] 각 카테고리로 이동할 수 있는 링크 추출 --------------------
url = "https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=job.latest_order&years=-1&locations=all"
url_main = requests.get(url) # http get request를 통해, 내가 데이터를 가져오고자 하는url 내에 있는 데이터를 가져온다.

url_main_list = BeautifulSoup(url_main.content, "html.parser", from_encoding='utf=8')
# bs4로 데이터를 python이 이해할 수 있는 구조로 parsing한다.

link_list = url_main_list.select('._3SgvgiuDypnw8sSW2Pxngs > a')  # ._3SgvgiuDypnw8sSW2Pxngs 클래스의 a태그만 추출
print(link_list[0]['href'])  # a태그의 'herf'만 추출해보기 (임의로 0번째만 추출)
#print(link_list)

len(link_list) # 0~34 -> 총 35개 카테고리

link = []  # 빈 리스트를 만들어 카테고리의 'href', 즉 링크만 추출해 저장
for i in range(len(link_list)):
    link.append(link_list[i]['href'])
print(link)
print(len(link))

# 완전한 링크로 만들기
add_link = "https://www.wanted.co.kr"
add_link + link[1]

category_link = []  # 빈 리스트를 만들어, 각 링크 앞에 "https://www.wanted.co.kr"를 붙여 완전해진 링크를 저장한다.
for i in range(len(link)):
    category_link.append(add_link + link[i])

print(category_link)  # 각 카테고리로 이동할 수 있는 최종 링크 확인.



# [selenium] 카테고리의 채용공고 링크 추출 (for문 이용해서 만들기, 스크롤다운 추가해야됨) --------------------
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 파이썬개발자[6] 데이터엔지니어[7] 데이터사이언티스트[12] 머신러닝엔지니어[13] 빅데이터엔지니어[15]
category = [6, 7, 12, 13, 15]
for i in category:
    driver = webdriver.Chrome(r"D:\chromedriver_win32\chromedriver.exe")
    driver.get(category_link[i])
    time.sleep(1)

    body = driver.find_element_by_tag_name("body")

    num_of_pagedowns = 100
    while num_of_pagedowns:  # 웹페이지 스크롤 하기!!
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)
        num_of_pagedowns -= 1

    html = driver.page_source  # 스크롤한 웹 페이지의 html 저장
    soup = BeautifulSoup(html, 'html.parser')

    employ_link_list = soup.select('._3D4OeuZHyGXN7wwibRM5BJ > a')

    link = []  # 빈 리스트를 만들어 카테고리의 'href', 즉 링크만 추출해 저장
    for a in range(len(employ_link_list)):
        link.append(employ_link_list[a]['href'])

    add_link = "https://www.wanted.co.kr"
    employ_link = []  # 빈 리스트를 만들어, 각 링크 앞에 "https://www.wanted.co.kr"를 붙여 완전해진 링크를 저장한다.
    for b in range(len(link)):
        employ_link.append(add_link + link[b])
    print(len(employ_link))  # 카테고리당 사용한 데이터(채용공고) 개수

    text = []
    for j in range(len(employ_link)):
        driver.get(employ_link[j])
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            str = soup.select('._1LnfhLPc7hiSZaaXxRv11H')[0].text
        except:
            pass

        try:
            found = re.search('자격요건(.+?)혜택 및 복지', str).group(1)
        except AttributeError:
            # 자격요건, 혜택 및 복지 not found in the original string
            found = ''  # apply your error handling

        text.append(found)

    final_text = '\n'.join(text)
    f = open("category{0}.txt".format(i), "w", encoding='utf8')
    f.write(final_text)
    f.close()

