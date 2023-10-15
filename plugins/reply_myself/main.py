from plugins.reply_myself.reply_myself import ReplyMyself


def start():
    UID = input('请输入您登录的B站UID，如果没有填写正确，无法正常运行哦：')
    reply_self = ReplyMyself(UID)
    reply_self.start_loop()
