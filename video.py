from bilibili_api import user

import persistent
from config import config, log
from login import login, get_session


async def get_all_videos(uid=1472871866, persistent_response=False):
    """
    获取某个用户所有的视频的BV号
    """
    if not config.credential:
        config.credential = login()
    myself = user.User(uid, get_session(
        config.credential))

    # 原始的 response
    response = await myself.get_videos()

    # 获取所有视频的BV号
    videos = []
    for video in response['list']['vlist']:
        videos.append(video['bvid'])
    log.info(videos)

    # 持久化 response
    if persistent_response:
        try:
            persistent.save_json(f'videos-{uid}.json', response)
        except Exception:
            log.error('保存video时发生了异常')

    return videos
