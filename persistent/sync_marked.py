import persistent.simple as simple
from context.__init__ import context, log
from core.comment.__init__ import Comment


# TODO 如果没有那个回复策略的配置，则不需要同步那个策略
def sync():
    log.debug('开始同步标记数据')

    sync_list = [
        [simple.marked_set, simple.mark]
        # [mysql.marked_set, mysql.mark]
        # [delegate.marked_set, delegate.mark]
    ]
    if context.config_manager.exists('mysql'):
        import persistent.mysql as mysql
        sync_list.append([mysql.marked_set, mysql.mark])
    for i in range(len(sync_list)):
        for j in range(len(sync_list)):
            if i == j: continue
            syncer = sync_list[i]
            reference = sync_list[j]
            syncer_marked_set = syncer[0]()
            reference_marked_set = reference[0]()
            log.warning(f'{reference_marked_set} ---> {syncer_marked_set}')
            syncer[1]([Comment(bid, cid) for bid, cid in reference_marked_set if (bid, cid) not in syncer_marked_set])

    log.debug('标记数据同步完毕')
