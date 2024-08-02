import logging
import traceback
from core.login.__init__ import LoginInfo, LoginManager
from bilibili_api import login
from bilibili_api.user import User


class SimpleLoginManager(LoginManager):
    def __init__(self) -> None:
        self._session_dict: dict[int, LoginInfo] = dict()

    def login(self, uid: int) -> LoginInfo:
        logging.info("正在获取登录二维码...")

        credential = login.login_with_qrcode_term()  # 在终端扫描二维码登录
        try:
            credential.raise_for_no_bili_jct()  # 判断是否成功
            credential.raise_for_no_sessdata()  # 判断是否成功
        except:
            traceback.format_exc()
            return login(uid)  # 重新登录一下

        login_info = LoginInfo(credential, User(uid, credential))
        self._session_dict[uid] = login_info

        logging.info("登录成功，程序开始运行...")

        return login_info

    def get_session(self, uid: int) -> LoginInfo:
        if uid in self._session_dict:
            return self._session_dict[uid]

        return self.login(uid)
