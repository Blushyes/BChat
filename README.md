# BChat

b站回复小助手。

### 如何部署？

#### Linux

1. 安装`git`
2. 克隆项目到本地
   ```shell
   cd /home
   git clone https://github.com/Blushyes/BChat.git
   cd ./BChat
   ```
3. 把`config.ini.example`重命名`config.ini`并填写好对应的`APPID`、`API_KEY`、`API_SECRET`
   ```shell
   mv config.ini.example config.ini
   ```
   ```shell
   vim config.ini
   ```
   ```ini
   [global]
   ; 回复功能开关，ON为开启，需要打开才能自动回复
   reply_switch = ON
   
   ; 讯飞大模型的APPID、API_SECRET、API_KEY，需要去讯飞开放平台注册并获取
   [model.xunfei]
   appid = 你的APPID
   api_secret = 你的API_SECRET
   api_key = 你的API_KEY
   
   [persistent]
   ; 已回复评论标记的持久化方式
   ; simple：简单标记模式，即在根目录创建一个markedfile文件
   ; mysql：连接mysql进行标记
   ; delegate：委托标记策略，委托其他服务进行标记
   strategy = simple   
   ```
4. 安装`docker`
5. 在项目根目录运行如下指令
    ```shell
    chmod +x ./build.sh
    ./build.sh
    ```
6. 现在程序已经运行了，在`BChat/tmp`文件夹内找到`qrcode.png`文件打开并扫码即可登录成功

#### Windows

1. 直接去`GitHub`下载项目解压到本地
2. 把`config.ini.example`重命名`config.ini`并填写好对应的`APPID`、`API_KEY`、`API_SECRET`
   ```ini
   [global]
   ; 回复功能开关，ON为开启，需要打开才能自动回复
   reply_switch = ON
   
   ; 讯飞大模型的APPID、API_SECRET、API_KEY，需要去讯飞开放平台注册并获取
   [model.xunfei]
   appid = 你的APPID
   api_secret = 你的API_SECRET
   api_key = 你的API_KEY
   
   [persistent]
   ; 已回复评论标记的持久化方式
   ; simple：简单标记模式，即在根目录创建一个markedfile文件
   ; mysql：连接mysql进行标记
   ; delegate：委托标记策略，委托其他服务进行标记
   strategy = simple   
   ```
3. 安装`Python`环境
4. 在项目根目录打开`cmd`运行如下命令：
   ```shell
   pip install -r requirements.txt # 安装程序所需的库
   ```
5. 直接打开`main.py`文件即可运行扫码登录