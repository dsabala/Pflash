"""
Plo bootloader management module
"""

import serial
import time
from loguru import logger


def boot_plo_naively(port: str, baud: int, dry: bool):
    """Make sure target is stopped in plo bootloader"""

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


def plo_copy(port: str, baud: int, size: int, alias: str, offset: int, dry: bool):
    copy_command = f"copy ramdisk 0 {size} {alias} {offset} {size}"
    logger.info(f"Bootloader 'plo' copy command: {copy_command}")

    if dry:
        logger.info("Dry run, skip plo copy command")
        return

    start = time.time()
    with serial.Serial(port, baudrate=baud, timeout=60) as ser:
        ser.write(copy_command.encode())
        while 1:
            expected_char = "%".encode()
            recv = ser.read_until(expected=expected_char).decode()
            print(f"Recv = {recv}")
            if "(plo)%" in recv:
                break
    end = time.time()
    duration = end - start
    logger.info(f"Successfully copied image to flash in {duration}s")
    return
