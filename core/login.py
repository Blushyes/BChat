import time
import traceback
from io import BytesIO

from PIL import Image
from bilibili_api import login_func, Credential
from bilibili_api.user import User

from context.main import log, context, RuntimePlatform, LoginInfo


def login(uid: int) -> LoginInfo:
    """
    登录并获取凭证
    """

    # 获取登录二维码
    log.info('正在获取登录二维码...')
    try:
        picture, credential_str = login_func.get_qrcode()

        # 打开图片文件
        img = Image.open(picture.url.replace('file://', ''))

        # 将图片转换为二进制数据
        data = BytesIO()
        img.save(data, format='JPEG')
        data.seek(0)

    except Exception:
        traceback.format_exc()

        # 重新登录一下
        return login(uid)

    log.info(f'{picture} {credential_str}')
    log.info('二维码获取完毕，请前往扫码')

    while True:
        state, credential = login_func.check_qrcode_events(credential_str)
        user = User(uid, credential)
        login_info = LoginInfo(credential_str, credential, user)

        # 检测登录状态，若已经登录则进行下一步动作
        log.info(f'当前二维码状态为：{state}')
        if state == login_func.QrCodeLoginEvents.DONE:
            # 存session
            context.session_dict[uid] = login_info
            break

        # 如果操作系统为Windows则直接打开图片扫码
        if RuntimePlatform.WINDOWS == context.runtime_platform:
            img.show()

        time.sleep(3)

    # 设置全局凭证
    log.info('登录成功，程序开始运行...')
    img.close()

    return login_info


def get_session(uid: int) -> Credential:
    """
    获取凭证对象

    Args:
        uid: 用户的UID

    Returns:
        billbill_api的登录的凭证

    """

    assert uid

    # 若session已经存在则直接返回
    if uid in context.session_dict:
        return context.session_dict[uid].credential

    return login(uid).credential
