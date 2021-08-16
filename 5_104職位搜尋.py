import time
import os
import requests
import json
from bs4 import BeautifulSoup

resource_path = r'./104_searching'

if not os.path.exists(resource_path):
    os.mkdir(resource_path)

"https://www.104.com.tw/jobs/search/?keyword=DevOps%20data%20cloud"

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
           'Referer': 'https://www.104.com.tw/jobs/search/'}
ss = requests.session()

keywords_list = ['Data', 'Science', 'Cloud']

keywords = '%20'.join(keywords_list)

url_count = 'https://www.104.com.tw/jobs/search/list'
query = f'&keyword={keywords}'

params = f'{query}'

r = requests.get(url_count, params=params, headers=headers)

data = r.json()
total_count = data['data']['totalCount']


if (total_count/30) >= 150:
    page = 150
else:
    page = round((total_count/30),0)

for i in range(1, 3):

    pages = f'&page={i}'
    urlKeywords = "https://www.104.com.tw/jobs/search/?keyword=" + keywords + pages

    res = ss.get(urlKeywords, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    articles_list = soup.select('div[id="js-job-content"] article')
    for i in range(len(articles_list)):
        articles = soup.select('div[id="js-job-content"] article')[i]
        # print(articles)
        article_title = articles.select('a[target="_blank"]')[0].text
        print(article_title)
        article_companyName = articles.select('a[target="_blank"]')[1].text
        # print(article_companyName)
        article_city = articles.select('ul[class="b-list-inline b-clearfix job-list-intro b-content"] li')[0].text
        # print(article_city)
        article_experiences = articles.select('ul[class="b-list-inline b-clearfix job-list-intro b-content"] li')[1].text
        # print(article_experiences)
        article_degree = articles.select('ul[class="b-list-inline b-clearfix job-list-intro b-content"] li')[2].text
        # print(article_degree)
        # print("============Describtion=================")
        article_positionDescribe = articles.select('p[class="job-list-item__info b-clearfix b-content"]')[0].text
        # print(article_positionDescribe)
        # print("========================================")
        article_contents = ""
        article_contents += '職位名稱: %s\n'%(article_title)
        article_contents += '公司名稱: %s\n' % (article_companyName)
        article_contents += '上班地點: %s\n' % (article_city)
        article_contents += '經驗要求: %s\n' % (article_experiences)
        article_contents += '學歷要求: %s\n' % (article_degree)
        # article_contents += '\n============Describtion=================\n'
        article_contents += '職位描述: %s\n' % (article_positionDescribe)

        try:
            with open(r'%s/%s.txt' % (resource_path, article_title), 'w', encoding='utf-8') as w:
                w.write(article_contents)
        except FileNotFoundError:
            pass

