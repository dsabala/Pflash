"""
OpenOCD subprocess run module
"""

import shutil
import subprocess
from pathlib import Path
from dataclasses import dataclass
from loguru import logger

from pflash.exceptions import LackOfPrerequisite, OpenOcdTimeout, OpenOcdFail


def which_openocd() -> Path:
    """
    Search for the OpenOCD binary in the system PATH

    Returns:
        Path: Path to the OpenOCD binary

    Raises:
        LackOfPrerequisite: If the OpenOCD binary is not found
    """
    openocd_binary = shutil.which("openocd")
    if openocd_binary:
        return Path(openocd_binary)
    raise LackOfPrerequisite("OpenOCD binary not found in system PATH")


@dataclass
class UploadParameters:
    """
    Parameters of the OpenOCD upload functionality

    Attributes:
        target_config (str): path to the OpenOCD config file e.g. target/xilinx_zynqmp.cfg
        board_config (Path): path to the file with debug adapter and board config
        binary_image (Path): path to the binary image to upload
        address (int): address in RAM where the image will be loaded
        upload_timeout_s (int, optional): timeout for the upload in seconds
    """

    target_config: str
    board_config: Path
    binary_image: Path
    address: int
    upload_timeout_s: int = None


def upload(parameters: UploadParameters, dry: bool):
    """
    Upload a binary image to the target's RAM using OpenOCD

    Args:
        parameters (UploadParameters): Parameters for the upload operation
        dry (bool): If True, simulate the operation without executing it

    Raises:
        OpenOcdTimeout: If the OpenOCD command times out
        OpenOcdFail: If the OpenOCD command fails with a non-zero return code
    """
    # Form the OpenOCD command
    # fmt: off
    openocd_cmd = [
        str(which_openocd()),
        "-f", str(parameters.board_config),
        "-f", str(parameters.target_config),
        "-c", "reset_config srst_only",
        "-c", "init",
        "-c", "halt",
        "-c", f'load_image "{parameters.binary_image}" {parameters.address} bin',
        "-c", "resume",
        "-c", "exit",
    ]
    # fmt: on
    openocd_cmd_str = " ".join(openocd_cmd)
    logger.info(f"OpenOCD command: {openocd_cmd_str}")

    if dry:
        return

    try:
        # Run the OpenOCD command
        result = subprocess.run(
            openocd_cmd,
            check=True,
            timeout=parameters.upload_timeout_s,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        logger.info("OpenOCD command completed successfully")
        logger.debug(f"OpenOCD stdout:\n{result.stdout}")
        logger.debug(f"OpenOCD stderr:\n{result.stderr}")

    except subprocess.TimeoutExpired as e:
        raise OpenOcdTimeout(
            f"OpenOCD upload timed out after {parameters.upload_timeout_s} seconds"
        ) from e

    except subprocess.CalledProcessError as e:
        logger.error("OpenOCD command failed with a non-zero return code")
        logger.error(f"OpenOCD stdout:\n{e.stdout}")
        logger.error(f"OpenOCD stderr:\n{e.stderr}")
        raise OpenOcdFail("OpenOCD command failed") from e
