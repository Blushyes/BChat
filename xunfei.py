import configparser
import logging

import SparkApi

XUNFEI = 'XUN_FEI'

config = configparser.ConfigParser()
config.read('api.ini')

appid = config.get(XUNFEI, 'appid')
api_secret = config.get(XUNFEI, 'api_secret')
api_key = config.get(XUNFEI, 'api_key')

# 用于配置大模型版本，默认“general/generalv2”
domain = "general"  # v1.5版本
# domain = "generalv2"    # v2.0版本
# 云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址

text = []
# length = 0

simple_preset = {
    ('你是', '你是谁', '你叫', '你的名字', '你叫', '你的身份', '你的原型', '你是基于',
     '你基于'): '你好，我是Blushyes的自动回复机器人~'
}

preset = {
    '你是谁': '你好，我是Blushyes的自动回复机器人~',
    '你是基于什么模型的': '你猜~',
    'UP主是谁': '当然是Blushyes呀~',
}


class PresetFlag:
    T = 'T'
    F = 'F'


def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


def ask(content: str):
    # 下面这句话如果和“你是谁”很相似，你就回答true，否则回答false
    # TODO 复杂预处理之前还需要一道简单查表预处理
    flag, answer = _pre_ask(content)
    return answer if flag == PresetFlag.T else _ask(content)


def _simple_pre_ask(content):
    for keys, value in simple_preset.items():
        for key in keys:
            if key in content:
                return [{'content': value}]


def _pre_ask(content: str):
    """
    问题预处理，如果为预设问题则返回相应答案
    """
    # f'下面这句话如果和"{key}"很相似，你就回答{PresetFlag.T}，否则回答{PresetFlag.F}："{content}"'
    question = f'下面这句话如果和给定python列表中的任意一个字符串很相似，你就回答{PresetFlag.T}，否则回答{PresetFlag.F}，并告诉我跟哪个相似\n' \
               f'例如：当列表为["你的职业是什么","yes"]，我给出的句子为"你的工作是？"的时候，因为"你的工作是？"和列表中的"你的职业是什么"是相似的，所以你要输出"T|你的职业是什么"\n' \
               f'现在，列表为：{[i for i in preset.keys()]}，我给你的句子是："{content}"'
    print('question', question)
    response = _proxy_ask(question)
    flag, key = response.split('|')
    # 要strip三次的原因是防止遇见这样的情况：'"hello"'，这样的话里面的双引号无法消除
    # key = key.strip('"').strip("'").strip('"')
    while key.startswith('"') or key.startswith("'"):
        key = key.strip(key[0])

    # TODO 如果有相似的，则存入简单表，之后直接查简单表就行
    if key in preset and flag == PresetFlag.T:
        return flag, preset[key]
    return flag, None


def _ask(content):
    try:
        print(api_key, api_secret, appid)
        text.clear()
        question = checklen(getText("user", content))
        SparkApi.answer = ""
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
        getText("assistant", SparkApi.answer)
        return text
    except Exception as e:
        logging.error('访问讯飞出错了')
        logging.error(str(e))
        return [{'content': f'这个回答在请求的时候发生了错误，错误信息为：\n{str(e)}'}]


def _proxy_ask(content) -> str:
    return _ask(content)[-1]['content']


print(ask("你是谁？"))