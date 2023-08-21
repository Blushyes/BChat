from core.login import login
from big_model.reply_myself import ReplyMyself
import os

# 根目录
top_path = os.path.dirname(__file__)

# 回复自己视频实例
# 1472871866
reply_self = ReplyMyself(1472871866)

def getpath(path):
    return f'{top_path}/{path}'

if __name__ == '__main__':
    login()
    reply_self.start_loop()
