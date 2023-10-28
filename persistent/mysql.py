# 连接MySQL
import pymysql.cursors

from context.config import DefaultConfig
from context.main import context
from core.comment.comment import Comment


def get_mysql_config(item: str):
    return context.config_manager.get_config(DefaultConfig.MYSQL, item)


host = get_mysql_config('host')
port = get_mysql_config('port')
user = get_mysql_config('user')
password = get_mysql_config('password')
database = get_mysql_config('database')


def connect():
    return pymysql.connect(host=host,
                           port=int(port),
                           user=user,
                           password=password,
                           database=database,
                           cursorclass=pymysql.cursors.DictCursor)


def mark(comment_list: list[Comment]):
    if len(comment_list) == 0:
        return
    connection = connect()
    with connection:
        with connection.cursor() as cursor:
            values = str([(f'{cmt.bv}', cmt.id) for cmt in comment_list]).lstrip('[').rstrip(']')
            sql = f"INSERT INTO marked (bid, cid) VALUES {values};"
            cursor.execute(sql)

        try:
            connection.commit()
        except Exception:
            connection.rollback()


def marked_set():
    connection = connect()
    marked = set()
    with connection:
        with connection.cursor() as cursor:
            sql = f'SELECT bid, cid FROM marked'
            cursor.execute(sql)
            for cmt in cursor.fetchall():
                marked.add((cmt['bid'], cmt['cid']))
    return marked
