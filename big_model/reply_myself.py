import asyncio
import logging
import os
import random

import big_model.xunfei.base as xunfei
import persistent.base as persistent
from config import config, Profile
from core.comments import *
from core.video import get_all_videos
from persistent.simple import SIMPLE_MARKED_FILENAME

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
            if os.path.exists(SIMPLE_MARKED_FILENAME):
                marked = persistent.marked_set()
                log.debug(f'marked: {marked}')

            replied_list = []  # 已回复列表
            for cmt in comment_list:
                if (cmt.bv, cmt.id) in marked:
                    log.debug(f'评论 [{cmt.id}] 已回复')
                    continue
                if config.profile == Profile.PROD:  # 生产环境下，通过 Q 开头
                    if cmt.message.startswith('Q:') or cmt.message.startswith('Q：'):
                        if await reply(cmt):
                            replied_list.append(cmt)


                elif config.profile == Profile.DEV:  # 开发环境下，通过 T 开头
                    if cmt.message.startswith('T:') or cmt.message.startswith('T：'):
                        if await reply(cmt):
                            replied_list.append(cmt)

            # 批量标记已经回复的评论
            persistent.mark(replied_list)

            await asyncio.sleep(SLEEP_TIME + random.randint(0, 6))


async def reply(cmt, mark_switch=False):
    """
    回复某一个问题

    返回是否回复成功
    """
    log.info(f'问题：{cmt.message}')
    log.info('正在准备回复中......')
    if config.reply_switch and await send_comment(config.credential, xunfei.ask(cmt.message), cmt.bv, cmt.id):
        # 如果单回复标记开关打开才进行单回复标记
        if mark_switch:
            persistent.mark([cmt])
        log.info('已回复')
        return True
    else:
        log.warning('回复开关没有打开')
        return False
