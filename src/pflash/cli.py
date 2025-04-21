import os
import sys
from loguru import logger
import click
from pflash.config import load_config_entry
from pflash.env_check import get_invocation_directory
#from pflash.project_check import load_project_nvm
from pflash.ramdisk_flash import ramdisk_flash

# Configuration paths
CONFIG_DIR = os.path.expanduser("~/.config/pflash")
CONFIG_FILE = os.path.expanduser("~/.config/pflash/config.json")
LOG_FILE = os.path.join(CONFIG_DIR, "log.txt")

# Logger/config initialization
os.makedirs(CONFIG_DIR, exist_ok=True)
logger.remove()
logger.add(LOG_FILE, rotation="10 MB", retention="7 days", level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
logger.add(sys.stdout, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> {message}")

@click.group()
def main():
    """pflash - Phoenix RTOS flash utility"""
    logger.debug("Pflash CLI started")
    pass

@main.command()
@click.argument("partition", type=str, nargs=-1)
@click.option("-s", "--serial", required=True, type=str)
@click.option("-c", "--config", required=True, type=str)
@click.option("-r", "--root", type=str)
def flash_via_ramdisk(partition: tuple[str, ...], serial: str, config: str, root: str):
    """Flash target using Plo bootloader ramdisk, debugger and console"""

    # Load dedicated entry from config file either internal or user defined
    try:
        config_entry = load_config_entry(CONFIG_FILE, config)
    except (FileNotFoundError, KeyError, ValueError) as e:
        logger.error(e)

    # Get project root directory
    inv_dir = get_invocation_directory(root)
    logger.info(f"Project root: {inv_dir}")

    ramdisk_flash(partition=partition, serial=serial, config=config, root=root)


if __name__ == "__main__":
    main()


#def unused():
#    # Get detailf of memory layout in desired projects
#    try:
#        nvm_layout = load_project_nvm(config_entry["project"], inv_dir)
#        print("Memory layout:", nvm_layout)
#    except FileNotFoundError as e:
#        print(f"Error: {e}")
#    except ValueError as e:
#        print(f"Error: {e}")