from bilibili_api import login_func
from PIL import Image
from config import config
import time


def login():
    '''
    登录并获取凭证
    '''
    # 获取登录二维码
    picture, credential = login_func.get_qrcode()
    print(picture, credential)

    while True:
        state, session = login_func.check_qrcode_events(credential)
        print('state', state)
        if state == login_func.QrCodeLoginEvents.DONE:
            config.session_dict[credential] = session
            break

        # windows打开
        # img = Image.open(picture.url.replace('file://', ''))
        # img.show()

        time.sleep(3)
        

    config.credential = credential
    return credential


def get_session(credential):
    '''
    获取凭证对象

    credential: 凭证str
    '''
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
        print(f'用户未登录，登录状态为：{state}')
        return get_session(login())
