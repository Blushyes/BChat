from login import login, get_session
from bilibili_api import user
from config import config
import persistent


class Video:
    async def get_all_videos(self, uid=1472871866, persistent_response=False):
        '''
        获取某个用户所有的视频的BV号
        '''
        if (not config.credential):
            config.credential = login()
        myself = user.User(uid, get_session(
            config.credential))

        # 原始的 response
        response = await myself.get_videos()

        # 获取所有视频的BV号
        videos = []
        for video in response['list']['vlist']:
            videos.append(video['bvid'])
        print(videos)

        # 持久化 response
        if (persistent_response):
            try:
                persistent.save_json(f'videos-{uid}.json', response)
            except Exception:
                print('保存video时发生了异常')

        return videos
