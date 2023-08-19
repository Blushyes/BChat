import logging
import time

from PIL import Image
from bilibili_api import login_func

from config import config, RuntimePlatform


def login():
    """
    登录并获取凭证
    """
    # 获取登录二维码
    picture, credential = login_func.get_qrcode()
    print(picture, credential)

    while True:
        state, session = login_func.check_qrcode_events(credential)

        # 检测登录状态，若已经登录则进行下一步动作
        print('state', state)
        if state == login_func.QrCodeLoginEvents.DONE:
            # 存session
            config.session_dict[credential] = session
            break

        # 如果操作系统为Windows则直接打开图片扫码
        if RuntimePlatform.WINDOWS == config.runtime_platform:
            img = Image.open(picture.url.replace('file://', ''))
            img.show()

        time.sleep(3)

    # 设置全局凭证
    config.credential = credential
    return credential


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
