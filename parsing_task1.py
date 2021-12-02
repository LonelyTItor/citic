#coding:utf-8
from bs4 import BeautifulSoup
import urllib.request as rqst
import jiagu
import jieba
import thulac
from datetime import date
import redis
from urllib import parse


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
    base_url = "http://www.mwr.gov.cn/zw/zcfg/gfxwj/"
    #set the stop flag
    flag = 1
    step = 0

    while(flag):
        # update pages
        pages = 'index{}.html'.format(page_generator(step))
        step += 1

        # read url and parsing the title
        cur_url = base_url + pages
        cur_file = rqst.urlopen(cur_url)
        cur_data = cur_file.read()
        cur_soup = BeautifulSoup(cur_data, 'lxml')
        news_slots = cur_soup.find_all('ul', class_='slnewsconlist')
        for slot in news_slots:
            news_elems = slot.find_all('li')
            for news_elem in news_elems:
                publish_time = news_elem.span.text
                title = news_elem.a.text
                content_url = parse.urljoin(cur_url, news_elem.a['href'])
                content_data = rqst.urlopen(content_url).read()
                content_soup = BeautifulSoup(content_data, 'html.parser')
                out = parsing_detail(content_soup)
                print(content_url)
        print('---------------')
        if step == 12:
            flag = 0

def parsing_detail(content_soup):
    new_obj = {}
    target_table = content_soup.body.find_all('table', class_='suoyin')[0]
    post_office = target_table.contents[1].contents[7].contents[1].text.replace('\n', "").replace(' ', '')
    source = target_table.contents[3].contents[3].text
    tag = target_table.contents[7].contents[3].text.replace('[', '〔').replace(']', '〕')
    a = str(content_soup.body)
    # print(a)
    print(tag, post_office, source)
    # post_office = content_soup.
    return None


if __name__ == '__main__':
    parsing_1()