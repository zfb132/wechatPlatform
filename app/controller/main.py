#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 19-01-05 19:34:14
from app import app
from flask import request, redirect, url_for
import app.config as config
import logging

from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

from app.model.HandleWeChatMsg import handlemsg
from app.model.SQLHelper import initDataBase, initTable, saveContent

# 初始化
logging = logging.getLogger('runserver.main')
initDataBase(config.DBMSGNAME, config.DBPWD)
initTable(config.DBMSGNAME, 'msg', config.DBPWD)

# 存放临时的消息记录列表
records = []
MAXLEN = 10

# 微信消息接口
@app.route('/',methods=["POST","GET"])
def main():
    logging.debug('进入主页面')
    if(len(request.args)<2):
        return redirect(url_for('index'))
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
        result = handlemsg(request.data)
        xml = result[0]
        # 若只调用records的值则不需要这句话
        global records
        records.append(result[1])
        if(len(records)>=MAXLEN):
            saveContent(config.DBMSGNAME, config.DBPWD, 'msg', records)
            records = []
        return xml
    # 处理异常情况或忽略
    except Exception as e:
        print(repr(e))

@app.route('/index',methods=["GET"])
def index():
    logging.debug('GET访问')
    return redirect("https://blog.whuzfb.cn/blog/2019/01/06/wechat_platform/", code=301)

