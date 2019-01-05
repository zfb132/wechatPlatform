#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 19-01-05 19:34:14
from app import app
from flask import request
import app.config as config
import logging

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply
from wechatpy.replies import ImageReply

logging = logging.getLogger('runserver.main')

def handlemsg(data):
    msg = parse_message(data)
    print(msg)
    logging.debug('handle msg:'.format(msg))
    xml = txtreply(msg,config.DEFAULTMSG + msg.content)
    return xml

# 微信消息接口
@app.route('/',methods=["POST","GET"])
def main():
    logging.debug('进入主页面')
    try:
        signature = request.args.get("signature", "")
        timestamp = request.args.get("timestamp", "")
        nonce = request.args.get("nonce", "")
        echostr = request.args.get("echostr", "")
        # echostr是微信用来验证服务器的参数，需原样返回
        if echostr:
            try:
                logging.debug('正在验证服务器签名')
                check_signature(config.token, signature, timestamp, nonce)
                logging.debug('验证签名成功')
                return echostr
            except InvalidSignatureException as e:
                logging.error('检查签名出错: '.format(e))
                return 'Check Error'
        # 也可以通过POST与GET来区别
        # 不是在进行服务器验证，而是正常提交用户数据
        logging.debug('开始处理用户消息')
        xml = handlemsg(request.data)
        return xml
    # 处理异常情况或忽略
    except Exception as e:
        logging.error('获取参数失败: '.format(e))

def imgreply(msg,id):
    reply = ImageReply(message=msg)
    reply.media_id = id
    xml = reply.render()
    return xml

def txtreply(msg,txt):
    reply = TextReply(content=txt, message=msg)
    xml = reply.render()
    return xml
