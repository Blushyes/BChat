import json

import pika
import requests

from config import config, log
from core.comment.comment import Comment

rabbitmq_host = config.get('rabbitmq', 'host')
delegate_host = config.get('delegate', 'host')
username = config.get('rabbitmq', 'username')
password = config.get('rabbitmq', 'password')
credentials = pika.PlainCredentials(username, password)


def connect():
    return pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, 5672, 'bchat_vhost', credentials))


# ch = connection.channel()
# ch.exchange_declare(exchange='comment', exchange_type='fanout')
# ch.queue_declare(queue='commented')
# ch.queue_declare(queue='all_comment')
# ch.queue_bind(queue='commented', exchange='comment')
# ch.queue_bind(queue='all_comment', exchange='comment')


def post(path, data, headers=None, files=None):
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    try:
        return requests.post(f'http://{delegate_host}:8888{path}', headers=headers, data=data, files=files)
    except Exception as e:
        log.error(e)
        return requests.Response()


def get(path, params=None, headers=None):
    if headers is None:
        headers = {'Content-Type': 'application/json'}
    try:
        return requests.get(f'http://{delegate_host}:8888{path}', headers=headers, params=params)
    except Exception as e:
        log.error(e)
        return requests.Response()


def send(queue_name, message, exchange='', is_json=True):
    try:
        connection = connect()
        with connection:
            channel = connection.channel()
            channel.queue_declare(queue=queue_name)
            if is_json:
                channel.basic_publish(exchange=exchange, routing_key=queue_name,
                                      body=json.dumps(message).encode('utf-8'))
            else:
                channel.basic_publish(exchange=exchange, routing_key=queue_name, body=message)
    except Exception as e:
        log.error('发送消息的时候出错了')
        log.error(e)


def fanout_send(exchange_name, message, binding_key=''):
    try:
        connection = connect()
        with connection:
            channel = connection.channel()
            channel.basic_publish(exchange=exchange_name, routing_key=binding_key,
                                  body=json.dumps(message).encode('utf-8'))
    except Exception as e:
        log.error('发送消息的时候出错了')
        log.error(e)


def mark(comment_list: list[Comment]):
    if len(comment_list) == 0:
        return
    response = post('/mark', json.dumps([cmt.to_simple_dict() for cmt in comment_list]))
    log.debug(f'MARK请求操作成功：{response.text}')


def marked_set():
    data = get('/mark').text
    comment_list = json.loads(data)['data']
    log.debug(f'收到的 MARKED SET 为：{comment_list}')
    return {(cmt['bid'], cmt['cid']) for cmt in comment_list}
