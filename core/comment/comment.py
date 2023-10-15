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