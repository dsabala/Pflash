"""
OpenOCD subprocess run module
"""

import shutil
import subprocess
from pathlib import Path

from loguru import logger


def which_openocd() -> Path:
    """Find OpenOCD binary in system PATH

    Raises:
        FileNotFoundError: OpenOCD binary is not available in PATH

    Returns:
        pathlib.Path: path to OpenOCD binary
    """
    openocd_binary = shutil.which("openocd")
    if openocd_binary:
        return Path(openocd_binary)
    raise FileNotFoundError("OpenOCD binary not found in PATH")


def upload_to_ram(probe_cfg: str, target_cfg: Path, image: Path, addr: int, dry: bool):
    """
    Upload binary image to RAM memory of target
    """

    # Form OpenOCD command
    openocd_binary_path = which_openocd()
    # fmt: off
    openocd_cmd = [
        f'{openocd_binary_path}',
        '-f', f'{probe_cfg}',
        '-f', f'{target_cfg}',
        '-c', 'reset_config srst_only',
        '-c', 'init',
        '-c', 'halt',
        '-c', f'load_image "{image}" {addr} bin',
        '-c', 'resume',
        '-c', 'exit'
    ]
    # fmt: on
    openocd_cmd_str = " ".join(str(arg) for arg in openocd_cmd)
    logger.info(f"OpenOCD cmd = {openocd_cmd_str}")
    if dry:
        return 0

    retval = subprocess.run(openocd_cmd, check=True)
    return retval
