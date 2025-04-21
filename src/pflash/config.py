import os
import json
from loguru import logger

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
    config_file = load_config_file(config_file_path)
    configurations = config_file.get("configuration", [])
    for entry in configurations:
        if entry.get("name") == config_entry_name:
            logger.debug(f"Configuration entry '{config_entry_name}' found")
            return entry
    logger.error(f"Configuration entry '{config_entry_name}' not found in the configuration file.")
    raise KeyError(f"Configuration entry '{config_entry_name}' not found in the configuration file.")
