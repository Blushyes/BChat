import SparkApi
import configparser

XUNFEI = 'XUN_FEI'

config = configparser.ConfigParser()
config.read('api.ini')

appid = config.get(XUNFEI, 'appid')
api_secret = config.get(XUNFEI, 'api_secret')
api_key = config.get(XUNFEI, 'api_key')

# 用于配置大模型版本，默认“general/generalv2”
domain = "general"   # v1.5版本
# domain = "generalv2"    # v2.0版本
# 云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址

text = []
# length = 0

preset = {
    ('你是', '你是谁', '你叫', '你的名字', '你叫', '你的身份', '你的原型', '你是基于', '你基于'): '你好，我是Blushyes的自动回复机器人~'
}


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
    for keys, value in preset.items():
        for key in keys:
            if key in content:
                return [{'content': value}]

    print(api_key, api_secret, appid)
    text.clear
    question = checklen(getText("user", content))
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    getText("assistant", SparkApi.answer)
    # ans = ''
    # print(str(text))
    return text

    # while(1):
    #     Input = input("\n" +"我:")
    #     question = checklen(getText("user",Input))
    #     SparkApi.answer =""
    #     print("星火:",end = "")
    #     SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    #     getText("assistant",SparkApi.answer)
    #     # print(str(text))


# ans = ask('写一个快速排序')
