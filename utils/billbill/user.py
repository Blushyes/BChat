import asyncio

from bilibili_api.user import User


def is_fans(user: User, uid: int):
    return asyncio.run(user.get_relation(uid))['be_relation']['mid'] == uid
