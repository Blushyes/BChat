import asyncio
import logging

from login import login
from reply_myself import ReplyMyself

# 配置日志输出格式和级别
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO)

# 回复自己视频实例
reply_self = ReplyMyself()

if __name__ == '__main__':
    login()
    reply_self.start_loop()
