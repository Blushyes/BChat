from video import Video
from config import config
from comments import *
import asyncio
import xunfei
import random
import os

MARKED_FILENAME = 'markedfile'
SPLIT = '-'
SLEEP_TIME = 10


class ReplyMyself(object):
    def __init__(self) -> None:
        self._video = Video()

    async def start_loop(self):
        await self.__reply_loop()

    async def __reply_loop(self):
        while True:
            my_video_list = await self._video.get_all_videos()

            comment_list = await get_comments_list(my_video_list)
            marked = set()
            if os.path.exists(MARKED_FILENAME):
                marked = marked_set()

            for cmt in comment_list:
                print(cmt)

            for cmt in comment_list:
                if (cmt.bv, cmt.id) in marked:
                    print(f'评论 [{cmt.id}] 已回复')
                    continue
                
                # int(cmt.uid) == 1472871866
                if cmt.message.startswith('Q:') or cmt.message.startswith('Q：'):
                    print('正在准备回复中......')
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
            print('line', line)
            bv, id = line.split(SPLIT)
            marked.add((bv, int(id)))

    return marked