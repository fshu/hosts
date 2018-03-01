#!/usr/bin/python
# -*- coding: utf-8 -*-
#pip install requests
#pip install beautifulsoup4

import re
import codecs
import requests
from bs4 import BeautifulSoup

BOOK_WEB="http://m.bxwx.io"
BOOK_IDX="65313"
BOOK_PAG=99

def get_web_html(url):
    resp = requests.get(url)
    resp.encoding = 'gbk'
    return resp.text

def get_chapters(idx,pag):
    ret_arr = []
    for i in xrange(1,pag):
        url = BOOK_WEB + "/chapters_" + idx + "/" + str(i)
        print(url)
        html = get_web_html(url)
        soup = BeautifulSoup(html,"html.parser")
        lists = soup.select('li a')
        for li in lists:
            arr_itm = {'name':'','href':''}
            arr_itm['name'] = li.get_text()
            arr_itm['href'] = li.get('href')
            if arr_itm['href'].endswith('html'):
                ret_arr.append(arr_itm)
    return ret_arr

def get_content(url):
    html = get_web_html(url)
    soup = BeautifulSoup(html,"html.parser")
    lists = soup.select("script")
    for li in lists:
        li.decompose()
    lists = soup.select("center")
    for li in lists:
        li.decompose()
    itm = soup.find(id="nr1")
    txt = itm.get_text()
    txt = txt.replace(u'\xa0', u' ')
    txt = txt.replace('            -->>', '')
    #txt = re.subn('')
    
    itm = soup.find(id="pb_next")
    s1 = itm.string
    s2 = u"下一页"
    if s1==s2:
        txt = txt + get_content(BOOK_WEB+itm.get("href"))
    return txt

arr = get_chapters(BOOK_IDX,BOOK_PAG)
txt = ""
for itm in arr:
    print( "%s - %s" % (itm['href'], itm['name']) )
    txt1 = get_content( BOOK_WEB + itm['href'] )
    print( txt1 )
    txt = txt + txt1

fo = codecs.open( BOOK_IDX + ".txt", "w", encoding='utf8' )
fo.write( txt )
fo.close()
