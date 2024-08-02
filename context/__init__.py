import logging
import os.path
import platform
from dataclasses import dataclass

from context.config import ConfigManager, LocalJsonConfigManager, DefaultConfig
from core.login import LoginManager
from core.login.simple import SimpleLoginManager


class RuntimePlatform:
    WINDOWS = "win"
    LINUX = "linux"
    UNKNOWN = "unknown"
    MAC = "mac"


class Profile:
    PROD = "prod"
    DEV = "dev"


@dataclass
class BChatContext:
    _instance = None
    uid: int
    runtime_platform: str
    config_manager: ConfigManager
    global_logger: logging.Logger
    profile: str = Profile.DEV
    login_manager: LoginManager = SimpleLoginManager()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def _auto_init_profile(self):
        if platform.system() == "Windows":
            self.runtime_platform = RuntimePlatform.WINDOWS

        elif platform.system() == "Linux":
            self.runtime_platform = RuntimePlatform.LINUX

            # 如果在Linux上运行，则为生产环境
            self.profile = Profile.PROD
        elif platform.system() == "Darwin":
            self.runtime_platform = RuntimePlatform.MAC

        else:
            self.runtime_platform = RuntimePlatform.UNKNOWN

    def _load_config_manager(self):
        if os.path.exists("config.json"):
            self.config_manager = LocalJsonConfigManager()

        # 中间可能还有其他情况
        else:
            # 默认采用本地JSON文件的方式
            self.config_manager = LocalJsonConfigManager()

    def _init_global_log(self):
        log_level = logging.DEBUG if self.profile == Profile.DEV else logging.INFO
        self.global_logger = logging.getLogger("GLOBAL_LOG")
        self.global_logger.setLevel(log_level)

    def __init__(self):
        self.session_dict = {}
        logging.basicConfig(
            format="%(asctime)s %(name)s %(levelname)s: %(message)s",
            level=logging.WARNING,
        )

        logging.info("加载配置管理器")
        self._load_config_manager()

        # TODO 支持多登录
        self.uid = self.config_manager.get_config(
            DefaultConfig.GLOBAL, DefaultConfig.Global.UID
        )

        logging.info("检查运行环境")
        if DefaultConfig.PROFILE in self.config_manager:
            self.profile = self.config_manager.get_config(DefaultConfig.PROFILE)
        else:
            self._auto_init_profile()

        logging.info("初始化全局日志器")
        self._init_global_log()
        # if self.runtime_platform:
        #     self.global_logger.info(f"当前登录平台为{self.runtime_platform}")


# 初始化上下文
context = BChatContext()

# 全局日志常量
log = context.global_logger
