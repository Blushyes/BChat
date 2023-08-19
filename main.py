import asyncio
import logging

from config import config, Profile
from login import login
from reply_myself import ReplyMyself

# 配置日志输出格式和级别
log_level = logging.DEBUG if config.profile == Profile.DEV else logging.INFO
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=log_level)

# 回复自己视频实例
# 1472871866
reply_self = ReplyMyself(1472871866)

if __name__ == '__main__':
    login()
    reply_self.start_loop()
