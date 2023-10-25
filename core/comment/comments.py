import httpx
from bilibili_api import comment, Credential, Api

import core.login as login
from config import log
from core.comment.comment import Comment, AtItem

GET_AT_URL = 'https://api.bilibili.com/x/msgfeed/at?build=0&mobi_app=web'


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
        try:
            c = await comment.get_comments(bv, comment.CommentResourceType.VIDEO, page)
        except httpx.ReadTimeout as time_out:
            log.error('获取B站评论时请求超时')
            log.error(time_out)
            continue
        except Exception as e:
            log.error('获取B站评论时发生错误')
            log.error(e)
            continue

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
    """
    根据bv号列表获取评论列表

    Args:
        bv_list: BV号列表

    Returns:

    """
    comment_list = []
    for bv in bv_list:
        comment_list.extend(await get_comments(bv))
    return comment_list


async def send_comment(credential: str, content: str, oid, replied: int | None):
    """
    发送评论

    Args:
        credential: 用户登录凭证
        content: 评论的内容
        oid: 资源 ID
        replied: 根评论 ID

    Returns:
        是否发送成功
    """
    # 获取大模型的回答内容
    # TODO 考虑抽象回答模块
    content = content.replace('\\n', '\r\n')
    log.info(content)

    # 分段，单条评论不能超过999字
    contents = tuple(content[i:i + 999] for i in range(0, len(content), 999))
    for answer in contents:
        # 出现过在大模型回复的过程中用户把评论给删了导致的接口返回报错而中断程序
        # 这里对该情况进行处理
        try:
            await comment.send_comment(oid=oid, text=answer, type_=comment.CommentResourceType.VIDEO,
                                       credential=login.get_session(credential), root=replied)
        except Exception as e:
            log.error(e)
            return False
    return True


async def get_at_list(credential: Credential) -> list[AtItem]:
    """
    获取@我的列表

    Args:
        credential: 凭证

    Returns:

    """
    res = await Api(url=GET_AT_URL, credential=credential, method='get').result
    log.debug(res)
    items = res['items']
    return [AtItem(
        item['id'],
        item['item']['uri'].split('/')[-1].strip(),
        item['item']['title'],
        item['item']['source_content'],
        item['user']['mid'],
        item['item']['source_id']
    ) for item in items]
