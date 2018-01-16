import re
import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from taobao import taobao
from tmall import tmall
from tmall_hk import tmall_hk
from jd import jd
from jd_hk import jd_hk

item_url = input("Please input the item url:") # 在终端输入url时，最后加个空格，再回车，不然Pycharm会自动打开这个url
driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver.get(item_url)

item_name = driver.title.replace('/', '-').replace('\\', '--').replace('《', '[').replace('》', ']')
path = 'all_items/' + item_name
if not os.path.exists (path):
    os.makedirs (path)

if 'detail.tmall.com/' in item_url:
    tmall(driver, time, re, urllib, path, ActionChains, Keys)
if 'detail.tmall.hk/' in item_url:
    tmall_hk (driver, time, re, urllib, path, ActionChains, Keys)
elif 'item.taobao.com/' in item_url:
    taobao (driver, time, re, urllib, path, ActionChains, Keys)
elif 'item.jd.com/' in item_url:
    jd (driver, time, re, urllib, path, ActionChains, Keys)
elif 'item.jd.hk/' in item_url:
    jd_hk (driver, time, re, urllib, path, ActionChains, Keys)
