
from util import FileSystem
from typing import Optional
import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class PluginUtility:

    def __init__(self) -> None:
        pass

    @staticmethod
    def read_plugin_config(plugin_name: str) -> dict:
        try:
            pluin_data = FileSystem.load_plugin(plugin_name=plugin_name)
        except FileNotFoundError:
            logger.info(f"Plugin_config {plugin_name} not found")
            pluin_default_data = FileSystem.load_plugin()
            return pluin_default_data
        return pluin_data

    @staticmethod
    def setup_plugin_config(plugin_name: str) -> str:
        plugin_data = PluginUtility.read_plugin_config(plugin_name)
        try:
            plugin_config_runtime = plugin_data["runtime"]["main"]
        except:
            logger.info(f"Plugin_config {plugin_name} not found runtime")
            return None
        return plugin_config_runtime

    # 比對config讀取的plugin_name與每一個plugin裡面的plugin.yaml名稱是否相同
    @staticmethod
    def compare_plugin_name(config_plugin_name: str) -> bool:
        plugin_data = PluginUtility.read_plugin_config(config_plugin_name)
        try:
            plugin_name = plugin_data["name"]
        except:
            logger.info(f"Plugin_config {plugin_name} not found plugin name")
            return False
        return config_plugin_name == plugin_name

    @staticmethod
    def register_plugin() -> dict:
        plugin_name = FileSystem.load_configuration()["plugins"]
        register_plugins = {}
        if plugin_name not in [None, []]:
            logger.info(f"Registering {plugin_name} ")
            for plugin in plugin_name:
                if PluginUtility.compare_plugin_name(plugin):
                    logger.info(f"Plugin_config {
                                plugin} registered successfully")
                    register_plugins[plugin] = PluginUtility.setup_plugin_config(
                        plugin)
                else:
                    logger.info(
                        f"Plugin_config {plugin} failed to register successfully")
                    register_plugins["plugin_default"] = PluginUtility.setup_plugin_config(
                        "plugin_default")
        return register_plugins


class LinebotUtility:

    def __init__(self) -> None:
        pass

    @staticmethod
    def setup_linebot() -> dict:
        try:
            config_data = FileSystem.load_line_bot_info()
            linebot_config = config_data["line-bot-info"]
        except FileNotFoundError:
            logger.info(f"Plugin_config linebot not found")
            return None
        return linebot_config
