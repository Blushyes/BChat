from context.main import context, log
from plugins.reply_myself.reply_myself import ReplyMyself


def start():
    if not context.config_manager.exists("global", "reply_myself_switch"):
        log.error("缺少config.ini中的reply_myself_switch配置项")
        return

    if context.config_manager.get_config("global", "reply_myself_switch") != "ON":
        log.info("回复评论区功能未开启")
        return
    reply_self = ReplyMyself(context.uid)
    reply_self.start_loop()
