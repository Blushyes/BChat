import json

from config import config

# 获取标记策略
mark_strategy = config.get_persistent_config('strategy')


def save_json(name, info):
    with open(name, 'w') as f:
        json.dump(info, f, ensure_ascii=False)


class MarkStrategy:
    SIMPLE = 'simple'
    MYSQL = 'mysql'


def get_mark_strategy(mark_strategy_type: str):
    if MarkStrategy.SIMPLE == mark_strategy_type:
        import persistent.simple as simple
        return simple.mark, simple.marked_set
    elif MarkStrategy.MYSQL == mark_strategy_type:
        import persistent.mysql as mysql
        return mysql.mark, mysql.marked_set
    else:
        raise Exception('不存在的标记策略')


mark, marked_set = get_mark_strategy(mark_strategy)
# print(marked_set())
