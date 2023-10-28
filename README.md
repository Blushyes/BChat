# BChat

B站回复小助手，接入大模型自动回复。

主要特性有：

- [x] 自动回复评论区
- [x] 支持自定义插件
- [x] 自动分析被@的视频

欢迎加入一起开发，或者分享你的建议和想法。

### 遇到问题？

请提[issue](https://github.com/Blushyes/BChat/issues)或者去[B站](https://www.bilibili.com/video/BV1Y14y1i7Nn)留言。

### 如何部署？

#### Linux

1. 安装`git`
2. 克隆项目到本地

   ```shell
   cd /home
   git clone https://github.com/Blushyes/BChat.git
   cd ./BChat
   ```

3. 把`config.example.json`重命名`config.json`并填写好对应的`APPID`、`API_KEY`、`API_SECRET`

   ```shell
   mv config.example.json config.json
   vim config.json
   ```
   ```json
   {
     "global": {
       "reply_myself_switch": "ON",
       "uid": 1472871866
     },
     "model": {
       "xunfei": {
         "appid": "你的讯飞星火大模型的APPID",
         "api_secret": "你的讯飞星火大模型的API_SECRET",
         "api_key": "你的讯飞星火大模型的API_KEY"
       }
     },
     "persistent": {
       "strategy": "simple"
     }
   }
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
2. 把`config.example.json`重命名`config.json`并填写好对应的`APPID`、`API_KEY`、`API_SECRET`

   ```json
   {
     "global": {
       "reply_myself_switch": "ON",
       "uid": 1472871866
     },
     "model": {
       "xunfei": {
         "appid": "你的讯飞星火大模型的APPID",
         "api_secret": "你的讯飞星火大模型的API_SECRET",
         "api_key": "你的讯飞星火大模型的API_KEY"
       }
     },
     "persistent": {
       "strategy": "simple"
     }
   }
   ```

3. 安装`Python`环境
4. 在项目根目录打开`cmd`运行如下命令：

   ```shell
   pip install -r requirements.txt # 安装程序所需的库
   ```

5. 直接打开`main.py`文件即可运行扫码登录