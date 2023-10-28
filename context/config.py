import json
import logging
import os.path
import shutil


class DefaultConfig:
    PROFILE = 'profile'
    GLOBAL = 'global'
    MODEL = 'model'
    MYSQL = 'mysql'
    PERSISTENT = 'persistent'

    class Global:
        UID = 'uid'

    class Model:
        XUNFEI = 'xunfei'
        class XunFei:
            APPID = 'appid'
            API_SECRET = 'api_secret'
            API_KEY = 'api_key'

    class Persistent:
        STRATEGY = 'strategy'

    class Mysql:
        HOST = 'host'
        PORT = 'port'
        USER = 'user'
        PASSWORD = 'password'
        DATABASE = 'database'


class ConfigManager:
    """
    配置管理接口
    """

    def get_config(self, *args):
        """
        获取配置项
        """
        ...

    def exists(self, *args):
        """
        是否存在某个配置
        """
        ...

    def __contains__(self, item):
        return self.exists(item)


class LocalJsonConfigManager(ConfigManager):
    """
    本地JSON格式配置
    """
    CONFIG_NAME = 'config.json'
    EXAMPLE_CONFIG_NAME = 'config.example.json'

    def __init__(self):
        if not os.path.exists(LocalJsonConfigManager.CONFIG_NAME):
            logging.warning('未检测到配置文件config.json，自动生成config.json')
            shutil.copy(
                LocalJsonConfigManager.EXAMPLE_CONFIG_NAME,
                LocalJsonConfigManager.CONFIG_NAME
            )
            raise Exception("""
            未检测到配置文件：config.json
            已自动生成config.json
            请前往配置
            """)

        with open(LocalJsonConfigManager.CONFIG_NAME, 'r') as f:
            self._config: dict = json.loads(f.read())

    def _save_config(self):
        with open(LocalJsonConfigManager.CONFIG_NAME, 'w') as f:
            f.write(json.dumps(self._config))

    def get_config(self, *args):
        assert len(args) > 0
        item = self._config[args[0]]
        for key in args[1:]:
            item = item[key]
        return item

    def exists(self, *args):
        assert len(args) > 0
        item = self._config.get(args[0])
        if item is None: return False
        for key in args[1:]:
            item = item.get(key)
            if item is None: return False
        return item is not None
