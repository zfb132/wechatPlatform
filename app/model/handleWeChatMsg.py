import logging
from wechatpy import parse_message
from wechatpy.replies import TextReply
from wechatpy.replies import ImageReply
from wechatpy import WeChatClient

logging = logging.getLogger('runserver.handleWeChatMsg')

# 未认证的个人号不支持创建自定义菜单
def handlemsg(data):
    msg = parse_message(data)
    print(msg)
    logging.debug('handle msg:'.format(msg))
    xml = txtreply(msg,'返回 :{}'.format(msg.content))
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
