from bilibili_api import comment

import login
import logging


class Comment(object):
    """
    评论封装类

    bv：视频的BV号
    cid：评论的id
    uid：用户的id
    uname：用户名
    message：评论的内容
    """
    def __init__(self, bv, cid, uid, uname, message):
        self.bv = bv
        self.id = cid
        self.uid = uid
        self.uname = uname
        self.message = message

    def __str__(self) -> str:
        return f'[ {self.bv} -- {self.id} -- {self.uid} -- {self.uname}: {self.message} ]'


async def get_comments(bv):
    """
    获取某个视频下的评论，封装为一个Comment对象
    """
    # 存储评论
    comments = []
    # 页码
    page = 1
    # 当前已获取数量
    count = 0
    while True:
        # 获取评论
        c = await comment.get_comments(bv, comment.CommentResourceType.VIDEO, page)
        # 存储评论
        if c['replies']:
            comments.extend(c['replies'])

        # 增加已获取数量
        count += c['page']['size']
        # 增加页码
        page += 1

        if count >= c['page']['count']:
            # 当前已获取数量已达到评论总数，跳出循环
            break

    # 打印评论
    # for cmt in comments:
    #     logging.info(f"{cmt['member']['uname']}: {cmt['content']['message']}")

    # 打印评论总数
    # logging.info(f"\n\n共有 {count} 条评论（不含子评论）")

    return [Comment(bv, cmt['rpid'], cmt['member']['mid'], cmt['member']['uname'], cmt['content']['message']) for cmt in
            comments]


async def get_comments_list(bv_list) -> list[Comment]:
    comment_list = []
    for bv in bv_list:
        comment_list.extend(await get_comments(bv))
    return comment_list


async def send_comment(credential, content, oid, replied):
    """
    发送评论

    oid: BV号
    replied: 父评论的id
    """
    # 获取大模型的回答内容
    # TODO 考虑抽象回答模块
    content = str(content[-1]['content'])
    content = content.replace('\\n', '\r\n')
    logging.info(content)

    # 分段，单条评论不能超过999字
    contents = tuple(content[i:i + 999] for i in range(0, len(content), 999))
    for answer in contents:
        await comment.send_comment(oid=oid, text=answer, type_=comment.CommentResourceType.VIDEO,
                                   credential=login.get_session(credential), root=replied)
