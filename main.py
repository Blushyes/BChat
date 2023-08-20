from login import login
from reply_myself import ReplyMyself

# 回复自己视频实例
# 1472871866
reply_self = ReplyMyself(1472871866)

if __name__ == '__main__':
    login()
    reply_self.start_loop()
