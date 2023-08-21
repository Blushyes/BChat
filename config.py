import configparser
import logging
import platform

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


class Config:
    _instance = None
    credential = ''
    session_dict = {}
    runtime_platform = None
    _parser = configparser.ConfigParser()
    reply_switch = False

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
        self._parser.read(CONFIG_FILENAME)

        # 获取开关配置
        self.reply_switch = self.get(GLOBAL_CONFIG, 'reply_switch') == 'ON'

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


# 唯一的单例config
config = Config()

# 配置日志输出格式和级别
log_level = logging.DEBUG if config.profile == Profile.DEV else logging.INFO
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.WARNING)
log = logging.getLogger('blushyes')
log.setLevel(log_level)
