#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 19-01-14 17:06:28
import random
import pymysql
from app.config import DBMSGNAME, DBHISTORYTABLE, DBUSERTABLE, DBPWD

def initDataBase():
    try:
        db = pymysql.connect(host='localhost',user='root', password=DBPWD, port=3306)
        cursor = db.cursor()
        cursor.execute(
            "create database if not exists {} default character set UTF8MB4".format(DBMSGNAME))
        cursor.close()
        db.close()
        print("创建数据库{}成功".format(DBMSGNAME))
    except Exception as e:
        print(e)
        
def initHistoryTable():
    try:
        db = pymysql.connect(host='localhost',user='root', 
            password=DBPWD, db=DBMSGNAME, port=3306, charset='UTF8MB4')
        cursor = db.cursor()
        # 由于微信每次发送内容字数限制，所以2000个字符位置已经足够了
        tablename = DBHISTORYTABLE
        sql = 'create table if not exists {}(\
                id int(20) auto_increment,\
                openid varchar(30) default null,\
                name varchar(20) default null,\
                send varchar(2000) default null,\
                receive varchar(2000) default null,\
                time datetime default null,\
                primary key(id)\
            )engine=InnoDB default charset=UTF8MB4'.format(tablename)
        cursor.execute(sql)
        cursor.close()
        db.close()
        print("创建数据表{}成功".format(tablename))
    except Exception as e:
        print(e)


#sql = "SELECT * FROM chinese WHERE id >= ((SELECT MAX(id) FROM chinese)-(SELECT MIN(id) FROM chinese)) * RAND() + (SELECT MIN(id) FROM chinese) LIMIT {}".format(num)
def randomdata(dbname, pwd, tablename, maxID):
    db = pymysql.connect(host='localhost', user='root',
                         password=pwd, db=dbname,
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


def saveContent(records):
    db = pymysql.connect(host='localhost', user='root',
                         password=DBPWD, db=DBMSGNAME,
                         port=3306, charset='utf8')
    cursor = db.cursor()
    for record in records:
        sql = 'insert into {}(openid,name,send,receive,time) values ("{}","{}","{}","{}","{}")'.format(DBHISTORYTABLE,record['openid'],record['name'],record['send'],record['receive'],record['time'])
        print(sql)
        cursor.execute(sql)
    cursor.execute("commit")
    cursor.close()
    db.close()

def initUserTable():
    try:
        db = pymysql.connect(host='localhost',user='root',
            password=DBPWD, db=DBMSGNAME, port=3306, charset='UTF8MB4')
        cursor = db.cursor()
        # 由于微信每次发送内容字数限制，所以2000个字符位置已经足够了
        tablename = DBUSERTABLE
        sql = 'create table if not exists {}(\
                id int(20) auto_increment,\
                openid varchar(30) default null,\
                name varchar(20) default null,\
                time datetime default null,\
                primary key(id)\
            )engine=InnoDB default charset=UTF8MB4'.format(tablename)
        cursor.execute(sql)
        cursor.close()
        db.close()
        print("创建数据表{}成功".format(tablename))
    except Exception as e:
        print(e)


def saveUser(openid, time):
    db = pymysql.connect(host='localhost', user='root',
                         password=DBPWD, db=DBMSGNAME,
                         port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'insert into {}(openid,time) values ("{}","{}")'.format(DBUSERTABLE, openid, time)
    print(sql)
    cursor.execute(sql)
    cursor.execute("commit")
    cursor.close()
    db.close()

def hasRight(openid):
    db = pymysql.connect(host='localhost', user='root',
                         password=DBPWD, db=DBMSGNAME,
                         port=3306, charset='utf8')
    cursor = db.cursor()
    sql = 'select * from {} where openid = "{}"'.format(DBUSERTABLE, openid)
    print(sql)
    cursor.execute(sql)
    record = cursor.fetchone()
    print(record)
    cursor.close()
    db.close()
    return record

    
