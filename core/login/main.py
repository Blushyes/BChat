from dataclasses import dataclass

from bilibili_api import Credential
from bilibili_api.user import User


@dataclass
class LoginInfo:
    credential: Credential
    user: User


class LoginManager:
    def login(uid: int) -> LoginInfo:
        ...

    def get_session(uid: int) -> LoginInfo:
        ...
