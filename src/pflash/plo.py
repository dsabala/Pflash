"""
Plo bootloader management module
"""

import serial
from loguru import logger


def boot_plo_naively(port: str, baud: int, dry: bool):
    """Make sure target is stopped in plo bootloader"""

    # If this is dry run then do not continue
    if dry:
        logger.info("Dry run, skip driving target into plo...")
        return

    # Check if target is locked in bootloader and ready
    logger.info("Checking if target is locked in bootloader...")
    with serial.Serial(port, baudrate=baud, timeout=0.5) as ser:
        ser.write("\n".encode())
        recv = ser.read_until(expected="%").decode()
    if "plo" in recv:
        logger.info("Success: target is stopped in bootloader")
        return

    # If there is no sign that we are in application then resign
    if "psh" not in recv:
        raise KeyError("Cannot confirm if target is in bootloader or system")

    # Reboot into plo
    logger.info("Target booted into the system, trying to reboot to bootloader")
    with serial.Serial(port, baudrate=115200, timeout=10) as ser:
        ser.write("reboot\n".encode())
    while 1:
        with serial.Serial(port, baudrate=115200, timeout=0.1) as ser:
            recv = ser.read_until(expected="\n").decode()
            # print(f"Recv = {recv}")
            if "Waiting for input" in recv:
                ser.write("\n".encode())
                logger.info("Target locked in bootloader")
                break
