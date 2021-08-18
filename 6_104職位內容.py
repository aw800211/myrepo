import time
import os
import requests
import json
from bs4 import BeautifulSoup

"https://www.104.com.tw/jobs/search/?keyword=DevOps%20data%20cloud"

headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
           'Referer': 'https://www.104.com.tw/jobs/search/'}
ss = requests.session()

keywords_list = ['Data']

keywords = '%20'.join(keywords_list)

urlKeywords = "https://www.104.com.tw/jobs/search/?keyword=" + keywords
res = ss.get(urlKeywords, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')

articles_list = soup.select('div[id="js-job-content"] article')

def get_job_contents(job_id):
    headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
               'Referer': f'https://www.104.com.tw/job/{job_id}'}
    ss = requests.session()
    articles_list_link = f'https://www.104.com.tw/job/ajax/content/{job_id}'
    res_jobs = ss.get(articles_list_link, headers=headers)
    data = res_jobs.json()
    return data['data']['jobDetail']['jobDescription']

for i in range(len(articles_list)):
    job_id =articles_list[i].a['href'].split('?')[0].split('/')[-1]
    job_description = get_job_contents(job_id)
    job_link ='https://' +  articles_list[i].a['href'].split('//')[1].split('?')[0]
    # print(job_description)
    print(job_link)
    print('======')




