import asyncio
import os
import random

import xunfei
from comments import *
from config import config, Profile
from video import get_all_videos

MARKED_FILENAME = 'markedfile'
SPLIT = '-'
SLEEP_TIME = 10


class ReplyMyself:
    """
    回复自己视频的评论
    """
    _UID = None

    def __init__(self, uid):
        self._UID = uid

    def start_loop(self):
        """
        异步开启回复自己视频评论的循环
        """
        asyncio.run(self._reply_loop())

    async def _reply_loop(self):
        while True:
            my_video_list = await get_all_videos(uid=self._UID)

            comment_list = await get_comments_list(my_video_list)
            marked = set()
            if os.path.exists(MARKED_FILENAME):
                marked = marked_set()

            for cmt in comment_list:
                if (cmt.bv, cmt.id) in marked:
                    log.debug(f'评论 [{cmt.id}] 已回复')
                    continue
                if config.profile == Profile.PROD:  # 生产环境下，通过 Q 开头
                    if cmt.message.startswith('Q:') or cmt.message.startswith('Q：'):
                        await reply(cmt)
                elif config.profile == Profile.DEV:  # 开发环境下，通过 T 开头
                    if cmt.message.startswith('T:') or cmt.message.startswith('T：'):
                        await reply(cmt)

            await asyncio.sleep(SLEEP_TIME + random.randint(0, 6))


async def reply(cmt):
    log.info(f'问题：{cmt.message}')
    log.info('正在准备回复中......')
    # TODO 考虑用数据库mark
    mark(cmt)
    await send_comment(config.credential, xunfei.ask(cmt.message), cmt.bv, cmt.id)


def mark(cmt: Comment):
    with open(MARKED_FILENAME, 'a') as f:
        f.write(f'{cmt.bv}{SPLIT}{cmt.id}\n')


def marked_set():
    marked = set()
    with open(MARKED_FILENAME, 'r') as f:
        for line in f:
            line = line.strip()
            # log.info('line', line)
            marked_bv, marked_id = line.split(SPLIT)
            marked.add((marked_bv, int(marked_id)))

    return marked
