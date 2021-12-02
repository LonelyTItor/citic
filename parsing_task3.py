#coding:utf-8
from bs4 import BeautifulSoup
import urllib.request as rqst
import jiagu
import jieba
import thulac
from datetime import date
import redis
from urllib import parse
import requests

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
    }

def new_policy_obj():
    obj = {
        "title": None,
        "source": None,
        "tag": None,
        "url": None,
        "publish_time": None,
        "content": None,
        "post office": None,
        }
    return obj


def page_generator(step):
    if step == 0:
        return ""
    else:
        return '_{}'.format(step)

def parsing_1():
    base_url = "http://www.moa.gov.cn/govsearch/simp_gov_list.jsp"
    #set the stop flag
    flag = 1
    step = 0

    while(flag):
        # update pages
        # pages = 'index_3081{}.html'.format(page_generator(step))
        step += 1
        # print(pages)
        # read url and parsing the title
        cur_file = requests.get(base_url, headers=headers)
        # print(cur_file.content)
        cur_soup = BeautifulSoup(cur_file.content, 'lxml')
        news_slots = cur_soup.find_all('ul', class_='commonlist')
        for slot in news_slots:
            news_elems = slot.find_all('li')
            for news_elem in news_elems:
                publish_time = news_elem.span.text
                # print(publish_time)
                title = news_elem.a.text
                ## decoding is wrong the
                # print(title)
                content_url = news_elem.a['href']
                content_file = requests.get(content_url, headers=headers)
                content_soup = BeautifulSoup(content_file.content, 'lxml')
                # print(title, content_url, publish_time)
                out = parsing_detail(content_soup)
        print('---------------')
        if step == 16:
            flag = 0

def parsing_detail(content_soup):
    new_obj = {}
    target_table = content_soup.body.find_all('div', class_='content_head')[0]
    head_table = target_table.find_all('div', class_='bod_head')
    title = head_table[0].dl.dd.text
    tag = head_table[1].find_all('dl')[1].dd.text.replace('[', '〔').replace(']', '〕')
    post_office = head_table[2].dl.dd.text
    if post_office == '文化部':
        print('no sub institude')
    source = ('10434235' + title).split('关于')[0].replace('10434235', '')
    if len(source) == 0:
        source = '文化部'
    print(tag, '|', source, '|', post_office, '|', title)
    # post_office = content_soup.
    return None


if __name__ == '__main__':
    parsing_1()