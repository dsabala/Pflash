"""
Command-line interface (CLI) module for the pflash utility.
"""

import os
import sys
import click
from loguru import logger
from pflash.config import CONFIG_DIR, LOG_FILE
from pflash.ramdisk_flash import ramdisk_flash

# Ensure the configuration directory exists
os.makedirs(CONFIG_DIR, exist_ok=True)

# Add verbose text file logging
logger.remove()
logger.add(
    LOG_FILE,
    rotation="100 MB",
    retention="120 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
)


@click.group()
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    default=False,
    help="Enable verbose output (debug logs on console).",
)
@click.option(
    "-d",
    "--dry",
    is_flag=True,
    default=False,
    help="Perform a dry run without making any changes.",
)
@click.pass_context
def cli_entrypoint(ctx: click.Context = None, verbose: bool = False, dry: bool = False):
    """pflash - Phoenix RTOS Flash Utility"""

    # Pass generic flags like --verbose or --dry using context
    ctx.ensure_object(dict)
    ctx.obj["dry"] = dry

    # Add console logging
    logger.add(
        sys.stdout,
        level="DEBUG" if verbose else "INFO",
        format="<level>{time:HH:mm:ss} {level} {message}</level>",
    )
    if dry:
        logger.info("Dry run mode enabled. No changes will be made.")


@cli_entrypoint.command(
    epilog="""Example:

    \b
    To flash the 'plo' and 'kernel' partitions on a aarch64a53-zynqmp-som,
    with the bootloader available at /dev/ttyUSB0, run the following command
    from your project root directory:

    \b
    pflash flash-via-ramdisk -p aarch64a53-zynqmp-som -c /dev/ttyUSB0 plo kernel
    """
)
@click.argument("parts", type=str, nargs=-1)
@click.option(
    "-c",
    "--console",
    "cnsl",
    required=True,
    type=str,
    help="Bootloader console device (e.g., /dev/ttyUSB0).",
)
@click.option(
    "-p",
    "--project",
    "prj",
    required=True,
    type=str,
    help="Project directory name (e.g., aarch64a53-zynqmp-som).",
)
@click.option(
    "-r",
    "--root",
    type=str,
    help="Path to the phoenix-rtos-project directory. If not passed it fallback to invokation dir",
)
@click.pass_context
def flash_via_ramdisk(ctx, parts: tuple[str, ...], cnsl: str, prj: str, root: str):
    """
    Flash target device using ramdisk, debugger, and console.

    \b
    This command automates the following steps:
      - Reads the list of available partitions from the nvm.yaml file.
      - Checks if the target is already in PLO bootloader mode.
        If not, it requests a reboot and waits for the bootloader.
      - Uploads the binary image to the target's RAM using OpenOCD.
      - Instructs PLO to copy the image from RAM to flash memory.
    """
    ramdisk_flash(parts=parts, cnsl=cnsl, prj=prj, root=root, dry=ctx.obj["dry"])


if __name__ == "__main__":
    cli_entrypoint()
