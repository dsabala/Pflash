"""
This module provides functionality for loading and retrieving configuration entries
from JSON configuration files. It supports both user-defined configuration files
(located in the user's home directory) and internal configuration files bundled
with the application.
"""

import os
import json
from loguru import logger

CONFIG_DIR = os.path.expanduser("~/.config/pflash")
LOG_FILE = os.path.expanduser("~/.config/pflash/log.json")
USER_CONFIG_FILE = os.path.expanduser("~/.config/pflash/config.json")
INTERNAL_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


def load_config_file(config_file_path: str):
    """Load the JSON configuration file."""
    try:
        with open(config_file_path, "r", encoding="utf-8") as file:
            config_data = json.load(file)
            logger.debug(f"Configuration loaded: {config_data}")
            return config_data
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {config_file_path}")
        raise e
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON configuration file: {e}")
        raise ValueError(f"Error decoding JSON configuration file: {e}") from e


def load_config_entry(config_entry_name: str) -> dict:
    """
    Returns a platform configuration dictionary containing all neccessary data

    Returns:
        dict: A configuration entry with 'name' equal to config_entry_name
    """

    # First search for desired config entry in the user config file
    try:
        user_config = load_config_file(USER_CONFIG_FILE)
        configurations = user_config.get("configuration", [])
        for entry in configurations:
            if entry.get("name") == config_entry_name:
                logger.info(
                    f"Configuration entry '{config_entry_name}' found in user config."
                )
                return entry
    except FileNotFoundError:
        logger.error(f"User configuration file not found: {USER_CONFIG_FILE}")

    # If not found, check the internal configuration file
    try:
        internal_config = load_config_file(INTERNAL_CONFIG_FILE)
        configurations = internal_config.get("configuration", [])
        for entry in configurations:
            if entry.get("name") == config_entry_name:
                logger.info(
                    f"Configuration entry '{config_entry_name}' found in internal config."
                )
                return entry
    except FileNotFoundError:
        logger.warning(f"Internal configuration file not found: {INTERNAL_CONFIG_FILE}")

    raise KeyError(
        f"Configuration entry '{config_entry_name}' not found in the configuration files."
    )
