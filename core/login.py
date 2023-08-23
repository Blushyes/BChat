import json
import logging
import time
from io import BytesIO

from PIL import Image
from bilibili_api import login_func

import persistent.base as persistent
import persistent.delegate as delegate
from config import config, RuntimePlatform, log


def login(uid=None):
    """
    登录并获取凭证
    """
    # 获取登录二维码
    log.info('正在获取登录二维码...')
    try:
        picture, credential = login_func.get_qrcode()
        # 打开图片文件
        img = Image.open(picture.url.replace('file://', ''))
        # 将图片转换为二进制数据
        data = BytesIO()
        img.save(data, format='JPEG')
        data.seek(0)
        # 把图片发给后端
        delegate.post('/login/img', '', {}, {'img': data.read()})
    except Exception as e:
        log.error(e)
        # 重新登录一下
        return login(uid)

    log.info(f'{picture} {credential}')
    log.info('二维码获取完毕，请前往扫码')

    while True:
        state, session = login_func.check_qrcode_events(credential)

        # 检测登录状态，若已经登录则进行下一步动作
        log.info(f'当前二维码状态为：{state}')
        if state == login_func.QrCodeLoginEvents.DONE:
            # 存session
            config.session_dict[credential] = session
            break

        # 如果操作系统为Windows则直接打开图片扫码
        if RuntimePlatform.WINDOWS == config.runtime_platform:
            img.show()

        time.sleep(3)

    # 设置全局凭证
    log.info('登录成功，程序开始运行...')
    img.close()

    # 登录成功发送登录成功的消息
    response = None
    if persistent.MarkStrategy.DELEGATE == config.get_persistent_config('strategy'):
        response = delegate.post('/login', json.dumps({'credential': credential, 'uid': str(uid)}).encode('utf-8'))
    config.credential = credential
    return response


def get_session(credential):
    """
    获取凭证对象

    credential: 凭证str
    """
    # 如果凭证为空则需要登录
    if not credential or credential == '':
        credential = login()

    # 若session已经存在则直接返回
    if credential in config.session_dict:
        return config.session_dict[credential]

    state, session = login_func.check_qrcode_events(credential)

    print(state, credential)
    if login_func.QrCodeLoginEvents.DONE == state:
        config.session_dict[credential] = session
        return session
    else:
        logging.error(f'用户未登录，登录状态为：{state}')
        return get_session(login())
