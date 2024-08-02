import importlib
import json
import os
import sys
import traceback
from concurrent.futures import ThreadPoolExecutor

from consts.names import PLUGIN_DIR_NAME, PLUGIN_CONFIG_FILE_NAME
from context.main import log
from exceptions.context import NotImplementException


class Plugin:
    def __init__(self, config: dict):
        self.config = config
        self.name = config["name"]
        self.version = config["version"]
        # plugin = __import__(self.config['path'], globals(), locals(), [], 0)


class PluginManager:
    def __init__(self) -> None:
        pass

    def get_plugin(self, name: str):
        """
        根据插件名获取插件实例

        Args:
            name: 插件名

        Returns:

        """
        raise NotImplementException()

    def all_plugins(self):
        """
        获取所有插件

        Returns:

        """
        raise NotImplementException()


class SimplePluginManager(PluginManager):
    def __init__(self, executor: ThreadPoolExecutor) -> None:
        super().__init__()

        log.info("开始读取插件...")

        # 获取所有文件夹的名字
        plugin_paths = os.listdir(PLUGIN_DIR_NAME)
        log.info(f"获取到的插件有：{plugin_paths}")

        # 读取配置文件
        plugins: list[Plugin] = []
        sys.path.append(PLUGIN_DIR_NAME)
        for plugin_path in plugin_paths:
            real_path = os.path.join(PLUGIN_DIR_NAME, plugin_path)
            plugin_config_path = os.path.join(real_path, PLUGIN_CONFIG_FILE_NAME)
            if not os.path.exists(plugin_config_path):
                log.error(f"{plugin_path} 配置文件 meta.json 不存在，跳过该插件")
                continue
            with open(plugin_config_path, "r", encoding="utf-8") as f:
                plugin_config: dict = json.load(f)
                plugin_config["path"] = plugin_path

                try:
                    plugin = Plugin(plugin_config)

                    # 运行当前插件
                    main = importlib.import_module(
                        plugin_path + ".main", package="widget"
                    )
                    executor.submit(main.start)
                except Exception as e:
                    traceback.format_exc()
                    log.error(f"解析{plugin_path}插件时出现问题：{e}，跳过当前插件")
                    raise e
                    # continue
                plugins.append(plugin)
        self._plugins = {plugin.name: plugin for plugin in plugins}

    def get_plugin(self, name: str):
        return self._plugins[name]

    def all_plugins(self):
        return self._plugins.values()
