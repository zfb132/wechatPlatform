#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 19-01-05 19:15:12
from app import app
from log import initLog

logging = initLog('wechat.log','runserver')

if __name__ == '__main__':
    app.run(debug=True,port=8111)

application = app
