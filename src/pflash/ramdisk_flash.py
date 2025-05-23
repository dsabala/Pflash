"""
This module implements flash-via-ramdisk functionality
"""

import sys
from pathlib import Path
from loguru import logger

from pflash.project import get_inv_directory, get_flash_jobs_list
from pflash.config import load_config_entry
from pflash.plo import boot_plo_naively, plo_copy
from pflash.openocd import upload, UploadParameters


class RamdiskFlashParameters: # pylint: disable=too-few-public-methods
    """Operation parameters parsed from config file"""

    def __init__(self, cfg_entry: dict):
        self.project: str = cfg_entry["project"]
        self.baudrate: int = int(cfg_entry["console"]["baudrate"])
        self.reboot_timeout_s: int = int(cfg_entry["console"]["reboot_timeout_s"])
        self.target_config: Path = Path(cfg_entry["openocd"]["target_config"])
        cfg_dir = Path(__file__).parent / "assets" / "openocd"
        self.board_config: Path = cfg_dir / cfg_entry["openocd"]["board_config"]
        self.upload_timeout_s = cfg_entry["openocd"]["upload_timeout_s"]
        self.ramdisk_address = cfg_entry["ramdisk_flash"]["ramdisk_address"]


def ramdisk_flash(parts: tuple[str, ...], cnsl: str, prj: str, root: str, dry: bool):
    """Flash-via-ramdisk functionality main function"""
    logger.debug(f"Request to flash via ramdisk, project: {prj}")

    # 1. Load part of user defined or internal config file appropriate for this project
    cfg_entry = load_config_entry(prj)
    params = RamdiskFlashParameters(cfg_entry)

    # 2. Find out project directory, run program where it was called if no --root passed
    root_dir = get_inv_directory(root)

    # 3. Acquire some knowledge about job to do
    flash_jobs = get_flash_jobs_list(prj=prj, root=root_dir, parts=parts)
    if len(flash_jobs) == 0:
        logger.error("Lack of partitions to flash")
        sys.exit(1)

    # 4. Ensure target is in bootloader
    boot_plo_naively(port=cnsl, baud=params.baudrate, dry=dry)

    # 5. Perform all jobs (flash all mentioned partitions)
    for flash_job in flash_jobs:
        binary_image_path = (
            Path(root_dir) / "_boot" / params.project / flash_job.filename
        )

        # 6. Use JTAG probe to upload binary image to ramdisk
        parameters = UploadParameters(
            target_config=params.target_config,
            board_config=params.board_config,
            binary_image=binary_image_path,
            address=params.ramdisk_address,
            upload_timeout_s=params.upload_timeout_s,
        )
        upload(parameters=parameters, dry=dry)

        # 7. Send command to PLO to copy image from ramdisk to non volatile memory
        plo_copy(
            port=cnsl,
            baud=params.baudrate,
            size=flash_job.size,
            alias=flash_job.block_device,
            offset=flash_job.offs,
            dry=dry,
        )
