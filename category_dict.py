
import requests
from bs4 import BeautifulSoup


# [BeautifulSoup] 각 카테고리로 이동할 수 있는 링크 추출 --------------------
url = "https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=job.latest_order&years=-1&locations=all"
url_main = requests.get(url) # http get request를 통해, 내가 데이터를 가져오고자 하는url 내에 있는 데이터를 가져온다.

soup = BeautifulSoup(url_main.content, "html.parser", from_encoding='utf=8')

category_name = []
for p in soup.find_all("span", {"class": "P__4XM_mbNn2CH6kDyUUJ hidden-xs"}):
    category_name.append(p.string)

print(category_name)
print(len(category_name))

category_dict = []
for i in range(len(category_name)):
    category_dict.append("category{}.txt".format(i) + " : " +  category_name[i])
print(category_dict)

dict_sum = '\n'.join(category_dict)
print(dict_sum)

f = open("category_dict.txt", "w", encoding='utf8')
f.write(dict_sum)
f.close()