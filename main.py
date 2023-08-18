from reply_myself import ReplyMyself
from login import login
from config import config
import asyncio

reply_self = ReplyMyself()

if __name__ == '__main__':
    login()
    asyncio.run(reply_self.start_loop())
