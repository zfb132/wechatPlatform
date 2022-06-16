# wechatPlatform
微信公众号的开发
## 准备工作
本仓库的使用教程，参考[此文章](https://blog.whuzfb.cn/blog/2019/01/06/wechat_platform/ "网址")  
如果需要对接各国人名的数据库，那么首先下载人名数据并存入数据库，参考[此仓库](https://github.com/zfb132/ParseNames "网址")  
## 功能
下面是命令列表  

| 命令代号  | 功能 |  
:--:|:--:|  
|0|菜单|  
|1|随机返回5个中文名字|  
|2|随机返回五个日本名字|  
|3|随机返回五个英语名字|  
|4|随机返回五个成语|  
|5|成语接龙（待实现）|  
### 详细操作
1. 在shell窗口切换到本目录，输入 `python3 -m venv myvenv` 创建 Python3 虚拟环境，然后激活此环境并安装 `requirements.txt` 中的依赖库
2. 安装MySQL，创建 `names` 数据库
3. 修改文件 `config.example.py` 名字为 `config.py`，并修改其内容
4. 在当前目录下创建 `log` 空文件夹用以存放日志
## 手动运行
启动程序：在shell窗口输入 `uwsgi uwsgi_wechat.ini -d ./log/server.log`  
终止程序：在shell窗口输入 `kill -9 $(lsof -t -i:8111)`  
重启程序：shell窗口输入 `chmod +x restart.sh` 给文件 `restart.sh` 执行权限，然后输入 `./restart.sh` 来执行此脚本  
**初学者注意**：此时程序运行在服务器端的8111端口，若要联通微信的网站接口认证，还要配置 `nginx` 反向代理

## 添加自启动
修改`wechat-platform.service`文件的uwsgi路径和配置文件路径为本机的路径，修改用户为本机的用户名  
```conf
[Unit]
Description=Wechat Platform service
After=network.target

[Service]
Type=simple
User=ubuntu
Restart=on-failure
RestartSec=5s
WorkingDirectory=/home/ubuntu/wechatPlatform
ExecStart=/home/ubuntu/wechatPlatform/myvenv/bin/uwsgi --ini /home/ubuntu/wechatPlatform/uwsgi_wechat.ini

[Install]
WantedBy=multi-user.target
```
然后将此文件移动到系统服务目录：`sudo mv ./wechat-platform.service /etc/systemd/system/`  
启动开机自启功能：`systemctl enable wechat-platform`  
手动运行服务：`service wechat-platform start`  
则所有配置完成，插件已正常工作，若重新启动系统，则`wechat-platform`的service会启动

## 服务管理
重载服务后台（手动修改service文件后执行）：`sudo systemctl daemon-reload`  
关闭服务：`service wechat-platform stop`  
手动重启服务：`service wechat-platform restart`  
查看开机自启的服务：`systemctl list-unit-files --type=service|grep enabled`   
```txt
ubuntu@VM-16-13-ubuntu:~/$ systemctl status wechat-platform.service
● wechat-platform.service - Wechat Platform service
   Loaded: loaded (/etc/systemd/system/wechat-platform.service; enabled; vendor preset: enabled)
   Active: active (running) since Thu 2022-06-16 11:31:06 CST; 5s ago
 Main PID: 7224 (uwsgi)
    Tasks: 10 (limit: 570)
   CGroup: /system.slice/wechat-platform.service
           ├─7224 /home/ubuntu/wechatPlatform/myvenv/bin/uwsgi --ini /home/ubuntu/wechatPlatform/uwsgi_wechat.ini
           ├─7226 /home/ubuntu/wechatPlatform/myvenv/bin/uwsgi --ini /home/ubuntu/wechatPlatform/uwsgi_wechat.ini
           ├─7227 /home/ubuntu/wechatPlatform/myvenv/bin/uwsgi --ini /home/ubuntu/wechatPlatform/uwsgi_wechat.ini
           ├─7228 /home/ubuntu/wechatPlatform/myvenv/bin/uwsgi --ini /home/ubuntu/wechatPlatform/uwsgi_wechat.ini
           ├─7229 /home/ubuntu/wechatPlatform/myvenv/bin/uwsgi --ini /home/ubuntu/wechatPlatform/uwsgi_wechat.ini
           └─7233 /home/ubuntu/wechatPlatform/myvenv/bin/uwsgi --ini /home/ubuntu/wechatPlatform/uwsgi_wechat.ini

Jun 16 11:31:08 localhost.localdomain uwsgi[7224]: WSGI app 0 (mountpoint='') ready in 2 seconds on interpreter 0x558a4b
Jun 16 11:31:08 localhost.localdomain uwsgi[7224]: *** uWSGI is running in multiple interpreter mode ***
Jun 16 11:31:08 localhost.localdomain uwsgi[7224]: spawned uWSGI master process (pid: 7224)
Jun 16 11:31:08 localhost.localdomain uwsgi[7224]: spawned uWSGI worker 1 (pid: 7226, cores: 2)
Jun 16 11:31:08 localhost.localdomain uwsgi[7224]: spawned uWSGI worker 2 (pid: 7227, cores: 2)
Jun 16 11:31:08 localhost.localdomain uwsgi[7224]: spawned uWSGI worker 3 (pid: 7228, cores: 2)
Jun 16 11:31:08 localhost.localdomain uwsgi[7224]: spawned uWSGI worker 4 (pid: 7229, cores: 2)
Jun 16 11:31:08 localhost.localdomain uwsgi[7224]: spawned uWSGI http 1 (pid: 7233)
ubuntu@VM-16-13-ubuntu:~/$
```
