import os
import sys
from loguru import logger
import click

LOG_DIR = os.path.expanduser("~/.config/pflash")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "log.txt")
logger.remove()
logger.add(LOG_FILE, rotation="10 MB", retention="7 days", level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> {message}")

@click.group()
def cli_entrypoint():
    """pflash - Phoenix RTOS flash utility"""
    logger.debug("Pflash CLI started")
    pass

@cli_entrypoint.command()
@click.argument("partition", type=str, nargs = -1)
@click.option("-s", "--serial", required=True, type=str)
@click.option("-c", "--config", required=True, type=str)
def flash_via_ramdisk(partition: tuple[str, ...], serial: str, config: str):
    """Flash board using plo RAMDISK, debugger and console"""
    logger.info(f"pflash CLI request to flash {', '.join(partition) if len(partition) > 1 else partition[0]} {'partitions' if len(partition) > 1 else 'partition'} via RAMDISK, serial = {serial}, config = {config}")
