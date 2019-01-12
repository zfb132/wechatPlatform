import logging
import random
import pymysql
from wechatpy import parse_message
from wechatpy.replies import TextReply
from wechatpy.replies import ImageReply
from wechatpy import WeChatClient
from app.config import APPID,APPSECRET,DBNAME,DBPWD

logging = logging.getLogger('runserver.handleWeChatMsg')
db = pymysql.connect(host='localhost', user='root',
                         password=DBPWD, db=DBNAME,
                         port=3306, charset='utf8')


#sql = "SELECT * FROM chinese WHERE id >= ((SELECT MAX(id) FROM chinese)-(SELECT MIN(id) FROM chinese)) * RAND() + (SELECT MIN(id) FROM chinese) LIMIT {}".format(num)
def randomdata(tablename,maxID):
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
    return ', '.join(result)


# 未认证的订阅号 
# https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433401084
# Message 类的成员变量
# id          消息 id, 64 位整型
# source      消息的来源用户，即发送消息的用户
# target      消息的目标用户
# create_time 消息的发送时间，UNIX 时间戳
# type        消息的类型
def handlemsg(data):
    msg = parse_message(data)
    #print(msg)
    logging.debug('id为{}的用户发送消息:{}'.format(msg.source,msg.content))
    #txt = '你发送了 :{}'.format(msg.content)
    content = msg.content
    if '名字' in content:
        if '中国' in content:
            txt = randomdata('chinese',1896600)
        elif '日本' in content:
            txt = randomdata('japanese',185500)
        elif '英国' in content:
            txt = randomdata('english',29710)
        elif '美国' in content:
            txt = randomdata('english',29710)
        else:
            txt = randomdata('chinese',1896600)
    else:
        if '成语' in content:
            txt = randomdata('idiom',50370)
        else:
            txt = '你发送了 :{}'.format(content)
    xml = txtreply(msg, txt)
    #activeSend(msg)
    return xml

def txtreply(msg,txt):
    reply = TextReply(content=txt, message=msg)
    xml = reply.render()
    return xml

def imgreply(msg,id):
    reply = ImageReply(message=msg)
    reply.media_id = id
    xml = reply.render()
    return xml
