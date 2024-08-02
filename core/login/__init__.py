from abc import ABC, abstractmethod
from dataclasses import dataclass

from bilibili_api import Credential
from bilibili_api.user import User


@dataclass
class LoginInfo:
    credential: Credential
    user: User


class LoginManager(ABC):
    @abstractmethod
    def login(self, uid: int) -> LoginInfo: ...

    @abstractmethod
    def get_session(self, uid: int) -> LoginInfo: ...
