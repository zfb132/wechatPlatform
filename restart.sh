#! /bin/bash
PORT=8111
kill -9  $(lsof -t -i:8111) > /dev/null 2>&1
if [ $? -eq 0 ];then
    echo "Kill $PORT port successfully!"
else
    echo "Fail to kill $PORT port"
fi
NAME=~/wechatPlatform/log/server.log
uwsgi uwsgi_wechat.ini -d $NAME > /dev/null 2>&1
if [ $? -eq 0 ];then
    echo "Restart successfully!"
else
    echo "Fail to restart"
fi
