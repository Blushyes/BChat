from context.config import DefaultConfig
from context.__init__ import context, log
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage


def get_xunfei_config(item: str):
    return context.config_manager.get_config(
        DefaultConfig.MODEL, DefaultConfig.Model.XUNFEI, item
    )


# 星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = "wss://spark-api.xf-yun.com/v3.5/chat"

# 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
appid = get_xunfei_config(DefaultConfig.Model.XunFei.APPID)
api_secret = get_xunfei_config(DefaultConfig.Model.XunFei.API_SECRET)
api_key = get_xunfei_config(DefaultConfig.Model.XunFei.API_KEY)

# 星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = "generalv3.5"

text = []

simple_preset = {
    (
        "你是",
        "你是谁",
        "你叫",
        "你的名字",
        "你叫",
        "你的身份",
        "你的原型",
        "你是基于",
        "你基于",
    ): "你好，我是Blushyes的自动回复机器人~"
}

preset = {
    "你是谁": "你好，我是Blushyes的自动回复机器人~",
    "你是基于什么模型的": "你猜~",
    "UP主是谁": "当然是Blushyes呀~",
}


class PresetFlag:
    T = "T"
    F = "F"


def ask(content: str):
    # 下面这句话如果和“你是谁”很相似，你就回答true，否则回答false
    # TODO 复杂预处理之前还需要一道简单查表预处理
    flag, answer = _pre_ask(content)
    return answer if flag == PresetFlag.T else _proxy_ask(content)


def direct_ask(content: str):
    return _proxy_ask(content)


def _simple_pre_ask(content):
    for keys, value in simple_preset.items():
        for key in keys:
            if key in content:
                return [{"content": value}]


def _pre_ask(content: str):
    """
    问题预处理，如果为预设问题则返回相应答案
    """
    # f'下面这句话如果和"{key}"很相似，你就回答{PresetFlag.T}，否则回答{PresetFlag.F}："{content}"'
    question = (
        f"下面这句话如果和给定python列表中的任意一个字符串很相似，你就回答{PresetFlag.T}，否则回答{PresetFlag.F}，并告诉我跟哪个相似\n"
        f'例如：当列表为["你的职业是什么","yes"]，我给出的句子为"你的工作是？"的时候，因为"你的工作是？"和列表中的"你的职业是什么"是相似的，所以你要输出"T|你的职业是什么"\n'
        f'现在，列表为：{[i for i in preset.keys()]}，我给你的句子是："{content}"'
    )
    print("question", question)
    response = _proxy_ask(question)
    # 防止出现空回复或者只回复了 T or F
    try:
        flag, key = response.split("|")
        # 要strip三次的原因是防止遇见这样的情况：'"hello"'，这样的话里面的双引号无法消除
        # key = key.strip('"').strip("'").strip('"')
        while key.startswith('"') or key.startswith("'"):
            key = key.strip(key[0])

        # TODO 如果有相似的，则存入简单表，之后直接查简单表就行
        if key in preset and flag == PresetFlag.T:
            return flag, preset[key]
        return flag, None
    except Exception:
        return response, question


def _ask(content):
    try:
        spark = ChatSparkLLM(
            spark_api_url=SPARKAI_URL,
            spark_app_id=appid,
            spark_api_key=api_key,
            spark_api_secret=api_secret,
            spark_llm_domain=SPARKAI_DOMAIN,
            streaming=False,
        )
        messages = [ChatMessage(role="user", content=content)]
        handler = ChunkPrintHandler()
        a = spark.generate([messages], callbacks=[handler])
        return a
    except Exception as e:
        log.error("访问讯飞出错了")
        log.error(str(e))
        return [{"content": f"这个回答在请求的时候发生了错误，错误信息为：\n{str(e)}"}]


def _proxy_ask(content) -> str:
    return _ask(content).generations[-1][-1].text


if __name__ == "__main__":
    print(ask("你是谁？"))
