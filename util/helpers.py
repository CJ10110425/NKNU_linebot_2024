import sys
import os
import yaml
from typing import Optional


class FileSystem:

    @staticmethod
    def __get_base_dir():
        current_path = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(current_path, '..')

    @staticmethod
    def __get_config_directory() -> str:
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, 'settings')

    @staticmethod
    def __get_plugin_directory(plugin_name) -> str:
        base_dir = FileSystem.__get_base_dir()
        return os.path.join(base_dir, f'plugins/{plugin_name}')

    @staticmethod
    def load_plugin(name: str = 'plugin.yaml', plugin_name: str = "plugin_default", plugin_config_directory: Optional[str] = None) -> dict:
        if plugin_config_directory is None:
            plugin_config_directory = FileSystem.__get_plugin_directory(
                plugin_name)
        with open(os.path.join(plugin_config_directory, name)) as file:
            input_data = yaml.safe_load(file)
        return input_data

    @staticmethod
    def load_configuration(name: str = 'configuration.yaml', config_directory: Optional[str] = None) -> dict:
        if config_directory is None:
            config_directory = FileSystem.__get_config_directory()
        with open(os.path.join(config_directory, name)) as file:
            input_data = yaml.safe_load(file)
        return input_data
    
    @staticmethod
    def load_line_bot_info(name: str = 'app_info.yaml',config_directory: Optional[str] = None) -> dict:
        if config_directory is None:
            config_directory = FileSystem.__get_config_directory()
        with open(os.path.join(config_directory, name)) as file:
            input_data = yaml.safe_load(file)
        return input_data


if __name__ == "__main__":
    print(FileSystem.load_configuration(
        name='configuration.yaml', config_directory=None))
    print(FileSystem.load_plugin(plugin_name='plugin_1'))
