import logging
import platform


class RuntimePlatform:
    WINDOWS = 'win'
    LINUX = 'linux'
    UNKNOWN = 'unknown'

class Profile:
    PROD = 'prod'
    DEV = 'dev'


class Config:
    _instance = None
    credential = ''
    session_dict = {}
    runtime_platform = None

    # 默认为开发环境
    profile = Profile.DEV

    def __int__(self):
        if platform.system() == 'Windows':
            self.runtime_platform = RuntimePlatform.WINDOWS

        elif platform.system() == 'Linux':
            self.runtime_platform = RuntimePlatform.LINUX

            # 如果在Linux上运行，则为生产环境
            self.profile = Profile.PROD

        else:
            self.runtime_platform = RuntimePlatform.UNKNOWN

        print(f'当前登录平台为{self.runtime_platform}')

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.__int__()
        return cls._instance

    def set_credential(self, credential):
        self.credential = credential

    def __str__(self) -> str:
        return f'credential: {self.credential}'


# 唯一的单例config
config = Config()
