"""
This module provides functionality for loading and retrieving configuration entries
from JSON configuration files. It supports both user-defined configuration files
(located in the user's home directory) and internal configuration files bundled
with the application.
"""

import json
from pathlib import Path
from loguru import logger
from pflash.exceptions import ConfigNotFoundError, InvalidConfigError

CONFIG_DIR = Path.home() / ".config/pflash"
LOG_FILE = CONFIG_DIR / "log.txt"
USER_CONFIG_FILE = CONFIG_DIR / "config.json"
INTERNAL_CONFIG_FILE = Path(__file__).parent / "assets" / "config.json"


def load_config_file(file_path: Path) -> dict:
    """
    Load a JSON configuration file.

    Args:
        file_path (Path): The path to the configuration file.

    Returns:
        dict: Parsed JSON data.

    Raises:
        ConfigNotFoundError: If the configuration file is not found.
        InvalidConfigError: If the configuration file contains invalid JSON.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config_data = json.load(file)
            logger.debug(f"Configuration loaded from {file_path}: {config_data}")
            return config_data
    except FileNotFoundError as e:
        raise ConfigNotFoundError(f"Configuration file not found: {file_path}") from e
    except json.JSONDecodeError as e:
        raise InvalidConfigError(f"Error decoding JSON file {file_path}") from e


def load_config_entry(entry_name: str) -> dict:
    """
    Retrieve a configuration entry by its name.

    Args:
        entry_name (str): The name of the configuration entry to retrieve.

    Returns:
        dict: A configuration entry with 'name' equal to entry_name.

    Raises:
        ConfigNotFoundError: If the configuration entry is not found in any configuration file.
    """

    # Helper function to search for an entry in a configuration file
    def find_entry(file_path: Path) -> dict:
        config_data = load_config_file(file_path)
        configurations = config_data.get("configuration", [])
        for entry in configurations:
            if entry.get("name") == entry_name:
                return entry
        return None

    # Search in the user configuration file
    try:
        entry = find_entry(USER_CONFIG_FILE)
        if entry:
            return entry
    except ConfigNotFoundError:
        logger.info(f"User configuration file not found: {USER_CONFIG_FILE}")

    # Search in the internal configuration file
    entry = find_entry(INTERNAL_CONFIG_FILE)
    if entry:
        return entry

    # Raise an error if the entry is not found in either file
    raise ConfigNotFoundError(
        f"Configuration '{entry_name}' not found in both user and internal config files."
    )
