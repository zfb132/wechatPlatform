# wechatPlatform
微信公众号的开发
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
## 准备工作
本仓库的使用教程，参考[此文章](https://blog.whuzfb.cn/blog/2019/01/06/wechat_platform/ "网址")  
如果需要对接各国人名的数据库，那么首先下载人名数据并存入数据库，参考[此仓库](https://github.com/zfb132/ParseNames "网址")  
### 详细操作
1. 在shell窗口切换到本目录，输入 `python3 -m venv myvenv` 创建 Python3 虚拟环境，然后激活此环境并安装 `requirements.txt` 中的依赖库
2. 安装MySQL，创建 `names` 数据库
3. 修改文件 `config.example.py` 名字为 `config.py`，并修改其内容
4. 在当前目录下创建 `log` 空文件夹用以存放日志
## 运行
启动程序：在shell窗口输入 `uwsgi uwsgi_wechat.ini -d ./log/server.log`  
终止程序：在shell窗口输入 `kill -9 $(lsof -t -i:8111)`  
重启程序：shell窗口输入 `chmod +x restart.sh` 给文件 `restart.sh` 执行权限，然后输入 `./restart.sh` 来执行此脚本  
**初学者注意**：此时程序运行在服务器端的8111端口，若要联通微信的网站接口认证，还要配置 `nginx` 反向代理
