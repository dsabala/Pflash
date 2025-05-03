"""
This module implements the command-line interface (CLI) for the pflash utility.
"""

import os
import sys
import click
from loguru import logger
from pflash.config import load_config_entry
from pflash.project import get_invocation_directory
from pflash.ramdisk_flash import ramdisk_flash

CONFIG_DIR = os.path.expanduser("~/.config/pflash")
LOG_FILE = os.path.expanduser("~/.config/pflash/log.json")

os.makedirs(CONFIG_DIR, exist_ok=True)
logger.remove()
logger.add(
    LOG_FILE,
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> {message}",
)


@click.group()
def cli_entrypoint():
    """pflash - Phoenix RTOS flash utility"""


@cli_entrypoint.command()
@click.argument("partition", type=str, nargs=-1)
@click.option("-s", "--serial", required=True, type=str)
@click.option("-c", "--config", required=True, type=str)
@click.option("-r", "--root", type=str)
def flash_via_ramdisk(partition: tuple[str, ...], serial: str, config: str, root: str):
    """Flash target using ramdisk, debugger and console"""

    try:
        config_entry = load_config_entry(config)
    except (FileNotFoundError, KeyError, ValueError) as e:
        logger.error(e)

    # Get project root directory
    inv_dir = get_invocation_directory(root)
    logger.info(f"Project root: {inv_dir}")

    ramdisk_flash(partition=partition, serial=serial, config=config_entry, root=root)


if __name__ == "__main__":
    cli_entrypoint()
