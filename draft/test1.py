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

base_url = "http://www.moa.gov.cn/govsearch/simp_gov_list.jsp"

cur_file = requests.get(base_url, headers=headers)

ee = BeautifulSoup(cur_file.content, 'lxml')

print(ee)