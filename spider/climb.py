#!/usr/bin/env python
# -*- coding:utf-8 -*-
import urllib
import re, os

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getImg(html):
    reg = r'src="(.+?\.jpg)"' 
    imgre = re.compile(reg)
    imglist = re.findall(imgre, html)
    if not imglist:
        print u'没找到任何图片...'
    else:
        # filepath = os.getcwd()+'\image'
        # if os.path.exists(filepath) is False:
            # os.mkdir(filepath)
        i = 1
        while True:
            filepath = os.getcwd()+'\image%d' %i
            if os.path.exists(filepath) is False:
                os.mkdir(filepath)
                break
            i += 1
        x = 1
        for imgurl in imglist:
            temp = filepath + '\%s.jpg' % x
            urllib.urlretrieve(imgurl, temp)
            print u'下载完成第%s张图片'%x
            x+=1
            

html = getHtml("http://tieba.baidu.com/p/3302953104")

getImg(html)
#开始抓图啦~
