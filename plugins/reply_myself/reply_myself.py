import asyncio
import os
import random

import big_model.xunfei.base as xunfei
import persistent.base as persistent
from config import config, Profile
from core.comment.comments import *
from core.video import get_all_videos
# from persistent import delegate
from persistent.simple import SIMPLE_MARKED_FILENAME

SLEEP_TIME = 10


class ReplyMyself:
    """
    回复自己视频的评论
    """

    def __init__(self, uid):
        self._UID = uid

    def start_loop(self):
        """
        异步开启回复自己视频评论的循环
        """
        return asyncio.run(self._reply_loop())

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
                        cmt.message.replace('Q:', '')
                        cmt.message.replace('Q：', '')
                        if await reply(cmt):
                            replied_list.append(cmt)


                elif config.profile == Profile.DEV:  # 开发环境下，通过 T 开头
                    if cmt.message.startswith('T:') or cmt.message.startswith('T：'):
                        cmt.message.replace('T:', '')
                        cmt.message.replace('T：', '')
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
    if config.reply_switch:
        answer = xunfei.ask(cmt.message)
        if await send_comment(config.credential, answer, cmt.bv, cmt.id):
            # 如果单回复标记开关打开才进行单回复标记
            if mark_switch:
                persistent.mark([cmt])

            # 如果采用委托策略，则发送已回复的数据
            # if persistent.MarkStrategy.DELEGATE == config.get_persistent_config('strategy'):
            #     full_dict = cmt.to_full_dict()
            #     full_dict['answer'] = answer
            #     delegate.send('commented', full_dict)
            log.info('已回复')
            return True
        else:
            log.warn('发送回复评论失败')
            return False
    else:
        log.warning('回复开关没有打开')
        return False
