#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 19-01-13 17:31:57
import pymysql
from app.config import DBNAME, DBPWD
from app.model.SQLHelper import randomdata

# 命令列表
# 0  菜单
# 1  随机返回5个中文名字
# 2  随机返回五个日本名字
# 3  随机返回五个英语名字
# 4  随机返回五个成语
# 5  成语接龙
def getcommand(content):
    # 如果是单个数字直接解析命令
    if len(content)==1 and content.isdigit():
        return int(content)
    if '名字' in content:
        if '中国' in content or "中文" in content:
            return 1
        elif '日本' in content or '日语' in content:
            return 2
        elif '英国' in content or '美国' in content or '英语' in content or "英文" in content:
            return 3
        else:
            return 1
    else:
        if '成语' in content:
            if '接龙' in content:
                return 5
            else:
                return 4
        else:
            if '命令' in content or '菜单' in content:
                return 0
            else:
                return 9

def parsecontent(content):
    command = getcommand(content)
    if command == 0:
        txt = menuReply()
    elif command == 1:
        txt = randomdata(DBNAME,DBPWD,'chinese',1896600)
    elif command == 2:
        txt = randomdata(DBNAME,DBPWD,'japanese',185500)
    elif command == 3:
        txt = randomdata(DBNAME,DBPWD,'english',29710)
    elif command == 4:
        txt = randomdata(DBNAME,DBPWD,'idiom',50370)
    elif command == 5:
        txt = tempReply(content)
    else:
        txt = defaultReply(content)
    return txt


def menuReply():
    txt = '命令列表\n0  菜单\n1  随机返回5个中文名字\n2  随机返回五个日本名字\n3  随机返回五个英语名字\n4  随机返回五个成语\n5  成语接龙(未实现)'
    return txt

def tempReply(content):
    return '你发送了 :{}'.format(content)

# 伪对话AI
def defaultReply(content):
    return content.replace('你', '我').replace('吗', '呀').replace('?', '!')

