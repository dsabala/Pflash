"""
This module implements flash-via-ramdisk functionality
"""

import sys
from loguru import logger

from pflash.project import get_inv_directory, get_flash_jobs_list
from pflash.config import load_config_entry


def ramdisk_flash(parts: tuple[str, ...], ser: str, prj: str, root: str):
    """Flash-via-ramdisk functionality main function"""

    logger.info("Command line request to flash via ramdisk")
    logger.info(f"Project name: {prj}")

    # 1. Find configuration
    try:
        config_entry = load_config_entry(prj)
    except (FileNotFoundError, KeyError, ValueError) as e:
        logger.error(e)
        sys.exit(1)

    # 2. Find out project directory
    root_dir = get_inv_directory(root)
    logger.info(f"Project root: {root_dir}")

    # 3. Acquire some knowledge about job to do
    flash_jobs = get_flash_jobs_list(prj=prj, root=root, parts=parts)
    if len(flash_jobs) == 0:
        logger.error("Lack of partitions to flash")
        sys.exit(1)

    # 4. Ensure target is in bootloader

    # 5. Perform all jobs (flash all mentioned partitions)
    for flash_job in flash_jobs:
        logger.info(f"Flashing partition {flash_job.name}")

        # 6. USe JTAG probe to upload binary image to ramdisk

        # 7. Send command to PLO to copy image from ramdisk to non volatile memory

    # 8. Show statistics
