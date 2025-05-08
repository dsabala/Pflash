"""
This module defines custom exceptions for the pflash utility.
"""

import sys
from loguru import logger


class PflashError(Exception):
    """Base class for all pflash-related exceptions."""

    def __init__(self, message: str):
        logger.error(message)
        sys.exit(1)


class LackOfPrerequisite(PflashError):
    """
    Raised when the system lacks a required prerequisite.
    Example: Missing OpenOCD binary in the system PATH.
    """


class ConfigNotFoundError(PflashError):
    """
    Raised when a configuration file or entry is not found.
    Example: Missing user or internal configuration file.
    """


class InvalidConfigError(PflashError):
    """
    Raised when a configuration file contains invalid JSON or is corrupted.
    Example: JSONDecodeError while parsing the configuration file.
    """


class OpenOcdTimeout(PflashError):
    """
    Raised when the OpenOCD subprocess times out.
    Example: The OpenOCD command exceeds the specified timeout duration.
    """


class OpenOcdFail(PflashError):
    """
    Raised when the OpenOCD subprocess fails with a non-zero return code.
    Example: OpenOCD fails to load a binary image into RAM.
    """


class BootloaderError(PflashError):
    """
    Raised when there is an issue with the bootloader.
    Example: Failure to enter bootloader mode or communicate with the bootloader.
    """
