from bs4 import BeautifulSoup
import urllib.request as rqst
import jiagu
import jieba
import thulac
from datetime import date
import redis


def page_generator(step):
    if step == 0:
        return ""
    else:
        return '_{}'.format(step)

# here we use redis as an easy example.
#
def database_init():
    # here set your own redis locations
    r = redis.Redis(host='localhost', port=6379, db=0)
    return r

# an example for creating
def save_to_database(sentence, date, words, redis):
    # 通过 zrank set_name keyvalue 判断有无
    words = list(set(words))
    for word in words:
        # filter the words
        if len(word) <= 1:
            continue
        else:
            mapping = {word: 1}
            if redis.zrank('word_test2', word) is not None:
                redis.zadd('word_test2', mapping, incr=True)
            else:
                redis.zadd('word_test2', mapping)
    return


def display_database(redis):
    pairs = redis.zrange('word_test2', 0, -1, withscores=True)
    for pair in pairs:
        value, score = pair
        print(value.decode("utf-8"), score)


def create_database(red):
    # init settings
    thu1 = thulac.thulac()
    # red = database_init()
    limit_date = date(2020, 11, 16)
    step = 0

    # set the base addrs
    base_site = 'http://www.cs.ecitic.com/newsite/news/'

    #set the stop flag
    flag = 1

    while(flag):
        # update pages
        pages = 'index{}.html'.format(page_generator(step))
        step += 1

        # read url and parsing the title
        cur_file = rqst.urlopen(base_site + pages)
        cur_data = cur_file.read()
        cur_soup = BeautifulSoup(cur_data, 'html.parser')
        cur_soup = cur_soup.body
        main_soup = None
        for divs in cur_soup.find_all('div'):
            try:
                _ = divs['class']
            except:
                continue
            if 'li' in divs['class']:
                print('catched!')
                main_soup = divs
                day = main_soup.div.h2.text
                timeline = main_soup.find_all('p', class_='font18')[0].text
                cur_date = date(int(timeline.split('-')[0]), int(timeline.split('-')[1]), int(day))

                # stop flag
                if cur_date < limit_date:
                    flag = 0
                    print('timeline reaches the limitation: {}'.format(cur_date))
                    break

                # get the title
                title = main_soup.find_all('a')[0].text
                ## comparison of several segmentation algorithms
                # print('---------------------------')
                # print(jiagu.seg(title))
                # print(thu1.cut(title))
                # print(jieba.lcut(title))
                word_cuts = jieba.lcut(title)
                save_to_database(title, cur_date, word_cuts, red)
                print(word_cuts)
                print('-----------')

    print('create done!')


if __name__ == '__main__':
    red = database_init()
    create_database(red)
    display_database(red)