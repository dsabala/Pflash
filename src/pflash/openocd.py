"""
OpenOCD subprocess run module
"""

import shutil
import subprocess
from pathlib import Path
from dataclasses import dataclass
from loguru import logger

from pflash.exceptions import LackOfPrerequisite, OpenOcdTimeout


def which_openocd() -> Path:
    """Search for OpenOCD binary"""
    openocd_binary = shutil.which("openocd")
    if openocd_binary:
        return Path(openocd_binary)
    raise LackOfPrerequisite("OpenOCD binary not found")


@dataclass
class OpenOcdUploadParameters:
    """Parameters required for uploading a binary image to the target's RAM"""

    target_config: str
    board_config: Path
    binary_image: Path
    ramdisk_address: int
    upload_timeout_s: int = None


def upload_to_ram(parameters: OpenOcdUploadParameters, dry: bool):
    """Upload binary image to RAM memory of target"""

    # Form OpenOCD command
    # fmt: off
    openocd_cmd = [
        f'{which_openocd()}',
        '-f', f'{parameters.target_config}',
        '-f', f'{parameters.board_config}',
        '-c', 'reset_config srst_only',
        '-c', 'init',
        '-c', 'halt',
        '-c', f'load_image "{parameters.binary_image}" {parameters.ramdisk_address} bin',
        '-c', 'resume',
        '-c', 'exit'
    ]
    # fmt: on
    openocd_cmd_str = " ".join(str(arg) for arg in openocd_cmd)
    logger.info(f"OpenOCD command = {openocd_cmd_str}")

    if dry:
        return

    try:
        subprocess.run(openocd_cmd, check=True, timeout=parameters.upload_timeout_s)
    except subprocess.TimeoutExpired as e:
        raise OpenOcdTimeout(
            f"OpenOCD command timed out after {parameters.upload_timeout_s} s"
        ) from e
