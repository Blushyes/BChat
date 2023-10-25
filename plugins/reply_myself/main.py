from config import config, log
from plugins.reply_myself.reply_myself import ReplyMyself


def start():
    parser = config.get_parser()
    if not parser.has_option('global', 'reply_myself_switch'):
        log.error('缺少config.ini中的reply_myself_switch配置项')
        return

    if parser.get('global', 'reply_myself_switch') != 'ON':
        log.info('回复评论区功能未开启')
        return
    reply_self = ReplyMyself(config.uid)
    reply_self.start_loop()
