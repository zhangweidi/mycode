# -*- coding:utf-8 -*-
import urllib2, urllib


# 设置代理
enable_proxy = True
proxy_handler = urllib2.ProxyHandler({"http": 'http://some-proxy.com:8000'})
null_proxy_handler = urllib2.ProxyHandler({})
if enable_proxy:
    opener = urllib2.build_opener(proxy_handler)
else:
    opener = urllib2.build_opener(null_proxy_handler)
urllib2.install_opener(opener)


value = {'username': '664345@qq.com', 'password': 123456}
data = urllib.urlencode(value)
url = "http://www.baidu.com"
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',    #设置headers，如果没有User-Agent表明代理身份，服务器可能不响应
          'Referer': 'http://www.zhihu.com/articles'}       #Referer表明从哪儿引入过来，加入Referer反盗链
request = urllib2.Request(url, data, headers)
response = urllib2.urlopen(request)
print response.read()