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
    """Parameters required for uploading a binary image to the target's RAM using OpenOCD

    Attributes:
        target_config (Path): Path to the target configuration file
        board_config (Path): Path to the board configuration file
        binary_image (Path): Path to the binary image to be uploaded
        ram_address (int): The RAM address where the binary image will be loaded
        timeout (int, optional): Timeout[s] for the OpenOCD subprocess
    """

    target_config: str
    board_config: Path
    binary_image: Path
    ram_address: int
    timeout_s: int = None


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
        '-c', f'load_image "{parameters.binary_image}" {parameters.ram_address} bin',
        '-c', 'resume',
        '-c', 'exit'
    ]
    # fmt: on
    openocd_cmd_str = " ".join(str(arg) for arg in openocd_cmd)
    logger.info(f"OpenOCD cmd = {openocd_cmd_str}")

    if dry:
        return

    try:
        subprocess.run(openocd_cmd, check=True, timeout=parameters.timeout_s)
    except subprocess.TimeoutExpired as e:
        raise OpenOcdTimeout(
            f"OpenOCD command timed out after {parameters.timeout_s} s"
        ) from e
