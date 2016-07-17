#!/usr/bin/python
# -*- coding:utf-8 -*-

import random, time

try:
    person = int(raw_input("你打算出什么呢?1.布 2.剪刀 3.石头\t\n你选择的是：".decode('utf-8').encode('gbk')))
except ValueError:
    print u'你需要在数字123中做出选择！', exit()
  
choice = {1:u'布', 2:u'剪刀', 3:u'石头'}
computer = random.randint(1, 3)
 
print u'你选择的是%s，电脑选择的是%s' %(choice[person], choice[computer])

if person == computer:
    print u'平局，真无趣！'
elif person - computer == 1:
    print u'哈哈，我赢了'
else:
    print u'你居然赢了，作弊吧'


