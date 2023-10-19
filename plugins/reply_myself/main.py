from config import config
from plugins.reply_myself.reply_myself import ReplyMyself


def start():
    parser = config.get_parser()
    if not parser.has_section('reply_myself'):
        raise Exception('缺少config.ini中的reply_myself配置项')
    uid = int(parser.get('reply_myself', 'uid'))
    reply_self = ReplyMyself(uid)
    reply_self.start_loop()
