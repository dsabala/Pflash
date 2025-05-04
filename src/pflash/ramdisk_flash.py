"""
This module implements flash-via-ramdisk functionality
"""

import sys
from pathlib import Path
from loguru import logger

from pflash.project import get_inv_directory, get_flash_jobs_list
from pflash.config import load_config_entry
from pflash.plo import boot_plo_naively, plo_copy
from pflash.openocd import which_openocd, upload_to_ram, OpenOcdUploadParameters
from pflash.exceptions import handle_exceptions


@handle_exceptions
def ramdisk_flash(parts: tuple[str, ...], ser: str, prj: str, root: str, dry: bool):
    """Flash-via-ramdisk functionality main function"""
    logger.info(f"Request to flash via ramdisk project: {prj}, dry run: {dry}")

    # 1. Load part of user defined or internal config file appropriate for this project
    cfg = load_config_entry(prj)

    # 2. Find out project directory, run program where it was called if no --root passed
    root_dir = get_inv_directory(root)
    logger.info(f"Project root: {root_dir}")

    # 3. Acquire some knowledge about job to do
    flash_jobs = get_flash_jobs_list(prj=prj, root=root, parts=parts)
    if len(flash_jobs) == 0:
        logger.error("Lack of partitions to flash")
        sys.exit(1)

    # 4. Ensure target is in bootloader
    try:
        baudrate = int(cfg["plo"]["baudrate"])
        boot_plo_naively(port=ser, baud=baudrate, dry=dry)
    except Exception as e:
        logger.error(e)
        sys.exit(1)

    # 5. Perform all jobs (flash all mentioned partitions)
    for flash_job in flash_jobs:
        logger.info(f"Flashing partition {flash_job.name}")

        # 6. Use JTAG probe to upload binary image to ramdisk
        parameters = OpenOcdUploadParameters(
            target_config=Path("target/zynq_7000.cfg"),
            board_config=Path("target/zynq_7000.cfg"),
            binary_image=Path("binary.img"),
            ram_address=0x80000000,
            timeout_s=30,
        )
        upload_to_ram(parameters=parameters, dry=dry)

        # 7. Send command to PLO to copy image from ramdisk to non volatile memory
        plo_copy(port=ser, baud=115200, size=1000, alias="flash0", offset=0, dry=dry)
