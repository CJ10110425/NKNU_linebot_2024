#  engin_core.py

import logging
from importlib import import_module
from usecase import PluginUtility

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class PluginEngine():
    def __init__(self, line_bot_api, event, plugins):
        self.event = event
        if plugins:
            self.plugins = [import_module(f"plugins.{plugin}.{runtime}").Plugin(line_bot_api, event)
                            for plugin, runtime in plugins.items()]
        else:
            self.plugins = [import_module(
                'plugins.plugin_default.main').Plugin()]
    # 註冊 plugins 並回傳一個 list

    @staticmethod
    def register_plugins():
        logger.info("Starting Registeration")
        logger.info("-" * 10)
        logger.info("Registeration is finished")
        logger.info("=" * 10)
        return PluginUtility.register_plugin()

    def run(self):
        logger.info("Starting PluginEngine")
        logger.info("-" * 10)
        logger.info("This is Engine core system")
        for plugin in self.plugins:
            plugin.run()
        logger.info("-" * 10)
        logger.info("PluginEngine is finished")
        logger.info("=" * 10)


if __name__ == "__main__":
    line_bot_api = None
    event = None
    app = PluginEngine()
    app.run()
