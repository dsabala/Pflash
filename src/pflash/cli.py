"""
This module implements the command-line interface (CLI) for the pflash utility.
"""

import os
import sys
import click
from loguru import logger

import pflash.config as config
from pflash.ramdisk_flash import ramdisk_flash

os.makedirs(config.CONFIG_DIR, exist_ok=True)
logger.remove()
logger.add(
    config.LOG_FILE,
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
)
logger.add(
    sys.stdout,
    level="INFO",
    format="<level>{time:YYYY-MM-DD HH:mm:ss} | {message} </level>",
)
logger.level("INFO", color="<white>")
logger.level("ERROR", color="<red>")


@click.group()
def cli_entrypoint():
    """pflash - Phoenix RTOS flash utility"""


@cli_entrypoint.command()
@click.argument("parts", type=str, nargs=-1)
@click.option("-s", "--serial", "ser", required=True, type=str)
@click.option("-p", "--project", "prj", required=True, type=str)
@click.option("-r", "--root", type=str)
def flash_via_ramdisk(parts: tuple[str, ...], ser: str, prj: str, root: str):
    """Flash target using ramdisk, debugger and console"""
    ramdisk_flash(parts=parts, ser=ser, prj=prj, root=root)


if __name__ == "__main__":
    cli_entrypoint()
