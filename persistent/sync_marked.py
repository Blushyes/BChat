import persistent.mysql as mysql
import persistent.simple as simple
from config import log
from core.comments import Comment

# TODO 后续扩展多种策略得修改同步策略
def sync():
    log.debug('开始同步标记数据')
    simple_marked = simple.marked_set()
    log.debug(f'simple: {simple_marked}')
    mysql_marked = mysql.marked_set()
    log.debug(f'mysql: {mysql_marked}')
    mysql.mark([Comment(bid, cid) for bid, cid in simple_marked if (bid, cid) not in mysql_marked])
    simple.mark([Comment(bid, cid) for bid, cid in mysql_marked if (bid, cid) not in simple_marked])
    log.debug('标记数据同步完毕')
