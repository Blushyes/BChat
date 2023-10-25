import asyncio
import configparser
import logging
import platform

from bilibili_api.user import User

CONFIG_FILENAME = 'config.ini'
XUNFEI_CONFIG = 'model.xunfei'
MYSQL_CONFIG = 'mysql'
GLOBAL_CONFIG = 'global'
PERSISTENT_CONFIG = 'persistent'


class RuntimePlatform:
    WINDOWS = 'win'
    LINUX = 'linux'
    UNKNOWN = 'unknown'


class Profile:
    PROD = 'prod'
    DEV = 'dev'


# TODO 待优化，这部分比较混乱
class Config:
    _instance = None
    credential = ''
    session_dict = {}
    runtime_platform = None
    _parser = configparser.ConfigParser()
    reply_switch = False
    uid = None
    USER = None

    # 默认为开发环境
    profile = Profile.DEV

    def __init__(self):
        if platform.system() == 'Windows':
            self.runtime_platform = RuntimePlatform.WINDOWS

        elif platform.system() == 'Linux':
            self.runtime_platform = RuntimePlatform.LINUX

            # 如果在Linux上运行，则为生产环境
            self.profile = Profile.PROD

        else:
            self.runtime_platform = RuntimePlatform.UNKNOWN

        # 读取配置文件
        self._parser.read(CONFIG_FILENAME, encoding='utf-8')

        # 获取开关配置
        self.reply_switch = self.get(GLOBAL_CONFIG, 'reply_myself_switch') == 'ON'
        if not self._parser.get('global', 'uid'):
            raise Exception('没有设置config.ini中的uid')

        self.uid = int(self._parser.get('global', 'uid'))
        print(self._parser.sections())
        print(f'当前登录平台为{self.runtime_platform}')

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __str__(self) -> str:
        return f'credential: {self.credential}'

    def set_credential(self, credential):
        self.credential = credential

    def get(self, section, option):
        return self._parser.get(section, option)

    def get_xunfei_config(self, key):
        return self.get(XUNFEI_CONFIG, key)

    def get_mysql_config(self, key):
        return self.get(MYSQL_CONFIG, key)

    def get_persistent_config(self, key):
        return self.get(PERSISTENT_CONFIG, key)

    def get_parser(self):
        return self._parser

    def is_fans(self, uid):
        if not self.USER:
            from core.login import get_session
            self.USER = User(self.uid, get_session(self.credential))
        return asyncio.run(self.USER.get_relation(uid))['be_relation']['mid'] == self.uid


# 唯一的单例config
config = Config()

# 配置日志输出格式和级别
log_level = logging.DEBUG if config.profile == Profile.DEV else logging.INFO
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.WARNING)
log = logging.getLogger('blushyes')
log.setLevel(log_level)
