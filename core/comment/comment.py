from dataclasses import dataclass


class Comment(object):
    """
    评论封装类

    bv：视频的BV号
    cid：评论的id
    uid：用户的id
    uname：用户名
    message：评论的内容
    """

    def __init__(self, bv: str, cid: int, uid: int = None, uname: str = None, message: str = None):
        self.bv = bv
        self.id = cid
        self.uid = uid
        self.uname = uname
        self.message = message

    def __str__(self) -> str:
        return f'[ {self.bv} -- {self.id} -- {self.uid} -- {self.uname}: {self.message} ]'

    def to_simple_dict(self):
        return {
            'bid': self.bv,
            'cid': self.id
        }

    def to_full_dict(self):
        return {
            'bid': self.bv,
            'cid': self.id,
            'uid': self.uid,
            'uname': self.uname,
            'message': self.message,
        }


@dataclass
class AtItem:
    """
    Args:
        id: @的唯一ID
        video_title: 被@的视频的标题
        content: @的完整内容
        mid: @我的那个人的UID
        source_id: 资源的ID，比如说评论

    """
    id: int
    bid: str
    video_title: str
    content: str
    mid: int
    source_id: int
