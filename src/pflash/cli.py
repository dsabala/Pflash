"""
This module implements the command-line interface (CLI) for the pflash utility.
"""

import os
import sys
import click
from loguru import logger
from pflash.config import CONFIG_DIR, LOG_FILE
from pflash.ramdisk_flash import ramdisk_flash

os.makedirs(CONFIG_DIR, exist_ok=True)
logger.remove()
logger.add(
    LOG_FILE,
    rotation="10 MB",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)
logger.add(
    sys.stdout,
    level="INFO",
    format="<level>{time:YYYY-MM-DD HH:mm:ss.SSS} | {message} </level>",
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
@click.option("-d", "--dry", is_flag=True, default=False, help="Dry run")
def flash_via_ramdisk(parts: tuple[str, ...], ser: str, prj: str, root: str, dry: bool):
    """Flash target using ramdisk, debugger and console"""
    ramdisk_flash(parts=parts, ser=ser, prj=prj, root=root, dry=dry)


if __name__ == "__main__":
    cli_entrypoint()
