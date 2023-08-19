import asyncio
import os
import random

import xunfei
from comments import *
from config import config
from video import Video

MARKED_FILENAME = 'markedfile'
SPLIT = '-'
SLEEP_TIME = 10


class ReplyMyself(object):
    def __init__(self) -> None:
        self._video = Video()

    def start_loop(self):
        """
        异步开启回复自己视频评论的循环
        """
        asyncio.run(self.__reply_loop())

    async def __reply_loop(self):
        while True:
            my_video_list = await self._video.get_all_videos()

            comment_list = await get_comments_list(my_video_list)
            marked = set()
            if os.path.exists(MARKED_FILENAME):
                marked = marked_set()

            for cmt in comment_list:
                if (cmt.bv, cmt.id) in marked:
                    logging.info(f'评论 [{cmt.id}] 已回复')
                    continue

                # int(cmt.uid) == 1472871866
                if cmt.message.startswith('Q:') or cmt.message.startswith('Q：'):
                    logging.info(f'问题：{cmt.message}')
                    logging.info('正在准备回复中......')
                    # TODO 考虑用数据库mark
                    mark(cmt)
                    await send_comment(config.credential, xunfei.ask(cmt.message), cmt.bv, cmt.id)

            await asyncio.sleep(SLEEP_TIME + random.randint(0, 6))


def mark(comment: Comment):
    with open(MARKED_FILENAME, 'a') as f:
        f.write(f'{comment.bv}{SPLIT}{comment.id}\n')


def marked_set():
    marked = set()
    with open(MARKED_FILENAME, 'r') as f:
        for line in f:
            line = line.strip()
            # logging.info('line', line)
            marked_bv, marked_id = line.split(SPLIT)
            marked.add((marked_bv, int(marked_id)))

    return marked
