"""
This module defines custom exceptions for the pflash utility
"""

import sys
from loguru import logger


class PflashError(Exception):
    """Base class for all pflash-related exceptions"""


class LackOfPrerequisite(PflashError):
    """Raised when system lacks some prerequisite"""


class ConfigNotFoundError(PflashError):
    """Raised when a configuration entry is not found"""


class InvalidConfigError(PflashError):
    """Raised when a configuration file is invalid"""


class OpenOcdTimeout(PflashError):
    """Raised when OpenOCD subprocess timeout"""


class OpenOcdFail(PflashError):
    """Raised when OpenOCD subprocess fails"""


class BootloaderError(PflashError):
    """Raised when there is an issue with the bootloader"""


def handle_exceptions(command_function):
    """
    Decorator to handle exceptions for CLI commands.
    This ensures consistent error handling across all commands.
    """

    def wrapper(*args, **kwargs):
        try:
            return command_function(*args, **kwargs)
        except LackOfPrerequisite as e:
            logger.error(f"Prerequisite not fulfilled: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            sys.exit(1)

    return wrapper
