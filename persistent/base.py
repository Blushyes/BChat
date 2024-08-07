import json

from context.config import DefaultConfig
from context.__init__ import context
from . import sync_marked

# 获取标记策略
mark_strategy = context.config_manager.get_config(
    DefaultConfig.PERSISTENT,
    DefaultConfig.Persistent.STRATEGY
)


def save_json(name, info):
    with open(name, 'w') as f:
        json.dump(info, f, ensure_ascii=False)


class MarkStrategy:
    SIMPLE = 'simple'
    MYSQL = 'mysql'
    DELEGATE = 'delegate'


def get_mark_strategy(mark_strategy_type: str):
    if MarkStrategy.SIMPLE == mark_strategy_type:
        import persistent.simple as simple
        return simple.mark, simple.marked_set
    elif MarkStrategy.MYSQL == mark_strategy_type:
        import persistent.mysql as mysql
        return mysql.mark, mysql.marked_set
    elif MarkStrategy.DELEGATE == mark_strategy_type:
        import persistent.delegate as delegate
        return delegate.mark, delegate.marked_set
    else:
        raise Exception('不存在的标记策略')


mark, marked_set = get_mark_strategy(mark_strategy)
sync_marked.sync()
# print(marked_set())
