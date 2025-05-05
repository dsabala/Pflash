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
        '-f', f'{parameters.board_config}',
        '-f', f'{parameters.target_config}',
        '-c', 'reset_config srst_only',
        '-c', 'init',
        '-c', 'halt',
        '-c', f'load_image "{parameters.binary_image}" {parameters.ramdisk_address} bin',
        '-c', 'resume',
        '-c', 'exit'
    ]
    # fmt: on
    openocd_cmd_str = " ".join(str(arg) for arg in openocd_cmd)
    logger.debug(f"OpenOCD command = {openocd_cmd_str}")

    if dry:
        return

    try:
        retval = subprocess.run(
            openocd_cmd,
            check=True,
            timeout=parameters.upload_timeout_s,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        #logger.info(f"OpenOCD stdout:\n{retval.stdout}")
        #logger.info(f"OpenOCD stderr:\n{retval.stderr}")
    except subprocess.TimeoutExpired as e:
        logger.error(f"OpenOCD command timed out after {parameters.upload_timeout_s} s")
        logger.error(f"OpenOCD stdout:\n{e.stdout}")
        logger.error(f"OpenOCD stderr:\n{e.stderr}")
        raise OpenOcdTimeout(
            f"OpenOCD command timed out after {parameters.upload_timeout_s} s"
        ) from e
    except subprocess.CalledProcessError as e:
        logger.error("OpenOCD command failed!")
        logger.error(f"OpenOCD stdout:\n{e.stdout}")
        logger.error(f"OpenOCD stderr:\n{e.stderr}")
        raise
