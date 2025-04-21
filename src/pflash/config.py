import os
import json
from loguru import logger

INTERNAL_CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def load_config_file(config_file_path: str):
    """Load the JSON configuration file."""
    try:
        with open(config_file_path, "r") as file:
            config_data = json.load(file)
            logger.debug(f"Configuration loaded: {config_data}")
            return config_data
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {config_file_path}")
        raise e
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON configuration file: {e}")
        raise ValueError(f"Error decoding JSON configuration file: {e}")

def load_config_entry(config_file_path: str, config_entry_name: str):
    """Load the single entry of JSON config file"""

    # First search for desired config entry in the user config file
    try:
        user_config = load_config_file(config_file_path)
        configurations = user_config.get("configuration", [])
        for entry in configurations:
            if entry.get("name") == config_entry_name:
                logger.debug(f"Configuration entry '{config_entry_name}' found in user config.")
                return entry
    except FileNotFoundError:
        logger.error(f"User configuration file not found: {config_file_path}")

    # If not found, check the internal configuration file
    try:
        internal_config = load_config_file(INTERNAL_CONFIG_FILE)
        configurations = internal_config.get("configuration", [])
        for entry in configurations:
            if entry.get("name") == config_entry_name:
                logger.debug(f"Configuration entry '{config_entry_name}' found in internal config.")
                return entry
    except FileNotFoundError:
        logger.warning(f"Internal configuration file not found: {INTERNAL_CONFIG_FILE}")

    # If not found in either file, raise an error
    logger.error(f"Configuration entry '{config_entry_name}' not found in the configuration files.")
    raise KeyError(f"Configuration entry '{config_entry_name}' not found in the configuration files.")
