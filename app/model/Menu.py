#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 19-01-13 17:31:57
import pymysql
import random
from app.config import DBNAME, DBPWD

# 命令列表
# 0  未知命令
# 1  随机返回5个中文名字
# 2  随机返回五个日本名字
# 3  随机返回五个英语名字
# 4  随机返回五个成语
# 5  成语接龙
def getcommand(content):
    if '名字' in content:
        if '中国' in content or "中文" in content:
            return 1
        elif '日本' in content:
            return 2
        elif '英国' in content or '美国' in content or '英语' in content or "英文" in content:
            return 3
        else:
            return 1
    else:
        if '成语' in content:
            return 4
        else:
            return 0

def parsecontent(content):
    command = getcommand(content)
    if command == 0:
        txt = defaultReply()
    elif command == 1:
        txt = randomdata('chinese',1896600)
    elif command == 2:
        txt = randomdata('japanese',185500)
    elif command == 3:
        txt = randomdata('english',29710)
    elif command == 4:
        txt = randomdata('idiom',50370)
    elif command == 5:
        txt = defaultReply()
    return txt


#sql = "SELECT * FROM chinese WHERE id >= ((SELECT MAX(id) FROM chinese)-(SELECT MIN(id) FROM chinese)) * RAND() + (SELECT MIN(id) FROM chinese) LIMIT {}".format(num)
def randomdata(tablename,maxID):
    db = pymysql.connect(host='localhost', user='root',
                         password=DBPWD, db=DBNAME,
                         port=3306, charset='utf8')
    cursor = db.cursor()
    num = 5
    result = []
    for i in range(num):
        offset = random.randint(1, maxID)
        sql = 'select content from {} where id>={} limit 1;'.format(tablename,offset)
        cursor.execute(sql)
        record = list(cursor.fetchone())[0]
        result.append(record)
    cursor.close()
    db.close()
    return ', '.join(result)

def errorReply(content):
    return '你发送了 :{}'.format(content)

def defaultReply():
    return "hhh"

