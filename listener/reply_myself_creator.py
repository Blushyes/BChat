import asyncio
import json

import persistent.delegate as delegate
from big_model.reply_myself import ReplyMyself
from config import log
from core.login import login

sessions = {}


def login_callback(ch, method, properties, body):
    body = int(str(body).lstrip('b').strip("'"))
    log.debug(f"接收到消息：{body}")
    response = login(body)
    response = json.loads(response.text.encode('utf-8'))
    log.debug(response)
    if response['success']:
        task = ReplyMyself(body).start_loop()
        sessions[body] = task
        log.error(f'任务注册成功：{sessions}')


# TODO 未完成
def logout_callback(ch, method, properties, body):
    body = int(str(body).lstrip('b').strip("'"))
    log.info(f'收到{body}的取消申请')
    try:
        if body in sessions:
            sessions[body].cancel()
        else:
            log.warning('用户未登录')
    except asyncio.CancelledError:
        log.info(f'{body}已取消自动回复')


def listen_qrcode_login():
    # 连接到RabbitMQ服务器
    connection = delegate.connect()
    channel = connection.channel()

    # 声明一个队列
    login_queue = 'qrcode_login'
    logout_queue = 'qrcode_logout'
    channel.queue_declare(queue=login_queue)
    channel.queue_declare(queue=logout_queue)

    # 开始监听队列中的消息
    channel.basic_consume(queue=login_queue, on_message_callback=login_callback, auto_ack=True)
    channel.basic_consume(queue=logout_queue, on_message_callback=logout_callback, auto_ack=True)

    log.debug('等待接收消息...')
    channel.start_consuming()