#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import pymysql

reload(sys)
sys.setdefaultencoding('utf8')

class Account(object):
    def __init__(self, conn):
        self.conn = conn

    def check_ac(self, ac):
        cursor = self.conn.cursor()
        try:
            sql = "select * from account where id=%s" %ac
            cursor.execute(sql)
            print "check_ac:"+ sql
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception(u"账号%s不存在" % ac)
        finally:
            cursor.close()

    def check_enough_money(self, ac, money):
        cursor = self.conn.cursor()
        try:
            sql = "select * from account where id=%s and money>=%s" %(ac, money)
            cursor.execute(sql)
            print "check_enough_money:" + sql
            rs = cursor.fetchall()
            if len(rs) != 1:
                raise Exception(u"账号%s没有足够钱" % ac)
        finally:
            cursor.close()

    def reduce_money(self, money, ac_out):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money=money-%s where id=%s" %(money, ac_out)
            cursor.execute(sql)
            print "reduce_money:" + sql
            if cursor.rowcount != 1:
                raise Exception(u"账号%s减账失败" % ac_out)
        finally:
            cursor.close()

    def add_money(self, money, ac_in):
        cursor = self.conn.cursor()
        try:
            sql = "update account set money=money+%s where id=%s" %(money, ac_in)
            cursor.execute(sql)
            print "reduce_money:" + sql
            if cursor.rowcount != 1:
                raise Exception(u"账号%s增账失败" % ac_out)
        finally:
            cursor.close()

    def transfer(self, ac_out, ac_in, money):
        try:
            self.check_ac(ac_out)
            self.check_ac(ac_in)
            self.check_enough_money(ac_out, money)
            self.reduce_money(money, ac_out)
            self.add_money(money, ac_in)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e



if __name__ == "__main__":
    ac_out = sys.argv[1]
    ac_in = sys.argv[2]
    money = sys.argv[3]

    conn = pymysql.connect(
        **{'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': 'aabbcc2',
        'db': 'dftc_patrol',
        'charset': 'utf8',
        'cursorclass': pymysql.cursors.DictCursor}
    )

    acc = Account(conn)

    try:
        acc.transfer(ac_out, ac_in, money)
    except Exception as e:
        print u'出现问题' + str(e)
    finally:
        conn.close()