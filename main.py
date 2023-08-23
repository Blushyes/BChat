from big_model.reply_myself import ReplyMyself
from core.login import login

# 回复自己视频实例
# 1472871866
reply_self = ReplyMyself(1472871866)

if __name__ == '__main__':
    # login()
    # reply_self.start_loop()
    import listener.reply_myself_creator as reply
    reply.listen_qrcode_login()
