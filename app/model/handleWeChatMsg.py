import logging
from wechatpy import parse_message
from wechatpy.replies import TextReply
from wechatpy.replies import ImageReply
from wechatpy import WeChatClient
from app.config import APPID,APPSECRET

logging = logging.getLogger('runserver.handleWeChatMsg')

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
    txt = '你发送了 :{}'.format(msg.content)
    xml = txtreply(msg, txt)
    #activeSend(msg)
    return xml

def activeSend(msg):
    client = WeChatClient(APPID, APPSECRET)
    logging.debug(client.access_token)
    #res = client.message.send_text(id,content)
    return 

def txtreply(msg,txt):
    reply = TextReply(content=txt, message=msg)
    xml = reply.render()
    return xml

def imgreply(msg,id):
    reply = ImageReply(message=msg)
    reply.media_id = id
    xml = reply.render()
    return xml
